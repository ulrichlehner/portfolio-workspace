# Tasks

## 1. Setup

- [ ] 1.1 In `portfolio/`, create `feature/fund-overlap` from `feature/revenue-regions` (single linear stack); verify with `git log --oneline -1`

## 2. Calculation

- [ ] 2.1 Compute pairwise overlap, shared company count and ordered shared companies from the result's contributions; verify with unit tests for the spec examples and an excluded fund

## 3. UI

- [ ] 3.1 Add the "Overlap" chart kind with an SWT-drawn matrix, shading, tooltips and the single-fund message; verify with a chart model test and in the running app in light and dark theme
- [ ] 3.2 Select the largest shared company in the table when a cell is clicked; verify in the running app
- [ ] 3.3 Add texts and translations; verify with the message checks

## 4. Verification and commit

- [ ] 4.1 Run the Docker UI reactor tests and Checkstyle, scan the diff for private data and create one focused commit
- [ ] 4.2 Build the app and let the user check the matrix with a private copy of the portfolio
