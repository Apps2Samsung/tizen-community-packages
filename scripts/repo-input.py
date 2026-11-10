#!/usr/bin/env python3
"""Add or remove an app in an independent repository's repository.input.json.

This is what the "Add an app" and "Remove an app" workflows of
Apps2Samsung/repository-template run, so a publisher never has to edit JSON.

  repo-input.py add    --file repository.input.json --repository owner/name
                       --app <github link or owner/repo> --category <id> [--name "Shown name"]
  repo-input.py remove --file repository.input.json --app <github link, owner/repo or provider id>

add creates the file when it does not exist yet, with a repository block made
from --repository (the publisher's own GitHub repo): id io.github.<owner>.<name>,
name "<owner>'s Tizen apps", maintainer <owner>, homepage the repo. Adding an
app that is already listed updates its category and name.

Before it writes anything, add checks on GitHub that the app's repository exists
and has a release with a .wgt or .tpk file, and that the category is one of the
ids in data/categories.json. Every outcome is explained in plain words, on stdout
and in the job summary when GITHUB_STEP_SUMMARY is set. Exit code 1 means nothing
was changed.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CATEGORIES = os.path.join(HERE, "..", "data", "categories.json")
APP = re.compile(r"^(?:https?://)?(?:www\.)?(?:github\.com/)?([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?(?:/.*)?$")
GUIDE = "https://github.com/Apps2Samsung/repository-template#make-a-release-of-your-app"


def say(lines, ok=True):
    text = "\n".join(lines)
    print(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(("## ✅ " if ok else "## ❌ ") + text + "\n\n")


def fail(*lines):
    say(list(lines), ok=False)
    sys.exit(1)


def slug(text):
    """A lowercase reverse-DNS segment: letters and digits joined by single '-'."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "x"


def parse_app(text):
    m = APP.match(text.strip())
    if not m:
        return None
    owner, name = m.group(1), m.group(2)
    if owner.lower() in ("orgs", "users", "settings"):
        return None
    return owner, name


def github(path):
    req = urllib.request.Request("https://api.github.com/" + path, headers={
        "User-Agent": "tizen-community-packages repo-input", "Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def check_app(owner, name):
    """Returns (canonical owner/repo, uses_prerelease). Exits with an explanation otherwise."""
    try:
        info = github(f"repos/{owner}/{name}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            fail(f"Can't find the app's repository {owner}/{name} on GitHub.",
                 "",
                 "Check the link, and that the repository is public (Settings > General > Danger Zone > Change visibility).")
        fail(f"GitHub didn't answer for {owner}/{name} (HTTP {e.code}). Try again in a few minutes.")
    full = info["full_name"]
    releases = github(f"repos/{full}/releases?per_page=20")
    def packages(r):
        return [a["name"] for a in r.get("assets", []) if a["name"].lower().endswith((".wgt", ".tpk"))]
    stable = [r for r in releases if not r.get("draft") and not r.get("prerelease") and packages(r)]
    pre = [r for r in releases if not r.get("draft") and r.get("prerelease") and packages(r)]
    if stable:
        return full, False
    if pre:
        return full, True
    fail(f"{full} has no release with a .wgt or .tpk file yet.",
         "",
         "Your repository lists the newest release of each app, so the app needs one first:",
         f"open https://github.com/{full}/releases/new, give it a version (for example v1.0.0),",
         "drag your .wgt or .tpk file into the box at the bottom, and click Publish release.",
         f"Step by step: {GUIDE}",
         "",
         "Then run Add an app again.")


def load_categories():
    with open(CATEGORIES, encoding="utf-8") as f:
        return [(c["id"], c["name"]) for c in json.load(f)]


def load(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def new_input(repository):
    owner, name = repository.split("/", 1)
    return {
        "repository": {
            "id": f"io.github.{slug(owner)}.{slug(name)}",
            "name": f"{owner}'s Tizen apps",
            "maintainer": owner,
            "homepage": f"https://github.com/{owner}/{name}",
        },
        "providers": [],
    }


def same_app(provider, full):
    m = parse_app(re.sub(r"^https://api\.github\.com/repos/", "", provider.get("url", "")).replace("/releases", ""))
    return bool(m) and f"{m[0]}/{m[1]}".lower() == full.lower()


def add(a):
    cats = load_categories()
    ids = [c for c, _ in cats]
    category = a.category.strip().lower()
    if category not in ids:
        fail(f"'{a.category}' is not a category.",
             "",
             "Pick one of these (the word on the left):",
             *[f"- {c}: {n}" for c, n in cats])
    parsed = parse_app(a.app)
    if not parsed:
        fail(f"'{a.app}' doesn't look like a GitHub repository.",
             "",
             "Paste the link of your app's repository, for example https://github.com/yourname/your-app.")
    full, prerelease = check_app(*parsed)

    data = load(a.file) or new_input(a.repository)
    providers = data.setdefault("providers", [])
    existing = next((p for p in providers if same_app(p, full)), None)
    name = (a.name or "").strip()
    if existing:
        existing["category"] = category
        if name:
            existing["displayName"] = name
        if prerelease:
            existing["prerelease"] = True
        verb = "Updated"
    else:
        taken = {p.get("id") for p in providers}
        pid, n = slug(full.split("/", 1)[1]), 2
        while pid in taken:
            pid, n = f"{slug(full.split('/', 1)[1])}-{n}", n + 1
        entry = {"id": pid, "category": category, "url": full}
        if name:
            entry["displayName"] = name
        if prerelease:
            entry["prerelease"] = True
        entry["source_url"] = f"https://github.com/{full}"
        providers.append(entry)
        verb = "Added"
    save(a.file, data)
    cat_name = dict(cats)[category]
    lines = [f"{verb} {name or full} in {cat_name}.", "",
             "Your repository is being published again now; that takes about a minute."]
    if prerelease:
        lines += ["", "Its newest release with a .wgt or .tpk is marked as a pre-release, so pre-releases are listed for this app."]
    say(lines)


def remove(a):
    data = load(a.file)
    if not data or not data.get("providers"):
        fail("There are no apps in your repository yet, so there is nothing to remove.")
    providers = data["providers"]
    parsed = parse_app(a.app)
    full = f"{parsed[0]}/{parsed[1]}" if parsed else None
    keep = [p for p in providers if not (p.get("id") == a.app.strip() or (full and same_app(p, full)))]
    if len(keep) == len(providers):
        fail(f"'{a.app}' is not in your repository. These are:",
             *[f"- {p.get('displayName') or p['url']}" for p in providers])
    if not keep:
        fail("That is the last app in your repository, and a repository needs at least one.",
             "",
             "Add another app first, or, to stop publishing altogether, disable the Publish workflow",
             "(Actions > Publish > the ... menu > Disable workflow).")
    gone = ", ".join(p.get("displayName") or p["url"] for p in providers if p not in keep)
    data["providers"] = keep
    save(a.file, data)
    say([f"Removed {gone}.", "", "Your repository is being published again now; that takes about a minute."])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add")
    p.add_argument("--file", default="repository.input.json")
    p.add_argument("--repository", required=True, help="the publisher's own GitHub repo, owner/name")
    p.add_argument("--app", required=True)
    p.add_argument("--category", required=True)
    p.add_argument("--name", default="")
    r = sub.add_parser("remove")
    r.add_argument("--file", default="repository.input.json")
    r.add_argument("--app", required=True)
    a = ap.parse_args()
    (add if a.cmd == "add" else remove)(a)


if __name__ == "__main__":
    main()
