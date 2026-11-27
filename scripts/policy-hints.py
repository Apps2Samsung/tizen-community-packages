#!/usr/bin/env python3
"""Hints for the reviewer of a package PR: things "What we accept" asks for that a
machine can only guess at (packages/README.md#-what-we-accept).

Usage:
  policy-hints.py MANIFEST... [--scan-dir _scan] [--md hints.md] [--pr-author LOGIN]

For every added or changed manifest it looks for:
  closed-source  the source isn't public (direct download, private or missing repo,
                 or a repo without source files) but the manifest has no
                 "closed-source" flag; or a closed-source app not submitted by the
                 repo owner (redistribution permission must be stated)
  self-updating  the shipped package fetches code from GitHub or a CDN and runs it,
                 or loads an npm package without a version, but has no
                 "self-updating" flag (packages in --scan-dir, as the security scan
                 downloaded them; build-from-source packages are not downloaded here)
  new-account    the repo or its owner's account is only days old
  fork-group     the repo is a fork of an app already in the catalog and doesn't
                 share its "group"
  default-source the app may ship with a content source of its own: the shipped
                 package has a hard-coded playlist, Xtream login, addon manifest or
                 magnet link (packages in --scan-dir), or the repo is a fork whose
                 source adds hosts its upstream doesn't have (compare with the parent)

Every hint is a guess for a person to check, never a verdict: this script always
exits 0 and never fails a PR. It prints ::warning annotations and, with --md,
writes a Markdown section (empty file when there is nothing to say). Packages are
opened as zip files and read; nothing in them is executed. GITHUB_TOKEN is used
for api.github.com when set.
"""

import argparse
import datetime as dt
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.request
import zipfile

NEW_DAYS = 14
SOURCE_EXT = re.compile(r"\.(js|mjs|cjs|ts|tsx|jsx|vue|svelte|html?|css|scss|c|cc|cpp|h|hpp|cs|py|java|kt|go|rs|swift|dart|lua)$", re.I)
# Code hosts an app could pull newer code from.
HOST = re.compile(rb"raw\.githubusercontent\.com|api\.github\.com/repos|cdn\.jsdelivr\.net/gh/|githack\.com|gitcdn")
# What turns fetched text into running code, or keeps it for the next launch.
EXEC = re.compile(rb"\beval\s*\(|new\s+Function\s*\(|createElement\(\s*[\"']script[\"']\s*\)|localStorage\.setItem\([^)]{0,40}(?:bundle|code|script)", re.I)
UPDATE = re.compile(rb"self.?update|auto.?update|update.?bundle|downloadUpdate|applyUpdate", re.I)
PASSIVE = re.compile(rb"\.(png|jpe?g|gif|svg|webp|ico|woff2?|ttf|otf|md|txt)$|/LICEN[SC]E|/README", re.I)
RELEASE_FILES = re.compile(rb"browser_download_url|zipball|tarball|/releases/download/")
WINDOW = 3000
UPDATE_PATH = re.compile(rb"/updates?(?:/|$)", re.I)
NPM = re.compile(rb"https?://(?:cdn\.jsdelivr\.net/npm|unpkg\.com)/((?:@[\w.-]+/)?[\w.-]+)(@[\w.^~-]+)?/")
CODE_FILE = re.compile(r"\.(js|mjs|html?)$", re.I)
# default-source: where a shipped package or a fork's diff names a content source.
SCAN_FILE = re.compile(r"\.(js|mjs|cjs|html?|json|xml|txt|m3u8?|so|dll|wasm|bin)$", re.I)
SCAN_MAX = 96 * 1024 * 1024
URL = re.compile(rb"https?://([A-Za-z0-9.-]+\.[A-Za-z0-9-]+)(?::\d+)?(/[^\s\"'`<>\\\x00-\x1f\x7f-\xff]{0,200})?")
MAGNET = re.compile(rb"magnet:\?xt=urn:bt[im]h:[A-Za-z0-9]{20,}")
SOURCE_KINDS = (
    ("playlist", re.compile(rb"\.m3u8?(?:[?#]|$)", re.I)),
    ("Xtream login", re.compile(rb"/(?:get|player_api|xmltv)\.php", re.I)),
    ("addon manifest", re.compile(rb"/manifest\.json(?:[?#]|$)", re.I)),
)
# Placeholders and the device itself: never a source.
LOCAL = re.compile(r"(^|\.)(localhost|example\.(com|org|net))$|\.(example|test|invalid|local)$|^(127|10|192\.168|0)\.", re.I)
# Allowed as a default by "What we accept".
SOURCE_OK = re.compile(r"(^|\.)iptv-org\.github\.io$", re.I)
IPTV_ORG = re.compile(rb"^/iptv-org/", re.I)
# Hosts every fork may add without it saying anything about content.
NEUTRAL = re.compile(r"(^|\.)(github\.com|w3\.org|tizen\.org|samsung\.com|apache\.org|gnu\.org|mozilla\.org|opensource\.org"
                     r"|creativecommons\.org|fonts\.googleapis\.com|fonts\.gstatic\.com|themoviedb\.org|tmdb\.org)$", re.I)
INCLUDE_EXT = re.compile(r"\.(inc|inl)$", re.I)
ROUTES = re.compile(r"/stream/|\.m3u8?\b|player_api\.php|get\.php\?username|/manifest\.json|magnet:\?", re.I)
ACCOUNT = re.compile(r"subscri|assinatura|suscrip|abonnement|\bplano\b|\bbanned\b|banido|anti-?bloqueio|anti-?block|unblock", re.I)
MAX_SHOWN = 8


def gh(path):
    req = urllib.request.Request("https://api.github.com" + path, headers={
        "Accept": "application/vnd.github+json", "User-Agent": "tizen-community-packages policy-hints"})
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"_status": e.code}
    except Exception:
        return None


def safe(text):
    """For text from a PR inside `code` in the comment: no backticks to break out of it."""
    return str(text).replace("`", "'").replace("\n", " ")


def age_days(stamp):
    try:
        t = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None
    return (dt.datetime.now(dt.timezone.utc) - t).days


def output_names(m):
    if m.get("assets"):
        return [a.get("output_name") for a in m["assets"] if a.get("output_name")]
    return [m["output_name"]] if m.get("output_name") else []


def code_findings(path):
    """Evidence that a package downloads and runs newer code: a list of short strings."""
    evidence = set()
    try:
        z = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError):
        return []
    for name in z.namelist():
        if not CODE_FILE.search(name) or "node_modules/" in name:
            continue
        try:
            data = z.read(name)
        except Exception:
            continue
        for m in NPM.finditer(data):
            ver = (m.group(2) or b"").decode("utf-8", "replace")
            if not ver or ver == "@latest" or ver.startswith(("@^", "@~")):
                evidence.add(f"`{name}` loads npm `{m.group(1).decode('utf-8', 'replace')}{ver}` without a fixed version")
        for h in HOST.finditer(data):
            url = re.split(rb"[\"'`\s)]", data[h.start():h.start() + 300], 1)[0]
            if PASSIVE.search(url):
                continue  # an image, font or licence link, not code
            window = data[max(0, h.start() - WINDOW): h.end() + WINDOW]
            # A releases API call that never touches the release's files is the usual
            # "new version available" notice.
            if h.group(0) == b"api.github.com/repos" and not RELEASE_FILES.search(window):
                continue
            runs, updates = bool(EXEC.search(window)), bool(UPDATE.search(window))
            feed = bool(UPDATE_PATH.search(url))
            if runs or updates or feed:
                what = "runs fetched code" if runs else ("has self-update logic" if updates else "points at an update feed")
                evidence.add(f"`{name}` references {h.group(0).decode()} and {what} nearby")
    return sorted(evidence)


def source_findings(path):
    """Content sources hard-coded in a package: {host or 'magnet link': kind}."""
    found = {}
    try:
        z = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError):
        return found
    for item in z.infolist():
        if not SCAN_FILE.search(item.filename) or "node_modules/" in item.filename or item.file_size > SCAN_MAX:
            continue
        try:
            data = z.read(item)
        except Exception:
            continue
        if MAGNET.search(data):
            found.setdefault("magnet link", "torrent")
        for m in URL.finditer(data):
            host, rest = m.group(1).decode("ascii", "replace").lower(), m.group(2) or b""
            if LOCAL.search(host) or SOURCE_OK.search(host) or (host == "raw.githubusercontent.com" and IPTV_ORG.search(rest)):
                continue
            for kind, pattern in SOURCE_KINDS:
                if pattern.search(rest):
                    found.setdefault(host, kind)
                    break
    return found


def fork_findings(repo, info, branch):
    """What a fork's source adds over its parent: (new hosts, most used first; notes)."""
    parent = info["parent"]
    base = f"{parent['owner']['login']}:{parent.get('default_branch', 'main')}"
    diff = gh(f"/repos/{repo}/compare/{base}...{branch or info.get('default_branch', 'main')}")
    if not diff or "_status" in diff:
        return [], []
    added, removed, routes, account = {}, set(), False, False
    for f in diff.get("files", []):
        name = f.get("filename", "")
        if not (SOURCE_EXT.search(name) or INCLUDE_EXT.search(name)):
            continue
        for line in (f.get("patch") or "").split("\n"):
            if line[:1] not in "+-" or line[:3] in ("+++", "---"):
                continue
            hosts = [m.group(1).decode("ascii", "replace").lower() for m in URL.finditer(line.encode("utf-8", "replace"))]
            if line[0] == "-":
                removed.update(hosts)
                continue
            for host in hosts:
                added[host] = added.get(host, 0) + 1
            routes = routes or bool(ROUTES.search(line))
            account = account or bool(ACCOUNT.search(line))
    hosts = sorted((h for h in added if h not in removed and not NEUTRAL.search(h) and not LOCAL.search(h)), key=lambda h: (-added[h], h))
    notes = (["stream, playlist or addon routes"] if routes else []) + (["account, subscription or unblocking wording"] if account else [])
    return hosts, notes


def has_source_files(repo):
    """True / False from the repo tree, None when it can't be told."""
    info = gh(f"/repos/{repo}")
    if not info or "_status" in info:
        return None, info
    tree = gh(f"/repos/{repo}/git/trees/{info.get('default_branch', 'main')}?recursive=1")
    if not tree or "_status" in tree or tree.get("truncated"):
        return None, info
    return any(SOURCE_EXT.search(t.get("path", "")) for t in tree.get("tree", []) if t.get("type") == "blob"), info


def hints_for(path, catalog, scan_dir, pr_author):
    m = json.load(open(path, encoding="utf-8"))
    name, repo, flags = m.get("name", path), m.get("repo", ""), set(m.get("flags") or [])
    host = m.get("host", "github")
    out = []

    # closed-source
    info = None
    if host == "github" and repo:
        has_src, info = has_source_files(repo)
        status = (info or {}).get("_status")
        if "closed-source" not in flags:
            if status == 404:
                out.append(("closed-source", f"`{repo}` can't be found (private or missing), so the source isn't public. If that's right, add `\"flags\": [\"closed-source\"]` and say where redistribution is allowed."))
            elif has_src is False:
                out.append(("closed-source", f"`{repo}` has no source files (only docs or releases). If the source isn't public, add `\"flags\": [\"closed-source\"]`."))
            elif m.get("source") == "direct" and has_src is not True:
                out.append(("closed-source", "Direct download and no public source found. If the source isn't public, add `\"flags\": [\"closed-source\"]`."))
    if "closed-source" in flags and pr_author and repo and pr_author.lower() != repo.split("/")[0].lower():
        out.append(("closed-source", f"Closed source, submitted by `{safe(pr_author)}` rather than the owner of `{repo}`. Check that the PR or the repo states redistribution is allowed."))

    # self-updating
    if "self-updating" not in flags and scan_dir:
        for out_name in output_names(m):
            f = os.path.join(scan_dir, out_name)
            if os.path.isfile(f):
                ev = code_findings(f)
                if ev:
                    out.append(("self-updating", f"`{out_name}` may download and run newer code: " + "; ".join(ev[:4])
                                + ". If it really does, add `\"flags\": [\"self-updating\"]` (allowed only from its own repo/domain or the upstream it names). A \"new version available\" notice alone doesn't count."))

    # default-source
    if scan_dir:
        for out_name in output_names(m):
            f = os.path.join(scan_dir, out_name)
            found = source_findings(f) if os.path.isfile(f) else {}
            if found:
                shown = ", ".join(f"`{safe(h)}` ({kind})" for h, kind in sorted(found.items())[:MAX_SHOWN])
                more = f" and {len(found) - MAX_SHOWN} more" if len(found) > MAX_SHOWN else ""
                out.append(("default-source", f"`{out_name}` has a content source built in: {shown}{more}. "
                            "A preset playlist, addon or scraper is not accepted, unless it is iptv-org or the rights holder's own server. A source the user adds is fine."))
    if info and info.get("fork") and info.get("parent"):
        hosts, notes = fork_findings(repo, info, m.get("branch"))
        if hosts:
            shown = ", ".join(f"`{safe(h)}`" for h in hosts[:MAX_SHOWN])
            more = f" and {len(hosts) - MAX_SHOWN} more" if len(hosts) > MAX_SHOWN else ""
            extra = f" The same changes also add {' and '.join(notes)}." if notes else ""
            out.append(("default-source", f"Compared with `{info['parent']['full_name']}`, the source adds these hosts: {shown}{more}.{extra} "
                        "Check that none of them is a content source the app ships with."))

    # new-account
    if info and "_status" not in info:
        repo_age = age_days(info.get("created_at"))
        owner = gh(f"/users/{info.get('owner', {}).get('login', '')}") if info.get("owner") else None
        owner_age = age_days((owner or {}).get("created_at"))
        young = []
        if repo_age is not None and repo_age < NEW_DAYS:
            young.append(f"repo created {repo_age} day(s) ago")
        if owner_age is not None and owner_age < NEW_DAYS:
            young.append(f"account created {owner_age} day(s) ago")
        if young:
            out.append(("new-account", f"`{repo}`: {', '.join(young)}. Not a problem by itself, but check the code rather than the description."))

    # fork-group
    if info and info.get("fork") and info.get("parent"):
        parent = info["parent"]["full_name"].lower()
        for other in catalog:
            if other.get("repo", "").lower() == parent and other.get("_path") != path:
                same = m.get("group") and m.get("group") == other.get("group")
                if not same:
                    out.append(("fork-group", f"Fork of `{info['parent']['full_name']}`, which is in the catalog as `{safe(other.get('name', ''))}`. Set the same `group` on both (with a `variant` each), so Apps2Samsung shows one entry with a picker."))
                break
    return name, out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Policy hints for a package PR (never fails).")
    ap.add_argument("manifests", nargs="*")
    ap.add_argument("--scan-dir")
    ap.add_argument("--md")
    ap.add_argument("--pr-author")
    a = ap.parse_args(argv)

    catalog = []
    for p in glob.glob("packages/*.json"):
        try:
            d = json.load(open(p, encoding="utf-8"))
            d["_path"] = p
            catalog.append(d)
        except (OSError, ValueError):
            pass

    sections = []
    for path in a.manifests:
        try:
            name, hints = hints_for(path, catalog, a.scan_dir, a.pr_author)
        except Exception as e:  # a hint must never break the check
            print(f"::notice::policy hints skipped for {path}: {e}")
            continue
        for kind, text in hints:
            plain = re.sub(r"[`*]", "", text)
            print(f"::warning file={path},title=Policy hint ({kind})::{plain}")
        if hints:
            sections.append(f"`{safe(name)}` (`{path}`)\n" + "\n".join(f"- **{kind}**: {text}" for kind, text in hints))

    if a.md:
        with open(a.md, "w", encoding="utf-8") as f:
            if sections:
                f.write("### Policy hints for the reviewer\n\n"
                        "Guesses a machine can make about [What we accept](https://github.com/Apps2Samsung/tizen-community-packages/blob/main/packages/README.md#-what-we-accept). "
                        "They don't fail the check; a maintainer decides.\n\n" + "\n\n".join(sections) + "\n")
    print(f"{sum(1 for _ in sections)} manifest(s) with hints")
    return 0


if __name__ == "__main__":
    sys.exit(main())
