#!/usr/bin/env python3
"""Regenerate the test vectors in this folder (docs/repositories.md, "Test vectors").

  python3 -I spec/fixtures/make-fixtures.py

The keys under keys/ are TEST ONLY and public on purpose: never sign a real
repository with them. They are created once (openssl genpkey) and committed, so
re-running this script reproduces the same .signed files byte for byte (RSA
PKCS#1 v1.5 signatures are deterministic). index.json lists every case with the
key to check it against, the "now" to check it at, and the expected outcome.
"""

import base64
import copy
import json
import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = os.path.join(HERE, "keys")
NOW = "2026-11-07T12:00:00Z"

BASE = {
    "schemaVersion": 1,
    "repository": {
        "id": "org.example.tizen",
        "name": "Example Tizen Repository",
        "maintainer": "Example Developer",
        "description": "Test vector, not a real repository",
        "homepage": "https://example.org/tizen",
    },
    "generatedAt": "2026-11-07T00:00:00Z",
    "providers": [
        {
            "id": "example-player",
            "category": "media",
            "url": "https://api.github.com/repos/example/player/releases",
            "displayName": "Example Player",
            "take": 1,
            "source_url": "https://github.com/example/player",
            "ok": True,
            "latestTag": "v1.2.0",
            "releases": [
                {
                    "url": "https://api.github.com/repos/example/player/releases/1",
                    "name": "Example Player 1.2.0",
                    "tag_name": "v1.2.0",
                    "published_at": "2026-11-06T10:00:00Z",
                    "draft": False,
                    "assets": [
                        {
                            "name": "ExamplePlayer.wgt",
                            "browser_download_url": "https://github.com/example/player/releases/download/v1.2.0/ExamplePlayer.wgt",
                            "size": 1234567,
                            "digest": "sha256:" + "0123456789abcdef" * 4,
                            "package_version": "1.2.0",
                            "app_id": "AbCdE12345.ExamplePlayer",
                            "package_id": "AbCdE12345",
                            "required_version": "5.0",
                        },
                        {
                            "name": "ExamplePlayer-legacy.wgt",
                            "browser_download_url": "https://github.com/example/player/releases/download/v1.2.0/ExamplePlayer-legacy.wgt",
                            "size": 1200000,
                            "digest": "sha256:" + "89abcdef01234567" * 4,
                            "package_version": "1.2.0",
                            "app_id": "AbCdE12345.ExamplePlayer",
                            "package_id": "AbCdE12345",
                            "required_version": "2.4",
                        },
                    ],
                }
            ],
        },
        {
            "id": "example-tool",
            "category": "tools",
            "url": "https://api.github.com/repos/example/tool/releases",
            "displayName": "Example Tool",
            "flags": ["closed-source"],
            "ok": True,
            "latestTag": "2026.11.01",
            "releases": [
                {
                    "tag_name": "2026.11.01",
                    "assets": [
                        {
                            "name": "ExampleTool-tizen6.tpk",
                            "browser_download_url": "https://github.com/example/tool/releases/download/2026.11.01/ExampleTool-tizen6.tpk",
                            "size": 2048,
                            "digest": "sha256:" + "fedcba9876543210" * 4,
                            "package_version": "2026.11.1",
                            "package_id": "org.example.tool",
                            "required_version": "6.0",
                        }
                    ],
                }
            ],
        },
    ],
}


def ensure_key(name, bits):
    priv = os.path.join(KEYS, f"{name}.key.pem")
    pub = os.path.join(KEYS, f"{name}.pub.pem")
    if not os.path.exists(priv):
        os.makedirs(KEYS, exist_ok=True)
        subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-pkeyopt", f"rsa_keygen_bits:{bits}", "-out", priv], check=True)
        subprocess.run(["openssl", "pkey", "-in", priv, "-pubout", "-out", pub], check=True)
    return priv


def payload(manifest):
    return (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def sign(priv, data):
    with tempfile.NamedTemporaryFile() as f:
        f.write(data)
        f.flush()
        sig = subprocess.run(["openssl", "dgst", "-sha256", "-sign", priv, f.name], check=True, capture_output=True).stdout
    return base64.b64encode(sig) + b"\n" + data


def variant(change):
    m = copy.deepcopy(BASE)
    change(m)
    return m


def asset(m, p=0):
    return m["providers"][p]["releases"][0]["assets"][0]


def main():
    test = ensure_key("test", 3072)
    other = ensure_key("other", 3072)
    weak = ensure_key("weak", 2048)

    cases = []

    def write(name, data, expect, reason=None, key="test", note="", **extra):
        with open(os.path.join(HERE, name), "wb") as f:
            f.write(data)
        case = {"file": name, "key": f"keys/{key}.pub.pem", "expect": expect}
        if reason:
            case["reason"] = reason
        case.update(extra)
        case["note"] = note
        cases.append(case)

    valid = sign(test, payload(BASE))
    write("valid.signed", valid, "accept", note="Two providers, signed with the test key. The first ships two builds of one version (current and legacy): variants, not a duplicate.")

    tampered = valid.replace(b'"size": 1234567', b'"size": 1234568')
    assert tampered != valid
    write("tampered.signed", tampered, "reject", "signature", note="valid.signed with one byte of the payload changed after signing.")
    write("bad-signature.signed", sign(other, payload(BASE)), "reject", "signature", note="Correct payload, signed with a different key.")
    write("no-signature.signed", payload(BASE), "reject", "no-signature", note="The bare JSON without a signature line.")
    write("weak-key.signed", sign(weak, payload(BASE)), "reject", "key", key="weak", note="Signed and checked with a 2048-bit key; at least 3072 is required.")

    cases.append({"file": "valid.signed", "key": "keys/test.pub.pem", "expect": "reject", "reason": "fingerprint",
                  "fingerprint": "0" * 64, "note": "valid.signed against an approved fingerprint that isn't the key's."})
    cases.append({"file": "valid.signed", "key": "keys/test.pub.pem", "expect": "reject", "reason": "rollback",
                  "notBefore": "2026-11-07T06:00:00Z", "note": "valid.signed after a newer manifest was already accepted."})
    cases.append({"file": "valid.signed", "key": "keys/test.pub.pem", "expect": "accept",
                  "notBefore": "2026-11-07T00:00:00Z", "note": "The same manifest again is not a rollback."})

    def bad(name, reason, change, note):
        write(name, sign(test, payload(variant(change))), "reject", reason, note=note)

    bad("expired.signed", "expired", lambda m: m.update(generatedAt="2026-10-30T00:00:00Z"), "Signed more than 7 days before now.")
    bad("future.signed", "future", lambda m: m.update(generatedAt="2026-11-08T00:00:00Z"), "Signed more than an hour after now.")
    bad("unknown-schema-version.signed", "schema-version", lambda m: m.update(schemaVersion=2), "schemaVersion 2: clients fail closed.")
    bad("http-url.signed", "schema", lambda m: asset(m).update(browser_download_url="http://example.org/ExamplePlayer.wgt"), "A download over plain HTTP.")
    bad("ip-url.signed", "url", lambda m: asset(m).update(browser_download_url="https://192.168.1.10/ExamplePlayer.wgt"), "A download from an IP address.")
    bad("localhost-url.signed", "url", lambda m: asset(m).update(browser_download_url="https://localhost/ExamplePlayer.wgt"), "A download from localhost.")
    bad("bad-digest.signed", "schema", lambda m: asset(m).update(digest="sha256:ABC"), "A digest that isn't 64 lowercase hex characters.")
    bad("missing-digest.signed", "schema", lambda m: asset(m).pop("digest"), "An asset without a digest cannot be verified, so it is invalid.")
    bad("icon-without-digest.signed", "schema", lambda m: asset(m).update(icon="https://example.org/icon.png"), "An icon must come with icon_digest.")
    bad("bad-repository-id.signed", "schema", lambda m: m["repository"].update(id="Example Repo"), "repository.id must be reverse-DNS.")

    def dup_provider(m):
        m["providers"][1]["id"] = m["providers"][0]["id"]
    bad("duplicate-provider.signed", "duplicate", dup_provider, "Two providers with the same id.")

    def dup_package(m):
        a = asset(m, 1)
        a.update(package_id="AbCdE12345", package_version="1.2.0")
    bad("duplicate-package.signed", "duplicate", dup_package, "The same package_id and version offered by two providers.")

    with open(os.path.join(HERE, "index.json"), "w", encoding="utf-8") as f:
        json.dump({"now": NOW, "cases": cases}, f, indent=2)
        f.write("\n")
    print(f"wrote {len(cases)} cases")


if __name__ == "__main__":
    main()
