#!/usr/bin/env python3
"""Check data/categories.json, and that every manifest uses one of its ids.

data/categories.json is the one list of catalog categories: an array whose
order is the display order, each entry {id, name, color, emoji?}. It feeds
catalog.json ("categories" and "category_colors", scripts/build-catalog.sh)
and the README sections (scripts/render-readme.py).

The file itself must have: ids matching ^[a-z0-9][a-z0-9_-]{0,31}$, no id
twice, a non-empty one-line name, a colour #RRGGBB, an optional non-empty
emoji, nothing else, and an "other" entry (where an unknown category lands).

Every manifest's "category" must be one of the ids: packages.schema.json only
checks the shape, so a typo would otherwise land an app under "Other".

usage: check-categories.py [--categories FILE] [manifest.json ...]
       (no manifests: every packages/*.json)
"""
import argparse
import glob
import json
import re
import sys

ID = re.compile(r"^[a-z0-9][a-z0-9_-]{0,31}$")
COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
KEYS = {"id", "name", "color", "emoji"}


def check_file(path):
    """Errors in the categories file, and its ids in order."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        return [f"{path}: cannot read: {e}"], []
    if not isinstance(data, list) or not data:
        return [f"{path}: must be a non-empty array of {{id, name, color}} objects"], []
    errors, ids = [], []
    for i, c in enumerate(data):
        where = f"{path}[{i}]"
        if not isinstance(c, dict):
            errors.append(f"{where}: must be an object")
            continue
        extra = sorted(set(c) - KEYS)
        if extra:
            errors.append(f"{where}: unknown field(s) {', '.join(extra)}")
        cid = c.get("id")
        if not isinstance(cid, str) or not ID.match(cid):
            errors.append(f"{where}: id {cid!r} must match {ID.pattern}")
        elif cid in ids:
            errors.append(f"{where}: id '{cid}' is listed twice")
        else:
            ids.append(cid)
        name = c.get("name")
        if not isinstance(name, str) or not name.strip() or "\n" in name or "|" in name:
            errors.append(f"{where}: name must be a non-empty line without '|'")
        if not isinstance(c.get("color"), str) or not COLOR.match(c["color"]):
            errors.append(f"{where}: color {c.get('color')!r} must be #RRGGBB")
        if "emoji" in c and (not isinstance(c["emoji"], str) or not c["emoji"].strip()):
            errors.append(f"{where}: emoji, when present, must be a non-empty string")
    if "other" not in ids:
        errors.append(f"{path}: must have an 'other' entry (where an unknown category lands)")
    return errors, ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--categories", default="data/categories.json")
    ap.add_argument("manifests", nargs="*")
    args = ap.parse_args()

    errors, ids = check_file(args.categories)
    if not errors:
        allowed = ", ".join(ids)
        for path in args.manifests or sorted(glob.glob("packages/*.json")):
            try:
                with open(path, encoding="utf-8") as f:
                    cat = json.load(f).get("category")
            except (OSError, ValueError, AttributeError) as e:
                errors.append(f"{path}: cannot read: {e}")
                continue
            if cat not in ids:
                errors.append(f"{path}: category {cat!r} is not one of: {allowed} (see {args.categories})")

    if errors:
        for e in errors:
            print(f"::error::{e}")
        sys.exit(1)
    print(f"OK: {len(ids)} categories ({', '.join(ids)}), every manifest uses one of them.")


if __name__ == "__main__":
    main()
