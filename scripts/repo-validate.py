#!/usr/bin/env python3
"""Check an independent repository's signed manifest (docs/repositories.md).

Usage:
  repo-validate.py FILE.signed --key repository.pem [--fingerprint HEX]
                   [--now ISO] [--not-before ISO] [--max-age-days 7] [--json]

FILE.signed is line 1 a base64 RSA-SHA256 signature, then the manifest JSON byte
for byte: the same envelope as Apps2Samsung's resolved.json.signed, so TV-Store
verifies both with one function. The checks, in order, each with the reason code
it reports on failure:

  size          the file is over MAX_FILE_BYTES
  no-signature  no signature line in the first 4096 bytes
  key           the key isn't an RSA public key of at least MIN_KEY_BITS
  fingerprint   --fingerprint was given and the key doesn't match it
  signature     the signature doesn't verify against the key
  json          the payload isn't JSON
  schema-version  schemaVersion isn't one this validator knows (fails closed)
  schema        spec/repository.schema.json rejects the payload
  url           a URL points at an IP address or localhost, or has credentials
  future        generatedAt is more than an hour ahead of --now
  expired       generatedAt is older than --max-age-days before --now
  rollback      generatedAt is older than --not-before (the last one accepted)
  duplicate     two providers share an id, or offer the same package_id + version

Exit code 0 when the file is accepted, 1 when rejected, 2 on usage errors. The
signature is checked with the openssl CLI and nothing in the payload is executed.
"""

import argparse
import base64
import datetime as dt
import hashlib
import ipaddress
import json
import os
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spec", "repository.schema.json")
SUPPORTED_SCHEMA_VERSIONS = (1,)
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_SIG_LINE = 4096
MIN_KEY_BITS = 3072
FUTURE_SKEW = dt.timedelta(hours=1)


class Rejected(Exception):
    def __init__(self, reason, message):
        super().__init__(message)
        self.reason = reason


def parse_time(value):
    if not isinstance(value, str):
        raise ValueError("not a string")
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(dt.timezone.utc)


def split_envelope(data):
    if len(data) > MAX_FILE_BYTES:
        raise Rejected("size", f"the file is {len(data)} bytes, over the {MAX_FILE_BYTES} limit")
    nl = data.find(b"\n", 0, MAX_SIG_LINE)
    if nl < 0:
        raise Rejected("no-signature", "no signature line: the file is not a signed manifest")
    try:
        sig = base64.b64decode(data[:nl].strip(), validate=True)
    except ValueError:
        raise Rejected("no-signature", "line 1 is not base64")
    if not sig:
        raise Rejected("no-signature", "the signature line is empty")
    return sig, data[nl + 1:]


def run_openssl(args, stdin=None):
    return subprocess.run(["openssl"] + args, input=stdin, capture_output=True)


def key_info(pem_path):
    """(bits, fingerprint) of an RSA public key: the fingerprint is the SHA-256 of its DER SubjectPublicKeyInfo."""
    der = run_openssl(["pkey", "-pubin", "-in", pem_path, "-outform", "DER"])
    if der.returncode != 0 or not der.stdout:
        raise Rejected("key", "the key file is not a PEM public key")
    text = run_openssl(["pkey", "-pubin", "-in", pem_path, "-noout", "-text"]).stdout.decode("utf-8", "replace")
    m = re.search(r"Public-Key: \((\d+) bit\)", text)
    if not m or "Modulus" not in text:
        raise Rejected("key", "the key is not an RSA key (TV-Store can only verify RSA-SHA256)")
    bits = int(m.group(1))
    if bits < MIN_KEY_BITS:
        raise Rejected("key", f"the key is {bits} bits; at least {MIN_KEY_BITS} is required")
    return bits, hashlib.sha256(der.stdout).hexdigest()


def verify_signature(pem_path, sig, payload):
    with tempfile.TemporaryDirectory(prefix="repo-validate-") as tmp:
        sig_path = os.path.join(tmp, "sig")
        payload_path = os.path.join(tmp, "payload")
        with open(sig_path, "wb") as f:
            f.write(sig)
        with open(payload_path, "wb") as f:
            f.write(payload)
        r = run_openssl(["dgst", "-sha256", "-verify", pem_path, "-signature", sig_path, payload_path])
    if r.returncode != 0:
        raise Rejected("signature", "the signature does not match the key: the file was changed or signed by someone else")


def check_schema(manifest):
    try:
        import jsonschema
    except ImportError:
        sys.exit("repo-validate.py needs the jsonschema package: pip install jsonschema")
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(validator.iter_errors(manifest), key=lambda e: list(e.absolute_path))
    if errors:
        e = errors[0]
        where = "/".join(str(p) for p in e.absolute_path) or "(top level)"
        more = f" (and {len(errors) - 1} more)" if len(errors) > 1 else ""
        raise Rejected("schema", f"{where}: {e.message}{more}")


def iter_urls(manifest):
    repo = manifest.get("repository") or {}
    if "homepage" in repo:
        yield "repository/homepage", repo["homepage"]
    for i, p in enumerate(manifest.get("providers") or []):
        for key in ("url", "source_url"):
            if key in p:
                yield f"providers/{i}/{key}", p[key]
        if "previewImage" in (p.get("buildInfo") or {}):
            yield f"providers/{i}/buildInfo/previewImage", p["buildInfo"]["previewImage"]
        for j, r in enumerate(p.get("releases") or []):
            if "url" in r:
                yield f"providers/{i}/releases/{j}/url", r["url"]
            for k, a in enumerate(r.get("assets") or []):
                for key in ("browser_download_url", "icon"):
                    if key in a:
                        yield f"providers/{i}/releases/{j}/assets/{k}/{key}", a[key]


def check_urls(manifest):
    for where, url in iter_urls(manifest):
        parts = urlsplit(url)
        host = (parts.hostname or "").lower()
        if parts.username or parts.password:
            raise Rejected("url", f"{where}: credentials in a URL are not allowed")
        if host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
            raise Rejected("url", f"{where}: {host} is a local address")
        try:
            ipaddress.ip_address(host.strip("[]"))
            raise Rejected("url", f"{where}: use a host name, not an IP address")
        except ValueError:
            pass


def check_semantics(manifest, now, not_before, max_age):
    at = parse_time(manifest["generatedAt"])
    if at - now > FUTURE_SKEW:
        raise Rejected("future", f"generatedAt {manifest['generatedAt']} is in the future: check the clock where it was signed")
    if now - at > max_age:
        raise Rejected("expired", f"generatedAt {manifest['generatedAt']} is more than {max_age.days} days old: the publisher must re-sign")
    if not_before is not None and at < not_before:
        raise Rejected("rollback", f"generatedAt {manifest['generatedAt']} is older than the last accepted manifest ({not_before.isoformat()})")

    seen_ids, seen_packages = set(), {}
    for p in manifest["providers"]:
        if p["id"] in seen_ids:
            raise Rejected("duplicate", f"provider id {p['id']} appears twice")
        seen_ids.add(p["id"])
        for r in p["releases"]:
            for a in r["assets"]:
                pid, ver = a.get("package_id"), a.get("package_version")
                # One provider may ship several builds of one version (a legacy and a current
                # Tizen build, per-version .tpk files): those are variants. Two providers
                # offering the same package and version is the conflict.
                if pid and ver:
                    key = (pid, ver)
                    if seen_packages.setdefault(key, p["id"]) != p["id"]:
                        raise Rejected("duplicate", f"package {pid} version {ver} is offered by providers {seen_packages[key]} and {p['id']}")


def validate(data, key_path, fingerprint=None, now=None, not_before=None, max_age_days=7):
    """Returns (manifest, fingerprint) or raises Rejected."""
    now = now or dt.datetime.now(dt.timezone.utc)
    sig, payload = split_envelope(data)
    _, fp = key_info(key_path)
    if fingerprint and fp != fingerprint.lower().replace(":", ""):
        raise Rejected("fingerprint", f"the key's fingerprint is {fp}, not the approved {fingerprint}")
    verify_signature(key_path, sig, payload)
    try:
        manifest = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise Rejected("json", f"the payload is not JSON: {e}")
    if not isinstance(manifest, dict) or manifest.get("schemaVersion") not in SUPPORTED_SCHEMA_VERSIONS:
        got = manifest.get("schemaVersion") if isinstance(manifest, dict) else None
        raise Rejected("schema-version", f"schemaVersion {got!r} is not supported (this validator knows {list(SUPPORTED_SCHEMA_VERSIONS)})")
    check_schema(manifest)
    check_urls(manifest)
    check_semantics(manifest, now, not_before, dt.timedelta(days=max_age_days))
    return manifest, fp


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check an independent repository's signed manifest.")
    ap.add_argument("file")
    ap.add_argument("--key", required=True, help="the repository's public key (PEM)")
    ap.add_argument("--fingerprint", help="the approved key fingerprint (hex SHA-256 of the DER public key)")
    ap.add_argument("--now", help="check as if it were this time (ISO 8601); default: now")
    ap.add_argument("--not-before", help="generatedAt of the last accepted manifest (rollback check)")
    ap.add_argument("--max-age-days", type=int, default=7)
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    a = ap.parse_args(argv)
    try:
        now = parse_time(a.now) if a.now else None
        not_before = parse_time(a.not_before) if a.not_before else None
    except ValueError as e:
        ap.error(f"bad time: {e}")
    with open(a.file, "rb") as f:
        data = f.read()
    try:
        manifest, fp = validate(data, a.key, a.fingerprint, now, not_before, a.max_age_days)
    except Rejected as e:
        if a.json:
            print(json.dumps({"ok": False, "reason": e.reason, "message": str(e)}))
        else:
            print(f"REJECTED [{e.reason}] {e}")
        return 1
    apps = sum(len(r["assets"]) for p in manifest["providers"] for r in p["releases"])
    if a.json:
        print(json.dumps({"ok": True, "fingerprint": fp, "repository": manifest["repository"]["id"],
                          "generatedAt": manifest["generatedAt"], "files": apps}))
    else:
        print(f"OK {manifest['repository']['id']} ({manifest['repository']['name']}), {len(manifest['providers'])} providers, "
              f"{apps} files, signed {manifest['generatedAt']}, key {fp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
