# Proposal

## Why

Returning to the Breakdown view always rebuilds the whole pipeline: the view is disposed on leave, and on return it shows "Aufschlüsselung wird berechnet …" while it re-runs the analysis and re-presents thousands of companies. With 4 180 companies that is a visible pause on every switch, even though nothing changed.

Two smaller problems sit in the same view. Changing "Aufteilung nach" widens both the title and the selector, and the toolbar then hides "Aktualisieren" behind the `>>` overflow. The data status pane spends three lines on facts that fit one, which costs table height whenever it is open.

## What Changes

- **Measure first.** An opt-in timing switch logs the duration of gathering inputs, analysis, presentation, table application and treemap per view creation. The numbers are recorded in the change; they decide how far the performance work goes.
- **Show the last result immediately.** Within one session the service keeps the last result and presentation per portfolio. On return the view shows that result at once and recalculates in the background, replacing it when the new result is ready. The date slot shows an indeterminate progress while this runs; this also applies when the file has unsaved changes.
- **Lazy company table (gated by the measurement).** If the table application dominates, the company table becomes a virtual tree that creates rows only when they scroll into view. If the measurement shows the cache already makes the return instant and the table share is small, the change records the numbers and leaves the tree eager instead of adding the risk.
- **Stable header controls.** "Aktualisieren" moves to the right action toolbar, which the overflow layout never collapses. The grouping selector names the current grouping in its label and menu; it may change width, but the refresh action keeps its position. The view title stays constant, so the header keeps room for the action.
- **Compact data status pane.** Storage mode, company data state and the assumed-company count become one line with a tooltip; a limitation of persistence (session only, disk failure) stays as its own visible warning line. Margins shrink from 5 to 2 pixels. A pane with a single page hides its page selector and its empty title row, so no redundant button and no gap sit above the content.

Out of scope:

- Refresh order, request budget, rate limits, retry backoff and provider requests stay unchanged.
- The treemap keeps one tile per company; small tiles are not aggregated.
- Selection and expansion are still not restored across a view switch; only the result and its presentation are.
- No change to other views or to the global information pane behaviour.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `breakdown-view`: immediate restore from the last result, a stable header that keeps the refresh action visible, and a compact data status summary line.

## Impact

- `portfolio/name.abuchen.portfolio.ui/src/name/abuchen/portfolio/ui/views/lookthrough/LookThroughView.java`, `LookThroughHeader.java`, `LookThroughDataStatusPane.java`, `LookThroughCompositionService.java`, `LookThroughViewPresenter.java`.
- `portfolio/name.abuchen.portfolio.ui/src/name/abuchen/portfolio/ui/editor/AbstractFinanceView.java` for the title width used by the breakdown view.
- `portfolio/name.abuchen.portfolio.ui/src/name/abuchen/portfolio/ui/messages*.properties` only if the updating indicator needs its own text.
- `portfolio/name.abuchen.portfolio.ui.tests` for the cache, the summary line and the header state; a manual check covers the layout on macOS and the VM.

This change is fork-only and targets `release/fork`. It follows Rule 4: a branch from `release/fork` and a pull request in `ulrichlehner/portfolio` into `release/fork`; no direct commit or push to `release/fork`.
