# Tasks

## 1. Setup

- [ ] 1.1 In `portfolio/`, create `feature/breakdown-ui-rework` from `feature/automatic-portfolio-xray` and verify with `git log --oneline upstream/master..HEAD` that it starts at the base branch tip with no extra commits

## 2. Responsiveness and selection (increment A)

- [ ] 2.1 Make `LookThroughStatusModel` notify only on observable state changes (no notification from an automatic check that schedules nothing) and verify with a new `LookThroughStatusModelTest` case that an idle `refreshAutomatically()` produces no notification
- [ ] 2.2 Add stable keys to presenter rows (company identity, category and source path for details, fund reference for status rows) and verify with `LookThroughViewPresenterTest` that equal results produce equal keys and distinct companies with the same label keep distinct keys
- [ ] 2.3 Split the view's status and result listeners and run recalculation as a coalescing background job with a generation counter (design D1); verify with a unit test of the coalescing scheduler that a burst of requests yields one calculation and stale results are discarded
- [ ] 2.4 Preserve selection, expansion and top index in the company table and the status pane across updates (design D2); verify manually in `scripts/dev.sh run-app` that a selected, expanded row survives a 60-second check and an incoming fund result
- [ ] 2.5 Run `scripts/dev.sh test` with Checkstyle, scan the diff for private data, and create the focused commit for increment A

## 3. Rename and placement (increment B)

- [ ] 3.1 Rename `PortfolioLensAnalysis`, `PortfolioLensCompositionService`, `PortfolioLensSession` and their tests to `LookThrough*` and verify with `grep -rn PortfolioLens portfolio/` returning no source or test hits
- [ ] 3.2 Replace `LabelPortfolioLens` with `LabelBreakdown` and a view title key (Breakdown / Aufschlüsselung, Breakdown by Company / Aufschlüsselung nach Unternehmen), set `PrefTitleEulerpool` to "Eulerpool", and update all `messages*.properties`; verify that no properties file still contains "Portfolio Lens"
- [ ] 3.3 Move the navigation item under Statement of Assets with the information pane visible (design D7) and verify in the running app that the German sidebar shows Vermögensaufstellung > Aufschlüsselung and the view title reads Aufschlüsselung nach Unternehmen
- [ ] 3.4 Run `scripts/dev.sh test`, scan the diff for private data, and create the focused commit for increment B

## 4. Settings page (increment C)

- [ ] 4.1 Rework `EulerpoolPreferencePage` to one key field with Apply/OK storage, an immediate remove control enabled only when a key exists, one status line and the request-key link (design D6); verify with `EulerpoolPreferencePageTest` that OK stores, cancel stores nothing and an empty field keeps the stored key
- [ ] 4.2 Add the session-only fallback that appears only when secure storage is unavailable and verify with a test using an unavailable credential store that the key is used for the session and nothing is written
- [ ] 4.3 Reject keys with whitespace or line breaks through the page error message and verify with a test that the page is invalid and nothing is stored
- [ ] 4.4 Reduce the persistence section to one checkbox plus one status line and verify in the running app that an unverified policy shows a disabled checkbox with a one-sentence reason
- [ ] 4.5 Remove the now unused message keys in all properties files, run `scripts/dev.sh test`, scan the diff for private data, and create the focused commit for increment C

## 5. View layout, onboarding and data status (increment D)

- [ ] 5.1 Add a presenter summary model (securities value, resolved share, top-10 share, decomposed and held fund counts, notice indicator text) and verify with `LookThroughViewPresenterTest` cases for partial coverage, missing denominator and empty portfolio
- [ ] 5.2 Add a coverage model (segments per category with minimum visible width for a nonzero remainder) and verify with tests that a tiny unresolved remainder keeps a visible segment and a missing denominator yields no bar
- [ ] 5.3 Build the header, summary strip and coverage bar controls and remove the permanent notice paragraphs; verify in the running app in light and dark theme that the notices are only in the indicator tooltip
- [ ] 5.4 Add the banner area with priority selection (refresh progress with stop > suspended > no key with funds > empty portfolio) and verify with a unit test of the selection logic plus a manual check that the no-key banner opens the Eulerpool settings page
- [ ] 5.5 Replace the Cancel toolbar action with the progress stop control and verify manually that refresh disables itself while running and stopping keeps applied results
- [ ] 5.6 Reduce the data status pane to fund, status icon, retrieved date and decomposed share with details in tooltips and verify with `LookThroughDataStatusTest` that the tooltip text contains failure reason and original dates
- [ ] 5.7 Run `scripts/dev.sh test`, scan the diff for private data, and create the focused commit for increment D

## 6. Charts (increment E)

- [ ] 6.1 Add a chart model (companies only, sorted, top-N with direct and indirect parts) and verify with tests that unresolved and other categories are excluded and a company held directly and through funds has both parts
- [ ] 6.2 Implement the company treemap with the engehausen treemap and theme colors (design D4) and verify in the running app that tiles show company, amount and share in the tooltip
- [ ] 6.3 Implement the top-N stacked bar chart with PP's SWTChart helpers and verify in the running app that bars show separate direct and indirect segments
- [ ] 6.4 Add the chart switcher, the stored sash weights and the empty-chart state, and verify manually that a portfolio without company exposure shows the empty-state message
- [ ] 6.5 Link chart and table selection in both directions and verify manually that clicking a tile selects and reveals the table row and selecting a row highlights the chart element
- [ ] 6.6 Run `scripts/dev.sh test`, scan the diff for private data, and create the focused commit for increment E

## 7. Integration checks

- [ ] 7.1 Build with `scripts/dev.sh app` and run `scripts/dev.sh run-app --webdav-copy` against a copy of the user's portfolio; verify each scenario of the `breakdown-view` and `composition-provider-settings` specs and record the results in this change without private values
- [ ] 7.2 Run `scripts/dev.sh clean`, then record the commit references and any remaining verification in this file

## Workflow follow-up

- Pushing `feature/breakdown-ui-rework` to the fork follows the existing authorization for experimental source-only pushes; upstream PRs need separate authorization.
- Plan the split of the combined look-through work into focused upstream PRs as a separate change.
- Follow-ups not in this change: fund overlap matrix, sector/country breakdown once provider data is checked, provenance tab in the information pane.
- Archive this change after the integration checks pass.
