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
