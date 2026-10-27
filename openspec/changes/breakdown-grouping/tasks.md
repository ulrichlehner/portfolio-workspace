# Tasks

## 1. Setup

- [x] 1.1 In `portfolio/`, create `feature/breakdown-grouping` from `feature/company-enrichment`; verify with `git log --oneline -1`

## 2. Presenter

- [x] 2.1 Add the grouping functions (country, region, market classification, sector, industry, currency) with template-based country and sector maps; verify with presenter tests per grouping including unknown and unmatched values
- [x] 2.2 Build group rows with totals, unknown and pending groups and stable group keys; verify with tests that group totals equal the company exposure and that keys survive an enrichment update

## 3. View and charts

- [x] 3.1 Add the "Breakdown by" selector to the toolbar, remembered in the view preferences; verify in a view test and in the running app
- [x] 3.2 Show group rows in the table with expansion into companies and contributions; verify selection restore across grouping switches
- [x] 3.3 Nest companies inside group tiles in the treemap and show groups in the bar chart with value labels; verify with chart model tests and in the running app in light and dark theme
- [x] 3.4 Show the country source in the country tooltip and add all new texts with translations; verify with the message checks

## 4. Verification and commit

- [x] 4.1 Run the Docker UI reactor tests and Checkstyle, scan the diff for private data and create one focused commit (fork 821a0bb55; UI tests pass)
- [ ] 4.2 Build the app and let the user check the country, region and sector groupings with a private copy of the portfolio

## Notes

- Visual checks of 3.1-3.4 (selector, group rows, nested treemap, grouped bars, tooltips) are part of 4.2.
- The selector sits before the chart-kind drop-down; there is no separate Top N menu.
- Sector names also match a small alias table (for example "Technology", "Healthcare", "Financial Services").
- Without profile access companies are not left in "Pending"; they show under their known attributes or "Unknown".
