# 📚 The official catalog: format v1

The **official catalog** is the list of community apps this repository builds, scans and ships. Apps2Samsung
and TV-Store read it. This page is for **other tools** that want to list or install the same apps, such as a
launcher on the TV, a phone app or a small installer: read what is described here and you don't have to
reverse-engineer anything, and a breaking change is announced before it happens.

This page is the normative spec. The schema is [`spec/catalog.schema.json`](../spec/catalog.schema.json), and a
small example that uses every field is [`spec/catalog-example.json`](../spec/catalog-example.json). The words
*must*, *must not* and *should* are used in their usual spec sense.

---

## Where to get it

| URL | What it is |
|-----|------------|
| `https://apps2samsung.com/catalog/resolved.json.signed` | The **signed snapshot**: per file the download URL, size, SHA-256 and ids, plus a copy of the catalog. Signed with the official key below. |
| `https://apps2samsung.com/catalog/resolved.json` | The same snapshot without the signature line, for people to read. |
| `catalog_url` in the snapshot | The **`catalog.json`** of the bundle the snapshot describes: names, descriptions, categories, flags, removed apps. |
| `https://github.com/Apps2Samsung/tizen-community-packages/releases/latest/download/catalog.json` | The `catalog.json` of the newest bundle, when you only want the list. |

A client that installs apps should do this:

1. Fetch `resolved.json.signed` and check it (see [The signed snapshot](#the-signed-snapshot)).
2. Take the provider with `id` `tizen-community`. Its `releases[0]` is the current bundle.
3. Fetch that release's `catalog_url` over HTTPS. A device that can't check HTTPS certificates (a TV) uses
   the copy in the provider's `catalog` instead, because the signature covers it.
4. Match each `apps[].file` in the catalog to the asset with the same `name`. Download it from its
   `browser_download_url` and install it **only when its bytes hash to `digest`**.

Reading `catalog_url` from the snapshot, rather than the `latest` link, keeps the catalog and the hashes
from the same bundle.

## `catalog.json`

```json
{
  "schemaVersion": 1,
  "categories": { "media": "Media servers & players", "games": "Games & emulators", "other": "Other" },
  "category_colors": { "media": "#2B59FF", "games": "#7048E8", "other": "#868E96" },
  "apps": [
    {
      "file": "RetroGame.tpk",
      "name": "Retro Game",
      "description": "One line about the app.",
      "category": "games",
      "group": "Retro Game",
      "variant": "Tizen 6 and later",
      "repo": "example-owner/retro-game",
      "host": "github",
      "app_id": "org.example.retrogame",
      "package_id": "org.example.retrogame",
      "required_version": "6.0",
      "version": "2.0.1"
    }
  ],
  "removed": [
    {
      "name": "Gone App",
      "repo": "example-owner/gone-app",
      "host": "github",
      "category": "media",
      "reason": "upstream-gone",
      "files": ["GoneApp.wgt"],
      "since": "2026-11-01"
    }
  ]
}
```

### Top level

| Field | Meaning |
|-------|---------|
| `schemaVersion` | `1`. See [Versioning](#versioning). |
| `categories` | Category id to English display name. **The key order is the display order.** Always contains `other`. |
| `category_colors` | Category id to tile colour, `#RRGGBB`. |
| `apps[]` | One entry **per shipped file**, sorted by file name. Several files can be one app (see `group`). |
| `removed[]` | Apps that left the catalog. Never installable; listed so a client can tell a user who still has one why it gets no more updates. |

### `apps[]`

| Field | Always there | Meaning |
|-------|:------------:|---------|
| `file` | ✅ | The file name in the release, ending in `.wgt` (web app) or `.tpk` (native app). Unique within `apps`. Matches `assets[].name` in the snapshot. |
| `name`, `description` | ✅ | Shown to users. English, one line. |
| `category` | ✅ | A key of `categories`. |
| `group` | ✅ | Files with the same non-null `group` are **one app**, offered as variants. `null` (or absent) means the file is an app on its own. |
| `variant` | ✅ | Label of this file within its group, e.g. `Tizen 6 and later`. |
| `repo`, `host` | ✅ | Where the app's source or releases live: `owner/name` on `github` (github.com) or `gitlab` (gitlab.com). Link users there for support. |
| `version` | | The version in the package's own `config.xml` / `tizen-manifest.xml`: what the TV reports once it is installed. Compare it with the installed version to offer an update. |
| `app_id`, `package_id` | | The ids in the package's manifest. Match installed apps on these. A `.wgt` has a 10-character package id (`AbCdE12345`), a `.tpk` a reverse-DNS one. |
| `required_version` | | The lowest Tizen version the package installs on (`required_version` of a `.wgt`, `api-version` of a `.tpk`). Don't offer it to an older TV: the install fails with error 118. |
| `adult` | | `true` for 18+ content. **Hide it until the user opts in.** Absent means false. |
| `flags` | | Any of `root` (gains root and runs a service from boot; the user must then set Developer Mode's Host PC IP to `127.0.0.1`), `closed-source` (the source is not public; the author allows this catalog to ship it) and `self-updating` (downloads and runs newer code after install, outside this catalog and its scan). Show them to the user before install. |
| `cert_level` | | `partner`: the app only works when signed with a Samsung **Partner** certificate. Absent means a Public certificate is enough. |
| `preview_image` | | HTTPS URL of a 16:9 screenshot. |
| `user_settings` | | Values the user fills in before install, which are written into the package before it is signed. The shape is `user_settings` in [`packages.schema.json`](../packages.schema.json) and is explained in [User settings](../packages/README.md#%EF%B8%8F-user-settings). |
| `moved_to` | | `{ "url", "fingerprint" }`: the app now lives in an [independent repository](repositories.md#moving-an-app-out-of-the-official-catalog). Offer users who have it installed to add that repository. |

`version`, `app_id`, `package_id` and `required_version` are read from the package itself. They are
left out, never empty, when the package doesn't carry them.

### `removed[]`

| Field | Always there | Meaning |
|-------|:------------:|---------|
| `name`, `repo`, `host`, `category` | ✅ | As in `apps`. `name` is the group's name when the app had several files. |
| `reason` | ✅ | `unlicensed-content`, `unlicensed-service`, `unlicensed-game-data`, `takedown`, `superseded` or `upstream-gone`. The meanings are in [packages/README.md](../packages/README.md). Show your own text for each one. |
| `note` | | One neutral line of detail, English. |
| `files` | ✅ | The file names the app had. |
| `since` | ✅ | The date (UTC, `YYYY-MM-DD`) the app was first listed as removed. |
| `package_ids`, `app_ids` | | The ids its files had. Use them to recognise an installed copy. |

Don't link to a removed app's source or offer a way to install it.

## Unknown fields and values

The catalog grows without a new `schemaVersion` (see [Versioning](#versioning)), so a client **must not**
break on something it doesn't know:

| What | What a client does |
|------|--------------------|
| A field it doesn't know | Ignore it. |
| A `category` that is not in `categories`, or not one it knows | Show the app under `other`. A client with its own translations uses the English name from `categories` for an id it has no translation for. |
| A category without a `category_colors` entry | Use its own default colour. |
| A missing `categories`, `category_colors` or `removed` | Treat it as empty (older releases don't have them). |
| A `flags` value it doesn't know | Ignore it, or show it as a plain label. |
| A `reason` it doesn't know | Show a generic "removed from the catalog" text. |
| A `cert_level` other than `partner` | Treat it as a Public certificate. |
| `adult` anything but `true` | Not adult. |
| `user_settings` it can't apply | Offer the file only when every field has `"required": false` (it then works with its defaults), otherwise leave it out or point the user to Apps2Samsung. |
| `moved_to` when it doesn't support independent repositories | Ignore it. The app stays installable from this catalog until it is retired. |

## The signed snapshot

Apps2Samsung's [catalog snapshot workflow](https://github.com/Apps2Samsung/Apps2Samsung/blob/main/.github/workflows/catalog-snapshot.yml)
resolves the current bundle every 30 minutes and publishes `resolved.json.signed`: the GitHub releases already
looked up, with the SHA-256 of every file. A client then needs no GitHub API calls, and a device without working
HTTPS can still trust what it installs.

### Envelope and key

The envelope is the one [independent repositories](repositories.md#the-signed-envelope) use:

```
<base64 RSA-SHA256 signature of everything after the first newline>\n
<resolved.json, byte for byte>
```

The public key is [`spec/official-catalog.pem`](../spec/official-catalog.pem) (RSA, 3072 bits), the same key
TV-Store has built in. Its fingerprint (SHA-256 of the DER public key, as in
[Key fingerprint](repositories.md#key-fingerprint)) is:

```
b4def3a962e321e60663a96f6c31b21e29151dca4caf1e223193b9a005c0cbd6
```

Build the key into your client. **Never trust a key you download at run time.** A new key will be announced
here well before it is used.

```sh
head -1 resolved.json.signed | base64 -d > sig
tail -n +2 resolved.json.signed > payload
openssl dgst -sha256 -verify spec/official-catalog.pem -signature sig payload
```

### What a client checks

- The signature verifies over the payload.
- `schemaVersion` is `1`.
- `generatedAt` is at most 1 hour in the future and at most **7 days** old (TV-Store's limit).
- `generatedAt` is not older than the last snapshot the client accepted (no rollback).

The snapshot is republished when anything in it changes, and at least every 12 hours when nothing does, so a
client that sees one older than a day has a stale copy. Don't fetch it more often than every 30 minutes: it
doesn't change faster.

### Fields

| Field | Meaning |
|-------|---------|
| `schemaVersion` | `1`. Same rules as the catalog's. |
| `generatedAt` | When the snapshot was made, ISO 8601 with a time zone. |
| `providers[]` | The sources Apps2Samsung lists. **This spec covers the one with `id` `tizen-community`.** The others are apps Apps2Samsung lists from their developers' own releases; which ones are there is up to Apps2Samsung. |
| `providers[].releases[0]` | The current bundle: `tag_name` (`community-<number>`), `published_at`, `assets[]` and `catalog_url`. |
| `providers[].catalog` | A copy of that bundle's `catalog.json`. |
| `assets[].name` | The file name; matches `apps[].file`. |
| `assets[].browser_download_url` | Where to download it (HTTPS, github.com). |
| `assets[].size` | Bytes. |
| `assets[].digest` | `sha256:<64 lowercase hex>` of the file. |
| `assets[].package_version`, `app_id`, `package_id`, `required_version` | As `version`, `app_id`, `package_id` and `required_version` in the catalog. |
| `assets[].icon` + `icon_digest` | The app's icon on apps2samsung.com and its `sha256:` hash. Both or neither. |

The embedded `catalog` is Apps2Samsung's reading of `catalog.json`, not the file byte for byte: fields that are
`null` are left out, a few fields of its own are added (ignore them), and **a field Apps2Samsung doesn't know yet
is missing** until Apps2Samsung supports it. When you can use HTTPS, read `catalog_url`.

## How often it changes

The bundle is rebuilt when an app has a new release (checked every two hours) and when a change to an app is
merged here. Each
rebuild is a new GitHub release, `community-<number>`, with every package, `catalog.json`, and the scan report.
The snapshot follows within 30 minutes. A file name can stay the same across bundles while its content changes:
compare `version` or `digest`, not the name.

## Versioning

`schemaVersion` is the format's major version: **1** today, for both `catalog.json` and the snapshot.

**Not breaking, no new version:** a new optional field; a new category; a new `flags`, `reason` or `cert_level`
value; more or fewer apps. The rules in [Unknown fields and values](#unknown-fields-and-values) are what make
these safe, so a client must follow them.

**Breaking, a new version:** a field removed or renamed, a field's type or meaning changed, or a change that
makes one of those rules unsafe.

A breaking change is announced in an issue on this repository **at least 30 days** before it ships. A client
that sees a `schemaVersion` higher than it knows should tell the user to update and keep using the last catalog
it understood, rather than guess at the new one.

## Not part of the format

These are internal and change without notice. Don't build on them:

- the manifests in [`packages/`](../packages/), [`packages.schema.json`](../packages.schema.json),
  `repos-build.json`, `repos-sync.json` and [`data/categories.json`](../data/categories.json) (read
  `categories` from `catalog.json` instead);
- `.github/state/` and the tables in the README;
- `scan.json` and `scan-report.md` in each release: they are for people, not a stable format;
- release names and bodies, and anything in `resolved.json` this page doesn't describe.

## Using it in your own tool

You are welcome to. Please:

- **Send users to the app's own repository** (`repo` on `host`) for help with an app. Problems with the catalog
  itself go to [this repository's issues](https://github.com/Apps2Samsung/tizen-community-packages/issues).
- **Credit the catalog**: say the apps come from the Apps2Samsung community catalog and link to
  [this repository](https://github.com/Apps2Samsung/tizen-community-packages).
- **Download from the release URLs** instead of re-hosting the files. Closed-source apps are here because their
  authors allow this catalog to ship them, not every copy of it.
- **Respect the labels**: hide `adult` apps until the user opts in, show `flags` before install, don't offer
  `removed` apps, and don't install a file whose hash doesn't match.
