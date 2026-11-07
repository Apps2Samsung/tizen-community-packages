#!/usr/bin/env bash
# Unwrap a zip that contains the real package.
#
# Some upstreams publish their .wgt inside a .zip release asset. Downloading
# that asset and renaming it to *.wgt produces a zip-of-a-wgt, which installs
# on nothing, and fails silently, because a .wgt is itself a zip so no glob or
# copy downstream notices. Packages in that situation set "extract" in their
# manifest and the sync workflow calls this script after the download.
#
# Usage: unwrap-zip.sh <file> <pattern>
#   file    - the downloaded file, replaced in place by the extracted entry
#   pattern - exact entry name or regex; empty/"null" makes this a no-op
#
# Never fails the caller: a wrapper that turns out not to match only warns, so
# one bad upstream cannot break the whole catalog sync.
set -euo pipefail

file="${1:?usage: unwrap-zip.sh <file> <pattern>}"
pattern="${2:-}"

[ -n "$pattern" ] && [ "$pattern" != "null" ] || exit 0

if [ ! -s "$file" ]; then
  echo "::warning title=Extract skipped::$(basename "$file") is missing or empty."
  exit 0
fi

inner=$(unzip -Z1 "$file" 2>/dev/null | grep -E "$pattern" | head -n 1 || true)
if [ -z "$inner" ]; then
  echo "::warning title=Extract failed::No entry matching '$pattern' inside $(basename "$file"); leaving the download as-is."
  echo "  Archive contents:"
  unzip -Z1 "$file" 2>/dev/null | sed 's/^/    /' || echo "    (not a zip archive)"
  exit 0
fi

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
unzip -q -j "$file" "$inner" -d "$tmp"
mv "$tmp/$(basename "$inner")" "$file"
echo "  Extracted '$inner' from the zip wrapper -> $(basename "$file")"
