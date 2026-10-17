#!/usr/bin/env python3
"""Static security scan of the Tizen packages that go into a community bundle.

This is NOT a code audit. It opens every .wgt/.tpk in a directory and reports what
can be checked mechanically, so anyone can see at a glance what an app asks for
and who it talks to:

  * manifest: app id, version, requested privileges (elevated ones flagged),
    network access rules, background services, signer of the package
  * contents: file inventory, native binaries inside a *web* app, nested packages
  * code: hostnames and raw IPs referenced by the HTML/JS, remote script loading,
    obfuscation / packer signatures, known crypto-miner strings
  * ClamAV, when `clamscan` is on PATH (known-malware signatures)

Findings have three levels. `info` is just reporting, `warn` deserves a look,
`critical` means the file must not ship. With --quarantine DIR, critical files are
moved out of the scan directory so the rest of the bundle can still be released.

Usage:
  scan-packages.py DIR [--json scan.json] [--md scan-report.md]
                       [--fail-on critical|warn|never] [--quarantine DIR] [--no-clamav]

Everything in DIR is treated as untrusted data: it is unzipped and read, never
executed. Exit status 0 unless a finding reaches --fail-on (default: critical).
"""
import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict

LEVELS = {"info": 0, "warn": 1, "critical": 2}

# Partner/platform-level privileges. Listed only so the report can mark them; a
# request for one is NOT a finding: Tizen ignores privileges the signing certificate
# does not cover, so a sideloaded app gains nothing by declaring them.
ELEVATED_PRIVILEGES = {
    "http://tizen.org/privilege/appmanager.kill",
    "http://tizen.org/privilege/appmanager.certificate",
    "http://tizen.org/privilege/packagemanager.install",
    "http://tizen.org/privilege/packagemanager.admin",
    "http://tizen.org/privilege/packagemanager.clearcache",
    "http://tizen.org/privilege/systemsettings.admin",
    "http://tizen.org/privilege/systemmanager",
    "http://tizen.org/privilege/keymanager.admin",
    "http://tizen.org/privilege/bluetooth.admin",
    "http://tizen.org/privilege/bluetoothmanager",
    "http://tizen.org/privilege/telephony",
    "http://tizen.org/privilege/telephony.admin",
    "http://tizen.org/privilege/tv.channel",
    "http://tizen.org/privilege/tv.window",
    "http://tizen.org/privilege/tv.display",
    "http://tizen.org/privilege/datasharing",
    "http://tizen.org/privilege/externalstorage",
    "http://tizen.org/privilege/developer.samsung.com",
    "http://developer.samsung.com/privilege/sso.partner",
    "http://developer.samsung.com/privilege/tvinputdevice.admin",
    "http://developer.samsung.com/privilege/appcommon",
    "http://developer.samsung.com/privilege/application.control",
}

# Privileges that are routine for a TV app but still worth showing explicitly
# (they touch the camera/microphone or local storage of the TV).
SENSITIVE_PRIVILEGES = {
    "http://tizen.org/privilege/mediacapture": "camera/microphone capture",
    "http://tizen.org/privilege/recorder": "audio/video recording",
    "http://tizen.org/privilege/camera": "camera",
    "http://developer.samsung.com/privilege/microphone": "microphone",
    "http://tizen.org/privilege/filesystem.write": "write to TV storage",
    "http://tizen.org/privilege/mediastorage": "media storage access",
    "http://tizen.org/privilege/externalstorage": "USB storage access",
    "http://tizen.org/privilege/location": "location",
    "http://tizen.org/privilege/contact.read": "contacts",
    "http://tizen.org/privilege/application.launch": "launch other apps",
    "http://tizen.org/privilege/appmanager.kill": "kill other apps",
}

TEXT_EXT = {".js", ".mjs", ".cjs", ".html", ".htm", ".json", ".css", ".xml", ".txt", ".map", ".ts", ".svelte", ".vue"}
CODE_EXT = {".js", ".mjs", ".cjs", ".html", ".htm"}
NATIVE_EXT = {".so", ".dll", ".exe", ".bin", ".sh", ".elf"}
MAX_TEXT_BYTES = 25 * 1024 * 1024

CRITICAL_PATTERNS = [
    ("crypto-miner", re.compile(r"coinhive|coin-hive|cryptonight|cryptoloot|webminepool|minero\.cc|stratum\+tcp://|jsecoin|deepminer", re.I)),
]
WARN_PATTERNS = [
    ("js-packer (eval(function(p,a,c,k,e,d)))", re.compile(r"eval\(function\(p,a,c,k,e,[dr]\)", re.I)),
    ("jjencode/aaencode obfuscation", re.compile(r"\$=~\[\];\$=\{___:\+\+\$|ﾟωﾟﾉ=")),
    ("javascript-obfuscator string array", re.compile(r"_0x[0-9a-f]{4,6}\s*\(\s*0x[0-9a-f]+\s*\)")),
]
INFO_PATTERNS = [
    ("eval()", re.compile(r"(?<![\w.$])eval\s*\(")),
    ("new Function()", re.compile(r"new\s+Function\s*\(")),
    ("document.write()", re.compile(r"document\.write(?:ln)?\s*\(")),
    ("runtime <script> injection", re.compile(r"createElement\s*\(\s*['\"]script['\"]\s*\)", re.I)),
    ("WebSocket", re.compile(r"new\s+WebSocket\s*\(")),
    ("tizen.filesystem", re.compile(r"\btizen\.filesystem\b")),
    ("tizen.application.launch", re.compile(r"\btizen\.application\.launch(?:AppControl)?\s*\(")),
    ("webapis.productinfo (TV serial/model)", re.compile(r"\bwebapis\.productinfo\.get(?:Duid|Serial|Model|FirmwareVersion|RealModel)")),
    ("webapis.network (MAC/IP)", re.compile(r"\bwebapis\.network\.get(?:Mac|Ip)\b")),
    ("tizen.systeminfo", re.compile(r"\btizen\.systeminfo\.getPropertyValue")),
]

URL_RE = re.compile(r"""(?:https?|wss?)://([A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+|\d{1,3}(?:\.\d{1,3}){3})(?::\d{1,5})?""")
_OCTET = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
RAW_IP_RE = re.compile(r"(?<![\w.])(" + _OCTET + r"(?:\." + _OCTET + r"){3})(?![\w.])")
REMOTE_SCRIPT_TAG_RE = re.compile(r"""<script[^>]+src\s*=\s*["']((?:https?:)?//[^"']+)["']""", re.I)
PLACEHOLDER_HOSTS = {"www.w3.org", "w3.org", "tizen.org", "developer.samsung.com", "samsung.com", "www.samsung.com",
                     "schemas.microsoft.com", "schemas.openxmlformats.org", "xmlns.com", "purl.org", "example.com",
                     "www.example.com", "localhost", "yourdomain", "github.com", "www.github.com", "ns.adobe.com",
                     "developer.mozilla.org", "www.apache.org", "opensource.org", "creativecommons.org",
                     "nodejs.org", "www.npmjs.com", "npmjs.com", "registry.npmjs.org", "reactjs.org",
                     "fb.me", "goo.gl", "bit.ly", "www.gnu.org", "gnu.org", "git.io", "webpack.js.org", "babeljs.io",
                     "unpkg.com", "cdn.jsdelivr.net", "fonts.googleapis.com", "fonts.gstatic.com", "www.google.com"}
_PRIVATE_IP = re.compile(r"^(10\.|127\.|0\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|169\.254\.|255\.|224\.)")


class Finding:
    __slots__ = ("level", "code", "message", "where")

    def __init__(self, level, code, message, where=None):
        self.level, self.code, self.message, self.where = level, code, message, where

    def to_dict(self):
        d = {"level": self.level, "code": self.code, "message": self.message}
        if self.where:
            d["where"] = self.where
        return d


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_text_file(path):
    return os.path.splitext(path)[1].lower() in TEXT_EXT


def read_text(path):
    try:
        if os.path.getsize(path) > MAX_TEXT_BYTES:
            return None
        with open(path, "rb") as f:
            return f.read().decode("utf-8", "replace")
    except OSError:
        return None


def local(tag):
    return tag.rsplit("}", 1)[-1]


def parse_wgt_manifest(root_dir, add):
    path = os.path.join(root_dir, "config.xml")
    info = {"kind": "wgt", "manifest": "config.xml"}
    if not os.path.isfile(path):
        add("warn", "no-manifest", "no config.xml at the root of the package")
        return info
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        add("warn", "bad-manifest", f"config.xml does not parse: {e}")
        return info
    w = tree.getroot()
    info["widget_id"] = w.get("id")
    info["version"] = w.get("version")
    privileges, access, services, settings, metadata = [], [], [], {}, {}
    for el in w.iter():
        t = local(el.tag)
        if t == "name" and "name" not in info and (el.text or "").strip():
            info["name"] = el.text.strip()
        elif t == "application":
            info["app_id"] = el.get("id")
            info["package_id"] = el.get("package")
            info["required_version"] = el.get("required_version")
        elif t == "privilege" and el.get("name"):
            privileges.append(el.get("name"))
        elif t == "access":
            access.append({"origin": el.get("origin"), "subdomains": el.get("subdomains")})
        elif t == "allow-navigation" and (el.text or "").strip():
            access.append({"allow-navigation": el.text.strip()})
        elif t == "service":
            services.append({"id": el.get("id"), "on_boot": el.get("on-boot"), "auto_restart": el.get("auto-restart")})
        elif t == "setting":
            settings.update(el.attrib)
        elif t == "metadata" and el.get("key"):
            metadata[el.get("key")] = el.get("value")
        elif t == "content-security-policy" and (el.text or "").strip():
            info["csp"] = el.text.strip()
    info.update(privileges=sorted(set(privileges)), access=access, services=services, settings=settings)
    if "http://samsung.com/tv/metadata/use.uwe" in metadata:
        info["uwe"] = metadata["http://samsung.com/tv/metadata/use.uwe"]
    if any(a.get("origin") == "*" for a in access):
        add("info", "network-any-origin", "may load content from any origin (`<access origin=\"*\">`); normal for apps that wrap a website")
    if settings.get("background-support") == "enable":
        add("info", "background-support", "keeps running when another app is in the foreground (background-support=enable)")
    for s in services:
        flag = "on_boot" if s.get("on_boot") == "true" else None
        add("warn" if flag else "info", "background-service",
            f"declares a background service `{s.get('id')}`" + (" that starts at TV boot and auto-restarts" if flag and s.get("auto_restart") == "true" else " that starts at TV boot" if flag else ""))
    if "app_id" not in info:
        add("warn", "no-app-id", "config.xml has no <tizen:application id=...>; the package will not install")
    return info


def parse_tpk_manifest(root_dir, add):
    path = os.path.join(root_dir, "tizen-manifest.xml")
    info = {"kind": "tpk", "manifest": "tizen-manifest.xml"}
    if not os.path.isfile(path):
        add("warn", "no-manifest", "no tizen-manifest.xml at the root of the package")
        return info
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        add("warn", "bad-manifest", f"tizen-manifest.xml does not parse: {e}")
        return info
    m = tree.getroot()
    info["package_id"] = m.get("package")
    info["version"] = m.get("version")
    info["api_version"] = m.get("api-version")
    privileges, apps = [], []
    for el in m.iter():
        t = local(el.tag)
        if t == "privilege" and (el.text or "").strip():
            privileges.append(el.text.strip())
        elif t in ("ui-application", "service-application", "widget-application", "watch-application"):
            apps.append({"type": t, "appid": el.get("appid"), "exec": el.get("exec"), "runtime": el.get("type")})
            if t == "service-application":
                add("warn" if el.get("auto-restart") == "true" or el.get("on-boot") == "true" else "info", "background-service",
                    f"declares a native service application `{el.get('appid')}`")
        elif t == "label" and "name" not in info and (el.text or "").strip():
            info["name"] = el.text.strip()
    if apps:
        info["app_id"] = apps[0].get("appid")
    info.update(privileges=sorted(set(privileges)), applications=apps)
    add("info", "native-package", "native (.tpk) package: compiled code, only the manifest and strings can be inspected")
    return info


def check_privileges(privs, add):
    for p in privs:
        if p in SENSITIVE_PRIVILEGES:
            add("info", "sensitive-privilege", f"requests `{p}` ({SENSITIVE_PRIVILEGES[p]})")


def signer_subjects(root_dir):
    """Best-effort: subject of the first certificate in each signature file (needs openssl)."""
    out = {}
    if not shutil.which("openssl"):
        return out
    for sig in ("author-signature.xml", "signature1.xml", "signature2.xml"):
        path = os.path.join(root_dir, sig)
        if not os.path.isfile(path):
            continue
        txt = read_text(path) or ""
        m = re.search(r"<(?:\w+:)?X509Certificate>\s*([A-Za-z0-9+/=\s]+?)\s*</(?:\w+:)?X509Certificate>", txt)
        if not m:
            continue
        try:
            der = base64.b64decode(re.sub(r"\s+", "", m.group(1)))
            r = subprocess.run(["openssl", "x509", "-inform", "DER", "-noout", "-subject", "-issuer"],
                               input=der, capture_output=True, timeout=20)
            if r.returncode == 0:
                lines = r.stdout.decode("utf-8", "replace").strip().splitlines()
                out[sig] = " | ".join(l.strip() for l in lines)
        except (subprocess.SubprocessError, ValueError):
            pass
    return out


def scan_code(root_dir, add):
    hosts, ips, remote_scripts = Counter(), Counter(), set()
    pattern_hits = defaultdict(lambda: defaultdict(int))
    minified, text_files = [], 0
    for dp, _dn, fns in os.walk(root_dir):
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, root_dir).replace(os.sep, "/")
            ext = os.path.splitext(fn)[1].lower()
            if not is_text_file(p) or rel in ("author-signature.xml", "signature1.xml", "signature2.xml", "config.xml", "tizen-manifest.xml"):
                continue
            txt = read_text(p)
            if txt is None:
                continue
            text_files += 1
            for m in URL_RE.finditer(txt):
                h = m.group(1).lower()
                if h in PLACEHOLDER_HOSTS or _PRIVATE_IP.match(h):
                    continue
                hosts[h] += 1
            if ext in CODE_EXT:
                lines = txt.count("\n") + 1
                if len(txt) > 50_000 and len(txt) / lines > 500:
                    minified.append(rel)
                for m in RAW_IP_RE.finditer(txt):
                    ip = m.group(1)
                    if all(int(o) < 256 for o in ip.split(".")) and not _PRIVATE_IP.match(ip) and not ip.endswith(".0.0"):
                        ips[ip] += 1
                for m in REMOTE_SCRIPT_TAG_RE.finditer(txt):
                    remote_scripts.add(m.group(1))
                for code, rx in CRITICAL_PATTERNS + WARN_PATTERNS + INFO_PATTERNS:
                    n = len(rx.findall(txt))
                    if n:
                        pattern_hits[code][rel] += n
    for code, rx in CRITICAL_PATTERNS:
        if code in pattern_hits:
            add("critical", "malicious-pattern", f"{code} signature found in " + ", ".join(sorted(pattern_hits[code])))
    for code, rx in WARN_PATTERNS:
        if code in pattern_hits:
            add("warn", "obfuscated-code", f"{code} in " + ", ".join(sorted(pattern_hits[code])))
    for code, rx in INFO_PATTERNS:
        if code in pattern_hits:
            files = sorted(pattern_hits[code])
            shown = ", ".join(files[:4]) + (f" (+{len(files) - 4} more)" if len(files) > 4 else "")
            add("info", "code-usage", f"uses {code} in {shown}")
    for src in sorted(remote_scripts):
        add("info", "remote-script", f"`<script src>` loads code from `{src}` at runtime")
    for ip in sorted(ips):
        add("info", "hardcoded-ip", f"references public IP address {ip}")
    if minified:
        add("info", "minified", f"{len(minified)} minified/bundled file(s): " + ", ".join(minified[:5]) + (" ..." if len(minified) > 5 else ""))
    return {"text_files": text_files, "hosts": dict(hosts.most_common()), "public_ips": dict(ips), "remote_scripts": sorted(remote_scripts), "minified": minified}


def inventory(root_dir, kind, add):
    by_ext, total, natives, nested = Counter(), 0, [], []
    for dp, _dn, fns in os.walk(root_dir):
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, root_dir).replace(os.sep, "/")
            ext = os.path.splitext(fn)[1].lower() or "(none)"
            by_ext[ext] += 1
            total += 1
            if ext in (".wgt", ".tpk"):
                nested.append(rel)
            if ext in NATIVE_EXT or ext in (".wasm", ".nexe", ".pexe"):
                natives.append(rel)
                continue
            try:
                with open(p, "rb") as f:
                    head = f.read(4)
                if head == b"\x7fELF" or head[:2] == b"MZ":
                    natives.append(rel)
            except OSError:
                pass
    if nested:
        add("critical", "nested-package", "contains another package: " + ", ".join(nested))
    if kind == "wgt":
        compiled = tuple((".wasm", ".nexe", ".pexe"))
        real = [n for n in natives if not n.endswith(compiled)]
        if real:
            add("warn", "native-in-webapp", "web app contains native binaries/scripts: " + ", ".join(real[:10]))
        if any(n.endswith(compiled) for n in natives):
            add("info", "compiled-module", "contains WebAssembly / NaCl modules (compiled code, not inspectable as text)")
    return {"files": total, "by_extension": dict(by_ext.most_common()), "native": natives}


# Parsers for file types that never occur in a Tizen package (mail, Office,
# PDF, Flash, Hangul) are disabled: they probe every file and cost minutes on a
# full bundle for nothing. HTML/JS normalization stays on: that is where the
# script-malware signatures apply.
CLAMSCAN_FLAGS = ["--no-summary", "--infected", "--max-filesize=400M", "--max-scansize=1000M", "--max-files=100000",
                  "--scan-mail=no", "--scan-ole2=no", "--scan-pdf=no", "--scan-swf=no", "--scan-xmldocs=no", "--scan-hwp3=no"]


def _parse_clamscan(stdout, pkg_dir, files, out):
    for line in stdout.splitlines():
        line = line.strip()
        if not line.endswith("FOUND"):
            continue
        path, _, sig = line[: -len("FOUND")].rpartition(": ")
        # clamscan reports "<package path>: <signature> FOUND"; nested entries
        # are reported under the archive path as well.
        name = os.path.basename(path.split("!")[0]) if path else ""
        for f in files:
            if name == f or path.startswith(os.path.join(pkg_dir, f)):
                out[f] = {"status": "infected", "hits": out[f].get("hits", []) + [sig.strip()]}
                break


def run_clamav(pkg_dir, files, jobs=1):
    """clamscan over a set of packages, in `jobs` size-balanced parallel chunks.

    clamscan loads the full signature database (~3.6M signatures, 5-20s) per
    invocation and then scans at only a few MB/s, so the work is split into a
    few chunks balanced by file size rather than one call per package. It
    unpacks zip archives itself, so the .wgt/.tpk files are scanned directly
    and hits are attributed to the package they were found in.
    Returns {file: status}.
    """
    if not files:
        return {}
    if not shutil.which("clamscan"):
        return {f: {"status": "not-run", "reason": "clamscan not installed"} for f in files}
    cmd = ["clamscan"] + CLAMSCAN_FLAGS
    if os.environ.get("CLAMAV_DB"):
        cmd.append("--database=" + os.environ["CLAMAV_DB"])
    # Greedy balancing: biggest file first into the currently lightest chunk.
    jobs = max(1, min(jobs, len(files)))
    chunks = [[] for _ in range(jobs)]
    load = [0] * jobs
    for f in sorted(files, key=lambda f: -os.path.getsize(os.path.join(pkg_dir, f))):
        i = load.index(min(load))
        chunks[i].append(f)
        load[i] += os.path.getsize(os.path.join(pkg_dir, f))
    procs = []
    for chunk in chunks:
        if chunk:
            procs.append((chunk, subprocess.Popen(cmd + [os.path.join(pkg_dir, f) for f in chunk],
                                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)))
    out = {}
    for chunk, p in procs:
        try:
            stdout, stderr = p.communicate(timeout=1800)
        except subprocess.TimeoutExpired:
            p.kill()
            out.update({f: {"status": "error", "reason": "clamscan timed out"} for f in chunk})
            continue
        if p.returncode in (0, 1):
            out.update({f: {"status": "clean"} for f in chunk})
            if p.returncode == 1:
                _parse_clamscan(stdout, pkg_dir, chunk, out)
        else:
            reason = (stderr or stdout).strip()[:500]
            out.update({f: {"status": "error", "reason": reason} for f in chunk})
    return out


def clamav_db_version():
    """Best-effort label of the signature set in use (for the verdict cache)."""
    db = os.environ.get("CLAMAV_DB") or "/var/lib/clamav"
    parts = []
    for name in ("main", "daily", "bytecode"):
        for ext in (".cld", ".cvd"):
            path = os.path.join(db, name + ext)
            if os.path.isfile(path):
                parts.append(f"{name}:{os.path.getsize(path)}:{int(os.path.getmtime(path))}")
                break
    return ",".join(parts) or "unknown"


def finalize(result):
    """Recompute sort order and overall level after findings were added."""
    result["findings"] = sorted(result["findings"], key=lambda f: -LEVELS[f["level"]])
    result["level"] = max((f["level"] for f in result["findings"]), key=lambda l: LEVELS[l], default="clean") if result["findings"] else "clean"
    return result


def scan_package(path):
    findings = []

    def add(level, code, message, where=None):
        findings.append(Finding(level, code, message, where))

    name = os.path.basename(path)
    result = {"file": name, "size": os.path.getsize(path), "sha256": sha256_file(path)}
    kind = "tpk" if name.lower().endswith(".tpk") else "wgt"
    tmp = tempfile.mkdtemp(prefix="pkgscan-")
    try:
        try:
            with zipfile.ZipFile(path) as z:
                for zi in z.infolist():
                    # Guard against zip-slip: never write outside the temp dir.
                    dest = os.path.realpath(os.path.join(tmp, zi.filename))
                    if not dest.startswith(os.path.realpath(tmp) + os.sep) and dest != os.path.realpath(tmp):
                        add("critical", "zip-slip", f"archive entry escapes the package directory: {zi.filename}")
                        continue
                    z.extract(zi, tmp)
        except zipfile.BadZipFile:
            add("critical", "not-a-zip", "file is not a valid zip archive (not a Tizen package)")
            result["findings"] = [f.to_dict() for f in findings]
            result["level"] = "critical"
            return result
        manifest = parse_tpk_manifest(tmp, add) if kind == "tpk" else parse_wgt_manifest(tmp, add)
        check_privileges(manifest.get("privileges", []), add)
        result["manifest"] = manifest
        # Signer subjects are reported when present. Unsigned packages are normal
        # here (signing happens at install time), so their absence is not a finding.
        result["signers"] = signer_subjects(tmp)
        result["inventory"] = inventory(tmp, kind, add)
        result["code"] = scan_code(tmp, add)
        result["clamav"] = {"status": "skipped"}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    result["findings"] = [f.to_dict() for f in sorted(findings, key=lambda f: -LEVELS[f.level])]
    result["level"] = max((f.level for f in findings), key=lambda l: LEVELS[l], default="info") if findings else "clean"
    return result


BADGE = {"clean": "✅ clean", "info": "✅ ok", "warn": "⚠️ review", "critical": "⛔ blocked"}


def short(privs):
    return ", ".join(p.rsplit("/", 1)[-1] for p in privs)


def render_md(results, meta):
    out = []
    out.append("# Package security scan\n")
    out.append(f"{meta['packages']} package(s) scanned on {meta['date']}. ClamAV: **{meta['clamav']}**.\n")
    out.append("This is an automated, mechanical scan: it shows what each app *asks for* (privileges), what it *references* (hosts), and whether anything "
               "known-bad or obfuscated turned up. It is not a code review. Details for each package are below the table.\n")
    out.append("| Package | Result | App id | Version | Privileges | Hosts referenced | Signed by |")
    out.append("|---|---|---|---|---|---|---|")
    for r in results:
        m = r.get("manifest", {})
        n_hosts = len(r.get("code", {}).get("hosts", {}))
        privs = str(len(m.get("privileges", [])))
        signer = r.get("signers", {}).get("author-signature.xml", "")
        cn = re.search(r"CN\s*=\s*([^,/|]+)", signer)
        out.append(f"| `{r['file']}` | {BADGE.get(r['level'], r['level'])} | `{m.get('app_id') or m.get('package_id') or '?'}` | {m.get('version') or '?'} | {privs} | {n_hosts} | {cn.group(1).strip() if cn else '—'} |")
    out.append("")
    for r in results:
        m = r.get("manifest", {})
        out.append(f"<details><summary><b>{r['file']}</b> — {BADGE.get(r['level'], r['level'])}</summary>\n")
        out.append(f"- **sha256** `{r['sha256']}` · {r['size']:,} bytes · {r.get('inventory', {}).get('files', 0)} files")
        if m:
            out.append(f"- **{m.get('manifest')}**: {m.get('name', '?')} · id `{m.get('app_id') or m.get('package_id')}` · version {m.get('version')}"
                       + (f" · required Tizen {m['required_version']}" if m.get("required_version") else "")
                       + (f" · API {m['api_version']}" if m.get("api_version") else ""))
        for sig, subj in r.get("signers", {}).items():
            out.append(f"- **{sig}**: {subj}")
        cl = r.get("clamav", {})
        out.append(f"- **ClamAV**: {cl.get('status')}" + (f" ({cl.get('reason')})" if cl.get("reason") else ""))
        fnd = [f for f in r["findings"] if f["level"] != "info"]
        if fnd:
            out.append("- **Findings:**")
            for f in fnd:
                out.append(f"  - {'⛔' if f['level'] == 'critical' else '⚠️'} {f['message']}")
        notes = [f for f in r["findings"] if f["level"] == "info"]
        if notes:
            out.append("- **Notes:**")
            for f in notes:
                out.append(f"  - {f['message']}")
        privs = m.get("privileges", [])
        if privs:
            out.append(f"- **Privileges ({len(privs)}):** " + ", ".join(
                f"`{p.rsplit('/', 1)[-1]}`" + (" (partner-level, inert without a partner certificate)" if p in ELEVATED_PRIVILEGES else "") for p in privs))
        hosts = r.get("code", {}).get("hosts", {})
        if hosts:
            shown = list(hosts.items())[:40]
            out.append(f"- **Hosts referenced ({len(hosts)}):** " + ", ".join(f"`{h}`" for h, _ in shown) + (" …" if len(hosts) > 40 else ""))
        out.append("\n</details>\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--json")
    ap.add_argument("--md")
    ap.add_argument("--fail-on", choices=["critical", "warn", "never"], default="critical")
    ap.add_argument("--quarantine", metavar="DIR", help="move packages with critical findings here instead of leaving them in DIR")
    ap.add_argument("--no-clamav", action="store_true")
    ap.add_argument("--clamav-jobs", type=int, default=max(1, os.cpu_count() or 1), help="parallel clamscan processes (default: CPU count)")
    ap.add_argument("--clamav-cache", metavar="FILE", help="JSON file of ClamAV verdicts keyed by sha256; packages already in it are not rescanned, new verdicts are added")
    args = ap.parse_args()

    files = sorted(f for f in os.listdir(args.dir) if f.lower().endswith((".wgt", ".tpk")))
    results = []
    from concurrent.futures import ProcessPoolExecutor
    workers = max(1, min(len(files), os.cpu_count() or 1))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [(f, pool.submit(scan_package, os.path.join(args.dir, f))) for f in files]
        for f, fut in futures:
            r = fut.result()
            print(f"scanned {f}: {r['level']}", flush=True)
            results.append(r)
    clam_cached = 0
    if not args.no_clamav and files:
        cache = {}
        if args.clamav_cache and os.path.isfile(args.clamav_cache):
            try:
                with open(args.clamav_cache) as fh:
                    cache = json.load(fh)
            except (OSError, ValueError):
                cache = {}
        clam = {}
        to_scan = []
        for r in results:
            hit = cache.get(r["sha256"]) if isinstance(cache, dict) else None
            if hit and hit.get("status") in ("clean", "infected"):
                clam[r["file"]] = dict(hit, cached=True)
                clam_cached += 1
            else:
                to_scan.append(r["file"])
        if to_scan:
            print(f"clamscan: {len(to_scan)} package(s) to scan, {clam_cached} verdict(s) from cache, {args.clamav_jobs} parallel ...", flush=True)
            fresh = run_clamav(args.dir, to_scan, jobs=args.clamav_jobs)
            clam.update(fresh)
            dbv = clamav_db_version()
            for r in results:
                v = fresh.get(r["file"])
                if v and v.get("status") in ("clean", "infected"):
                    cache[r["sha256"]] = dict(v, db=dbv)
            if args.clamav_cache:
                with open(args.clamav_cache, "w") as fh:
                    json.dump(cache, fh)
        else:
            print(f"clamscan: all {clam_cached} verdict(s) from cache.", flush=True)
        for r in results:
            r["clamav"] = clam.get(r["file"], {"status": "error", "reason": "no result"})
            for sig in r["clamav"].get("hits", []):
                r["findings"].append({"level": "critical", "code": "clamav", "message": f"ClamAV: {sig}"})
            finalize(r)
    for r in results:
        f = r["file"]
        for fd in r["findings"]:
            if fd["level"] == "critical":
                print(f"::error title=Blocked package::{f}: {fd['message']}")
            elif fd["level"] == "warn":
                print(f"::warning title=Review package::{f}: {fd['message']}")
        if r["level"] == "critical" and args.quarantine:
            os.makedirs(args.quarantine, exist_ok=True)
            shutil.move(os.path.join(args.dir, f), os.path.join(args.quarantine, f))
            r["quarantined"] = True
            print(f"  -> moved to {args.quarantine}/")

    import datetime
    clam = "not run"
    statuses = {r.get("clamav", {}).get("status") for r in results}
    if statuses and statuses <= {"clean", "infected"}:
        clam = "ran on every package" + (f" ({clam_cached} verdict(s) reused from an earlier scan of the identical file)" if clam_cached else "")
    elif "clean" in statuses or "infected" in statuses:
        clam = "ran on some packages"
    elif "skipped" in statuses:
        clam = "skipped"
    meta = {"date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), "packages": len(results), "clamav": clam}

    if args.json:
        with open(args.json, "w") as fh:
            json.dump({"meta": meta, "packages": results}, fh, indent=2)
    md = render_md(results, meta)
    if args.md:
        with open(args.md, "w") as fh:
            fh.write(md)
    else:
        print(md)

    worst = max((r["level"] for r in results), key=lambda l: LEVELS.get(l, -1), default="clean")
    counts = Counter(r["level"] for r in results)
    print(f"\n{len(results)} package(s): " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    if args.fail_on != "never" and LEVELS.get(worst, -1) >= LEVELS[args.fail_on] and not (args.quarantine and worst == "critical" and args.fail_on == "critical"):
        sys.exit(1)


if __name__ == "__main__":
    main()
