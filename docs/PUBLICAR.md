# Publishing on GitHub

1. Repository: `pascaltll/miniTube` (set in `REPO`, `ytmini/__init__.py`).
2. For each version: bump `__version__`, add a `## X.Y.Z` section to `CHANGELOG.md` and run `tools/release.sh X.Y.Z`. The `release.yml` workflow builds the release with the zip and its sha256.
3. Users: `./launcher.sh update` (checks) and `./launcher.sh update --install`.

## Privacy
MiniTube sends no telemetry. `./launcher.sh report` only writes a local file with sensitive data hidden; the user decides whether to attach it to an issue.
