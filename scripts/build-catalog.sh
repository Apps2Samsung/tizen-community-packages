#!/usr/bin/env bash
# Compile packages/*.json into catalog.json, the per-file index Apps2Samsung
# reads from the community release to filter by category and fold variants.
#
# One entry per shipped file (output_name), keyed to the package it came from.
# "group" folds files into one app: explicit "group" wins, a package with
# several assets[] folds by itself (group = name), anything else stands alone.
# "variant" labels a file inside its group; it defaults to the file name.
# Disabled packages are left out, like everywhere else downstream.
# "user_settings" is copied through as-is when the package declares it.
# "adult": true is copied onto each of the package's files when the package
# declares it, so Apps2Samsung can hide those entries until the user turns on
# its 18+ toggle (a group is adult when any of its files is). Left out when false.
# "flags" (e.g. ["root"]) is copied onto each of the package's files when the
# package declares it, so Apps2Samsung can warn before installing.
# "cert_level": "partner" is copied onto each of the package's files when the
# package declares it, so Apps2Samsung and TV-Store sign it with a Partner certificate.
# "moved_to" ({url, fingerprint}) is copied onto each of the package's files when the
# package declares it: the app now lives in an independent repository, and Apps2Samsung
# offers to add that repository with the fingerprint pre-approved (docs/repositories.md).
# Disabled packages with a "removed" block are listed under top-level "removed" (one entry
# per package, never in "apps"): name, repo, category, reason, note, files, since, and the
# package_ids / app_ids its files had, so Apps2Samsung and TV-Store can flag an installed
# copy and answer a search with why it is gone. The ids and "since" are carried from
# prev-catalog (the previous release's catalog.json), where the package was still in "apps"
# or already in "removed"; "since" is today the first time a package shows up as removed.
#
# Usage: scripts/build-catalog.sh [packages-dir] [out-file] [shipped-dir] [prev-catalog]   (run from the repo root)
# With shipped-dir, entries whose file is not in that directory are dropped, so
# the catalog never lists a build that failed and did not make the bundle, and
# each remaining entry gets "version", "app_id" and "package_id" read from the
# manifest inside its file (scripts/package-info.py): the version the TV will
# report once installed, and the ids Apps2Samsung matches installed apps on
# (Apps2Samsung/Apps2Samsung#820). Fields are left out, never empty, when a
# manifest does not carry them.
set -euo pipefail

PKG_DIR="${1:-packages}"
OUT="${2:-catalog.json}"
SHIPPED_DIR="${3:-}"
PREV="${4:-}"

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
      } + (if $p.user_settings then { user_settings: $p.user_settings } else {} end)
        + (if $p.adult == true then { adult: true } else {} end)
        + (if $p.flags then { flags: $p.flags } else {} end)
        + (if $p.cert_level == "partner" then { cert_level: "partner" } else {} end)
        + (if $p.moved_to then { moved_to: $p.moved_to } else {} end));
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
    apps: ( map(select(.enabled != false)) | map(entries) | add | sort_by(.file | ascii_downcase) ),
    removed: ( map(select(.enabled == false and .removed))
               | map({ name: (.group // .name), repo, host: (.host // "github"), category, reason: .removed.reason,
                       files: (if has("assets") then [ .assets[].output_name ] else [ .output_name ] end) }
                     + (if .removed.note then { note: .removed.note } else {} end))
               | sort_by(.name | ascii_downcase) )
  }
' "${files[@]}" > "$OUT"

# Removed entries: ids and first-removed date from the previous release, when there is one.
prev='{}'
if [ -n "$PREV" ] && [ -s "$PREV" ] && jq -e . "$PREV" >/dev/null 2>&1; then prev=$(cat "$PREV"); fi
tmp=$(mktemp)
jq --argjson prev "$prev" --arg today "$(date -u +%F)" '
  def ids($r; $k): [ ($prev.apps // [])[] | select((.repo // "" | ascii_downcase) == $r) | .[$k] // empty ]
               + [ ($prev.removed // [])[] | select((.repo // "" | ascii_downcase) == $r) | (.[$k + "s"] // [])[] ]
               | unique;
  .removed |= map(
    (.repo | ascii_downcase) as $r
    | . + { since: ([ ($prev.removed // [])[] | select((.repo // "" | ascii_downcase) == $r) | .since // empty ][0] // $today) }
        + (ids($r; "package_id") as $p | if ($p | length) > 0 then { package_ids: $p } else {} end)
        + (ids($r; "app_id") as $a | if ($a | length) > 0 then { app_ids: $a } else {} end))
' "$OUT" > "$tmp"
mv "$tmp" "$OUT"

if [ -n "$SHIPPED_DIR" ]; then
  shipped=$(cd "$SHIPPED_DIR" && ls -1 2>/dev/null | jq -R . | jq -s .)
  tmp=$(mktemp)
  jq --argjson shipped "$shipped" '.apps |= map(select(.file as $f | $shipped | index($f)))' "$OUT" > "$tmp" && mv "$tmp" "$OUT"

  # What each file says about itself: version + ids from its manifest.
  info=$(mktemp)
  python3 "$(dirname "$0")/package-info.py" "$SHIPPED_DIR" > "$info"
  jq --slurpfile info "$info" '.apps |= map(. + ($info[0][.file] // {}))' "$OUT" > "$tmp" && mv "$tmp" "$OUT"
  rm -f "$info"
  echo "Manifest info for $(jq '[.apps[] | select(.version)] | length' "$OUT") of $(jq '.apps | length' "$OUT") files"
fi

echo "Wrote $OUT: $(jq '.apps | length' "$OUT") files, $(jq '[.apps[] | .group // .file] | unique | length' "$OUT") apps, $(jq '.removed | length' "$OUT") removed ($(jq '[.removed[] | select(.package_ids)] | length' "$OUT") with ids)"
