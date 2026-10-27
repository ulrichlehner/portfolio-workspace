# Tasks

## 1. Setup

- [x] 1.1 In `portfolio/`, create `feature/breakdown-chart-polish` from `fix/signed-cash-rows` and verify with `git log --oneline -1`

## 2. Improvements

- [x] 2.1 Expand the company row when a chart selects it and verify in the running app that clicking a tile of a collapsed company shows its contributions
- [x] 2.2 Give the coverage legend a caption, hide zero categories and move cash/other off green; replace the treemap legend by a labelled direct-to-funds scale; verify with a presenter test for zero categories and in the running app in light and dark theme
- [x] 2.3 Fill the whole treemap area so tiles too small to draw leave no blank region, keep every company as its own tile, and verify in the running app with a large portfolio. A first version grouped small companies into one "other companies" tile; with about 4000 companies the group became the largest tile and dominated the chart, so grouping was dropped
- [x] 2.4 Separate the chart and table area from the header and from the data status pane with a custom-drawn line (the native separator is invisible on macOS) and verify in the running app in light and dark theme
- [x] 2.5 Draw treemap gaps only on tiles of at least 6 px; the gap lines covered the smallest tiles and left a white corner. The treemap library offers no minimum tile size or grouping option
- [x] 2.6 Show percent signs in the summary, the coverage legend and the charts, and write amount and share next to each bar with room on the value axis; verify with presenter tests and in the running app

## 3. Verification and commit

- [x] 3.1 Run the Docker UI reactor tests, scan the diff for private data and create one focused commit (fork commit c17c4e59c, 115 UI tests pass)
- [x] 3.2 Build the app and let the user confirm the four improvements with a private copy of the portfolio
