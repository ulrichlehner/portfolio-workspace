# Proposal

## Why

The Breakdown view ends in a data status pane that is open by default and takes a large share of the window, although it is needed rarely. When it is needed, it is unclear: the progress line above the table counts arrivals, not results, so a running refresh looks like nothing is happening while funds wait for the rate limit. In addition, the summary label "Effektive Anzahl" reads as a portfolio split or a count of positions; a real user asked whether the value is the number of companies that make up 50 percent of the portfolio.

## What Changes

- The data status pane starts collapsed in portfolios that have no stored state for it. An explicit user choice to open or close it stays remembered and is never overridden.
- One always-visible status row sits between the table and the pane. It is the control for opening and closing the pane and states the current refresh situation in plain words: running lookups and waiting ones, how many funds have been answered, how many have data, how many have no composition, how many failed, and when the next attempt is due. A warning marker appears when something failed or was rejected.
- The row wording distinguishes arrivals from results. It never claims that a running or waiting lookup has produced data.
- The summary figure "Effektive Anzahl" becomes "Konzentration" and shows the approximate number of equally sized companies. The tooltip explains the calculation with the worked example of 3 equal shares and a 50/25/25 split, states that a smaller figure means higher concentration, and names the basis: only the companies recognized in the company exposure, not the unresolved remainder.
- All new and changed texts are translated into every locale.

Out of scope:

- Refresh order, request budget, rate limits, retry backoff, cadence and suspension rules stay unchanged.
- The two startup gaps found while investigating the first opening (an automatic round that runs before the fund list is known, and no automatic round directly after the key is entered in the settings dialog) stay unchanged; the status row makes the resulting wait visible. They are candidates for a later change.
- The handling of the information pane shared with every other view (sash behavior, the global menu item and its shortcut) is not changed.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `breakdown-view`: the data status pane defaults to collapsed and gains an always-visible status row that reports the refresh state; the concentration figure is renamed and explained.

## Impact

- `portfolio/name.abuchen.portfolio.ui/src/name/abuchen/portfolio/ui/views/lookthrough/LookThroughDataStatusPane.java`, `LookThroughView.java`, `LookThroughDataStatus.java`, `LookThroughStatusModel.java`, `LookThroughViewPresenter.java` and `LookThroughViewPart`/navigation registration for the default of the information pane.
- `portfolio/name.abuchen.portfolio.ui/src/name/abuchen/portfolio/ui/messages*.properties`: new and renamed keys in all locales.
- `portfolio/name.abuchen.portfolio.ui.tests`: status text, toggle behavior and concentration wording.

This change is fork-only. The look-through view exists only in the fork, so the branch starts from `release/fork` and the pull request targets `release/fork`. No upstream pull request is planned.
