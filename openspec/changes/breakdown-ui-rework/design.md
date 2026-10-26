# Design

## Context

See proposal.md for motivation. The current state in the fork branch `feature/automatic-portfolio-xray` that
shapes the approach:

- `LookThroughView` registers a change listener on `LookThroughStatusModel`. Every notification calls
  `recalculate()` on the UI thread, which builds a `ClientSnapshot`, runs `PortfolioLensAnalysis` and calls
  `viewer.setInput(...)` with newly created row records. The status pane does the same with its own
  `setInput` + `refresh`.
- `LookThroughStatusModel.refresh(...)` calls `notifyChanged()` unconditionally, including from the 60-second
  `refreshAutomatically()` timer when nothing is due. It also notifies once per fund result.
- The presenter's `CompanyRow` carries only a label, not the company identity (`LookThroughResult.Company`
  has an `Identifier identity`), so rows have no stable key.
- `EulerpoolPreferencePage` applies actions immediately through three buttons and calls
  `noDefaultAndApplyButton()`. Other API key pages in PP are `FieldEditorPreferencePage`s with a single field.
- The item is registered in `Navigation.createPerformanceSection()` as a separate report entry.
- Available chart libraries in the UI bundle: SWTChart (used by PP's `PlainChart`, `BarChart`,
  `CircularChart`) and the engehausen treemap (`de.engehausen.treemap.swt.TreeMap`, used by
  `TreeMapViewer`, which is bound to `TaxonomyModel`). There is no refresh icon in `Images`; `REMOVE`, `INFO`
  and `WARNING` exist.

## Goals / Non-Goals

**Goals:**
- Fix selection loss and UI-thread recalculation without changing calculation results.
- Restructure the view around a summary, a coverage bar, charts and the table, using only bundled libraries.
- Make the settings page behave like other PP preference pages (Apply/OK semantics).

**Non-Goals:**
- No changes to the engine (`name.abuchen.portfolio/.../snapshot/lookthrough`), the provider adapter, the
  credential store API or persistence policies.
- No new third-party dependencies and no browser-based (JavaScript) charts.

## Decisions

### D1 Recalculate on input change, off the UI thread
`LookThroughStatusModel` notifies only when its observable state changed (outstanding count, refreshing set,
last refresh entries). The view separates two listeners: a cheap status listener that updates the progress
line, actions and status pane, and a result listener that runs only when retained compositions or
classifications changed (compared by a version counter on the gateway reads) or on `notifyModelUpdated()`.
Recalculation runs as a coalescing background job (one pending run, newer requests replace it), then applies
the result with `asyncExec`.
*Alternative:* debouncing only on the UI thread. Rejected because a single calculation on a large portfolio is
already noticeable.

### D2 Stable row keys and selection preservation
Add the company identity (or, for categories and details, a composed key of category and source path) to the
presenter rows. Before applying a new model, the view stores the keys of the selection and the expanded
elements and the top index, and restores them after `setInput`. The status pane keys rows by fund reference.
An `IElementComparer` on the key lets JFace match old and new elements.
*Alternative:* `refresh()` with updated element content in place. Rejected because the row records are
immutable and the tree shape changes between results.

### D3 Layout
```
+---------------------------------------------------------------+
| Breakdown by Company - 26.10.2026              [Refresh]      |
| [banner: onboarding / suspended / progress with stop]         |
| value | resolved % (i) | top 10 % | funds 4/5                 |
| [ companies | ungrouped | other | unresolved ]  coverage bar  |
+------------------------------+--------------------------------+
| chart: (Treemap | Top 20)    | company table                  |
+------------------------------+--------------------------------+
| information pane: Data status | (later: provenance)           |
+---------------------------------------------------------------+
```
Chart and table share a `SashForm` whose weights are stored in the view preferences. The chart switches
through a view-menu or toolbar dropdown (PP's pattern in `HoldingsPieChartView`) rather than tabs, to keep
the header small. The summary strip and coverage bar are custom-painted `Canvas` controls, so they follow
the theme colors through the CSS styling engine as `TreeMapViewer` does.

### D4 Charts
- Treemap: reuse the rendering approach of `TreeMapViewer` (squarified layout, label and color providers)
  with a small look-through tree model (root, then companies). It is not built on `TaxonomyModel`. Colors:
  direct-dominant vs. fund-dominant using two theme colors, with the share in the label.
- Top-N bar: SWTChart horizontal stacked bars via PP's `PlainChart`/`BarChart` helpers, N = 20, with direct
  and indirect series.
- Selection link: a click on a tile or bar resolves the company key and selects it in the table (D2 keys).
  The reverse highlight sets the chart's selected element.

### D5 Actions and progress
Keep one toolbar action, "Refresh" (text action, because there is no refresh icon). The progress line is part
of the banner area: a `ProgressBar` with "x of y" text and a `REMOVE` icon button that calls
`statusModel.cancel()`. The banner area shows at most one banner, chosen by priority:
running refresh > suspended > no key with funds > empty portfolio.

### D6 Settings page
Switch to Apply/OK semantics: `performOk()`/`performApply()` call `replaceSecure` when the field is not empty,
and the remove control acts immediately (it is an explicit destructive action, as in other PP pages) and is
only enabled when a key exists. If `replaceSecure` returns `STORAGE_UNAVAILABLE`, the page shows a single
checkbox "Use for this session only" and stores via `replaceSession` on the next Apply. Validation errors use
`setErrorMessage`/`setValid(false)`, so the dialog stays open. `DevelopmentCredentials.install` stays as is.

### D7 Rename
- Navigation: `statementOfAssets.add(new Item(Messages.LabelBreakdown, LookThroughView.class))`, keeping the
  information pane visible (unlike Chart and Holdings).
- Messages: replace `LabelPortfolioLens` with `LabelBreakdown` and `LookThroughViewTitle`; change
  `PrefTitleEulerpool` to "Eulerpool"; remove keys that no longer have a use. Every language file already
  carries translations of the look-through keys, so new and changed texts are translated in all of them.
- Classes: `PortfolioLensAnalysis`, `PortfolioLensCompositionService`, `PortfolioLensSession` become
  `LookThroughAnalysis`, `LookThroughCompositionService`, `LookThroughSession`. Packages stay `lookthrough`.

## Risks / Trade-offs

- [Column and sash settings reset once after the rename] → acceptable for an unreleased feature; no migration.
- [Background recalculation races with a model update] → a generation counter discards stale results.
- [Treemap code duplicates parts of `TreeMapViewer`] → extract only if the duplication is large; upstream
  prefers not touching the taxonomy viewer in the same PR.
- [Apply/OK semantics change when the key takes effect] → the status line shows the state after Apply, and
  the view banner updates when the credential state changes.
- [Many removed message keys across 18 properties files] → remove keys in all files in the same commit to
  keep the bundle consistent.

## Migration Plan

Not released, so there is no user migration. The work is a stack of focused commits on
`feature/breakdown-ui-rework` on top of `feature/automatic-portfolio-xray`. Rollback is dropping the stacked
branch.

## Open Questions

- The exact top-N count and treemap color pair can be tuned during manual testing without changing specs.
