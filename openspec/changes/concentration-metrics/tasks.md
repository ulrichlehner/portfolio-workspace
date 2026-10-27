# Tasks

## 1. Setup

- [ ] 1.1 In `portfolio/`, create `feature/concentration-metrics` from `feature/fund-overlap` (single linear stack); verify with `git log --oneline -1`

## 2. Implementation

- [ ] 2.1 Compute the effective number of companies and the largest company in the presenter summary; verify with presenter tests for the even-spread and dominant-company examples
- [ ] 2.2 Show both in the header with tooltips and extend the attention indicator above 10 percent; add texts and translations; verify with a header test and the message checks

## 3. Verification and commit

- [ ] 3.1 Run the Docker UI reactor tests and Checkstyle, scan the diff for private data and create one focused commit
- [ ] 3.2 Build the app and let the user check the summary with a private copy of the portfolio
