#!/usr/bin/env bash
# Regenerate the legacy repos-build.json / repos-sync.json from packages/*.json.
#
# packages/ is the source of truth (one file per app). This script compiles
# those files back into the two aggregate manifests the sync workflow already
# consumes, so nothing downstream had to change. Run from the repo root.
#
# Manifests with "enabled": false are dropped here. That single filter retires a
# package everywhere downstream — change detection, the build matrix, the release
# downloads and the published bundle all read only these compiled manifests — so
# the file can stay in packages/ without shipping.
set -euo pipefail

PKG_DIR="${1:-packages}"

shopt -s nullglob
files=("$PKG_DIR"/*.json)
if [ ${#files[@]} -eq 0 ]; then
  echo "ERROR: no package manifests found in $PKG_DIR/" >&2
  exit 1
fi

# --- repos-build.json : { "<repo>": { branch, project_path, output_name, [skip_npm], [pre_build], [overlay], [host] } }
jq -s '
  map(select(.enabled != false))
  | map(select(.source == "build"))
  | map({
      key: .repo,
      value: (
        { branch, project_path: (.project_path // "."), output_name }
        + (if has("skip_npm")  then { skip_npm:  .skip_npm }  else {} end)
        + (if has("pre_build") then { pre_build: .pre_build } else {} end)
        + (if has("overlay")   then { overlay:   .overlay }   else {} end)
        + (if has("host")      then { host:      .host }      else {} end)
      )
    })
  | from_entries
' "${files[@]}" > repos-build.json

# --- repos-sync.json : { releases: {...}, direct: {...} }
jq -s '
  map(select(.enabled != false))
  | {
    releases: (
      map(select(.source == "release"))
      | map({
          key: .repo,
          value: ({ branch }
                   + (if has("assets")  then { assets }  else { output_name } end)
                   + (if has("extract") then { extract } else {} end))
        })
      | from_entries
    ),
    direct: (
      map(select(.source == "direct"))
      | map({
          key: .repo,
          value: ({ url, output_name }
                   + (if has("extract") then { extract } else {} end))
        })
      | from_entries
    )
  }
' "${files[@]}" > repos-sync.json

disabled=$(jq -s '[.[] | select(.enabled == false) | .repo] | join(", ")' -r "${files[@]}")
[ -n "$disabled" ] && echo "Skipped (enabled: false): $disabled"

echo "Read ${#files[@]} manifest(s), compiled:"
echo "  build:   $(jq 'length' repos-build.json)"
echo "  release: $(jq '.releases | length' repos-sync.json)"
echo "  direct:  $(jq '.direct  | length' repos-sync.json)"
