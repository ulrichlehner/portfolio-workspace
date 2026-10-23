# Local macOS foundation verification

Date: 2026-10-23. Scope: section 0 only. Provider, calculation and UI feature
implementation in sections 1–6 has not started.

## Repository isolation

- Workspace tooling branch: `feature/automatic-portfolio-xray-tooling`.
- Clean PP branch: `feature/automatic-portfolio-xray`, created directly from
  `upstream/master` at `31094c7de87f9d637988c98908a0c9ef73f19442`.
- All tooling, tests, documentation and OpenSpec tracking stay in this workspace.
  No upstream PP source changes or commits were needed. No branches were pushed
  and no PR was opened.

## Automated verification

- Rebuilt the `portfolio-dev` image with Python's standard library support.
- `scripts/dev.sh test-tools`: 39 tests passed in Docker, external networking
  disabled. Synthetic HTTPS server and synthetic Git/app/container fixtures only.
- Covered source revision/content fingerprints, failed rebuild invalidation,
  modified/missing runtime or artifact rejection, architecture mismatch,
  verified TLS and hostname checking, redirects/auth failures, redaction,
  URI encoding, incomplete/stalled/oversized transfers, XML/ZIP/binary/encrypted
  envelope checks, atomic activation failure, changed/unchanged remote bytes,
  edited local copies, previous/kept generations, unsafe links/paths, cleanup,
  startup-model path selection and kernel locking.
- `scripts/dev.sh app`: Docker Maven build reported `BUILD SUCCESS`; ARM64
  macOS distribution and bundled Java passed the provenance/architecture checks.
  The build skips Java test execution; the targeted tooling suite is the test
  gate for this workspace-only milestone. Current-wrapper manifest checks and
  native launches succeeded against the resulting build.
- `git diff --check`: passed before commit. Commit review includes a private-value
  scan against the local WebDAV configuration and identifiers/long text in the
  private binary source, without printing their contents. Both scans passed.

## macOS verification

- Direct native launch opened the selected regular local portfolio through a
  generated resource-only Eclipse model bundle. Original packaged PP jars and
  application identifiers remain unchanged; translation resources are included.
- A separate Eclipse workspace/configuration and Java user home isolate
  preferences, recent files and secure storage. Managed launch resets its
  workspace; PP receives no WebDAV configuration or credentials.
- Concurrent online launch, data mutation and ordinary cleanup were rejected.
  Native kernel locks were reusable after process exit without stale-PID logic.
- Synthetic local watchlist edit saved successfully; untouched baseline digest
  was preserved, adjacent local backup/settings files existed, and offline
  reopen succeeded with the explicit stale-data notice.
- An encrypted envelope was preserved without claiming content validation.
  Recovery selected and reopened the previous valid local generation. Full
  encrypted-content/password validation remains PP's responsibility.
- Normal online launch with temporarily invalid local configuration aborted
  before starting PP; valid private setup was restored automatically.

## Private acceptance

Private server configuration and read-only confirmation were supplied locally.
Configuration permissions were restricted to 600 and its directory to 700.
No write-permission probes, mutating WebDAV methods or source mounts were used.

The real source was downloaded with verified HTTPS. The binary container is
preserved byte-for-byte; local ZIP containers use `.portfolio` because PP treats
`.zip` filenames as compressed XML. A local synthetic marker edit was saved
successfully, with an unchanged downloaded baseline, and the saved binary copy
reopened successfully offline. Identifiers, payloads and source digests are
intentionally excluded from this record.

The next online launch retrieved a fresh coherent generation, retained the
previous locally edited generation and excluded the local test marker from the
fresh working copy. Separate remote snapshots and validators differed because
an external process saves production periodically. The user explicitly accepted
this behaviour: a plausible coherent snapshot is sufficient, with no continuous
synchronization or requirement for byte equality between remote downloads.
The local test marker was absent from both downloaded baselines. Confirmed
read-only credentials and GET-only transport establish that this workflow does
not write to the remote source; independent production saves remain allowed.

## Completion

The development process was stopped after the local save/reopen checks.
`scripts/dev.sh clean` removed build outputs and isolated application state.
`scripts/dev.sh clean-data` removed the managed private generations; its bind
mount cleanup was corrected and verified against the actual Docker mount.
Temporary process/build logs were removed. The targeted synthetic suite passed
again after this correction. Strict OpenSpec validation passed.
The private configuration remains available for future local testing; it is
ignored by Git and is never included in the tooling commit.

Section 0 is complete. No setup blocker remains. Workspace commit subject:
`feat(dev): add isolated macOS portfolio tests`. The commit identifier is
reported on completion; sections 1–6 remain outstanding and publishing is not
authorized by this milestone.
