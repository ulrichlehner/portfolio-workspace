# Tasks

## 1. Setup

- [x] 1.1 In `portfolio/`, create `feature/concentration-metrics` from `feature/fund-overlap` (single linear stack); verify with `git log --oneline -1`

## 2. Implementation

- [x] 2.1 Compute the effective number of companies and the largest company in the presenter summary; verify with presenter tests for the even-spread and dominant-company examples
- [ ] 2.2 Show both in the header with tooltips and extend the attention indicator above 10 percent; add texts and translations; verify with a header test and the message checks

## 3. Verification and commit

- [x] 3.1 Run the Docker UI reactor tests and Checkstyle, scan the diff for private data and create one focused commit (fork 37b3cfeab; 135 UI tests pass)
- [ ] 3.2 Build the app and let the user check the summary with a private copy of the portfolio

## Notes

- 2.2 is implemented; the header has no SWT test, so its check is part of 3.2.
- Attention uses the share of the portfolio value; the effective number uses shares of the company exposure.
