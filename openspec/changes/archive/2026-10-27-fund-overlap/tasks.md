# Tasks

## 1. Setup

- [x] 1.1 In `portfolio/`, create `feature/fund-overlap` from `feature/revenue-regions` (single linear stack); verify with `git log --oneline -1`

## 2. Calculation

- [x] 2.1 Compute pairwise overlap, shared company count and ordered shared companies from the result's contributions; verify with unit tests for the spec examples and an excluded fund

## 3. UI

- [x] 3.1 Add the "Overlap" chart kind with an SWT-drawn matrix, shading, tooltips and the single-fund message; verify with a chart model test and in the running app in light and dark theme (checked by the user in the running app)
- [x] 3.2 Select the largest shared company in the table when a cell is clicked; verify in the running app (dropped after the user's check: cells no longer navigate, each pair is shown once with its shared count)
- [x] 3.3 Add texts and translations; verify with the message checks

## 4. Verification and commit

- [x] 4.1 Run the Docker UI reactor tests and Checkstyle, scan the diff for private data and create one focused commit (fork d03839b40; 132 UI tests pass)
- [x] 4.2 Build the app and let the user check the matrix with a private copy of the portfolio (checked by the user; lower-triangle layout after feedback)

## Notes

- 3.1 and 3.2 are implemented and covered by model tests; the visual check is part of 4.2.
- Cell shading is relative to the largest overlap; cell text is always the absolute value.
- The matrix has no scrolling; with many funds on a small pane cells use the minimum size.
