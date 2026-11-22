#!/usr/bin/env python3
"""Run repo-validate.py against every case in spec/fixtures/index.json.

  python3 -I scripts/test-repo-spec.py

Exit code 0 when every case gives the expected outcome and reason.
"""

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "..", "spec", "fixtures")


def load_validator():
    spec = importlib.util.spec_from_file_location("repo_validate", os.path.join(HERE, "repo-validate.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    v = load_validator()
    with open(os.path.join(FIXTURES, "index.json"), encoding="utf-8") as f:
        index = json.load(f)
    now = v.parse_time(index["now"])
    failures = 0
    for case in index["cases"]:
        with open(os.path.join(FIXTURES, case["file"]), "rb") as f:
            data = f.read()
        not_before = v.parse_time(case["notBefore"]) if "notBefore" in case else None
        try:
            v.validate(data, os.path.join(FIXTURES, case["key"]), case.get("fingerprint"), now, not_before)
            got, reason = "accept", None
        except v.Rejected as e:
            got, reason = "reject", e.reason
        ok = got == case["expect"] and reason == case.get("reason")
        failures += not ok
        label = case["file"] + ("" if "notBefore" not in case and "fingerprint" not in case else " (" + ", ".join(k for k in ("notBefore", "fingerprint") if k in case) + ")")
        print(f"{'ok  ' if ok else 'FAIL'} {label}: expected {case['expect']}{' [' + case['reason'] + ']' if case.get('reason') else ''}, got {got}{' [' + reason + ']' if reason else ''}")
    print(f"{len(index['cases']) - failures}/{len(index['cases'])} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
