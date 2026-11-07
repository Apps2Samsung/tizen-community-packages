# Your own Tizen app repository

Publish your apps as a **signed repository** that users add in Apps2Samsung. They don't need a manifest
in tizen-community-packages and don't have to wait for a review there. Your apps show up next to the
official catalog, labelled with your repository's name. The format is in
[`docs/repositories.md`](../../docs/repositories.md).

## Setup (once)

1. **Make a repo** for it (or use an existing one) and copy these files in:
   - `repository.input.json`
   - `.github/workflows/publish-repository.yml`

2. **Make a signing key** on your own computer:

   ```sh
   openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out repository-key.pem
   ```

   Keep `repository-key.pem` private and keep a backup somewhere safe. If you lose it, every user has
   to approve a new key; if it leaks, someone can publish apps in your name. **Never commit it.**

3. **Add it as a secret**: Settings → Secrets and variables → Actions → New repository secret, name
   `REPO_SIGNING_KEY`, value: the whole content of `repository-key.pem`, including the `BEGIN` and `END`
   lines.

4. **Turn on Pages**: Settings → Pages → Source: **GitHub Actions**.

5. **Fill in `repository.input.json`**:
   - `repository.id`: a reverse-DNS id that's yours, e.g. `io.github.your-name.tizen`. It can never change.
   - one provider per app: `url` is the app's GitHub repo (`owner/repo`); `take` is how many recent
     releases to list (default 1); `match` is an optional regex to pick assets when a release has
     several `.wgt` / `.tpk` files; `prerelease: true` also takes prereleases.
   - optional per provider: `source_url`, `adult`, `flags` (`closed-source`, `self-updating`, `root`),
     `cert_level: "partner"`, `buildInfo` (`name`, `description`, `previewImage`).

6. **Run it**: Actions → Publish Tizen repository → Run workflow. When it's green, your repository is at

   ```
   https://<your-name>.github.io/<repo>/repository.json.signed
   ```

   The workflow log prints the **key fingerprint**. Put it in your README, so users can check that the
   fingerprint Apps2Samsung shows them is really yours.

From then on the workflow runs on every release you publish and once a day. The daily run matters:
clients stop accepting a manifest after 7 days.

## Check it yourself

```sh
pip install jsonschema
python3 -I scripts/repo-validate.py repository.json.signed --key repository.pem
```

(run from a checkout of tizen-community-packages, with the two files downloaded from your Pages site).

## What users see

When they add your URL, Apps2Samsung shows your repository's name, maintainer, domain and key
fingerprint, and asks them to trust it. Your apps carry your repository's name everywhere, and they update
only from your repository. A valid signature means "this comes from you", not "checked by
Apps2Samsung". Users decide whether they trust you.

## Rotating or losing the key

There is no automatic key rotation in v1. With a new key, clients stop using your repository until each
user approves the new fingerprint. Announce it where your users will see it.
