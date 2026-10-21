#!/usr/bin/env python3
"""Reject a package that is already offered somewhere else.

Two places an app can already live:

  * another manifest in packages/ (same repo in a different case, or the same
    display name), and
  * the providers hardcoded in Apps2Samsung's third-party-apps.json (Jellyfin,
    Moonfin, TizenTube, ...), which the installer lists on its own, so shipping
    them in the community bundle again would show the app twice.

usage: check-duplicates.py [--manifest <path-or-url>] [--changed <file>...]

Conflicts in a manifest named by --changed (the files a PR adds or modifies)
are errors; conflicts elsewhere are only warnings, so a later addition to
Apps2Samsung's built-in list cannot start failing every unrelated PR.
Without --changed every conflict is an error.

A retired manifest (enabled: false) ships nothing, so it is not compared with
the built-in list; it still reserves its repo and name among the manifests.
"""
import argparse
import glob
import json
import os
import re
import sys
import urllib.request

DEFAULT_MANIFEST = "https://raw.githubusercontent.com/Apps2Samsung/Apps2Samsung/main/third-party-apps.json"
# The provider that points at this very repo (the community bundle itself).
SELF_REPO = "apps2samsung/tizen-community-packages"

GITHUB_URL = re.compile(
    r"https?://(?:api\.github\.com/repos|github\.com|raw\.githubusercontent\.com)"
    r"/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")


def slug(host, owner, repo):
    repo = repo[:-4] if repo.lower().endswith(".git") else repo
    return f"{host}:{owner}/{repo}".lower()


def github_slugs_in(text):
    return {slug("github", o, r) for o, r in GITHUB_URL.findall(text or "")}


def load_builtin(source):
    """repo slug / display name -> provider id, from Apps2Samsung's provider list."""
    if re.match(r"^https?://", source):
        with urllib.request.urlopen(source, timeout=30) as resp:
            doc = json.load(resp)
    else:
        with open(source, encoding="utf-8") as fh:
            doc = json.load(fh)
    repos, names = {}, {}
    for p in doc.get("providers", []):
        pid = p.get("id", "?")
        for s in github_slugs_in(p.get("url")):
            if s.split(":", 1)[1] == SELF_REPO:
                continue
            repos.setdefault(s, pid)
        for n in (p.get("displayName"), (p.get("prefix") or "").strip(" -")):
            if n and n.strip():
                names.setdefault(n.strip().lower(), pid)
    return repos, names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST,
                    help="Apps2Samsung third-party-apps.json (URL or path)")
    ap.add_argument("--packages", default="packages")
    ap.add_argument("--changed", nargs="*", default=None,
                    help="manifests the PR adds or modifies; conflicts in other files only warn")
    args = ap.parse_args()

    changed = None if args.changed is None else {os.path.normpath(c) for c in args.changed}

    try:
        builtin_repos, builtin_names = load_builtin(args.manifest)
    except Exception as ex:  # network blip: don't block the PR on it
        print(f"::warning::Could not load Apps2Samsung's provider list ({args.manifest}): {ex}; "
              "skipping the built-in app check.")
        builtin_repos, builtin_names = {}, {}

    errors = warnings = 0

    def report(path, msg):
        nonlocal errors, warnings
        if changed is None or os.path.normpath(path) in changed:
            errors += 1
            print(f"::error file={path},title=Already in the catalog::{msg}")
        else:
            warnings += 1
            print(f"::warning file={path},title=Already in the catalog::{msg}")

    seen_repos, seen_names = {}, {}
    for path in sorted(glob.glob(os.path.join(args.packages, "*.json"))):
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
        base = os.path.basename(path)
        host = doc.get("host", "github")
        owner, repo = doc["repo"].split("/", 1)
        keys = {slug(host, owner, repo)}
        if doc.get("source") == "direct":
            keys |= github_slugs_in(doc.get("url"))
        name = doc["name"].strip().lower()

        # Against the other manifests (the structural check only catches exact-case repeats).
        for k in sorted(keys):
            if k in seen_repos:
                report(path, f"repo '{k.split(':', 1)[1]}' is already packaged by {seen_repos[k]}")
            seen_repos.setdefault(k, base)
        if name in seen_names:
            report(path, f"name '{doc['name']}' is already used by {seen_names[name]}; "
                         "pick a distinct name (and a group/variant if it is the same app)")
        seen_names.setdefault(name, base)

        # Against the apps Apps2Samsung lists on its own.
        if doc.get("enabled") is False:
            continue
        for k in sorted(keys):
            if k in builtin_repos:
                report(path, f"repo '{k.split(':', 1)[1]}' is already built into Apps2Samsung "
                             f"(provider '{builtin_repos[k]}' in third-party-apps.json)")
        if name in builtin_names:
            report(path, f"name '{doc['name']}' is already an Apps2Samsung built-in app "
                         f"(provider '{builtin_names[name]}' in third-party-apps.json)")

    print(f"Checked {len(seen_names)} manifests against each other and "
          f"{len(builtin_repos)} Apps2Samsung built-in repos: "
          f"{errors} error(s), {warnings} warning(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
