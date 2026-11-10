#!/usr/bin/env python3
"""Regenerate the Current Packages section of README.md from packages/*.json.

Packages are grouped by category, one collapsed <details> table per category
in the order of data/categories.json (title: its emoji and name), so the README stays short as the catalog grows. Rows (name / repo link /
description) come from the manifests; the Version column comes from
.github/state/last_seen.json. Manifests with "enabled": false are retired - the
sync no longer ships them, so they are left out of the tables and the badge.
Manifests with "adult": true are kept out of the category sections and listed
in their own collapsed 18+ section after them.

Everything between the packages:start / packages:end markers is replaced;
the rest of the README is left untouched.

usage: render-readme.py [README.md]
"""
import glob
import json
import pathlib
import re
import sys

STATE = pathlib.Path(".github/state/last_seen.json")
START, END = "<!-- packages:start -->", "<!-- packages:end -->"

CATEGORIES = pathlib.Path("data/categories.json")


def category_titles():
    """Manifest category -> section title, in display order (data/categories.json)."""
    cats = json.loads(CATEGORIES.read_text(encoding="utf-8"))
    return {c["id"]: (c["emoji"] + " " if c.get("emoji") else "") + c["name"] for c in cats}


# end of the first sentence: . ! or ? followed by whitespace and a capital/digit
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"(])")


def version_map():
    """'<source>:<repo>' (repo lowercased) -> version shown in the table."""
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    ver = {}
    for k, v in state.items():
        if k.startswith("release:"):
            repo, version = k[8:], v
        elif k.startswith("build:"):
            repo, version = k[6:].split("@", 1)[0], v[:7]   # short SHA
        elif k.startswith("direct:"):
            repo = k[7:]
            m = re.search(r"mod:([^|]*)", v)
            version = (m.group(1).strip() or "latest") if m else "latest"
        else:
            continue
        ver[k.split(":", 1)[0] + ":" + repo.lower()] = version
    return ver


def first_sentence(text):
    return SENTENCE_END.split(text.strip(), 1)[0]


def manifests():
    for path in sorted(glob.glob("packages/*.json")):
        d = json.loads(pathlib.Path(path).read_text())
        if d.get("enabled", True):
            yield d


def table(items):
    out = ["| \U0001F9E9 Application | \U0001F4DD Description | ⚙️ Version |",
           "|----------------|----------------|------------|"]
    out += [f"| **{n}**<br>{link} | {desc} | `{v}` |" for n, link, desc, v in items]
    return out


def details(summary, items):
    items = sorted(items, key=lambda r: r[0].lower())
    return ["", "<details>", f"<summary>{summary}</summary>", "", *table(items), "", "</details>"]


def section():
    ver = version_map()
    titles = category_titles()
    groups = {key: [] for key in titles}
    adult = []
    for d in manifests():
        repo = d["repo"]
        label = d.get("repo_label", repo.split("/")[0])
        forge = "gitlab.com" if d.get("host") == "gitlab" else "github.com"
        cat = d.get("category") if d.get("category") in titles else "other"
        (adult if d.get("adult") is True else groups[cat]).append((
            d["name"], f"[{label}](https://{forge}/{repo})",
            first_sentence(d["description"]).replace("|", "\\|"),
            ver.get(f"{d['source']}:{repo.lower()}", "n/a"),
        ))

    out = [START]
    for key, title in titles.items():
        if groups[key]:
            out += details(f"<b>{title}</b> ({len(groups[key])})", groups[key])
    if adult:
        out += details(f"\U0001F51E <b>Adult (18+)</b>: {len(adult)} package(s). "
                       "Hidden in Apps2Samsung until you turn on its 18+ toggle.", adult)
    out += ["", END]
    return out


def main():
    readme = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "README.md")
    text = readme.read_text()
    if START not in text or END not in text:
        sys.exit(f"{readme}: missing {START} / {END} markers")
    head, rest = text.split(START, 1)
    tail = rest.split(END, 1)[1]
    text = head + "\n".join(section()) + tail
    # keep the package-count badge in sync (enabled packages only)
    count = sum(1 for _ in manifests())
    text = re.sub(r"(img\.shields\.io/badge/packages-)\d+(-)", rf"\g<1>{count}\g<2>", text)
    readme.write_text(text)
    print(f"Rendered README package sections + badge ({count} enabled packages).")


if __name__ == "__main__":
    main()
