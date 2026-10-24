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

## 2026-10-24: Eulerpool adapter (task 4.1)

- Sol 6.1 medium implemented the adapter; parent reviewed the implementation
  and synthetic tests. Injected credentials, transport and clock support
  identifier-only requests, Bearer authentication and sanitized failures.
- `scripts/dev.sh test EulerpoolFundCompositionProviderTest`: 16 tests passed,
  zero failures/errors/skips and zero Checkstyle violations.
- PP checkpoint: `350c4ae41`. Only the adapter, service descriptor and synthetic
  tests were committed after review; no live payloads or private data included.
- Denominator, exposure basis, completeness and effective date remain unknown.
  Persistence policy remains unverified; task 1.3 is still open.
- Task 4.2 is delegated to Sol 6.1 medium for budgeting, coalescing and refresh
  control. Parent coordinates verification. Full integration checks and focused
  upstream commit consolidation remain outstanding; no publishing performed.

## 2026-10-24: budgeted refresh (task 4.2)

- Parent reviewed both core classes and both synthetic test classes supplied by
  Sol 6.1 medium. PP checkpoint: `4f0a6e840`; no private data included.
- `scripts/dev.sh test 'CompositionRequestBudgetTest,CompositionRefreshCoordinatorTest'`:
  23 tests passed, zero failures/errors/skips; Checkstyle passed.
- Shared weighted allowance covers retrieval and bounded enrichment; identical
  account/identifier requests coalesce. Automatic eligibility uses 24 rolling
  hours from admitted attempts, including failed/manual attempts. Manual refresh
  bypasses cadence only. Retry-After protects the provider allowance; auth and
  entitlement suspension is account-local and needs a configuration revision.
- Reads never request data. Task 5.2 must supply initial/periodic eligibility
  calls from application-lifetime background jobs and wire cancellation.
  Close discards queued/late work but cannot interrupt synchronous transport.
- Next: task 4.3 policy-gated composition storage with synthetic providers.
  Full integration verification and publication gates remain outstanding.

## 2026-10-24: composition stores (task 4.3)

- Sol 6.1 medium implemented the stores and corrected a parent-identified
  portability limitation. Parent reviewed all five files and synthetic tests.
- `scripts/dev.sh test CompositionStoreTest`: 25 tests passed, no failures,
  errors or skips; Checkstyle passed. PP checkpoint: `125b8802d`.
- Session and disk modes share bounded validation; tests compare exact engine
  results after restart. Versioned records preserve dates, decimal text and
  duplicate rows. Failed refreshes preserve last-valid data within retention.
- Account policy/preference generations invalidate pending disk writes after
  withdrawal/deletion, including re-enable races. Real Eulerpool policy remains
  unverified and cannot activate persistence.
- Portable file operations require an application-owned private directory;
  observed links are rejected. This is not protection against hostile concurrent
  replacement of directory ancestors. Atomic replacement is mandatory; failure
  preserves the previous file and exposes DISK_FAILURE with session analysis.
  No SecureDirectoryStream or POSIX capability is required. Capability-fallback
  tests ran in Linux Docker; native Windows/macOS verification is outstanding.
- Integration must share one store ticket per coalesced retrieval, complete it
  with the actual attempt, and read active funds during eligibility passes to
  enforce retention even when retrieval is deferred. Evidence-backed resolutions
  are supplied separately, not serialized. Tasks 4.5/5.2 own application wiring.
- No private data included or publishing performed. Next: task 4.4 credentials.

## 2026-10-24: credential setup (task 4.4)

- Sol 6.1 medium implemented credentials, Equinox backend, masked preferences
  page and synthetic tests. Parent reviewed all code/tests/documentation and
  corrected message ordering using the upstream sorter in Docker.
- PP checkpoint: `1882e6d1a`. Only the 11 reviewed feature files were included;
  no real keys, private data or unrelated Eclipse metadata were committed.
- Core command selecting CompositionCredentialsTest,
  EquinoxCompositionCredentialStoreTest and EulerpoolFundCompositionProviderTest:
  31 tests passed, zero failures/errors/skips; Checkstyle passed.
- Focused EulerpoolPreferencePageTest via the Docker UI reactor (including REST
  and bootstrap): one test passed; Checkstyle passed.
- `scripts/dev.sh app` initially failed canonical message ordering after UI
  compilation. After sorting, the complete build and packaging passed, including
  managed-resource checks and Checkstyle. Tests are skipped by this app command.
- Existing target/product supplies Equinox security and OS-specific fragments;
  only the provider-hints package import was added. Encrypted writes verify the
  round trip and flush. Failure permits explicit session entry, never plaintext
  fallback. Unconfirmed deletion is reported and blocks old access this session.
- Native unlocking and isolated-app setup/restart/replacement/deletion checks
  remain for integration/manual verification (6.2); mock tests do not prove OS
  keychain behavior. Translation work remains in 5.3.
- Task 5.2 must construct the credential-enabled provider explicitly and forward
  the account's non-secret credential revision to configurationChanged before
  refresh. Discovery remains unconfigured. Next: task 4.5 persistence preferences.
