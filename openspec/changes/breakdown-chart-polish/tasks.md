# Tasks

## 1. Setup

- [x] 1.1 In `portfolio/`, create `feature/breakdown-chart-polish` from `fix/signed-cash-rows` and verify with `git log --oneline -1`

## 2. Improvements

- [x] 2.1 Expand the company row when a chart selects it and verify in the running app that clicking a tile of a collapsed company shows its contributions
- [x] 2.2 Give the coverage legend a caption, hide zero categories and move cash/other off green; replace the treemap legend by a labelled direct-to-funds scale; verify with a presenter test for zero categories and in the running app in light and dark theme
- [x] 2.3 Group treemap companies below a readable size into one neutral "other companies" tile with tooltip, paint the whole chart area, and verify with a chart-model test for the grouping and in the running app that no blank region remains
- [x] 2.4 Separate the chart and table area from the data status pane within the view and verify in the running app in light and dark theme

## 3. Verification and commit

- [x] 3.1 Run the Docker UI reactor tests, scan the diff for private data and create one focused commit
- [ ] 3.2 Build the app and let the user confirm the four improvements with a private copy of the portfolio
