# 📦 `packages/` — one JSON file per app

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
| `repo` | string | `owner/repo` on the forge named by `host` (GitHub by default). Used as the manifest key, the README link, and (for `build`/`release`) the API target. |
| `source` | enum | One of `release`, `build`, `direct` — see below. |

### Optional (any type)

| Field | Type | Notes |
|-------|------|-------|
| `repo_label` | string | Link text for the README's Repository column. Defaults to the repo owner. |
| `output_name` | string | Filename inside the bundle. Must end in `.wgt` or `.tpk`. Required for every type **except** a `release` that uses `assets[]`. |
| `extract` | string | Only when upstream ships the package **inside a `.zip`**. Entry name or regex to pull out of the archive — see [Zip-wrapped downloads](#-zip-wrapped-downloads). |
| `enabled` | boolean | `false` retires the package without deleting the file — see [Retiring a package](#-retiring-a-package). Defaults to `true`. |
| `host` | enum | `github` (default) or `gitlab`. Where `repo` lives. `gitlab` is only supported for `source: "build"` — see [GitLab-hosted projects](#-gitlab-hosted-projects). |

### Which fields go with which `source`

| Field | `release` | `build` | `direct` |
|-------|:---------:|:-------:|:--------:|
| `branch` | ✅ required | ✅ required | ❌ |
| `output_name` | ✅ *(or `assets`)* | ✅ required | ✅ required |
| `assets[]` | ✅ *(or `output_name`)* | ❌ | ❌ |
| `extract` | ⬜ optional | ❌ | ⬜ optional |
| `url` | ❌ | ❌ | ✅ required |
| `project_path` | ❌ | ⬜ optional | ❌ |
| `skip_npm` | ❌ | ⬜ optional | ❌ |
| `pre_build` | ❌ | ⬜ optional | ❌ |
| `overlay` | ❌ | ⬜ optional | ❌ |
| `host` | ❌ | ⬜ optional | ❌ |

For a `release`, `output_name` and `assets[]` are **mutually exclusive** — use exactly one. With
`assets[]`, put `extract` on the individual asset entry rather than at the top level.

---

## 🚀 `source: "release"` — prebuilt `.wgt`/`.tpk` from GitHub Releases

The most common type. The build pulls the artifact from the repo's latest GitHub Release on
`branch`.

**One artifact** — name it with `output_name`:

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

**Pick the artifact by pattern** — when the release asset name varies (e.g. carries a version),
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

**Multiple artifacts from one release** — list several entries (e.g. per-Tizen-version builds):

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
zip-of-a-`.wgt` that installs on nothing — and it fails *silently*, because a `.wgt` is itself a zip,
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

## 🔨 `source: "build"` — compiled from source with Tizen Studio

Use when there's no prebuilt release and the app is a Tizen web project the CI can package.

| Field | Purpose |
|-------|---------|
| `branch` | Branch to check out. |
| `project_path` | Subdirectory containing the Tizen web project. Defaults to `"."`. |
| `skip_npm` | `true` to skip the automatic `npm install` (for projects with no `package.json`, or that vendor their deps). |
| `pre_build` | Shell command run **before** packaging (e.g. build the web bundle). |
| `overlay` | Name of a directory under [`../apps/`](../apps/) whose contents are copied over the project before packaging — e.g. a `config.xml` the upstream repo doesn't ship. |

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

**Build with an overlay** (copies `apps/react-iptv/` over the checked-out project — e.g. to supply a
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

Only `source: "build"` supports `host: "gitlab"` for now — GitLab Releases and the Package Registry are
not wired up, so a `release` or `direct` manifest must not set `host`.

---

## 🔗 `source: "direct"` — a fixed URL

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

## 🚫 Retiring a package

To stop shipping an app without deleting its manifest — upstream went away, the fix was merged
upstream, the fork is superseded — set `enabled` to `false`:

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
- The fields match your `source` (see the table above) — the schema rejects mismatches, e.g. `url`
  on a `release`, or both `output_name` and `assets` on the same `release`.
- `output_name` ends in `.wgt` or `.tpk`.
- The app is open-source / redistributable, and tested on at least one Tizen device or emulator.

The PR bot validates against [`../packages.schema.json`](../packages.schema.json) automatically —
a green check means it's ready.
