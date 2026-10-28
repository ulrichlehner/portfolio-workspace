# Tasks

## 1. Data status pane starts collapsed, with a visible control

- [x] 1.1 Register the Breakdown item in `Navigation` with the information pane hidden by default, so an unstored pane size resolves to collapsed; verified with the local app build on the synthetic demo portfolio: first launch collapsed, after opening the pane and restarting the same workspace the pane was still open.
- [x] 1.2 Let `SashLayout` notify its owner when a hide or show happens (grip double-click and programmatic flip) and forward that notification through `AbstractFinanceView`; verified in the app that arrow and text follow the menu action, which uses the same `flip()` path as the grip double-click (a widget unit test is not possible because the test suite runs headless).
- [x] 1.3 Add the full-width status row at the bottom of `LookThroughView.createBody` (replacing the plain separator) with `Datenstatus >` / `Datenstatus v`, activation calling `flipPane()`; verify in the running app that the row stays visible in both states and that text and arrow follow the pane state.
- [x] 1.4 Keep the global information pane menu item and its shortcut working for the view; verify that showing and hiding the pane from the menu updates the row as well.

## 2. Status row wording

- [x] 2.1 Build the compact row text in `LookThroughDataStatus` from the same fund facts and disposition names as the pane, covering running (active, waiting, answered), settled (with data, without composition) and problem (failed or rejected, next attempt) phases; verify with `LookThroughDataStatusTest` cases for each phase, including that "answered" includes no-composition and failed outcomes.
- [x] 2.2 Push the row text in the existing status update path only, with a fixed-height single-line control that elides and carries the full text as tooltip; verified in the app: the row changed from empty to `Fonds mit Daten: 1, ohne Zusammensetzung: 1` when the status arrived, the table did not move, and a narrow window elides the text with an ellipsis. The running wording itself is covered by the row tests because the provider fetch finished before the window appeared.
- [x] 2.3 Show a warning marker in the row when a lookup failed or a composition was rejected; the warning flag is verified with failed and rejected facts in `LookThroughDataStatusTest`. No live failure was produced in the app.

## 3. Concentration instead of effective number

- [x] 3.1 Rename the summary label to "Konzentration" and keep the current calculation and value format; verify that `LookThroughViewPresenterTest` still passes with the new message keys and that the summary shows `~X von Y`.
- [x] 3.2 Rewrite the tooltip with the two worked examples (three equal shares, 50/25/25), the direction of the scale and the basis (recognized companies only); the text is asserted by `LookThroughViewPresenterTest` (both examples, direction, no split claim) and the app shows the label `Konzentration` with `~86 von 1 246`. The hover was not automated.

## 4. Translations

- [x] 4.1 Add and rename the message keys in `messages.properties` and all 18 locale files with ASCII escapes and canonical order; verify with `MessagesTest` over every locale (165 tests green, including the look-through tests) and a key/placeholder parity check across all 19 files.
- [x] 4.2 Check the row in a narrow window and in German in the running app; verified at 420 points width: the text is shortened with an ellipsis in one line and the row keeps its height. The tooltip was not hovered.

## 5. Verification and commit

- [x] 5.1 Run `scripts/dev.sh test` and verify it is green, including the new and changed look-through UI tests.
- [x] 5.2 Verify the scenarios in the app with the synthetic demo portfolio and the development key: first opening collapsed, row visible with the settled wording, menu action opens the pane and flips the arrow, pane state survives a restart, narrow window elides. The running row and the warning marker were not reproduced live; both are covered by the unit tests.
- [x] 5.3 Scan the diff for private data, restore any modified `*/.project` files, and verify `git status` shows only intended files. No `.project` changes, no key material or personal values in the diff, and the staged list contains only the look-through UI, its tests and the message files.
- [x] 5.4 Commit `847de8e3e` (`feat(ui): clarify status and concentration`) on `feature/breakdown-status-and-concentration` and pull request #2 into `release/fork`; the fork CI run `Maven Build` passed in 9m26s and pull request #2 was merged into `release/fork` as `9ae194f03`. The planning artifacts are in workspace commit `fd4c561`.

## Workflow follow-up

- Archive the change after the pull request is merged and the fork CI is green.
