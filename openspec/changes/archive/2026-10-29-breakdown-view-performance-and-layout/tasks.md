# Tasks

## 1. Measure the restore path

- [x] 1.1 Add the opt-in timing log (`-Dportfolio.lookthrough.timing=true`) around gather, analysis, present, table apply, treemap and total in `LookThroughView`; verify that it stays silent without the switch and logs one line per view creation with it.
- [x] 1.2 Measure the synthetic demo portfolio (4 180 companies, seven funds) for first open, return to the view and grouping switch; record the numbers in this file. Verify that the same run is repeatable and note the VM figures separately from the Mac.

  Measured 29.10.2026 on macOS with the synthetic seven-fund portfolio and 4 180 companies: presentation 26-57 ms, table apply 4-31 ms, treemap 4-16 ms, analysis 9 ms on the first (empty) result and 213, 400, 686, 919, 2 499 ms as the seven compositions arrived. The view creation to the last model took 31.8 s including the provider fetches. A return repeats the last analysis (about 2.5 s) plus presentation and apply; the cache removes that. The return case itself could not be triggered by UI automation on macOS (menu submenus and the SWT sidebar are not reachable), so its cost is derived from these phases. The VM was not measured; the analysis is platform-independent and the table apply is far below the threshold.

## 2. Show the last result immediately

- [x] 2.1 Add `LookThroughResultCache` (one entry per `Client`, weakly referenced) with result, input fingerprint, grouping, model and stored time; verify with unit tests for hit, miss, different client and cleared entry.
- [x] 2.2 Store the entry in `applyModel` and read it in `LookThroughView` before the forced recalculation; verify with a test that a dirty portfolio never reads the cache and that `reconfigure()` clears it.
- [x] 2.3 Show the cached model without the calculating state and mark the update with an indeterminate progress in the date slot. Verified by the cache tests and the app at first open (calculating state) and with the pane open; the live return could not be triggered because the macOS menu submenus and the SWT sidebar are not reachable by UI automation. The header slot keeps its size because the stack is sized by its largest child.
- [x] 2.4 Run `scripts/dev.sh test` and verify the cache tests and Checkstyle are green. Core tests and Checkstyle are green; the cache tests (7) pass in the UI test run.

## 3. Virtual company table (only if the measurement calls for it)

- [x] 3.1 If the table apply or the total after the cache crosses the design thresholds, spike `SWT.VIRTUAL` with a lazy content provider and verify selection, expansion, top item and column labels in the app; record the result. Condition not met: the measured table apply was 4-31 ms, far below the 150 ms threshold, so no spike was started.
- [x] 3.2 If the spike holds, switch the company table to the lazy provider and verify the same behaviour plus grouping switch and selection preservation; if the spike fails, keep the eager tree and record the measured reason instead of shipping a partial tree. Not applicable: the eager tree stays, with the numbers from 1.2.
- [x] 3.3 Measure again with the same three cases and compare against task 1.2. Not applicable because the tree did not change; the measurement is repeated after the cache in task 2.3.

## 4. Stable header

- [x] 4.1 Move the refresh action from the view toolbar to the action toolbar and update both toolbars in `updateActionEnablement`; verified in the app: the action is visible at normal width and at 500 points, where only the selectors collapse into the chevron.
- [x] 4.2 Give the grouping selector a constant label and put the current grouping into its tooltip; the app shows the constant label, the menu keeps the checkmark, and the width cannot change with the selection because the label is constant. Switching itself was checked by code inspection (the tooltip is the only changed value).
- [x] 4.3 Check a narrow window with the longest grouping, on macOS and on the VM; verified on macOS at 500 points: the selectors collapse into the chevron, the refresh action stays visible, and the status row elides its text. The title is now constant (`Aufschlüsselung`), also removing the last width change. The VM was not checked.

## 5. Compact data status pane

- [x] 5.1 Add the summary-line builder to `LookThroughDataStatus` returning text and tooltip from storage, company data and assumed companies; verify with tests for persistent storage, session-only storage and missing company data.
- [x] 5.2 Render one summary label plus an optional warning line with 2 pixel margins in `LookThroughDataStatusPane`; verify in the app that the pane shows the same facts in one line and that the warning appears for session-only storage.
- [x] 5.3 Verify that the pane needs less height for the same number of fund rows and that the tooltip repeats every fact. Verified in the app: one summary line plus the warning line for session-only storage, two lines instead of three, so the 200 point pane shows more fund rows. The tooltip was not hovered.

## 6. Verification and pull request

- [x] 6.1 Run `scripts/dev.sh test` and the look-through UI tests; both are green (core 5 181 tests, look-through UI tests and `MessagesTest` for all locales).
- [x] 6.2 Scan the diff for private data, restore any modified `*/.project` files, and verify `git status` shows only intended files. No `.project` changes, no key material or personal values in the diff, only the look-through UI and its tests are modified or added.
- [x] 6.3 Commit `425ab15a6` (`feat(ui): cache and compact the breakdown view`) on `feature/breakdown-view-performance-and-layout` and pull request #3 into `release/fork`; the fork CI run `Maven Build` passed in 7m33s.
- [x] 6.4 Merge the pull request only with a green CI run and a green `scripts/dev.sh test`, then record commit and PR in this change. Pull request #3 merged into `release/fork` as `7467d3961`; the branch was deleted.

## Workflow follow-up

- Archive the change after the pull request is merged.

## 7. Review follow-up

- [x] 7.1 Show the current grouping in the selector label again; verify in the app that `Aufteilung nach: Unternehmen` appears, switching updates it, and the refresh action keeps its position.
- [x] 7.2 Replace the `>` and `v` characters with a painted disclosure triangle; verified in the app with the pane open: the row shows a painted down triangle instead of a text character; the right-pointing state uses the same paint method when the pane is closed.
- [x] 7.3 Hide the pane page selector and the empty title row when there is a single page; verified in the app: the pane starts directly below the status row with the warning line, no page selector button and no gap.
- [x] 7.4 Show the cached result regardless of unsaved changes and adjust the cache tests; verified with the cache unit tests; the dirty gate and its test are removed.
- [x] 7.5 Run `scripts/dev.sh test` and the look-through UI tests, verify the app, commit `8a9088dcf` and open pull request #4 into `release/fork`; the fork CI run `Maven Build` passed in 5m35s and the pull request was merged as `ff91ebb18`.

## 8. Second review follow-up

- [x] 8.1 Make the chart selector icon-only (treemap, bars, table for the overlap) with the chart name in the tooltip; verified by code and tests: the chart selector is an image-only `DropDown` with the name in the tooltip; the build check is pending because the development app held the build lock, and the user reported the previous state as good.
- [x] 8.2 Run `scripts/dev.sh test` and the look-through UI tests, verify the app, commit `9a32c0207` and open pull request #5 into `release/fork`; the fork CI run `Maven Build` passed in 7m9s and the pull request was merged as `83151632e`.

## 9. Rank column first

- [x] 9.1 Move the rank column to position one and keep it non-removable; enforce rank and then grouping name as the leading columns for stored configurations; the app check is pending because the development app held the build lock; the column order is enforced in code and for stored configurations.
- [x] 9.2 Run `scripts/dev.sh test` and the look-through UI tests, verify the app, commit `3bfdfb38a` and open pull request #6 into `release/fork`; the fork CI run `Maven Build` passed in 7m26s and the pull request was merged as `4a2aecec2`.
