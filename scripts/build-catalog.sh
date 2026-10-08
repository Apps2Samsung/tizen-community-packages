#!/usr/bin/env bash
# Compile packages/*.json into catalog.json, the per-file index Apps2Samsung
# reads from the community release to filter by category and fold variants.
#
# One entry per shipped file (output_name), keyed to the package it came from.
# "group" folds files into one app: explicit "group" wins, a package with
# several assets[] folds by itself (group = name), anything else stands alone.
# "variant" labels a file inside its group; it defaults to the file name.
# Disabled packages are left out, like everywhere else downstream.
#
# Usage: scripts/build-catalog.sh [packages-dir] [out-file] [shipped-dir]   (run from the repo root)
# With shipped-dir, entries whose file is not in that directory are dropped, so
# the catalog never lists a build that failed and did not make the bundle.
set -euo pipefail

PKG_DIR="${1:-packages}"
OUT="${2:-catalog.json}"
SHIPPED_DIR="${3:-}"

shopt -s nullglob
files=("$PKG_DIR"/*.json)
if [ ${#files[@]} -eq 0 ]; then
  echo "ERROR: no package manifests found in $PKG_DIR/" >&2
  exit 1
fi

jq -s '
  def strip_ext: sub("\\.(wgt|tpk)$"; "");
  def entries:
    . as $p
    | (if has("assets") then
         [ .assets[] | { file: .output_name, variant: (.variant // (.output_name | strip_ext)) } ]
       else
         [ { file: .output_name, variant: ($p.variant // ($p.output_name | strip_ext)) } ]
       end)
    | map({
        file,
        name: $p.name,
        description: $p.description,
        category: $p.category,
        group: ($p.group // (if ($p.assets // [] | length) > 1 then $p.name else null end)),
        variant,
        repo: $p.repo,
        host: ($p.host // "github")
      });
  {
    schemaVersion: 1,
    categories: {
      media: "Media servers & players",
      iptv: "IPTV & Live TV",
      streaming: "Streaming",
      games: "Games & emulators",
      casting: "Casting & cameras",
      tools: "Tools & system",
      other: "Other"
    },
    apps: ( map(select(.enabled != false)) | map(entries) | add | sort_by(.file | ascii_downcase) )
  }
' "${files[@]}" > "$OUT"

if [ -n "$SHIPPED_DIR" ]; then
  shipped=$(cd "$SHIPPED_DIR" && ls -1 2>/dev/null | jq -R . | jq -s .)
  tmp=$(mktemp)
  jq --argjson shipped "$shipped" '.apps |= map(select(.file as $f | $shipped | index($f)))' "$OUT" > "$tmp" && mv "$tmp" "$OUT"
fi

echo "Wrote $OUT: $(jq '.apps | length' "$OUT") files, $(jq '[.apps[] | .group // .file] | unique | length' "$OUT") apps"
