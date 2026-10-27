# Tasks

## 1. Setup

- [ ] 1.1 In `portfolio/`, create `feature/revenue-regions` from `feature/breakdown-grouping`; verify with `git log --oneline -1`

## 2. Core

- [ ] 2.1 Parse revenue region responses with latest-period and axis selection; verify with synthetic fixture tests including mixed members and several periods
- [ ] 2.2 Normalize members and scale incomplete splits; verify with tests for country, region, unknown and 90 percent sums
- [ ] 2.3 Schedule value-ordered retrieval after profiles and cache splits for 90 days under the account policy; verify with fake clock and withdrawal tests

## 3. UI

- [ ] 3.1 Add the "Revenue region" grouping with allocation, "No revenue data" group and coverage notice; verify with presenter tests that totals equal company exposure
- [ ] 3.2 Add texts and translations; verify with the message checks

## 4. Verification and commit

- [ ] 4.1 Run `scripts/dev.sh test` and the Docker UI reactor tests with Checkstyle, scan the diff for private data and create one focused commit
- [ ] 4.2 With the user's private portfolio copy, compare Country and Revenue region totals and check coverage; report aggregates only
