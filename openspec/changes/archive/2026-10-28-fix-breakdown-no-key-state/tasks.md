# Tasks

`design.md` is deliberately skipped: the change touches one UI bundle, adds one status kind and four message keys, and changes no model, persistence or provider behavior. The one non-obvious constraint is recorded in task 2.1.

## 1. Status model

- [x] 1.1 Add a terminal status kind for missing provider credentials to `LookThroughDataStatus` and select it when there is no attempt, no usable data and the credentials are known to be absent; add its explanation text. Verify with new cases in `LookThroughDataStatusTest`: no key plus no attempt yields the new kind, a configured key plus no attempt still yields the checking kind, a rejected key still yields the rejected-key kind, and a retained composition still yields the ok kind.
- [x] 1.2 Change the checking text so it states that nothing was retrieved yet, and add the two new message keys in English and all 18 locales. Verify with `MessagesTest` and by confirming that no checking string claims a running check.

## 2. View wiring

- [x] 2.1 Pass the credential state into the status model: add an overload of `present(...)` that takes the key fact and a parameter on `LookThroughStatusModel.statusTask(...)`, filled from `LookThroughView.keyConfigured`. Do not read the secure storage in `globalFacts()`, which runs on the user interface thread. Verify with `LookThroughStatusModelTest` that the fact reaches the model and that the existing overload keeps the current behavior.
- [x] 2.2 Correct the no-key banner text so it names funds and directly held securities as both requiring the key, in English and all 18 locales. Verify with `MessagesTest` and `LookThroughBannerTest` (the banner selection stays unchanged).

## 3. Integration checks

- [x] 3.1 Run `scripts/dev.sh test` and confirm core tests and Checkstyle pass, including `LookThroughDataStatusTest`, `LookThroughStatusModelTest` and `MessagesTest`.
- [x] 3.2 Open the view without an API key and confirm the banner names the key for funds and direct holdings, every row states that no key is configured, no row claims a running check, the coverage states that no value is attributed to companies, and the refresh action stays disabled.
- [x] 3.3 Open the view with the development key and confirm rows show the not-yet-retrieved text before the first pass and normal statuses afterwards; reject the key once and confirm the row still reports a rejected key.
  Verified on 2026-10-28 with the synthetic portfolio (fund `IE00B4L5Y983`, one directly held share): both rows read "Noch nicht abgerufen" before the first pass, afterwards "OK" with 99,53 % decomposed and "Keine Zusammensetzung verfügbar" for the share. The rejected-key row could not be produced against the live provider: the holdings endpoint answers 200 for a well-formed but unknown key, and a fake key only loses the company entitlement ("Zugriff vom Anbieter verweigert"). The rejected-key kind therefore stays covered by `LookThroughDataStatusTest`.
- [x] 3.4 Scan the diff for private data, confirm no `.project` file changed, and commit on `fix/breakdown-no-key-state` from `upstream/master` with a Conventional Commit subject of at most 50 characters.
  Committed as `f10b1b503` ("fix: report a missing provider key, not progress", 25 files) on top of `release/fork`; the diff scan found no private data and no `.project` change. Pushed to the fork and opened as a development PR against `release/fork`: https://github.com/ulrichlehner/portfolio/pull/1

## Workflow follow-up

- Archive the change after the manual checks pass and the commit is verified.
