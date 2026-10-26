# Local macOS testing

These helpers belong to the workspace. Never copy them, their private
configuration or the OpenSpec artifacts into the upstream PP repository.
All builds, downloads and automated tests run in the `portfolio-dev` container.
Only the bundled macOS launcher and the native kernel lock run on the host.

## Build and launch

After updating the Dockerfile, rebuild the project image:

```sh
docker build -t portfolio-dev .devcontainer
scripts/dev.sh test-tools
scripts/dev.sh app
scripts/dev.sh run-app
```

The host architecture selects `aarch64` or `x86_64`. A private manifest in
`scratch/pp-dev-build/` records the PP Git revision, dirty state, source-content
SHA-256, build time, architecture and packaged-app digest. Launch checks both
the native executable and bundled Java runtime. Missing, modified or stale
builds require `scripts/dev.sh app`; there is no automatic old-build fallback.
Changes during a build invalidate it. Untracked, nonignored source files also
participate in the fingerprint. Do not put relevant sources in ignored paths.

A kernel lock in `scratch/pp-dev.lock` covers each managed operation. The open
lock descriptor passes into the native application and remains held until it
exits. A concurrent launch, refresh, build or cleanup fails immediately. The
lock file remains on disk, but a file alone is not a lock; after process exit
it is reusable without deleting files or trusting stale PIDs. Leave the launch
terminal running until the app exits.

## Private WebDAV setup

Configure only after synthetic isolation tests pass. Obtain a dedicated
**server-side read-only** account or token, restricted to the required file.
Confirm its permissions through server configuration or the server operator.
The downloader cannot establish this safely by probing writes, and does not
try. If read-only access is unavailable, stop setup; do not substitute a
production credential with write access.

Create the private directory and file locally. Never paste a real URL, user
name, token or password into the chat, a command argument or a tracked file.
Use a local editor to fill the file:

```sh
mkdir -p scratch/pp-dev-secrets
chmod 700 scratch/pp-dev-secrets
touch scratch/pp-dev-secrets/webdav.json
chmod 600 scratch/pp-dev-secrets/webdav.json
```

The following is a synthetic schema example, not a working configuration:

```json
{
  "url": "https://webdav.example.invalid/test/portfolio.xml",
  "format": "xml",
  "read_only_confirmed": true,
  "auth": {
    "method": "basic",
    "username": "read-only-example",
    "password": "replace-locally"
  }
}
```

For Bearer authentication, replace `auth` with
`{"method":"bearer","token":"replace-locally"}`. Supported formats are
`xml`, `zip` and `encrypted`; set the actual container format, not merely the
file extension. Encrypted passwords are entered only in PP, never in this
configuration. `read_only_confirmed` records the operator's permission check;
it does not grant or verify server permissions.

The source is one HTTPS file, never a mounted share or sync directory. TLS
certificate and hostname verification are required. Redirects and URL userinfo
are rejected. Only GET is currently needed; HEAD is reserved for read-only
acceptance evidence. No mutating HTTP method is implemented. Credentials are
mounted read-only into the short-lived downloader, never passed to PP, URLs in
arguments, public logs or Git. Errors omit remote identifiers and response
bodies. Each launch downloads the whole file, with a 15-second socket timeout,
a 120-second transfer deadline and a 512 MiB compressed/expanded limit.

## Refresh, recovery and retention

```sh
scripts/dev.sh run-app --webdav-copy
scripts/dev.sh run-app --webdav-copy --offline
scripts/dev.sh keep-data
scripts/dev.sh recover-data
```

### Development API key

If `scratch/eulerpool-api-key.txt` exists as a regular file, `run-app` passes only
its path to the app as `-Dportfolio.lens.developmentKeyFile=...`. Portfolio Lens
installs that key as a session key when no key is configured yet. The managed
workspace is recreated on each launch, so this is what makes repeated local tests
possible without retyping the key.

The key itself never appears in arguments, logs, preferences or exports. The
property is read once at startup, ignored when a secure or session key already
exists, and refuses links, oversized files and malformed content. This is a
development convenience in the workspace tooling and the fork; it is not part of
an official PP feature. Keep the file private, mode 600, and remove it with the
rest of the private test data when testing ends.

Online launch aborts on failed setup, authentication, TLS, transfer or container
validation. It never silently opens an old copy. Explicit offline launch
prints a stale-data notice and the last successful check/download times.

Every successful refresh creates a generation under `scratch/pp-dev-data/`:

- `baseline`: untouched downloaded bytes, mode 400.
- `Development-Copy.xml` or `.portfolio`: separate writable inode. ZIP and
  encrypted containers use `.portfolio` so PP detects their content; PP treats
  `.zip` filenames as compressed XML even when the bytes contain binary data.
- `manifest.json`: private check/download dates, validators if supplied, digest,
  build identity and validation level. No URL or credential is recorded.
- Any adjacent PP settings and backups stay with that generation.

Activation atomically replaces one pointer after complete staging and
validation. The current and immediately preceding generations remain. Older
ones are pruned only after successful activation. `keep-data` marks the current
generation to survive pruning until explicit data cleanup. `recover-data`
swaps current and previous; follow it with explicit offline launch to inspect
or reopen the recovered local copy. Local edits are never merged into the
remote file. Even an unchanged remote response produces a fresh working copy
from downloaded bytes rather than reusing an edited local file.

Periodic saves by production PP or another external process are expected.
A coherent snapshot is sufficient for local testing. Later remote changes do
not replace or invalidate the running local copy, and separate downloads need
not have matching digests. There is no continuous synchronization. Source
protection is established by read-only credentials and read-only requests;
it does not require other applications to stop saving the source.

Validation checks XML structure and PP root, ZIP integrity/entry safety and the
PP encrypted envelope. ZIP protobuf and encrypted content still require PP to
validate their semantics; encrypted content additionally needs its password.
A successful download alone is not evidence that encrypted content opened.
If opening fails, quit the app, recover the previous generation and use the
explicit offline launch. No source file has been changed.

The generated private resource-only Eclipse bundle and startup model open the
exact local file through PP's existing portfolio part. They are derived from
the checked-out PP model, without changing upstream code or application
identifiers. Managed launches
reset `scratch/pp-dev-workspace/` and use a separate Eclipse configuration and
Java user-home directory (`scratch/pp-dev-home/`). Production recent files and
persisted application state are not imported.
The app is not an OS sandbox: manually opening an unrelated production file
would bypass this managed workflow.

## Cleanup

Quit the development app, then:

```sh
scripts/dev.sh clean
scripts/dev.sh clean-data
```

Ordinary `clean` removes PP target directories, the development Eclipse
workspace, configuration and Java user home, preserving generations and the
build manifest.
`clean-data` explicitly deletes only `scratch/pp-dev-data/`, including kept
generations, local edits and adjacent backups. It preserves unrelated scratch
files and private configuration. Remove the private configuration separately
with a local editor or file manager when it is no longer needed. Neither
command contacts WebDAV. Never remove unrelated Docker resources.

## Acceptance

`test-tools` runs against synthetic repositories and a local HTTPS server with
external networking disabled. It exercises build provenance, transport failure,
redaction, local-edit recovery, atomic activation, retention, container checks,
unsafe links/paths and cleanup. It requires no real credentials.

Before real use, verify on macOS: exact-file opening in the development process,
concurrent launch/refresh rejection, post-exit lock recovery, local save and
backup paths, reopen and explicit offline/default failure behaviour. Then use
private read-only setup for task 0.6: compare source digests or validators from
read-only retrieval before/after local edits, test next-launch refresh, quit,
and explicitly remove private test data. Record only pass/fail evidence in
public artifacts, never identifiers, contents, quantities or source digests.
