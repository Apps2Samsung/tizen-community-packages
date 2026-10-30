# 📦 `packages/`: one JSON file per app

Every app in the community bundle is defined by **a single JSON file in this folder**. A PR bot
validates each file against [`../packages.schema.json`](../packages.schema.json); the build then
compiles them into `repos-build.json` / `repos-sync.json` via
[`../scripts/build-manifests.sh`](../scripts/build-manifests.sh). You don't edit anything else.

To add an app: **fork → add `packages/<owner>__<repo>.json` → open a PR.** A green check means the
file is valid and ready to merge.

---

## 🏷️ File name

Name the file after the app's repository (`owner/repo`, on GitHub or GitLab), with the `/` replaced by a
**double underscore**:

```
packages/<owner>__<repo>.json
```

Examples: `PatrickSt1991/flixor-tizen` → `packages/PatrickSt1991__flixor-tizen.json`;
`Apps2Samsung/Overscan` → `packages/Apps2Samsung__Overscan.json`.

---

## 🧩 Fields

### Always required

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Display name in the README table. No `\|` or newlines. |
| `description` | string | One-line description for the README table. No `\|` or newlines. |
| `category` | enum | Where the app shows up when the Apps2Samsung list is filtered: see [Category, group and variant](#%EF%B8%8F-category-group-and-variant). |
| `repo` | string | `owner/repo` on the forge named by `host` (GitHub by default). Used as the manifest key, the README link, and (for `build`/`release`) the API target. |
| `source` | enum | One of `release`, `build`, `direct`: see below. |

### Optional (any type)

| Field | Type | Notes |
|-------|------|-------|
| `repo_label` | string | Link text for the README's Repository column. Defaults to the repo owner. |
| `group` | string | Folds this package into one Apps2Samsung entry together with every other package that names the same group (the Moonlight forks). A package with several `assets[]` folds by itself. |
| `variant` | string | Label for this package's file inside its group, e.g. `OneLiberty · Chrome`. Single-file packages only; with `assets[]` put `variant` on each asset entry. Defaults to the file name. |
| `output_name` | string | Filename inside the bundle. Must end in `.wgt` or `.tpk`. Required for every type **except** a `release` that uses `assets[]`. |
| `extract` | string | Only when upstream ships the package **inside a `.zip`**. Entry name or regex to pull out of the archive: see [Zip-wrapped downloads](#-zip-wrapped-downloads). |
| `release_tag_prefix` | string | `release` only. For a monorepo that releases the Tizen build under its own tags while GitHub's "latest" points at another component (e.g. `smart-tv-v` for `smart-tv-v0.7.0`). Uses the newest stable release whose tag starts with this prefix (a prerelease only if none is stable) instead of `/releases/latest`. |
| `enabled` | boolean | `false` retires the package without deleting the file: see [Retiring a package](#-retiring-a-package). Defaults to `true`. |
| `adult` | boolean | `true` marks an 18+ app: hidden in Apps2Samsung until the user turns on its 18+ toggle, listed in a collapsed README section: see [Adult (18+) apps](#-adult-18-apps). Defaults to `false`. |
| `flags` | array | `["root"]` for a package that gains root on the TV. Apps2Samsung asks for confirmation before installing it, see [Root packages](#-root-packages). |
| `user_settings` | object | Values the user fills in before install, written into the package before re-signing, see [User settings](#%EF%B8%8F-user-settings). |
| `host` | enum | `github` (default) or `gitlab`. Where `repo` lives. `gitlab` is only supported for `source: "build"`: see [GitLab-hosted projects](#-gitlab-hosted-projects). |

### Which fields go with which `source`

| Field | `release` | `build` | `direct` |
|-------|:---------:|:-------:|:--------:|
| `branch` | ✅ required | ✅ required | ❌ |
| `output_name` | ✅ *(or `assets`)* | ✅ required | ✅ required |
| `assets[]` | ✅ *(or `output_name`)* | ❌ | ❌ |
| `extract` | ⬜ optional | ❌ | ⬜ optional |
| `release_tag_prefix` | ⬜ optional | ❌ | ❌ |
| `url` | ❌ | ❌ | ✅ required |
| `project_path` | ❌ | ⬜ optional | ❌ |
| `skip_npm` | ❌ | ⬜ optional | ❌ |
| `pre_build` | ❌ | ⬜ optional | ❌ |
| `overlay` | ❌ | ⬜ optional | ❌ |
| `host` | ❌ | ⬜ optional | ❌ |

For a `release`, `output_name` and `assets[]` are **mutually exclusive**: use exactly one. With
`assets[]`, put `extract` on the individual asset entry rather than at the top level.

---

## 🏷️ Category, group and variant

Apps2Samsung reads a `catalog.json` from every community release (built by
[`../scripts/build-catalog.sh`](../scripts/build-catalog.sh), one entry per shipped file) and uses it
to filter the app list and to fold variants of the same app into one entry.

**`category`** is required and is one of:

| Value | Shown as | What goes here |
|-------|----------|----------------|
| `media` | Media servers & players | Clients for Jellyfin, Plex, Kodi, Immich, music servers; local USB / DLNA / SMB players |
| `iptv` | IPTV & Live TV | M3U / Xtream / Stalker players, live TV and broadcaster apps |
| `streaming` | Streaming | Clients for streaming services and sites: YouTube, Twitch, Kick, anime, Nuvio, Stremio |
| `games` | Games & emulators | Games, emulators and game streaming (Moonlight, Chiaki) |
| `casting` | Casting & cameras | AirPlay / FCast receivers, IP camera and NVR viewers |
| `tools` | Tools & system | Browsers, loaders, network and system utilities |
| `other` | Other | Anything that fits none of the above |

**`group`** folds packages together. Every package that names the same group becomes one entry in the
Apps2Samsung app list, and its files are offered in a variant picker. Use it when several repos ship
the same app (forks, a web and a native build):

```json
{
  "name": "Moonlight (No Gamemode)",
  "description": "Open-source client for NVIDIA GameStream and Sunshine with gamemode disabled.",
  "category": "games",
  "group": "Moonlight",
  "variant": "MrPhaze62 · No Gamemode",
  "repo": "MrPhaze62/moonlight-chrome-tizen-no-gamemode",
  "source": "release",
  "branch": "main",
  "output_name": "Moonlight-Chrome-NoGame.wgt"
}
```

A package with **several `assets[]`** is folded by itself (its group defaults to its `name`), so it only
needs a `variant` per asset:

```json
"assets": [
  { "match": "Overscan-tizen4.tpk", "variant": "Tizen 4", "output_name": "Overscan-tizen4.tpk" },
  { "match": "Overscan-nui.tpk",    "variant": "Tizen 9", "output_name": "Overscan-tizen9.tpk" }
]
```

Without a `variant` the picker shows the file name without its extension. Keep variant labels short
and distinctive within the group: the fork or author, the Tizen version range, or what differs.

### What `catalog.json` carries

Every community release ships a `catalog.json` next to its packages, one entry per shipped file.
Each entry copies the manifest's `name`, `description`, `category`, `group`, `variant`, `repo`,
`adult`, `flags` and `user_settings`, and adds what the package says about itself, read from its own
`config.xml` or `tizen-manifest.xml` when the bundle is assembled
([`../scripts/package-info.py`](../scripts/package-info.py)): `version`, `app_id`, `package_id` and
`required_version` (the `required_version` of a `.wgt`, the `api-version` of a `.tpk`). Apps2Samsung
compares `version` with what the TV reports after an install. TV-Store labels an app whose
`required_version` is newer than the TV it runs on and does not push it, because the TV would refuse
it with `install failed[118, -19]` (TV-Store#44). None of these come from the manifest in this
folder; they are read from the package itself.

---

## 🚀 `source: "release"`: prebuilt `.wgt`/`.tpk` from GitHub Releases

The most common type. The build pulls the artifact from the repo's latest GitHub Release on
`branch`.

**One artifact**: name it with `output_name`. This only works when the release has **exactly one
asset**: the build downloads the first asset it finds, so a release that also ships an `.apk`, a zip
or a checksum file would hand you the wrong file. The PR check rejects a single `output_name` on a
release with several assets; use `assets[]` with a `match` (below) instead.

```json
{
  "name": "Flixor-Tizen",
  "description": "Modern cross-platform Plex client. Ported to Tizen OS.",
  "repo": "PatrickSt1991/flixor-tizen",
  "repo_label": "Flixor-Tizen",
  "source": "release",
  "branch": "release",
  "output_name": "Plex-Flixor.wgt"
}
```

**Pick the artifact by pattern**: when the release asset name varies (e.g. carries a version),
use `assets[]` with a `match` (an exact asset name **or a regex** tested against each release asset
name) and the `output_name` to save it as:

```json
{
  "name": "Nuvio",
  "description": "TV-first streaming UI for Samsung Tizen.",
  "repo": "NuvioMedia/NuvioWeb",
  "source": "release",
  "branch": "main",
  "assets": [
    { "match": "NuvioTV-Tizen-.*[.]wgt$", "output_name": "NuvioTV-Official.wgt" }
  ]
}
```

**Multiple artifacts from one release**: list several entries (e.g. per-Tizen-version builds):

```json
{
  "name": "Overscan",
  "description": "Sideloadable web browser for Samsung Tizen TVs: desktop user agent, JavaScript on, D-pad cursor.",
  "repo": "Apps2Samsung/Overscan",
  "repo_label": "Apps2Samsung",
  "source": "release",
  "branch": "release",
  "assets": [
    { "match": "Overscan-tizen4.tpk", "output_name": "Overscan-tizen4.tpk" },
    { "match": "Overscan-tizen5.tpk", "output_name": "Overscan-tizen5.tpk" },
    { "match": "Overscan-tizen8.tpk", "output_name": "Overscan-tizen8.tpk" },
    { "match": "Overscan-nui.tpk",    "output_name": "Overscan-tizen9.tpk" }
  ]
}
```

---

## 🗜️ Zip-wrapped downloads

Some upstreams publish their `.wgt` **inside a `.zip`** instead of as a bare release asset. Without
`extract` the sync would download that zip and simply rename it to `output_name`, producing a
zip-of-a-`.wgt` that installs on nothing, and it fails *silently*, because a `.wgt` is itself a zip,
so no glob or copy downstream notices.

Set `extract` to the entry name (or a regex) to pull out of the archive:

```json
{
  "name": "EN TV Player",
  "description": "IPTV player for Samsung Tizen TVs with full remote control, DRM support, and per-channel proxy.",
  "repo": "Nur-allhi/en-tvplayer",
  "source": "release",
  "branch": "main",
  "extract": "[.]wgt$",
  "output_name": "EN-IPTV_Player.wgt"
}
```

The download is replaced in place by the extracted entry, then kept under `output_name`. With
`assets[]`, `extract` goes on the entry whose asset is the zip:

```json
"assets": [
  { "match": "MyApp-.*[.]zip$", "extract": "[.]wgt$", "output_name": "MyApp.wgt" }
]
```

If nothing in the archive matches, the sync warns and leaves the download untouched rather than
failing the run. As a backstop, the publish job inspects every file in the final bundle and drops
any `.wgt`/`.tpk` that turns out to contain another `.wgt`/`.tpk`.

---

## 🔨 `source: "build"`: compiled from source with Tizen Studio

Use when there's no prebuilt release and the app is a Tizen web project the CI can package.

| Field | Purpose |
|-------|---------|
| `branch` | Branch to check out. |
| `project_path` | Subdirectory containing the Tizen web project. Defaults to `"."`. |
| `skip_npm` | `true` to skip the automatic `npm install` (for projects with no `package.json`, or that vendor their deps). |
| `pre_build` | Shell command run **before** packaging (e.g. build the web bundle). |
| `overlay` | Name of a directory under [`../apps/`](../apps/) whose contents are copied over the project before packaging, e.g. a `config.xml` the upstream repo doesn't ship. |

**Minimal build** (project lives in `app/`, no npm):

```json
{
  "name": "iperf3 TV",
  "description": "Measures your Samsung TV's network throughput to an iperf3 server, upload or download. Requires a small WebSocket-to-TCP relay on your LAN.",
  "repo": "DmitryMaksakov/samsung-tv-iperf3",
  "source": "build",
  "branch": "main",
  "project_path": "app",
  "skip_npm": true,
  "output_name": "iperf3-TV.wgt"
}
```

**Build with a pre-build step:**

```json
{
  "name": "Reiverr",
  "description": "A clean combined interface for Jellyfin, TMDB, Radarr and Sonarr, as well as a replacement to Overseerr.",
  "repo": "aleksilassila/reiverr",
  "source": "build",
  "branch": "master",
  "project_path": "tizen",
  "pre_build": "npm install --no-audit --no-fund && VITE_PLATFORM=tv npx vite build --mode production --outDir tizen/dist",
  "output_name": "Reiverr.wgt"
}
```

**Build with an overlay** (copies `apps/react-iptv/` over the checked-out project, e.g. to supply a
`config.xml`):

```json
{
  "name": "React IPTV",
  "description": "IPTV player for Samsung Tizen TV, built with React.",
  "repo": "anandsimmy/react-iptv",
  "source": "build",
  "branch": "main",
  "project_path": "build",
  "pre_build": "CI=false npm run build",
  "overlay": "react-iptv",
  "output_name": "React-IPTV.wgt"
}
```

### 🦊 GitLab-hosted projects

If the Tizen project lives on **gitlab.com** instead of GitHub, add `"host": "gitlab"`. The sync then
tracks the branch head through the GitLab API and clones from `https://gitlab.com/<owner>/<repo>.git`;
everything else (`project_path`, `skip_npm`, `pre_build`, `overlay`) works the same. The file is still
named `packages/<owner>__<repo>.json`.

```json
{
  "name": "ImmiTV",
  "description": "Lightweight Immich photo and video client for Samsung Tizen 4.0 TVs.",
  "repo": "xHiqhAim/immitv",
  "host": "gitlab",
  "source": "build",
  "branch": "main",
  "skip_npm": true,
  "output_name": "ImmiTV.wgt"
}
```

Only `source: "build"` supports `host: "gitlab"` for now: GitLab Releases and the Package Registry are
not wired up, so a `release` or `direct` manifest must not set `host`.

---

## 🔗 `source: "direct"`: a fixed URL

Use when the `.wgt`/`.tpk` is hosted at a stable absolute URL (including one committed under
[`../apps/`](../apps/) in this repo). Requires `url` + `output_name`; no `branch`.

```json
{
  "name": "Stremio (Tizen 4)",
  "description": "Stremio media center packaged for Tizen 4.0 devices.",
  "repo": "Apps2Samsung/tizen-community-packages",
  "source": "direct",
  "url": "https://raw.githubusercontent.com/Apps2Samsung/tizen-community-packages/main/apps/Stremio.wgt",
  "output_name": "Stremio-Tizen4.wgt"
}
```

---

## 🔞 Adult (18+) apps

An app whose content is for adults only (pornography or other sexually explicit material) is
accepted under the same rules as everything else (open-source, redistributable, scanned), but must
carry `"adult": true`:

```json
{
  "name": "StashZen",
  "description": "A Stash client for Samsung Tizen TVs.",
  "category": "media",
  "adult": true,
  "repo": "Stashified/StashZen",
  "source": "release",
  "branch": "main",
  "assets": [
    { "match": "StashZen-.*[.]wgt$", "output_name": "StashZen.wgt" }
  ]
}
```

What the flag does:

- **Apps2Samsung** reads `adult: true` on every file of the package in `catalog.json` and hides those
  entries (and any group one of them belongs to) until the user turns on the 18+ toggle in its
  settings. The toggle is off by default.
- **The README** lists the package in a collapsed *Adult (18+)* section right under the main table,
  not in the table itself.
- **The bundle** is unchanged: the file is built, scanned and shipped like any other package.

`adult` is independent of `category`: still give the app the category that says what it *is* (a
Stash client is `media`, an adult IPTV player is `iptv`). Keep `name` and `description` plain :
they are the only text a user sees before opting in, and they land in a public README.

---

## ⚙️ User settings

A package that needs a per-user value (an API key, a server URL, a port) declares a
`user_settings` block. Apps2Samsung shows a form before installing, stores the answers per app (and
prefills them on update), and writes them into the package before it re-signs it.

When the value goes into **one file**, set `file` and give every field a `find` / `replace`:

```json
"user_settings": {
  "help_url": "https://github.com/joseamijares/frame-dashboard#readme",
  "file": "dashboard-url.js",
  "fields": [
    {
      "key": "dashboard_url",
      "label": "Dashboard URL",
      "type": "text",
      "find": "window.DASHBOARD_URL = \"\";",
      "replace": "window.DASHBOARD_URL = \"{value}\";"
    }
  ]
}
```

When a value lands in **several places or files**, leave `file` out and give every field a
`targets` list instead. Every target is applied:

```json
"user_settings": {
  "fields": [
    {
      "key": "port",
      "label": "Dashboard port",
      "type": "number",
      "required": false,
      "default": "8099",
      "min": 1024,
      "max": 65535,
      "disallow": [8001, 8002, 26101],
      "targets": [
        { "file": "config.xml", "find": "http://127.0.0.1:8099", "replace": "http://127.0.0.1:{value}" },
        { "file": "service/main.js", "find": "|| 8099;", "replace": "|| {value};" }
      ]
    }
  ]
}
```

The two forms don't mix: either `file` plus `find` / `replace` on every field, or `targets` on
every field and no `file`.

| Field key | Notes |
|-----------|-------|
| `key` | Stable id (`a-z`, `0-9`, `_`). The stored value is kept under it, so don't rename it later. |
| `label` | Shown in the form. |
| `type` | `number` (written as-is) or `text` (quotes and backslashes escaped). |
| `required` | Defaults to `true`. |
| `pattern` | Regex the value must match. |
| `default` | Written when the field is optional and left empty, so every `find` is always replaced. |
| `min`, `max`, `disallow` | `number` only. Inclusive range, and values the form rejects. |
| `find`, `replace` | Exact text to replace and its replacement; `replace` must contain `{value}`. |
| `targets` | `[{ file, find, replace }]`, same rules per entry. |

Paths are relative to the package root (for `build`, relative to `project_path`), with no leading
`/` and no `..`. Each `find` must be in its file: when upstream changes the text, the install fails
instead of handing the TV an unpatched package.

---

## 🔓 Root packages

A package that gains root on the TV (an on-boot service plus a root agent started through the TV's
own SDB) must carry `"flags": ["root"]`. Before installing it, Apps2Samsung tells the user that:

- the package gains root and runs a background service from boot;
- after install, Developer Mode **Host PC IP** must be set to `127.0.0.1` and the TV restarted;
- while it is `127.0.0.1`, no PC (Apps2Samsung included) can reach the TV over SDB, so updates and
  other installs need Host PC IP set back to the PC first.

Put the Host PC IP step in the `description` too: older Apps2Samsung versions don't know the flag.

---

## 🚫 Retiring a package

To stop shipping an app without deleting its manifest (upstream went away, the fix was merged
upstream, the fork is superseded), set `enabled` to `false`:

```json
{
  "name": "TVapp (Fixed)",
  "description": "TVapp with community fixes.",
  "repo": "PatrickSt1991/TVapp",
  "enabled": false,
  "source": "release",
  "branch": "main",
  "assets": [
    { "match": "TVapp.wgt", "output_name": "TVApp-Fixed.wgt" }
  ]
}
```

`build-manifests.sh` drops disabled manifests before compiling `repos-build.json` /
`repos-sync.json`, and every downstream job reads only those two files. So the package is no longer
checked for upstream changes, built, downloaded or attached to the release, and its row disappears
from the README table and the package-count badge. The file itself stays valid and fully
schema-checked, so removing the line is all it takes to bring the app back.

---

## ✅ Before you open the PR

- File is named `packages/<owner>__<repo>.json`.
- `name` and `description` contain no `|` or newlines (they land in a Markdown table).
- `category` is one of the seven values above; if the app belongs with an existing one, set the same `group`.
- Adult-only content? Set `"adult": true` and keep `name` / `description` plain.
- Gains root on the TV? Set `"flags": ["root"]`.
- The fields match your `source` (see the table above): the schema rejects mismatches, e.g. `url`
  on a `release`, or both `output_name` and `assets` on the same `release`.
- `output_name` ends in `.wgt` or `.tpk`.
- For a `release`: if the upstream release has more than one asset, you used `assets[]` with a `match`.
- The app is open-source / redistributable, and tested on at least one Tizen device or emulator.
- The app isn't offered already: not by another manifest in this folder (search for the repo and the
  name, in any case), and not by Apps2Samsung itself, which lists Jellyfin, Moonfin, Litefin and
  TizenTube on its own from its
  [`third-party-apps.json`](https://github.com/Apps2Samsung/Apps2Samsung/blob/main/third-party-apps.json).
  The PR check rejects both.

The PR bot validates against [`../packages.schema.json`](../packages.schema.json) automatically, and
downloads the file your manifest picks: it fails if that file has no `config.xml` /
`tizen-manifest.xml` (not an installable Tizen package). A green check means it's ready.
