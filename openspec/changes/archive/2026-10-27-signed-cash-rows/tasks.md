# Tasks

## 1. Setup

- [x] 1.1 In `portfolio/`, create `fix/signed-cash-rows` from `feature/breakdown-ui-rework` and verify with `git log --oneline -1` that it starts at the Breakdown branch tip

## 2. Validation

- [x] 2.1 Add `NETTED_IDENTIFIERLESS_ROWS` and a fatal-reason set to `CompositionValidationResult`, switch every "diagnostics non-empty means unusable" check to the fatal set, and verify with existing `CompositionValidatorTest` and coordinator tests that every existing reason still rejects
- [x] 2.2 Net identifier-less rows in `CompositionValidator.check` (design D1) and verify with new `CompositionValidatorTest` cases: the spec scenario (+0.05 % / -0.015 %) yields exact identified weights, one netted unresolved row and a netting diagnostic; a negative net rejects; a negative identified row rejects; an overfull total still rejects; source rows are unchanged
- [x] 2.3 Add a `LookThroughEngineTest` case with a synthetic fund containing negative identifier-less rows and verify that companies keep their exact values, the netted remainder is unresolved and the fund reconciles exactly

## 3. UI hint

- [x] 3.1 Add the netting sentence to the data status tooltip in all message files and verify with a `LookThroughDataStatusTest` case

## 4. Verification and commit

- [x] 4.1 Run `scripts/dev.sh test` and the Docker UI reactor tests, scan the diff for private data (no real ISINs or holdings in tests), and create one focused commit
- [x] 4.2 Build the app, open a private copy of the portfolio, and verify that the previously rejected funds show OK with a decomposed share and that their constituents appear in the breakdown; record the result without private values

## Workflow follow-up

- Push follows the same authorization as the Breakdown branch.
- Archive after the checks pass.
