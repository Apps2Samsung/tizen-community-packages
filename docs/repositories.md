# 🗂️ Independent repositories: format v1

An **independent repository** is a signed list of Tizen apps that a developer publishes from their own
place, usually GitHub Pages. Users add it in Apps2Samsung, which can also hand it to TV-Store. The apps
then show up next to the official catalog, labelled with the repository's name.

This page is the normative spec. The schema is [`spec/repository.schema.json`](../spec/repository.schema.json);
the test vectors are in [`spec/fixtures/`](../spec/fixtures/). To publish one, start from
[Apps2Samsung/repository-template](https://github.com/Apps2Samsung/repository-template) (set up by clicking,
key made at [apps2samsung.com/repository-key](https://apps2samsung.com/repository-key/)); the manual setup
is in [`templates/independent-repo/`](../templates/independent-repo/), and a working example is
[Apps2Samsung/repository-example](https://github.com/Apps2Samsung/repository-example).

The official catalog these repositories sit next to has a written format too: [`catalog.md`](catalog.md).

The words *must*, *must not* and *should* are used in their usual spec sense.

---

## What a repository publishes

Three files at stable HTTPS URLs, next to each other:

| File | What it is |
|------|------------|
| `repository.json.signed` | What clients read: the signature line, then the manifest. |
| `repository.pem` | The public key. Clients show its fingerprint when the user adds the repository. |
| `repository.json` | The manifest without the signature, for people to read. Clients ignore it. |

The URL users add is the one of `repository.json.signed`. `repository.pem` must be in the same folder.

## The signed envelope

The same envelope as Apps2Samsung's official `resolved.json.signed`, so TV-Store verifies both with one
function:

```
<base64 RSA-SHA256 signature of everything after the first newline>\n
<the manifest JSON, byte for byte>
```

- The signature is RSASSA-PKCS1-v1_5 with SHA-256 over the exact payload bytes. That is what
  `openssl dgst -sha256 -sign` makes and what Node's `crypto.createVerify('RSA-SHA256')` checks.
- The key is RSA, **at least 3072 bits**. TV-Store's background service runs on Node 4.4.3, which can't
  verify anything more modern (Ed25519 and so on), so RSA it is.
- The signature line must end within the first 4096 bytes.
- The whole file must be at most 8 MiB.

### Key fingerprint

The fingerprint identifies the key: the **SHA-256 of the DER-encoded public key (SubjectPublicKeyInfo)**,
as 64 lowercase hex characters.

```sh
openssl pkey -pubin -in repository.pem -outform DER | sha256sum
```

## The manifest

```json
{
  "schemaVersion": 1,
  "repository": {
    "id": "io.github.owner.tizen",
    "name": "Owner's Tizen apps",
    "maintainer": "Owner",
    "description": "Optional, one line",
    "homepage": "https://owner.github.io/tizen"
  },
  "generatedAt": "2026-11-07T00:00:00Z",
  "providers": [
    {
      "id": "my-player",
      "category": "media",
      "url": "https://api.github.com/repos/owner/my-player/releases",
      "displayName": "My Player",
      "take": 1,
      "source_url": "https://github.com/owner/my-player",
      "ok": true,
      "latestTag": "v1.2.0",
      "releases": [
        {
          "tag_name": "v1.2.0",
          "name": "My Player 1.2.0",
          "published_at": "2026-11-06T10:00:00Z",
          "assets": [
            {
              "name": "MyPlayer.wgt",
              "browser_download_url": "https://github.com/owner/my-player/releases/download/v1.2.0/MyPlayer.wgt",
              "size": 1234567,
              "digest": "sha256:<64 lowercase hex>",
              "package_version": "1.2.0",
              "app_id": "AbCdE12345.MyPlayer",
              "package_id": "AbCdE12345",
              "required_version": "5.0"
            }
          ]
        }
      ]
    }
  ]
}
```

The provider and release shapes are the ones Apps2Samsung's `resolved.json` already uses (a provider of
`third-party-apps.json` with its releases resolved), so the clients read them with code they already
have. What's new is the top-level `repository` block.

### Fields

| Field | Required | Meaning |
|-------|:--------:|---------|
| `schemaVersion` | ✅ | `1`. A client rejects any version it doesn't know. |
| `repository.id` | ✅ | Stable reverse-DNS id, e.g. `io.github.owner.tizen`. **Never change it**: clients pin it. |
| `repository.name`, `.maintainer` | ✅ | Shown to users. One line, no `\|`. |
| `repository.description`, `.homepage` | | Shown to users. |
| `generatedAt` | ✅ | When the manifest was signed (ISO 8601 with a time zone). |
| `providers[]` | ✅ | One per app, 1 to 500. |
| `providers[].id` | ✅ | Unique within the repository. |
| `providers[].category` | ✅ | Any id from the official catalog's `categories` (today `media`, `iptv`, `streaming`, `games`, `casting`, `tools`, `other`), matching `^[a-z0-9][a-z0-9_-]{0,31}$`. A client shows an id it does not know under `other`. |
| `providers[].url` | ✅ | Where the releases come from. For information only: clients install only the assets listed. |
| `providers[].releases[]` | ✅ | Newest first, at most 20. |
| `providers[].displayName`, `prefix`, `take`, `buildInfo` | | As in `third-party-apps.json`. |
| `providers[].source_url` | | The app's source code, when it is open source. |
| `providers[].adult`, `flags`, `cert_level` | | Same meaning as in the official catalog: 18+ (hidden until the user opts in), `root` / `closed-source` / `self-updating`, `partner`. |
| `releases[].tag_name`, `assets[]` | ✅ | |
| `assets[].name` | ✅ | Ends in `.wgt` or `.tpk`. |
| `assets[].browser_download_url` | ✅ | HTTPS. |
| `assets[].size` | ✅ | Bytes, at most 512 MiB. |
| `assets[].digest` | ✅ | `sha256:<64 lowercase hex>` of the file. Clients install only bytes that hash to this. |
| `assets[].package_version`, `app_id`, `package_id`, `required_version` | | Read from the package's own `config.xml` / `tizen-manifest.xml`. Clients use them to match installed apps and to skip TVs that are too old. |
| `assets[].icon` + `icon_digest` | | Both or neither, as in `resolved.json`. |

Clients ignore fields they don't know, so later versions can add optional fields without a new
`schemaVersion`.

## Rules a manifest must meet

A client must reject the whole manifest when any of these fails. Each comes with the reason code that
`repo-validate.py` and the test vectors use:

| Reason | Rule |
|--------|------|
| `size` | The file is at most 8 MiB. |
| `no-signature` | Line 1 is a base64 signature. |
| `key` | The key is RSA and at least 3072 bits. |
| `fingerprint` | The key matches the fingerprint the user approved. |
| `signature` | The signature verifies over the payload. |
| `json` | The payload is JSON. |
| `schema-version` | `schemaVersion` is one the client knows. |
| `schema` | The payload matches `spec/repository.schema.json`: HTTPS only, the digest format, the required fields. |
| `url` | No URL points at an IP address, `localhost` or `*.local`, and none has a user name or password in it. |
| `future` | `generatedAt` is at most 1 hour ahead of the client's clock. |
| `expired` | `generatedAt` is at most **7 days** old. |
| `rollback` | `generatedAt` is not older than the last manifest the client accepted from this repository. |
| `duplicate` | Provider ids are unique, and no `package_id` + `package_version` is offered by two different providers. One provider may list several files of one version: those are variants, such as a legacy build and a current one. |

So a publisher **must re-sign at least every 7 days**, even when nothing changed. The template's
workflow does this daily, and keeps that daily run switched on in a quiet repo.

## What clients do with it

**Adding a repository** (Apps2Samsung):
1. Fetch `repository.json.signed` and `repository.pem` over HTTPS with certificate validation.
2. Validate, then show the repository name, domain, maintainer and **key fingerprint**. Make clear that
   a valid signature means "comes from this publisher", not "checked by Apps2Samsung".
3. Store the URL, `repository.id`, the approved fingerprint and the `generatedAt` accepted, only after the
   user says yes.

**Every refresh:**
- Verify against the **stored** key, never a newly downloaded one.
- When `repository.pem` changes, stop using the repository until the user approves the new fingerprint.
- When a refresh fails, keep the other sources and the official catalog working. A previously accepted
  manifest may still be listed with a warning, but nothing new is installed from it.

**The TV** (TV-Store) can't validate HTTPS, so it must never trust a key it downloaded itself. It gets
repositories (URL, `repository.id`, fingerprint) only from Apps2Samsung, and asks the user to confirm each.

**Installing and updating:**
- Install a file only when its bytes hash to `digest`.
- Every app shows which repository it comes from.
- An installed app is updated **only from the repository it was installed from**. When two sources offer
  the same `package_id`, both are listed; moving an app to another source is an explicit user action.
- Apps2Samsung and TV-Store sign every package with the user's own certificate, so the publisher's
  signing certificate plays no part.

## Moving an app out of the official catalog

When an app in [`packages/`](../packages/) moves to its author's own repository, its manifest gets:

```json
"moved_to": {
  "url": "https://owner.github.io/tizen/repository.json.signed",
  "fingerprint": "<64 lowercase hex>"
}
```

`catalog.json` carries it on each of the app's files. Apps2Samsung offers users who have the app
installed to add that repository, with the fingerprint already approved by the official catalog, so
their updates continue from there. After a notice period the manifest is set to `enabled: false`.

## Tooling

| Script | What it does |
|--------|--------------|
| [`scripts/repo-generate.py`](../scripts/repo-generate.py) | Builds and signs a manifest from a small input file, reading GitHub releases. Used by the template. |
| [`scripts/repo-validate.py`](../scripts/repo-validate.py) | Checks a `.signed` file against a key: every rule above, with its reason code. |
| [`scripts/test-repo-spec.py`](../scripts/test-repo-spec.py) | Runs the validator over every test vector. |

```sh
pip install jsonschema
python3 -I scripts/repo-validate.py repository.json.signed --key repository.pem
```

## Test vectors

[`spec/fixtures/index.json`](../spec/fixtures/index.json) lists every case: the file, the key to check it
with, the time to check it at (`now`), optionally `notBefore` (the last accepted `generatedAt`) and
`fingerprint`, and the expected outcome with its reason code. A client implementation should run them
all. [`make-fixtures.py`](../spec/fixtures/make-fixtures.py) regenerates them. The keys in
`spec/fixtures/keys/` are **test-only and public**: never sign a real repository with them.
