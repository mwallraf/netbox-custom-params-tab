# CI and releases

Pull requests and pushes to `main` run `.github/workflows/ci.yml` on a disposable
GitHub runner. It starts the pinned NetBox stack, runs helper/live smoke checks,
builds wheel/source distributions and runs all native tests from the installed
wheel on a fresh database. The exact tested artifacts and SHA-256 checksums are
retained as a workflow artifact; credentials and `.env` are never uploaded.

## Publish an existing tag

Run **Actions → Publish → Run workflow**, choose `main`, and enter a tag such as
`v0.1.0`. The first release uses this path because its tag predates the workflow.
Future `v*` tag pushes also trigger publishing. The tag must exist on `main`'s
history and match both package and PluginConfig versions. Do not move released
tags or reuse a version for changed package contents.

`publish.yml` validates the tagged product source using current release tooling.
It changes relative README links only in the temporary build input so images and
links resolve on PyPI; committed tag files remain unchanged. It tests the built
wheel before uploading either distribution. Both PyPI and GitHub Release receive
those exact artifacts, with checksum verification between jobs. PyPI digests must
match before GitHub release assets are created/updated. If a version already exists
with different contents, verification fails: use a new version rather than replacing it.

## Authentication and permissions

PyPI Trusted Publisher configuration must specify:

- Owner: `mwallraf`
- Repository: `netbox-custom-params-tab`
- Workflow: `publish.yml`
- Environment: `pypi`
- Project: `netbox-custom-field-profiles`

The publishing job uses OIDC (`id-token: write`) and PyPI attestations, without a
stored PyPI token. Ordinary CI has read-only repository permissions. A separate
GitHub Release job has `contents: write`; it runs only after PyPI publishing and
digest verification succeed. Actions are pinned to commit hashes and Dependabot
opens update PRs weekly. Untrusted pull requests do not enter publishing jobs.

## Local verification

With the sandbox running:

```sh
python3 scripts/release_check.py --dist-dir dist/verified --release-tag v0.1.0
```

Choose an empty output directory. This retains the exact tested wheel and source
archive after successful validation and live-data preservation checks. Without
`--dist-dir`, temporary distributions are removed as before. Local checks do not
publish or prove PyPI Trusted Publisher configuration.

[Maintainer index](README.md) · [Installation](../installation.md)
