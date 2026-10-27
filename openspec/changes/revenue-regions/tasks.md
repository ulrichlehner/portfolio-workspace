# Tasks

## 1. Setup

- [x] 1.1 In `portfolio/`, create `feature/revenue-regions` from `feature/breakdown-grouping`; verify with `git log --oneline -1`

## 2. Core

- [x] 2.1 Parse revenue region responses with latest-period and axis selection; verify with synthetic fixture tests including mixed members and several periods
- [x] 2.2 Normalize members and scale incomplete splits; verify with tests for country, region, unknown and 90 percent sums
- [x] 2.3 Schedule value-ordered retrieval after profiles and cache splits for 90 days under the account policy; verify with fake clock and withdrawal tests

## 3. UI

- [x] 3.1 Add the "Revenue region" grouping with allocation, "No revenue data" group and coverage notice; verify with presenter tests that totals equal company exposure
- [x] 3.2 Add texts and translations; verify with the message checks

## 4. Verification and commit

- [x] 4.1 Run `scripts/dev.sh test` and the Docker UI reactor tests with Checkstyle, scan the diff for private data and create one focused commit (fork 456ce8c39; 5140 core and 130 UI tests pass)
- [ ] 4.2 With the user's private portfolio copy, compare Country and Revenue region totals and check coverage; report aggregates only

## Notes

- The coverage notice is a paragraph in the header's info tooltip, not a permanent line.
- Percentages at or below 1 that sum to at most 1.5 are read as fractions; confirm with a real response in 4.2.
- The country grouping is labelled "Country (headquarters)" / "Land (Firmensitz)" to set it apart from revenue regions.
- One company appears once per revenue group; each allocation has its own row key.
