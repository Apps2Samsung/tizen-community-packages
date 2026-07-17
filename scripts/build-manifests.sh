#!/usr/bin/env bash
# Regenerate the legacy repos-build.json / repos-sync.json from packages/*.json.
#
# packages/ is the source of truth (one file per app). This script compiles
# those files back into the two aggregate manifests the sync workflow already
# consumes, so nothing downstream had to change. Run from the repo root.
set -euo pipefail

PKG_DIR="${1:-packages}"

shopt -s nullglob
files=("$PKG_DIR"/*.json)
if [ ${#files[@]} -eq 0 ]; then
  echo "ERROR: no package manifests found in $PKG_DIR/" >&2
  exit 1
fi

# --- repos-build.json : { "<repo>": { branch, project_path, output_name, [skip_npm], [pre_build] } }
jq -s '
  map(select(.source == "build"))
  | map({
      key: .repo,
      value: (
        { branch, project_path: (.project_path // "."), output_name }
        + (if has("skip_npm")  then { skip_npm:  .skip_npm }  else {} end)
        + (if has("pre_build") then { pre_build: .pre_build } else {} end)
      )
    })
  | from_entries
' "${files[@]}" > repos-build.json

# --- repos-sync.json : { releases: {...}, direct: {...} }
jq -s '
  {
    releases: (
      map(select(.source == "release"))
      | map({
          key: .repo,
          value: ({ branch } + (if has("assets") then { assets } else { output_name } end))
        })
      | from_entries
    ),
    direct: (
      map(select(.source == "direct"))
      | map({ key: .repo, value: { url, output_name } })
      | from_entries
    )
  }
' "${files[@]}" > repos-sync.json

echo "Compiled ${#files[@]} manifest(s):"
echo "  build:   $(jq 'length' repos-build.json)"
echo "  release: $(jq '.releases | length' repos-sync.json)"
echo "  direct:  $(jq '.direct  | length' repos-sync.json)"
