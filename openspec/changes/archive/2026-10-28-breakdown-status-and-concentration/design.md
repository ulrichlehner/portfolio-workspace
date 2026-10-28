# Design

## Context

See `proposal.md` for motivation. Relevant current state:

- The Breakdown view extends `AbstractFinanceView`, which owns a vertical `SashLayout` with the body above and the `InformationPane` below. The pane size is stored in the view's preference store under the view identifier; `0` means "no stored state" and falls back to `-200` when `hideInformationPane` is set, otherwise `200`. A negative size is collapsed and leaves a 10 px grip that is only usable by double-click.
- `LookThroughView` registers itself in `Navigation` without the hide flag, so the pane starts open. It registers `LookThroughDataStatusPane` as a pane page and pushes the status through `setInformationPaneInput(...)`.
- The pane renders a model built by `LookThroughDataStatus` from `LookThroughStatusModel` facts. All data is memory-only; the pane starts no request and has no timer.
- The header already shows a refresh progress line (`completed of total`) that counts arrivals, including "no composition" and failures.
- `LookThroughViewPresenter.effective(...)` computes `1 / sum(share^2)` over the company exposure and formats "value of companies" with `LookThroughSummaryEffective*` messages.

## Goals / Non-Goals

**Goals:**

- The status area costs no table space by default and stays one click away, with a control that is visible without hovering.
- The current refresh state is understandable without opening the pane: running, waiting, answered, usable, failed, next attempt.
- The concentration figure is understood as a concentration measure, not a split or a position count.

**Non-Goals:**

- No change to refresh scheduling, budgets, retries, cadence or the coordinator.
- No new provider requests, timers or background work.
- No change to other views' information pane behavior.

## Decisions

### Decision 1: Collapse the existing pane instead of building a new drawer

Reuse `SashLayout` and the `InformationPane`, set the hide flag for the Breakdown item in `Navigation`, and keep everything else. Stored sizes keep working because the fallback only applies when the stored value is `0`.

Alternatives rejected: a separate collapsible composite would duplicate the pane machinery and lose the global "Show information pane" menu item and its key binding; a dialog would take the status out of the view and need a new window with its own selection handling.

### Decision 2: The summary row lives in the view body and toggles the pane

`LookThroughView.createBody` already places a separator above the information pane. The row replaces that separator: a full-width `Link` or owner-drawn label row whose activation calls `flipPane()`. The arrow in the text (`Datenstatus >` / `Datenstatus v`) reflects `isPaneHidden()`.

Because `SashLayout` also flips on a grip double-click, the row needs to learn about that change. `SashLayout` gets a small optional callback invoked whenever it hides or shows its second child; `AbstractFinanceView` forwards it to the active view, and the Breakdown view updates the arrow and the text. No other view is affected.

### Decision 3: One status model, two presentations

The row and the pane render the same facts. `LookThroughDataStatus` gains a compact text builder next to the existing detail builder, using the same `FundStatus`/`Health` values and the same status terminology. The row uses:

- a running phase: active, waiting and answered counts, taken from `LookThroughStatusModel.total()`, `outstanding()` and the per-fund dispositions;
- a settled phase: funds with data and funds without composition;
- a problem phase: failures and rejections with a warning marker and, where known, the next attempt time.

The row updates where the pane input is already pushed (`updateStatus()` / `applyStatusUpdate`), so it never introduces another read path. The row keeps a fixed height and only sets its text when the string changed, so repeated status updates do not cause layout jitter.

The row text must never say that waiting or running lookups are loaded. "Answered" covers every arrived outcome, including no composition and failures; the settled text is the only place that talks about data.

### Decision 4: Rename the figure and explain it with two examples

`LookThroughSummaryEffective` becomes a "Konzentration" label, and the value stays `X von Y` formatted as today. The tooltip is rewritten to:

- name the calculation: square every company share, add them up, take the reciprocal;
- show two examples with the same 100 percent: three equal shares (about 3) and 50/25/25 (about 2.67), with the conclusion that the second is more concentrated;
- state the direction: smaller means more concentrated, equal to the number of companies means evenly spread;
- name the basis: only recognized companies in the company exposure, not the unresolved remainder.

The existing calculation and rounding stay untouched; only labels and tooltip text change, plus the "about" wording in the value.

Alternatives rejected: replacing the figure with "positions for 50 percent" measures something else and was explicitly not wanted; a second figure would add a number nobody asked for.

### Decision 5: Texts and translations

New keys for the row (label, running, settled, failure, toggle tooltip) and rewritten keys for the concentration label and tooltip. All locales are updated with ASCII escapes and canonical order, as for every other UI text in the fork.

## Risks / Trade-offs

- The row costs about one text line of table height permanently. Accepted; it is much smaller than the pane it replaces and carries the only visible explanation of the refresh state.
- Long translated row texts in narrow windows. Mitigation: single line with ellipsis and the full text in the tooltip; the pane remains the detailed view.
- Users who liked the open pane must re-open it once. Mitigation: their stored state wins as soon as they toggle, and the row is visible in both states.
- A second status presentation can drift from the pane wording. Mitigation: both are built in `LookThroughDataStatus` from the same facts and status names, and tests assert the wording for running, waiting, failed and settled.
- The rename can break tests or screenshots that reference the old label. Mitigation: search the UI tests for the old key and update them with the rename.

## Migration Plan

No data migration. Workspaces without a stored pane size switch to collapsed on the next open; all others keep what they had. Rolling back is a revert of the commit, which restores the previous default and labels.
