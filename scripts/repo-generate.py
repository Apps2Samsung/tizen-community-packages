#!/usr/bin/env python3
"""Build and sign an independent repository's manifest (docs/repositories.md).

Usage:
  repo-generate.py --input repository.input.json --out site/
                   [--key PATH | env REPO_SIGNING_KEY] [--previous URL_OR_PATH]

Reads the publisher's input file (the repository block and a list of providers in
the third-party-apps.json shape), takes each provider's newest GitHub releases,
and for every .wgt/.tpk asset records its size, SHA-256 and what the package says
about itself (package-info.py: version, app_id, package_id, required_version).
Then it signs the result and writes into --out:

  repository.json.signed   what clients read: base64 RSA-SHA256 signature line + the JSON
  repository.json          the same JSON, unsigned, for people to read
  repository.pem           the public key, so Apps2Samsung can show its fingerprint

Finally it checks its own output with repo-validate.py, so a broken manifest is
never published.

--previous (the URL or path of the currently published repository.json.signed)
lets unchanged assets be reused without downloading them again, and keeps a
provider whose GitHub fetch failed (marked "ok": false) instead of dropping it.
GITHUB_TOKEN, when set, is sent to api.github.com (60 requests/hour without it).

The private key never touches the output folder: it comes from --key or from the
REPO_SIGNING_KEY environment variable (the PEM text), and openssl reads it from a
temporary file only this process can read.
"""

import argparse
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
GENERATOR_ONLY = ("match", "prerelease")
MAX_ASSET_BYTES = 512 * 1024 * 1024
USER_AGENT = "tizen-community-packages repo-generate"


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def warn(msg):
    print(f"::warning::{msg}" if os.environ.get("GITHUB_ACTIONS") else f"warning: {msg}", file=sys.stderr)


def http_get(url, accept=None):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    if accept:
        req.add_header("Accept", accept)
    host = urllib.parse.urlsplit(url).hostname or ""
    token = os.environ.get("GITHUB_TOKEN")
    if token and host == "api.github.com":
        req.add_header("Authorization", f"Bearer {token}")
    return urllib.request.urlopen(req, timeout=60)


def releases_api_url(url):
    """Accepts https://api.github.com/repos/o/r/releases, https://github.com/o/r or o/r."""
    m = re.match(r"^(?:https://(?:api\.)?github\.com/(?:repos/)?)?([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?(?:/releases)?/?$", url.strip())
    if not m:
        raise ValueError(f"{url} is not a GitHub repository or releases URL")
    return f"https://api.github.com/repos/{m.group(1)}/{m.group(2)}/releases"


def download(url, dest):
    h = hashlib.sha256()
    size = 0
    with http_get(url) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_ASSET_BYTES:
                raise ValueError(f"{url} is larger than {MAX_ASSET_BYTES} bytes")
            h.update(chunk)
            f.write(chunk)
    return size, h.hexdigest()


def previous_assets(previous):
    """browser_download_url -> asset entry, and provider id -> provider, from the published manifest."""
    by_url, by_provider = {}, {}
    if not previous:
        return by_url, by_provider
    for p in previous.get("providers", []):
        by_provider[p.get("id")] = p
        for r in p.get("releases", []):
            for a in r.get("assets", []):
                by_url[a.get("browser_download_url")] = a
    return by_url, by_provider


def load_previous(src, validator):
    if not src:
        return None
    try:
        if re.match(r"^https?://", src):
            with http_get(src) as r:
                data = r.read(validator.MAX_FILE_BYTES + 1)
        else:
            with open(src, "rb") as f:
                data = f.read()
        _, payload = validator.split_envelope(data)
        return json.loads(payload.decode("utf-8"))
    except Exception as e:  # first run, or the old file is gone: just build from scratch
        warn(f"no usable previous manifest at {src} ({e}); every asset is downloaded")
        return None


def resolve_provider(p, prev_by_url, scanner, pkginfo, workdir):
    api = releases_api_url(p["url"])
    with http_get(api + "?per_page=30", "application/vnd.github+json") as r:
        releases = json.load(r)
    match = re.compile(p["match"]) if p.get("match") else None
    take = int(p.get("take", 1))
    out = []
    for rel in releases:
        if rel.get("draft") or (rel.get("prerelease") and not p.get("prerelease")):
            continue
        assets = []
        for a in rel.get("assets", []):
            name = a.get("name", "")
            if not name.lower().endswith((".wgt", ".tpk")) or (match and not match.search(name)):
                continue
            url = a["browser_download_url"]
            gh_digest = a.get("digest") if isinstance(a.get("digest"), str) else None
            old = prev_by_url.get(url)
            if old and old.get("size") == a.get("size") and (not gh_digest or gh_digest == old.get("digest")):
                assets.append(old)
                continue
            path = os.path.join(workdir, name)
            size, sha = download(url, path)
            if gh_digest and gh_digest != f"sha256:{sha}":
                raise ValueError(f"{name}: downloaded bytes hash to {sha}, GitHub reports {gh_digest}")
            entry = {"name": name, "browser_download_url": url, "size": size, "digest": f"sha256:{sha}"}
            info = pkginfo.package_info(scanner, path)
            if not info:
                warn(f"{name} has no config.xml / tizen-manifest.xml: is it a Tizen package?")
            for src, dst in (("version", "package_version"), ("app_id", "app_id"), ("package_id", "package_id"), ("required_version", "required_version")):
                if info.get(src):
                    entry[dst] = info[src]
            os.remove(path)
            assets.append(entry)
        if not assets:
            continue
        out.append({
            "url": rel.get("url"),
            "name": (p.get("prefix") or "") + (rel.get("name") or rel.get("tag_name")),
            "tag_name": rel["tag_name"],
            "published_at": rel.get("published_at"),
            "draft": False,
            "assets": assets,
        })
        if len(out) >= take:
            break
    return out


def sign(payload, key_pem_text):
    fd, key_path = tempfile.mkstemp(prefix="repo-key-")
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(key_pem_text)
        sig = subprocess.run(["openssl", "dgst", "-sha256", "-sign", key_path], input=payload, capture_output=True)
        if sig.returncode != 0:
            sys.exit("openssl could not sign with the key: " + sig.stderr.decode("utf-8", "replace").strip())
        pub = subprocess.run(["openssl", "pkey", "-in", key_path, "-pubout"], capture_output=True, check=True).stdout
    finally:
        os.remove(key_path)
    return base64.b64encode(sig.stdout) + b"\n" + payload, pub


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build and sign an independent repository's manifest.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--key", help="private key PEM file (default: the REPO_SIGNING_KEY environment variable)")
    ap.add_argument("--previous", help="URL or path of the currently published repository.json.signed")
    a = ap.parse_args(argv)

    if a.key:
        with open(a.key, encoding="utf-8") as f:
            key_text = f.read()
    else:
        key_text = os.environ.get("REPO_SIGNING_KEY", "")
    if "PRIVATE KEY" not in key_text:
        sys.exit("no signing key: pass --key or set REPO_SIGNING_KEY to the PEM text of the private key")

    validator = load("repo_validate", "repo-validate.py")
    pkginfo = load("package_info", "package-info.py")
    scanner = pkginfo.load_scanner()

    with open(a.input, encoding="utf-8") as f:
        spec = json.load(f)
    previous = load_previous(a.previous, validator)
    prev_by_url, prev_by_provider = previous_assets(previous)

    providers = []
    workdir = tempfile.mkdtemp(prefix="repo-generate-")
    try:
        for p in spec["providers"]:
            entry = {k: v for k, v in p.items() if k not in GENERATOR_ONLY}
            try:
                entry["url"] = releases_api_url(p["url"])
                releases = resolve_provider(p, prev_by_url, scanner, pkginfo, workdir)
                if not releases:
                    warn(f"{p['id']}: no release with a .wgt/.tpk asset; left out")
                    continue
                entry.update(ok=True, latestTag=releases[0]["tag_name"], releases=releases)
            except Exception as e:
                old = prev_by_provider.get(p["id"])
                if not old or not old.get("releases"):
                    warn(f"{p['id']}: {e}; left out (nothing published before to fall back on)")
                    continue
                warn(f"{p['id']}: {e}; keeping the previously published releases")
                entry.update(ok=False, latestTag=old.get("latestTag", ""), releases=old["releases"])
            for r in entry["releases"]:
                for k in [k for k, v in r.items() if v is None]:
                    del r[k]
            providers.append(entry)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    if not providers:
        sys.exit("no provider produced any package: nothing to publish")

    manifest = {
        "schemaVersion": 1,
        "repository": spec["repository"],
        "generatedAt": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "providers": providers,
    }
    payload = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    signed, pub = sign(payload, key_text)

    os.makedirs(a.out, exist_ok=True)
    paths = {name: os.path.join(a.out, name) for name in ("repository.json.signed", "repository.json", "repository.pem")}
    with open(paths["repository.json.signed"], "wb") as f:
        f.write(signed)
    with open(paths["repository.json"], "wb") as f:
        f.write(payload)
    with open(paths["repository.pem"], "wb") as f:
        f.write(pub)

    try:
        _, fp = validator.validate(signed, paths["repository.pem"])
    except validator.Rejected as e:
        sys.exit(f"the generated manifest does not validate [{e.reason}]: {e}")
    files = sum(len(r["assets"]) for p in providers for r in p["releases"])
    print(f"signed {len(providers)} providers, {files} files -> {paths['repository.json.signed']}")
    print(f"key fingerprint: {fp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
