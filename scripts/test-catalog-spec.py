#!/usr/bin/env python3
"""Check catalog.json files against the official catalog format (docs/catalog.md).

  python3 -I scripts/test-catalog-spec.py [catalog.json ...]

Without arguments it checks spec/catalog-example.json. For each file:
  - spec/catalog.schema.json (strict: every field the build writes is in it);
  - every user_settings block against properties.user_settings in packages.schema.json;
  - what a schema can't say: file names unique, every category used is a key of
    categories, category_colors only for known categories.

Only for the release's catalog.json: the copy embedded in resolved.json is Apps2Samsung's
re-serialization (null fields left out, fields of its own added), see docs/catalog.md.

Exit code 0 when every file passes.
"""

import json
import os
import sys

import jsonschema

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check(catalog, schema, settings_schema):
    errors = []
    validator = jsonschema.Draft202012Validator(schema)
    for e in sorted(validator.iter_errors(catalog), key=lambda e: list(e.absolute_path)):
        where = "/".join(str(p) for p in e.absolute_path) or "(top level)"
        errors.append(f"{where}: {e.message}")
    if errors:
        return errors  # the checks below assume the shape is right

    settings = jsonschema.Draft202012Validator(settings_schema)
    for i, app in enumerate(catalog["apps"]):
        if "user_settings" in app:
            for e in settings.iter_errors(app["user_settings"]):
                where = "/".join(str(p) for p in e.absolute_path)
                errors.append(f"apps/{i}/user_settings/{where}: {e.message}")

    files = [a["file"] for a in catalog["apps"]]
    for f in sorted({f for f in files if files.count(f) > 1}):
        errors.append(f"apps: file {f!r} is listed more than once")
    cats = catalog["categories"]
    for i, app in enumerate(catalog["apps"]):
        if app["category"] not in cats:
            errors.append(f"apps/{i} ({app['file']}): category {app['category']!r} is not in categories")
    for i, r in enumerate(catalog["removed"]):
        if r["category"] not in cats:
            errors.append(f"removed/{i} ({r['name']}): category {r['category']!r} is not in categories")
    for c in catalog["category_colors"]:
        if c not in cats:
            errors.append(f"category_colors: {c!r} is not in categories")
    return errors


def main(argv):
    schema = load(os.path.join(ROOT, "spec", "catalog.schema.json"))
    packages = load(os.path.join(ROOT, "packages.schema.json"))
    settings_schema = dict(packages["properties"]["user_settings"])
    settings_schema["$schema"] = packages["$schema"]
    settings_schema["$defs"] = packages.get("$defs", {})

    paths = argv or [os.path.join(ROOT, "spec", "catalog-example.json")]
    failures = 0
    for path in paths:
        data = load(path)
        errors = check(data, schema, settings_schema)
        if errors:
            failures += 1
            print(f"FAIL {path}:")
            for e in errors:
                print(f"  {e}")
        else:
            print(f"ok   {path}: {len(data['apps'])} files, {len(data['removed'])} removed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
