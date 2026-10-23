#!/usr/bin/env python3
"""Read what each shipped package says about itself, for catalog.json.

For every .wgt/.tpk in DIR, the manifest inside the package (config.xml for a web
app, tizen-manifest.xml for a native one) gives the version, the application id
and the package id. Those three go into catalog.json so Apps2Samsung can show an
app's real version before install, match a package installed on a TV to its
catalog entry by id, and tell whether the catalog has a different version than
the TV reports (Apps2Samsung/Apps2Samsung#820).

The manifest is the same thing the TV reads at install, so the version here is
the one the TV's app list shows afterwards. A GitHub tag is not involved at all.

Usage:
  package-info.py DIR            prints {"<file>": {"version": ..., "app_id": ..., "package_id": ...}, ...}

Only the manifest entry is taken out of the zip, nothing is executed. A package
without a readable manifest gets an empty object, and the catalog entry simply
stays without these fields. The parsing itself is scan-packages.py's, so the two
scripts never disagree about a manifest.
"""

import importlib.util
import json
import os
import sys
import tempfile
import zipfile


def load_scanner():
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("scan_packages", os.path.join(here, "scan-packages.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def package_info(scanner, path):
    name = os.path.basename(path)
    kind = "tpk" if name.lower().endswith(".tpk") else "wgt"
    manifest_name = "tizen-manifest.xml" if kind == "tpk" else "config.xml"
    try:
        with zipfile.ZipFile(path) as z:
            try:
                data = z.read(manifest_name)
            except KeyError:
                return {}
    except zipfile.BadZipFile:
        return {}

    # The parsers take a directory with the manifest at its root; hand them one
    # holding just that file. Nothing else from the package touches the disk.
    tmp = tempfile.mkdtemp(prefix="pkginfo-")
    try:
        with open(os.path.join(tmp, manifest_name), "wb") as f:
            f.write(data)
        parse = scanner.parse_tpk_manifest if kind == "tpk" else scanner.parse_wgt_manifest
        manifest = parse(tmp, lambda *args, **kwargs: None)
    finally:
        try:
            os.remove(os.path.join(tmp, manifest_name))
            os.rmdir(tmp)
        except OSError:
            pass

    info = {}
    for key in ("version", "app_id", "package_id"):
        value = manifest.get(key)
        if isinstance(value, str) and value.strip():
            info[key] = value.strip()
    return info


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        print("usage: package-info.py DIR", file=sys.stderr)
        return 2
    scanner = load_scanner()
    result = {}
    for name in sorted(os.listdir(sys.argv[1])):
        if not name.lower().endswith((".wgt", ".tpk")):
            continue
        result[name] = package_info(scanner, os.path.join(sys.argv[1], name))
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
