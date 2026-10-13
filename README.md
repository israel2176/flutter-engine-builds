# flutter-engine-builds

Public build farm for NetFree-patched Flutter engines (`libflutter.so`).
Public repo => free, unlimited GitHub Actions minutes. It holds only the build
recipe, the (public) NetFree root certificates and the resulting releases.
APKs, signing keys and app configs stay in the private `flutter-custom-ssl` repo.

- **Build**: Actions → *Build Flutter Engine (NetFree CA)* → inputs `engine_hash`, `android_cpu`.
- **Output**: release `engine-<cpu>-<engine_hash>` with `libflutter-<cpu>-<engine_hash>.so`.
- **Download**: `gh release download engine-arm64-<hash> --repo israel2176/flutter-engine-builds -p '*.so'`

## Security
Keep the workflow `workflow_dispatch`-only (no `pull_request_target`), and set
Settings → Actions → General → *Require approval for all outside collaborators*.

## Secrets
- `PATCH_REPO_TOKEN` (optional): fine-grained PAT with *Actions: read/write* on
  `israel2176/flutter-custom-ssl`, used to re-run *Patch App* after a build.
