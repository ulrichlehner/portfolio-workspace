# Implementation progress

## 2026-10-23: composition foundations (task 2.1)

- Workspace orchestration documentation committed as `848561c`. Subsequent
  model-routing clarification is in the working tree.
- PP branch: `feature/automatic-portfolio-xray`, based on `upstream/master`
  at `31094c7de`. Foundation code remains uncommitted pending the focused
  composition/calculation increment.
- Added immutable composition, instrument, provenance, retrieval-result,
  provider/account and persistence-policy types, a dedicated online provider
  contract, Factory discovery and the domain package export.
- Synthetic providers verify substitution, account isolation, policy/preference
  interaction, independent unknown dates and immutable source rows. Source
  weights remain raw decimal text for subsequent numerical validation.
- Parent reviewed code and tests. Independent Sol 6.1 medium review found no
  concrete correctness/specification violations.
- `scripts/dev.sh test FundCompositionProviderTest`: 5 tests, no failures/errors;
  Checkstyle passed.
- `scripts/dev.sh test`: 4,868 tests, no failures/errors, 1 skipped;
  Checkstyle passed. No UI build was required for this core-only step.
- Next: task 2.2, conservative decimal validation. Tasks 1.2 and 1.3 remain
  open; no provider permission or validated real-fund exposure is claimed.

## 2026-10-23: conservative validation (task 2.2)

- Sol 6.1 medium implemented the validator and result types; parent reviewed
  all three added files, including the synthetic tests.
- Exact decimal arithmetic preserves shortfalls and ordered duplicate rows.
  Unverified denominators, unsupported exposure bases, missing/invalid weights,
  signed allocations and overfull totals reject the complete snapshot while
  preserving source information. Completeness and identity are not inferred.
- `scripts/dev.sh test CompositionValidatorTest`: 13 tests passed, zero
  failures/errors/skips; Checkstyle passed. The first attempt was cancelled by
  a server restart; only that interrupted check was rerun.
- Task 2.3 is assigned to Sol 6.1 medium, limited to new classification and
  identity-resolution files and tests. No shared build operations are delegated.

## 2026-10-23: identity and classification (task 2.3)

- Sol 6.1 medium implemented independent evidence assertions, resolution states
  and a bounded resolver. Parent reviewed all four added files.
- Instrument identity, classification and company grouping retain separate
  provenance. Matching uses exact namespaced identifiers, never labels alone.
  Identified equity without company evidence is ungrouped; missing/conflicting
  identity or classification is unresolved. Cash/other and funds remain distinct.
- At most one budget-admitted injected lookup occurs per invocation. Completely
  identifierless rows remain unresolved; provider identifiers can support rows
  without ISINs. Request costs and deadlines belong to the later adapter/scheduler.
- `scripts/dev.sh test InstrumentResolverTest`: 19 tests passed, zero
  failures/errors/skips; Checkstyle passed.
- Task 3.1 is assigned to Sol 6.1 medium for current snapshot valuation and
  selected positive-securities scope. Unrelated Eclipse `.project` and m2e
  settings changes are left untouched and excluded from feature scope.

## 2026-10-23: valuation integration (task 3.1, review pending)

- Sol 6.1 medium implemented the selected-securities valuation adapter and
  result type using joint snapshot positions and reporting-currency conversion.
- `scripts/dev.sh test SecuritiesValuationAdapterTest`: 15 tests passed, zero
  failures/errors/skips; Checkstyle passed.
- Independent Sol 6.1 medium review is checking actual PP transaction-price
  and missing-FX fallback behavior. Task 3.1 remains unchecked pending review.

- Review found negative historical FX could be mistaken for an excluded short,
  incorrectly retaining a complete denominator. The implementation agent corrected
  check ordering and added negative/zero historical FX and missing chained-rate
  regressions. The updated 17-test class still needs execution before completion.

## 2026-10-23: provider decisions and public acceptance research

- User confirmed development-only runtime/display and adapter distribution
  permission assumptions. Task 1.2 records that decision; task 6.3 now contains
  the actual pre-publish permission checklist. Real-data disk persistence remains
  disabled pending verified permission and retention. Strict OpenSpec validation
  passed after reconciling the artifacts.
- Sol 6.1 medium investigated the independent public iShares Core DAX example.
  No private portfolio data, credentials or provider contact were used.
- Public Eulerpool payload:
  https://api.eulerpool.com/api/1/etf/holdings/DE0005933931
  It returned 43 rows, all with null asset type, and no holdings-effective date.
  Each percentage agreed with its value divided by the sum of returned values
  to the reported precision. This does not prove a total-fund NAV denominator.
- Issuer comparison:
  https://www.ishares.com/de/privatanleger/de/produkte/251464/ishares-core-dax-ucits-etf-de/latest-holdings.csv
  The 2026-10-22 disclosure includes a zero-market-value futures row with nonzero
  notional exposure. The provider snapshot's effective date is unknown, so this
  is not a matched-date omission finding. Physical replication is not proof of
  derivative-free economic exposure. Current weights and quantities differ.
- Issuer annual report:
  https://www.ishares.com/gls-download/literature/annual-report/ishares-core-dax-ucits-etf-de-jahresbericht-2026.pdf
  The 2026-04-30 report explicitly reconciles NAV with derivatives, bank balances,
  other assets and liabilities. It supports classification/issuer evidence for
  38 of the 40 current equity-candidate ISINs; public primary sources explain the
  remaining identifiers:
  https://www.fresenius.com/Fresenius-transitions-to-registered-shares
  https://www.hochtief.com/investor-relations/hochtief-share
- Task 1.3 remains open. Missing evidence: authoritative Eulerpool NAV semantics
  or a matched-date NAV reconciliation, supported exposure basis, and reproducible
  automatic classification/company mappings. The DAX example is a useful negative
  control, not a certified usable decomposition.
- PP code is uncommitted pending the corrected valuation tests, full core checks
  and a focused composition/calculation milestone. Workspace progress is committed
  independently; unrelated Eclipse metadata is excluded.

## 2026-10-23: verified core milestone committed

- Workspace planning/progress checkpoint: `abefb43`.
- PP foundation milestone: `929e5e11e` (`feat: add portfolio look-through foundations`).
  Includes tasks 2.1–2.3 and 3.1, synthetic tests and service discovery only;
  unrelated Eclipse metadata was excluded. No push or PR was performed.
- Parent reviewed the corrected valuation check order and regression tests.
  `scripts/dev.sh test`: 4,917 tests, zero failures/errors, one skipped;
  Checkstyle passed, including all 17 valuation tests. Task 3.1 is complete.
- Valuation follows PP joint net security positions and monetary rounding.
  Malformed null-currency portfolios can fail during PP snapshot construction;
  the adapter's guard does not establish support for that upstream failure.
- Next core increment: contribution aggregation, residuals and bounded nested
  traversal (tasks 3.2–3.4). Keep focused milestone commits; consolidate the core
  increment to one commit per upstream PR before publishing as required.

## 2026-10-24: exposure engine (tasks 3.2–3.4)

- Sol 6.1 medium implemented the related tasks together. Parent reviewed all
  four added files; no additional review agent was needed for this increment.
- Exact decimal minor-unit contributions reconcile across company, ungrouped
  equity, cash/other and unresolved categories. Paths preserve duplicate source
  occurrences and provenance. Cycles are identity-based and path-local; leaves
  at edge eight are usable, while expansion to edge nine stops that branch.
- `scripts/dev.sh test LookThroughEngineTest`: 13 tests passed, no failures,
  errors or skips; Checkstyle passed. Includes the exact 80%/20% example.
- PP checkpoint: `afbe745cb`. Only the four reviewed engine/test files were
  staged; no provider payloads, private data or Eclipse metadata were included.
- Full core verification remains required before publishing the combined core
  increment. No publishing performed. Next: task 4.1 adapter, preserving unknown
  denominator/exposure/classification rather than claiming task 1.3 acceptance.
