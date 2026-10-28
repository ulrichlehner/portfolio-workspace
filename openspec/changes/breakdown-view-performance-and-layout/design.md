# Design

## Context

See `proposal.md` for motivation. The current state that shapes the approach:

- `PortfolioPart.activateView` disposes the current view and creates a fresh one on every switch. `LookThroughView.createBody` creates the executors, the table, the chart and the status row; `notifyViewCreationCompleted` starts a status read, a forced recalculation and a credential read.
- `calculatedInputs` is a field of the view instance, so the "only when inputs changed" guard never triggers after a re-creation.
- The calculation, the presentation (`LookThroughViewPresenter.present`) and the enrichment snapshot read run on one background executor. The result is applied on the user interface thread; the table is a non-virtual `TreeViewer` (`LookThroughView:613`) and the treemap lays out one tile per company.
- `AbstractFinanceView` builds the header as title | view toolbar inside `ToolBarPlusChevronLayout` | action toolbar. The chevron layout hides items from the right; "Aktualisieren" is the last item of the view toolbar, so it disappears first. `selectGrouping` calls `updateTitle(...)` and `groupingDropDown.setLabel(...)`, which both change widths and relayout the header.
- `LookThroughDataStatusPane` renders three wrapping labels (storage, company data, assumed companies) plus the fund table, with 5 pixel margins.

## Goals / Non-Goals

**Goals:**

- Returning to the view shows data immediately; the expensive work still runs and still updates the view.
- The measured numbers decide whether the table itself needs a virtual implementation.
- The refresh action is always reachable; the grouping selector does not change width.
- The status pane uses less height without losing any fact.

**Non-Goals:**

- No change to requests, budgets or the refresh cadence.
- No persistence of results: the cache lives in memory for the session only.
- No selection or expansion restoration across a view switch.
- No treemap content changes.

## Decisions

### Decision 1: One result cache per portfolio in the app-lifetime service

`LookThroughCompositionService` is an application singleton. It gets a small `LookThroughResultCache` with one entry per `Client`, held in a `WeakHashMap` so the entry disappears when the portfolio is closed and collected.

The entry stores the `LookThroughResult`, the `Inputs` fingerprint (funds, retained snapshots, classifications), the grouping it was presented with, the presented `Model` and the time it was stored. Only the production source writes and reads it; an injected preview result bypasses the cache.

The view writes the entry in `applyModel` (user interface thread, after a successful presentation). At creation, before `recalculate(true)`, it asks the cache for the current client.

Alternatives rejected: keeping the whole view alive would change `PortfolioPart` for every view and keep executors and charts of unused views; a disk cache would persist derived provider data and survive restarts, which this change does not need.

### Decision 2: Show the cached model and mark it as updating

When the cache delivers a model and the portfolio has no unsaved changes (`getPart().getClientInput().isDirty()`), the view applies the model immediately: summary, charts, table and status. It does not show the calculating state. The background calculation runs regardless and replaces the model when it arrives.

While the cached model is shown and the new one has not arrived, the valuation-date slot of the header shows an indeterminate `ProgressBar` (`SWT.INDETERMINATE`) with the existing calculating text as tooltip. The slot already uses a `StackLayout` sized by its largest child, so the header does not move.

With unsaved changes, or without an entry, the current calculating state stays and the cache entry is cleared: unsaved edits make the stored numbers wrong.

Alternatives rejected: a silent replacement without any indicator would present possibly stale prices as current; a new text line would need a new key in 19 locales for no additional information.

### Decision 3: Measure with an opt-in timing log, then decide on the virtual tree

The view gets a timing block that is only active with `-Dportfolio.lookthrough.timing=true` and logs one info line per view creation: gather, analysis, present, table apply (`setRows`/`setInput`), treemap and total. The switch is off by default, so normal logs stay quiet, and the measurement is repeatable on the VM.

Measurements run with the synthetic demo portfolio (4 180 companies, seven funds, development key) for three cases: first open, return to the view and grouping switch. The numbers are recorded in `tasks.md`.

The virtual tree (`SWT.VIRTUAL` with an `ILazyTreeContentProvider`, rows created on demand) is implemented when the table apply is a relevant share, set here as at least 150 ms, or the total restore still exceeds 300 ms on the VM after the cache. A spike validates selection, expansion, top item and column labels before the view switches to it. If the spike cannot keep those semantics inside this change, the eager tree stays and the measured numbers are recorded instead of shipping a half-working lazy tree.

Alternatives rejected: paging or capping the company list would hide data; a batched insertion keeps the total time and only spreads it.

### Decision 4: Refresh action outside the collapsing toolbar

`LookThroughView.addViewButtons` keeps the two selectors; the refresh action moves to `addButtons`, which fills the right action toolbar of `AbstractFinanceView`. That toolbar is outside `ToolBarPlusChevronLayout`, so it can never be moved into the chevron. `updateActionEnablement` updates both toolbars.

The grouping selector keeps the constant label `Messages.LookThroughBreakdownBy`; its tooltip becomes `Aufteilung nach: <current>` and the menu keeps the checkmark. Its width no longer changes with the selection. The chart selector keeps its current label: its labels are short and the refresh action no longer disappears. The view title keeps naming the grouping; a residual width change of the title only moves the selectors, never the actions.

Alternatives rejected: a fixed pixel width for the selector needs a custom toolbar control to override the text-based item width; truncating the selected value in the label hides the state instead of showing it in the tooltip.

### Decision 5: One summary line in the data status pane

`LookThroughDataStatus` gains a builder for the pane header that returns text and tooltip from the storage text, the company data line and the assumed-company line. Persistent storage joins the three facts with ` · ` on one line and puts each fact on its own line in the tooltip. Session-only storage or a disk failure keeps the limitation as a separate line with the warning icon, and the summary line carries company data and assumed count only.

The pane drops from three wrapping labels to one summary label plus an optional warning label, with margins of 2 pixels. No new message keys are needed: the existing texts are joined in code.

### Decision 6: Tests and platform check

The cache and the summary line are SWT-free and get unit tests. The header change, the updating indicator and the elision are checked in the running app on macOS and on the VM (Linux), because platform toolbars and table columns differ. The timing numbers are recorded with the measurement.

## Risks / Trade-offs

- Stale numbers for a moment after quote updates. Mitigated by the visible indeterminate progress and by always running the calculation.
- The cache holds one result and one model per portfolio, a few megabytes with thousands of companies. Mitigated by the `WeakHashMap` and by replacing the entry on every presentation.
- Cached labels can lag behind enrichment until the first new presentation. Accepted; the background presentation replaces them within the same update.
- A virtual tree changes selection and expansion behavior in subtle ways. Mitigated by the spike and by the explicit fallback.
- The constant selector label hides the current grouping from the toolbar. Mitigated by the tooltip, the checked menu entry, the view title and the first table column, which names the grouping.
- Linux and macOS lay out toolbars and table columns differently. Mitigated by checking both.

## Migration Plan

No data migration. The cache starts empty in every session; a portfolio with an unsaved state never sees it. Reverting the change removes the cache and restores the fixed toolbar placement.
