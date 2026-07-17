# Adding a package

Each app is one JSON file in this folder. To add one: **copy an existing file,
edit it, open a pull request.** A bot validates it automatically — no need to
touch any other file.

- **Filename:** `owner__repo.json` (your GitHub `owner/repo` with `/` → `__`).
- **Validation:** every field is checked against [`packages.schema.json`](../packages.schema.json)
  on your PR. Green check = ready to merge.

Pick the `source` that matches how your `.wgt` is distributed:

### `release` — prebuilt `.wgt` attached to a GitHub Release (most common)

```json
{
  "name": "My App",
  "description": "Short one-line description.",
  "repo": "owner/my-app",
  "source": "release",
  "branch": "release",
  "output_name": "MyApp.wgt"
}
```

If a single release ships several `.wgt` files, use `assets` instead of `output_name`:

```json
{
  "name": "My App",
  "description": "Short one-line description.",
  "repo": "owner/my-app",
  "source": "release",
  "branch": "release",
  "assets": [
    { "match": "Full.wgt", "output_name": "MyApp.wgt" },
    { "match": "MyApp-.*[.]wgt$", "output_name": "MyApp-Nightly.wgt" }
  ]
}
```
`match` is an exact asset name first, then a regex fallback.

### `build` — compiled from source with Tizen Studio

```json
{
  "name": "My App",
  "description": "Short one-line description.",
  "repo": "owner/my-app",
  "source": "build",
  "branch": "main",
  "project_path": "tizen",
  "output_name": "MyApp.wgt"
}
```
Optional: `"skip_npm": true` (no npm install) and `"pre_build": "..."` (a shell
command run before packaging).

### `direct` — a fixed download URL

```json
{
  "name": "My App",
  "description": "Short one-line description.",
  "repo": "owner/my-app",
  "source": "direct",
  "url": "https://example.com/MyApp.wgt",
  "output_name": "MyApp.wgt"
}
```

---

These files are the source of truth. The daily sync workflow compiles them into
`repos-build.json` / `repos-sync.json` via `scripts/build-manifests.sh`; those
two files are generated and git-ignored, so don't edit them by hand.
