#!/usr/bin/env bash
# Download one upstream package file (.wgt, .tpk or a zip wrapping one).
#
# Plain `curl -L -o` saves whatever the server answers, so a GitHub
# "504 Gateway Time-out" page landed in the bundle as a 92-byte .wgt, failed the
# security scan and dropped the app (community-821 and 823 lost 62 apps that way).
# This retries transient errors, and when the download still fails, or the
# answer is not a zip, it leaves no file behind and exits 1. The caller then
# skips the package, and publish-release ships it from the last good bundle
# ("Keep previous files where the refresh came up short").
#
# Usage: fetch-asset.sh <out-file> <url>
set -uo pipefail

out="${1:?usage: fetch-asset.sh <out-file> <url>}"
url="${2:?usage: fetch-asset.sh <out-file> <url>}"

tmp="$out.part"
rm -f "$tmp"
if ! curl -fL --retry 4 --retry-all-errors --retry-delay 15 --connect-timeout 30 \
       --no-progress-meter -o "$tmp" "$url"; then
  rm -f "$tmp"
  echo "::warning title=Download failed::$(basename "$out") from $url failed after retries - keeping the previous version."
  exit 1
fi

# Every package format is a zip; anything else is an error page or a wrong asset.
if [ "$(head -c 2 "$tmp")" != "PK" ]; then
  echo "::warning title=Download not a package::$(basename "$out") from $url is not a zip ($(wc -c < "$tmp") bytes, starts with: $(head -c 60 "$tmp" | tr -c '[:print:]' ' ')) - keeping the previous version."
  rm -f "$tmp"
  exit 1
fi

mv "$tmp" "$out"
