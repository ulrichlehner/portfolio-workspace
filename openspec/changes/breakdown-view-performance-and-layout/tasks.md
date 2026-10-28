# Tasks

## 1. Measure the restore path

- [ ] 1.1 Add the opt-in timing log (`-Dportfolio.lookthrough.timing=true`) around gather, analysis, present, table apply, treemap and total in `LookThroughView`; verify that it stays silent without the switch and logs one line per view creation with it.
- [ ] 1.2 Measure the synthetic demo portfolio (4 180 companies, seven funds) for first open, return to the view and grouping switch; record the numbers in this file. Verify that the same run is repeatable and note the VM figures separately from the Mac.

## 2. Show the last result immediately

- [ ] 2.1 Add `LookThroughResultCache` (one entry per `Client`, weakly referenced) with result, input fingerprint, grouping, model and stored time; verify with unit tests for hit, miss, different client and cleared entry.
- [ ] 2.2 Store the entry in `applyModel` and read it in `LookThroughView` before the forced recalculation; verify with a test that a dirty portfolio never reads the cache and that `reconfigure()` clears it.
- [ ] 2.3 Show the cached model without the calculating state and mark the update with an indeterminate progress in the date slot; verify in the app that a return shows data immediately, the indicator disappears when the new result arrives, and the header does not move.
- [ ] 2.4 Run `scripts/dev.sh test` and verify the cache tests and Checkstyle are green.

## 3. Virtual company table (only if the measurement calls for it)

- [ ] 3.1 If the table apply or the total after the cache crosses the design thresholds, spike `SWT.VIRTUAL` with a lazy content provider and verify selection, expansion, top item and column labels in the app; record the result.
- [ ] 3.2 If the spike holds, switch the company table to the lazy provider and verify the same behaviour plus grouping switch and selection preservation; if the spike fails, keep the eager tree and record the measured reason instead of shipping a partial tree.
- [ ] 3.3 Measure again with the same three cases and compare against task 1.2.

## 4. Stable header

- [ ] 4.1 Move the refresh action from the view toolbar to the action toolbar and update both toolbars in `updateActionEnablement`; verify by unit-level inspection and in the app that the action stays visible while a long grouping is selected.
- [ ] 4.2 Give the grouping selector a constant label and put the current grouping into its tooltip; verify in the app that the selector keeps its width when switching groupings, while the menu keeps the checkmark.
- [ ] 4.3 Check a narrow window with the longest grouping, on macOS and on the VM; verify that no overflow marker covers the refresh action and record the observation.

## 5. Compact data status pane

- [ ] 5.1 Add the summary-line builder to `LookThroughDataStatus` returning text and tooltip from storage, company data and assumed companies; verify with tests for persistent storage, session-only storage and missing company data.
- [ ] 5.2 Render one summary label plus an optional warning line with 2 pixel margins in `LookThroughDataStatusPane`; verify in the app that the pane shows the same facts in one line and that the warning appears for session-only storage.
- [ ] 5.3 Verify that the pane needs less height for the same number of fund rows and that the tooltip repeats every fact.

## 6. Verification and pull request

- [ ] 6.1 Run `scripts/dev.sh test` and the look-through UI tests; verify both are green.
- [ ] 6.2 Scan the diff for private data, restore any modified `*/.project` files, and verify `git status` shows only intended files.
- [ ] 6.3 Commit with a Conventional Commit subject of at most 50 characters and open the pull request in `ulrichlehner/portfolio` into `release/fork` from a branch based on `release/fork`; verify the fork CI run is green.
- [ ] 6.4 Merge the pull request only with a green CI run and a green `scripts/dev.sh test`, then record commit and PR in this change.

## Workflow follow-up

- Archive the change after the pull request is merged.
