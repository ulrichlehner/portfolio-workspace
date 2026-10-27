# Tasks

## 1. Setup

- [x] 1.1 In `portfolio/`, create `feature/provider-cache-consent` from `feature/breakdown-chart-polish`; verify with `git log --oneline -1`

## 2. Core

- [x] 2.1 Store a per-account "local storage confirmed" preference next to the persistence preference and derive the provider policy from it (`PERMITTED` without maximum age when confirmed, else `UNVERIFIED`); verify with unit tests for both states in `scripts/dev.sh test`
- [x] 2.2 Make instrument classification evidence storable in the versioned store (codec record and version) if it is not yet; verify with a round-trip test and a test that withdrawal deletes it

## 3. UI

- [x] 3.1 Add the confirmation checkbox to the provider settings page, stored with Apply/OK, enabling the persistence checkbox and updating the status line; verify with `EulerpoolPreferencePageTest` cases for confirm, cancel and withdraw
- [x] 3.2 Construct `VersionedCompositionStore` in the workspace state area for the Breakdown session and pass the derived policy; verify with a session test that a confirmed account reads compositions after a new session without provider calls, and that withdrawal removes the cache directory contents
- [x] 3.3 Add the new texts to `messages.properties` and all translations; verify with the message key checks in the UI test run

## 4. Verification and commit

- [x] 4.1 Run the Docker UI reactor tests and Checkstyle, scan the diff for private data and create one focused commit (fork 0dad41ca7 incl. stored "no composition" answers; core and UI tests pass)
- [ ] 4.2 Build the app, confirm local storage with the user's private portfolio copy, restart the app and verify that the Breakdown appears without new retrieval; then withdraw and verify the cache is gone

## Notes

- Answers "no composition" (for example directly held shares) were not stored at first, so every restart
  asked the provider once per such security; now stored as well (folded into the same commit).
- The coordinator reserves a local budget permit before a stored classification is read; no provider call
  is made, only the local budget is consumed.
- A disk failure is not yet shown in the status line.
