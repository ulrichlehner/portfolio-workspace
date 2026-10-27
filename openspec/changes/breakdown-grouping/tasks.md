# Tasks

## 1. Setup

- [ ] 1.1 In `portfolio/`, create `feature/breakdown-grouping` from `feature/company-enrichment`; verify with `git log --oneline -1`

## 2. Presenter

- [ ] 2.1 Add the grouping functions (country, region, market classification, sector, industry, currency) with template-based country and sector maps; verify with presenter tests per grouping including unknown and unmatched values
- [ ] 2.2 Build group rows with totals, unknown and pending groups and stable group keys; verify with tests that group totals equal the company exposure and that keys survive an enrichment update

## 3. View and charts

- [ ] 3.1 Add the "Breakdown by" selector to the toolbar, remembered in the view preferences; verify in a view test and in the running app
- [ ] 3.2 Show group rows in the table with expansion into companies and contributions; verify selection restore across grouping switches
- [ ] 3.3 Nest companies inside group tiles in the treemap and show groups in the bar chart with value labels; verify with chart model tests and in the running app in light and dark theme
- [ ] 3.4 Show the country source in the country tooltip and add all new texts with translations; verify with the message checks

## 4. Verification and commit

- [ ] 4.1 Run the Docker UI reactor tests and Checkstyle, scan the diff for private data and create one focused commit
- [ ] 4.2 Build the app and let the user check the country, region and sector groupings with a private copy of the portfolio
