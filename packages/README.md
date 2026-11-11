# 📦 `packages/`: one JSON file per app

Every app in the community bundle is defined by **a single JSON file in this folder**. A PR bot
validates each file against [`../packages.schema.json`](../packages.schema.json); the build then
compiles them into `repos-build.json` / `repos-sync.json` via
[`../scripts/build-manifests.sh`](../scripts/build-manifests.sh). You don't edit anything else.

To add an app: **fork → add `packages/<owner>__<repo>.json` → open a PR.** A green check means the
file is valid and ready to merge.

---

## 📜 What we accept

### Accepted

- **Open-source apps**: the source is in the linked repository, under any license that allows
  redistribution (MIT, Apache, BSD, GPL, MPL and others). Without a license, the author's written
  permission in a public place is enough: an issue or discussion comment, linked from the manifest's
  PR (for example no-cover's apps, [#66](https://github.com/Apps2Samsung/tizen-community-packages/discussions/66)).
- **Closed-source apps**, only when all of these are true:
  1. The **author submits it themselves**, or the author explicitly allows redistribution: a
     LICENSE file, a line in the README, or written permission in a public issue or discussion.
  2. It is distributed from the **author's own place**. For a `release`: versioned releases (semver
     or dated tags on a real commit); no fixed tag names like `Releases` or `latest`, and no `.wgt`
     committed to `main` as the only distribution. For a `direct`: a URL the author controls, not a
     re-upload.
  3. It is **not a closed-off version of GPL/LGPL/AGPL code**. Open-source GPL apps are fine; this
     only rules out taking GPL code and shipping it without source, which breaks its license. We
     can't check this without the source, so the submitter declares it.
  4. The manifest carries `"flags": ["closed-source"]`.

### Never accepted (open or closed source)

- **Apps that ship with unlicensed content sources by default**: built-in IPTV playlists,
  pirate-site scrapers, torrent indexers, or clients for unlicensed streaming services. A player
  that only plays sources *the user adds* is fine. So is the public
  [iptv-org](https://github.com/iptv-org/iptv) playlist as a default: it only collects publicly
  available channels. Content streamed straight from the rights holder's own public servers is
  fine too (for example Apple's aerial videos from Apple's CDN).
  This is about what the package does out of the box. An app that downloads add-ons, plugins or
  site modules after install is fine as long as the user adds that add-on source themselves (your
  README may say where to find it). An add-on source the app presets, or one a later in-app update
  adds, counts as a default source.
- **Rebrands or forks that remove upstream credit or the license**, or that claim to be original
  work.
- **Modded, cracked or "premium unlocked" builds** of paid apps or services.
- **Commercial streaming apps** (Netflix, Disney+ and similar).
- **Duplicates** of an existing manifest or of an app Apps2Samsung lists itself
  ([`third-party-apps.json`](https://github.com/Apps2Samsung/Apps2Samsung/blob/main/third-party-apps.json)).
  A fork must add something real. It may keep upstream's package ID: Apps2Samsung and TV-Store
  install it under its own ID when a different app with that ID is already on the TV
  (Apps2Samsung#1028, TV-Store#84).
- **Apps that update themselves from someone else's server.** Self-updating is only accepted when
  the newer code comes from the same repository (or the author's own domain, for `direct`) that the
  manifest points at, **or** from the upstream project the app is openly built on and names in its
  `description` (e.g. a wrapper that loads the latest TizenTube from TizenTube's own release
  channel). Code from any other third party is not accepted.

### Doesn't fit?

An app that isn't accepted here can still reach users, without this review:

- People can add your app's GitHub link themselves in Apps2Samsung (**Settings > Installing > Your
  sources**), as long as it has a release with the `.wgt` or `.tpk`. Apps2Samsung only, not TV-Store.
- Or publish your own signed repository, for TV-Store too: start from
  [Apps2Samsung/repository-template](https://github.com/Apps2Samsung/repository-template), which is
  set up by clicking, no terminal (the format is in [`../docs/repositories.md`](../docs/repositories.md)).

What you publish that way isn't reviewed here, so you are responsible for having the right to
distribute it.

### Labels

| Flag | When | What users see |
|------|------|----------------|
| `closed-source` | The source isn't in the linked repository. | A "Closed source" badge; a setting can hide these apps. |
| `self-updating` | The app downloads and runs newer code after install, outside the catalogue. | A "Self-updating" badge and a note in the details. |
| `root` | The package gains root on the TV: see [Root packages](#-root-packages). | A confirmation before install. |

Every package, flagged or not, goes through the same ClamAV scan in the sync. A `self-updating`
package is only scanned at the version the catalogue ships; what it downloads later is not.

---

## 🏷️ File name

Name the file after the app's repository (`owner/repo`, on GitHub or GitLab), with the `/` replaced by a
**double underscore**:

```
packages/<owner>__<repo>.json
```

Examples: `PatrickSt1991/flixor-tizen` → `packages/PatrickSt1991__flixor-tizen.json`;
`Apps2Samsung/Overscan` → `packages/Apps2Samsung__Overscan.json`.

One repo can carry **one manifest per `source`** when the same app ships in two forms, e.g. a web
app built from source next to a native `.tpk` taken from the repo's releases. The second manifest
is a variant of the first, so both set the same `group` (see
[Category, group and variant](#%EF%B8%8F-category-group-and-variant)), and it gets a suffix:

```
packages/<owner>__<repo>__<suffix>.json      e.g. packages/pley-media-server__pley__native.json
```

The suffix is lowercase letters, digits and dashes. The `build` manifest always keeps the plain
name; only a `release` or `direct` one can take the suffix. The PR check rejects two manifests of
one repo with the same `source`, or without a shared `group`.

---

## 🧩 Fields

### Always required

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Display name in the README table. No `\|` or newlines. |
| `description` | string | One-line description for the README table. No `\|` or newlines. |
| `category` | string | Where the app shows up when the Apps2Samsung list is filtered: see [Category, group and variant](#%EF%B8%8F-category-group-and-variant). |
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
| `flags` | array | `["root"]`, `["closed-source"]`, `["self-updating"]` or a combination. See [What we accept](#-what-we-accept) and [Root packages](#-root-packages). |
| `moved_to` | object | `{ "url", "fingerprint" }` of the independent repository the app moved to. Apps2Samsung offers users who have the app installed to add it. See [`../docs/repositories.md`](../docs/repositories.md#moving-an-app-out-of-the-official-catalog). |
| `cert_level` | enum | `"partner"` for an app that only works when signed with a Samsung Partner certificate. Apps2Samsung and TV-Store then sign it with the user's Partner certificate, see [Partner certificate](#-partner-certificate). Defaults to `"public"`. |
| `preview_image` | string | HTTPS URL of a 16:9 screenshot, shown on the app's card in Apps2Samsung and TV-Store. Host it somewhere stable, the app's own repository is fine. |
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

**`category`** is required and is one of the ids in [`../data/categories.json`](../data/categories.json),
the one list of categories (their order, English names and tile colours in Apps2Samsung and TV-Store).
The validate check rejects any other value. The table below is generated from that file:

<!-- categories:start -->

| Value | Shown as | What goes here |
|-------|----------|----------------|
| `media` | Media servers & players | Clients for Jellyfin, Plex, Kodi, Immich, music servers; local USB / DLNA / SMB players |
| `iptv` | IPTV & Live TV | M3U / Xtream / Stalker players, live TV and broadcaster apps |
| `streaming` | Streaming | Clients for streaming services and sites: YouTube, Twitch, Kick, anime, Nuvio, Stremio |
| `games` | Games & emulators | Games, emulators and game streaming (Moonlight, Chiaki) |
| `casting` | Casting & cameras | AirPlay / FCast receivers, IP camera and NVR viewers |
| `tools` | Tools & system | Browsers, loaders, network and system utilities |
| `other` | Other | Anything that fits none of the above |

<!-- categories:end -->

**No category fits?** Use `other` and say in the pull request which category you'd suggest, or add it
yourself in the same pull request: one entry in [`../data/categories.json`](../data/categories.json)
with an `id` (lowercase letters, digits, `-` or `_`), an English `name`, a tile `color` (`#RRGGBB`), an
`emoji` for the README and a one-line `description` of what goes in it. Its place in the list is its
place in the apps and the README. Maintainers decide whether a new category goes in.

**`group`** folds packages together. Every package that names the same group becomes one entry in the
Apps2Samsung app list, and its files are offered in a variant picker. Use it when several repos ship
the same app (forks), or when one repo ships it in two forms from two manifests (a web app built from
source and a native build from its releases, see [File name](#%EF%B8%8F-file-name)):

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
`adult`, `flags`, `preview_image` and `user_settings`, and adds what the package says about itself, read from its own
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
accepted under the same rules as everything else (see [What we accept](#-what-we-accept); every
package is ClamAV-scanned), but must
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

## 🔏 Partner certificate

A sideloaded app is signed with the user's own Samsung certificate, Public by default. Tizen
ignores a privilege the certificate does not cover, so an app that uses partner-level rights (DRM
playback, Samsung sign-in, a VPN) or hooks into a Samsung native package installs fine when signed
Public and then fails at launch or at the call. Mark such a package:

```json
{
  "name": "YouTube for Tizen",
  "category": "streaming",
  "cert_level": "partner",
  ...
}
```

- **Apps2Samsung** signs it with the user's Partner certificate, creating one after a Samsung
  sign-in when there is none yet.
- **TV-Store** signs it with the Partner certificate the TV was armed with, and when the TV holds
  none, says so instead of installing a copy that will not work.

`cert_level` is copied onto each of the package's files in `catalog.json`. Leave it out for
everything else: a Public certificate is what nearly every app needs, and asking for Partner
without need costs the user a second certificate.

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

### Telling users why

A retired package without anything else disappears silently, which is right for a superseded fork.
When users should know why an app is gone (it broke the rules, a takedown), add `removed`:

```json
{
  "name": "Bisnor",
  "enabled": false,
  "removed": { "reason": "unlicensed-content", "note": "Gets its streams from unlicensed film servers." },
  ...
}
```

| `reason` | Shown as |
|---|---|
| `unlicensed-content` | Ships streams, playlists or scrapers for content it has no licence for |
| `unlicensed-service` | A client for a service that has no licence for its content |
| `unlicensed-game-data` | Ships commercial game data it may not redistribute |
| `takedown` | Removed after a copyright (DMCA) notice |
| `superseded` | Replaced by another app in the catalogue |
| `upstream-gone` | The developer removed or archived the project |

`note` is optional: one neutral line, English only, never a link to the app or a place to get it.
`catalog.json` then lists the package under `removed` instead of `apps`, with the package ids its
files had in the previous release and the date it was first removed. Apps2Samsung and TV-Store
flag an installed copy ("Removed from the catalogue: no more updates") and show the entry when
someone searches for it, with no install button and no source link.

When the files are no longer in the previous release (the app was disabled first and annotated
later), name the ids yourself with `package_ids` and `app_ids`; they are merged with any that are
carried over. Ids are matched per file, by repo and output name.

**When a repo stays in the catalogue with another app** (a Lite build replaces the full one), the
live manifest keeps `owner__repo.json` and the full app gets a retired manifest of its own,
`owner__repo__<suffix>.json`, with `enabled: false` and `removed`. A retired manifest may share its
repo with a live one; it needs a distinct `name` and `output_name`:

```json
{
  "name": "AniUltimatium",
  "repo": "AdvaithAvinash/AniUltimatium",
  "enabled": false,
  "removed": { "reason": "unlicensed-content", "package_ids": ["oXabc12345"], "app_ids": ["oXabc12345.EnglishAnime"] },
  ...
}
```

---

## ✅ Before you open the PR

- File is named `packages/<owner>__<repo>.json` (a second manifest of the same repo, with another
  `source` and the same `group`: `packages/<owner>__<repo>__<suffix>.json`).
- `name` and `description` contain no `|` or newlines (they land in a Markdown table).
- `category` is one of the ids in `data/categories.json`; if the app belongs with an existing one, set the same `group`.
- Adult-only content? Set `"adult": true` and keep `name` / `description` plain.
- Gains root on the TV? Set `"flags": ["root"]`.
- Source not in the repository? Set `"flags": ["closed-source"]`.
- Downloads and runs newer code after install? Set `"flags": ["self-updating"]`.
- The fields match your `source` (see the table above): the schema rejects mismatches, e.g. `url`
  on a `release`, or both `output_name` and `assets` on the same `release`.
- `output_name` ends in `.wgt` or `.tpk`.
- For a `release`: if the upstream release has more than one asset, you used `assets[]` with a `match`.
- The app meets [What we accept](#-what-we-accept), and was tested on at least one Tizen device or
  emulator.
- The app isn't offered already: not by another manifest in this folder (search for the repo and the
  name, in any case), and not by Apps2Samsung itself, which lists Jellyfin, Moonfin, Litefin and
  TizenTube on its own from its
  [`third-party-apps.json`](https://github.com/Apps2Samsung/Apps2Samsung/blob/main/third-party-apps.json).
  The PR check rejects both.

The PR bot validates against [`../packages.schema.json`](../packages.schema.json) automatically, and
downloads the file your manifest picks: it fails if that file has no `config.xml` /
`tizen-manifest.xml` (not an installable Tizen package). A green check means it's ready.

The bot may also post **Policy hints**: guesses about [What we accept](#-what-we-accept), such as a
missing `closed-source` or `self-updating` flag, or a fork that should share its original's `group`.
They never fail the check; a maintainer reads them while reviewing.
