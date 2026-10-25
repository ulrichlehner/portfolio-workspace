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

## 2026-10-24: checkpoint before free-model routing

- The user authorized continuing with the free models of the `opencode` provider.
  The routing baseline in the workspace `AGENTS.md` was updated accordingly.
- Rollback checkpoint: workspace tag `lens-checkpoint-before-free-models` and fork
  tag `lens-checkpoint-before-free-models` on PP commit `1882e6d1a` (task 4.4).
- State at the checkpoint: 19/30 tasks complete, all recorded checks green, no
  pushes or pull requests, publication gates still open.

## 2026-10-24: composition persistence preference (task 4.5)

- Bounded implementation ran on a free `opencode` model; the parent reviewed the
  entire diff, rewrote the assertions and fixed the compile, notification and
  message-ordering defects found during verification.
- `CompositionPersistencePolicy` now reports an `EffectiveMode` with mode and
  reason (`PERMITTED`, `USER_OPT_OUT`, `POLICY_PROHIBITED`,
  `POLICY_UNVERIFIED`); `effectiveMode` remains the consistent shorthand.
- `CompositionPersistencePreferences` is a non-secret, per-account interface with
  an in-memory test implementation and a listener binder returning an
  `AutoCloseable` handle. The desktop implementation uses Eclipse instance-scope
  preferences, keyed by hex-encoded provider/account identifiers; a single
  preference-change notification path reconfigures the affected account only.
- The Eulerpool preference page shows the effective mode and reason, disables the
  retain control while permission is unverified and enables it from the injected
  policy. New strings are externalized and canonically sorted.
- Toggling off deletes only that account's retained files, invalidates pending
  writes and keeps the current in-memory analysis usable; toggling on writes
  nothing retroactively; preference-on with unverified policy stays session-only
  and creates no cache directory.
- PP commit `01686706c` contains only the 11 reviewed feature files; unrelated
  `.project` and m2e preference changes remain excluded.
- Core command selecting CompositionStoreTest, CompositionStorePreferenceToggleTest,
  CompositionPersistencePolicyTest and CompositionPersistencePreferencesTest:
  41 tests passed, zero failures/errors/skips; Checkstyle passed.
- Focused EclipseCompositionPersistencePreferencesTest and
  EulerpoolPreferencePageTest via the Docker UI reactor (including REST and
  bootstrap bundles): 2 tests passed; UI and test-bundle Checkstyle passed.
- `docs/portfolio-lens-credentials.md` describes the preference, instance scope,
  deletion behaviour and session-only restart/offline limits.
- Remainder: provider permission and retention stay unverified, so the control is
  disabled and real-data disk persistence stays off until task 6.3 completes.
  Native platform and integrated-app checks remain in tasks 5.x/6.x.

## 2026-10-24: Portfolio Lens view (task 5.1)

- Bounded implementation ran at maximum effort on a free `opencode` model; the
  parent reviewed the full diff and corrected the completeness rule, the
  composition lookup and the share-column label.
- New package `name.abuchen.portfolio.ui.views.lookthrough`: a thin
  `LookThroughView` that performs no retrieval, holds no credentials, starts no
  jobs and persists no analysis, plus an SWT-free `LookThroughViewPresenter`
  that carries every presentation rule.
- Columns are company/instrument, source, direct, indirect, total and share.
  Company rows expand into their contributions with the direct/indirect flag and
  the fund path. Coverage categories (ungrouped equity, cash/other, unresolved)
  and valuation exclusions are always listed, including zero values, so a
  missing row cannot read as full coverage.
- Shares come only from `LookThroughResult.denominator()`; the label names the
  selected positive securities value and the account-cash exclusion. Without a
  denominator no percentage is rendered at all.
- Complete coverage requires a present denominator, a complete and fully
  supported valuation, exactly zero unresolved and ungrouped value, and an
  affirmative `Completeness.COMPLETE` on every composition used along a path.
  The validator treats completeness metadata as unverified, so anything below an
  affirmative declaration stays partial. The engine keeps the validation on the
  path edges of decomposed rows and only failed/shortfall rows carry it
  directly; the first implementation read the wrong field and the new test
  caught it.
- `Portfolio Lens` and all new labels are externalized in `Messages` and
  canonically sorted. `Navigation` registers the view in the reports section.
  No bundle, application or portfolio-format identifier changed and no image
  asset was added.
- PP commit `82052b608` contains only the six reviewed feature files.
- Core look-through suite, all ten test classes under
  `snapshot/lookthrough`: passed with zero failures and clean Checkstyle.
- Focused `LookThroughViewPresenterTest` through the Docker UI reactor
  including the REST and bootstrap bundles: 9 tests passed, UI and test-bundle
  Checkstyle clean.
- Message and label validation passed through `:portfolio-build-tools-check`,
  which the `local-dev` profile does not cover.
- Synthetic data only: no network access, no credentials, no persistence and no
  real values. The view shows the no-result state until task 5.2 supplies
  results, cancellable refresh and the data-status panel.

## 2026-10-24: look-through data status (task 5.2, in progress)

- Split into two increments so the state machine stays testable without SWT.
- Part 1 committed as PP commit `046847761`: `LookThroughDataStatus` renders
  per-fund provenance, freshness, source declaration, latest attempt and the
  global storage mode with its restart limitation; `LookThroughRefreshController`
  dispatches one coalesced manual request per account/identifier map.
- Freshness is a display fact: a retrieval exactly 24 hours old is fresh, one
  second older is stale. Holdings dates are never substituted by refresh or
  retrieval dates, provider refresh and local retrieval stay distinct, and a
  failed attempt keeps the retained dates beside it.
- Excluded positions are not duplicated in the status; they stay with
  `LookThroughViewPresenter` as the single source of truth.
- A superseded wait used to be dropped silently, which would have left a caller
  unable to learn that a refresh had ended. It now reports `CANCELLED`, and
  `refresh` returns the number of outcomes the caller will receive.
- Verification part 1: `LookThroughDataStatusTest` (11) and
  `LookThroughRefreshControllerTest` (10) through the Docker UI reactor including
  the REST and bootstrap bundles, Checkstyle clean, message and label validation
  through `:portfolio-build-tools-check` passed.
- Part 2 committed as PP commit `902f138dc`: SWT-free `LookThroughStatusModel`
  owns the current facts, the busy state and the memory-only status build; the
  view offers Refresh and Cancel, pushes the status into a new
  `LookThroughDataStatusPane` and re-pushes it after the information pane
  exists, because the first push happens before the pane is created.
- The composition source stays optional: without a backend the view shows no
  status and offers no refresh. Only the Refresh action calls `refresh()`, so a
  redraw, a resize, a recalculation or a selection change cannot cause provider
  traffic. Cancelling ends the wait immediately, and outcomes of the superseded
  call are ignored.
- Verification part 2: `LookThroughStatusModelTest` (7), `LookThroughDataStatusTest`
  (11), `LookThroughRefreshControllerTest` (10) and `LookThroughViewPresenterTest`
  (9) through the Docker UI reactor including the REST and bootstrap bundles:
  37 tests, no failures, Checkstyle clean, message and label validation passed.
- Task 5.2 stays unchecked: no composition source is supplied in the running
  application yet, so the required isolated-app check of responsive
  refresh/cancel and the status pane cannot be performed. Supplying the provider,
  credentials, coordinator, store and selected funds to `LookThroughCompositionSource`
  and the calculated result to the view remains open application wiring.

## 2026-10-24: application composition wiring

- PP commit `60932f64f` assembles the backend per client: the discovered
  Eulerpool adapter with the application-lifetime credentials, a conservative
  request budget, the refresh coordinator and a session-only composition store.
  `PortfolioLensCompositionService` exposes it as the optional
  `LookThroughCompositionSource`; the view falls back to it when no source is
  injected.
- The store is the read source and receives every coordinated attempt, so the
  status displays the same retained data a later calculation uses. A ticket is
  taken before the asynchronous work and completed with the actual attempt.
- Refresh candidates are the explicitly selected securities with an ISIN. The
  portfolio model has no fund classification, so unselected holdings never reach
  the provider; sending every holding ISIN would disclose portfolio composition
  and the provider contract forbids it. Enrichment lookups stay at zero because
  no verified evidence service exists, so nothing is resolved from a guess.
- Limits are placeholders, not provider entitlements: 100 requests per rolling
  24 hours, 15 minute failure backoff, two pending requests. Real-data disk
  storage stays off because the provider reports unverified persistence
  permission.
- A retry hint now appears whenever the coordination knows the next possible
  attempt, so deferred quota and the automatic cadence are visible, not only
  rate limits.
- Verification: 42 UI tests green through the Docker UI reactor including the
  REST and bootstrap bundles, Checkstyle clean, message and label validation
  passed.
- Still open for task 5.2: an interactive check in the isolated app (select
  funds, refresh, cancel) cannot be performed by the agent because it needs
  user interface interaction; the wiring compiles and its SWT-free parts are
  tested.

## 2026-10-24: Java language server broke builds

- `scripts/dev.sh app` produced a macOS app whose core jar contained no classes.
  The same command was flaky (1043 classes once, then 35, 247 and 294 classes),
  and `-Dprotobuf.execution.phase=none` only avoided it by timing. No Maven task
  reported a failure, so the result looked like a successful build.
- Cause: the VS Code dev container's Java language server imports the fork through
  m2e and uses each bundle's `target/classes` as output folder. Its background build
  deletes those folders while `scripts/dev.sh` compiles into them. Its log records
  `Error occurred while deleting: /name.abuchen.portfolio/target/classes/name`
  followed by `BatchImageBuilder.cleanOutputFolders`.
- Fix: `java.autobuild.enabled` is off in `.vscode/settings.json` (workspace commit
  `22986a6`). Editing and navigation still work; building is an explicit action.
- The same import rewrites the tracked `*/.project` files with the m2e builder,
  nature and language server filters. They were restored, not committed, and the
  rule is recorded in `AGENTS.md`. The `.tycho-consumer-pom.xml` files that every
  Maven build writes per bundle, and the m2e preference file, are untracked
  artifacts and are excluded in `portfolio/.git/info/exclude`, because the fork's
  `.gitignore` must stay equal to upstream.
- Verification after the fix: `scripts/dev.sh app` finished with `BUILD SUCCESS` in
  4:06 minutes and produced a 231 MB app with the bundled Zulu 21 JRE. The core jar
  holds 1043 classes and the UI jar 1581, including 45 look-through classes, so the
  build output is complete again.

## 2026-10-24: label translation (task 5.3)

- Externalization was already complete: the look-through package contains no
  hardcoded user-visible text, the view name comes from `LabelPortfolioLens`, and
  the status, category, reason, preference and limitation texts all use
  `Messages`. No icon was added, so the CC0, iconmonstr, SVG sizing and `Images`
  registration rules do not apply to this change.
- Upstream practice decided the translation scope: recent feature commits by
  external contributors change 17 or 18 `messages_*.properties` files, and
  `CONTRIBUTING.md` asks code contributors to translate new labels. The user chose
  that route over English-only keys.
- 83 new keys (view, data status, preferences, setup and limitation texts,
  missing-date states) are translated into all 18 supported languages and
  appended to the family through the managed properties tool, which produced the
  canonical order, escaping and alignment. The properties files stay pure ASCII
  with `\uXXXX` escapes, sorted, without duplicate keys.
- Reviewed and corrected before insertion: German needs the dative after `vor`
  (`einer Stunde`), Russian uses an abbreviation in the age formatter because
  MessageFormat cannot express Slavic plurals, Russian and Polish name the
  originating security instead of the underlying asset or the source column,
  Czech and Slovak say "or" rather than "and" for cash or other assets, and
  German uses `Barmittel` because PP's German does not use `Barschaft`.
- Verification: all 18 files carry exactly the reviewed 83 values with matching
  `{0}`/`{1}` counts and an intact `choice` pattern, the family passes
  `:portfolio-build-tools-check`, and `scripts/dev.sh app` finished with
  `BUILD SUCCESS` in 3:40 minutes. The packaged `messages_de`, `_zh`, `_ru` and
  `_tr` files are byte-identical to the sources, so the translations are in the
  built bundles. An earlier build was rejected by the build metadata check with
  "Sources changed during build", which confirms that guard works.
- Committed as PP commit `85709c513`.
- Task 5.4 documentation is PP commit `b82bc5a76`: `docs/portfolio-lens.md`
  describes scope, coverage rules, refresh and budget, data status, persistence,
  session-only limits and local data removal. Its isolated-app workflow checks
  stay open until the interactive run below.

## Integration review fixes (2026-10-24)

The user authorized immediate correction of the review findings in this chat.
PP commit: `41e4d60` (`fix: complete Portfolio Lens refresh wiring`). This is a
local integration milestone; nothing was pushed. Final upstream commit/PR
consolidation remains part of task 6.5.

This entry supersedes the earlier assessment that task 5.2 lacked only a manual
check. The review found missing calculation wiring, missing credential revision
forwarding, dropped multi-fund requests at the pending limit, and no automatic
eligibility dispatcher. Corrections:

- The view now calculates current selected securities values through
  ClientSnapshot, SecuritiesValuationAdapter and LookThroughEngine on opening,
  portfolio updates and refresh outcomes. A memory-only analysis bridge combines
  retained evidence and compositions; missing evidence remains unresolved.
- One application-wide provider session shares budgeting and coalescing across
  clients. It serializes admission of distinct funds instead of returning BUSY
  for the remainder of a selection. Provider quotas, suspension and backoff still
  defer requests; the queue does not override these limits.
- Credential state/revision is read on the background executor before dispatch
  and forwarded to the coordinator. Corrected authentication can trigger a new
  automatic attempt without waiting out the failed attempt's daily cadence.
- Opening the analysis and a minute-based eligibility timer request automatic
  refresh with manual=false. The coordinator enforces rolling 24-hour cadence.
  Redraw/status reads never dispatch. Disposing the view removes its timer and
  ignores late UI callbacks. Cancel ends the UI wait; provider work already
  queued can continue, as documented.
- Reapplying unchanged persistence preferences no longer invalidates pending
  store tickets. Invalid source previews retain provenance for status display,
  while only retained validated compositions enter calculation.
- User documentation now describes automatic/manual behaviour and explicitly
  states that the current real adapter lacks validated allocation and identity
  evidence. The full direct-plus-fund path is verified with synthetic evidence;
  this does not pass provider gate 1.3 or establish useful real-data coverage.

Verification:

- `scripts/dev.sh test`: 5,025 tests, zero failures/errors, one skipped;
  Checkstyle passed.
- Focused Docker UI reactor (`*LookThrough*Test,*PortfolioLens*Test`, including
  REST and bootstrap): 51 tests, zero failures/errors/skips; Checkstyle passed.
  Nine new regressions cover queued selections and coalescing, authentication
  recovery, initial/rolling/manual refresh, memory-only reads, pending store
  tickets, invalid-source provenance, selection valuation, exact direct/fund
  overlap with residual, updated valuations and automatic status dispatch.
- The first UI check identified an unused import; it was removed before the
  successful run. All test data and credentials are synthetic. No live provider
  requests or private portfolio reads were needed for these fixes.
- Diff/privacy review and `git diff --check` passed. No portfolio format, WebDAV
  tooling, credentials, translations or external permission assumptions changed.
- `scripts/dev.sh app`: BUILD SUCCESS in 3:33, including integrated UI
  compilation and macOS ARM64 packaging with bundled Java, at PP revision
  `41e4d609f`. Packaging skips test execution; test results above come from
  separate test runs. Retain the packaged app for the user's pending manual
  check rather than cleaning it before that check can run.
- Verification recorded on 2026-10-25: task 6.1 is complete. Task 5.2 still
  requires interactive acceptance; a successful build does not establish it.

Remaining acceptance:

Task 5.2 stays open until the user checks the isolated macOS app. Run
`scripts/dev.sh run-app --webdav-copy` from the macOS host, select securities,
then open Portfolio Lens. Confirm current values/unresolved rows, data status,
responsive refresh/cancel, credential replacement and revisiting the view.
Use only the managed local copy and keep identifiers/values out of public
records. Ordinary startup can retrieve selected identifiers once credentials
are configured; no quantities, transactions or portfolio files are submitted.

Task 1.3 and the task 6.3 permission/data-quality gates remain open. Unknown
allocation semantics can also cause validation backoff; queued admission does
not imply that every fund was fetched in a single pass. Real provider data stays
session-only. The 100% validated-coverage objective remains unchanged and is not
achieved by this integration milestone. Tasks 5.4, 6.2, 6.4 and 6.5 still need
their respective acceptance, follow-up and publication preparation work.

## First-open injection regression (2026-10-25)

The user's isolated manual check failed: Portfolio Lens showed neither an
analysis result nor composition status. This is an application-startup defect,
not evidence of a provider timeout or incomplete coverage. Task 5.2 remains
open; the earlier integration test suite did not exercise Eclipse injection.

Root cause: the view declared its creatable composition service as an optional
injection. In a fresh Eclipse context, optional lookup did not construct the
service, leaving the view without its backend. Required injection now creates
it; the redundant null guard no longer silently skips application wiring.

PP fix: `63f7fad` (`fix: initialize Portfolio Lens on first open`). The new
PortfolioLensInjectionTest uses Eclipse's actual ContextInjectionFactory on the
real view's annotated fields, with Mockito skipping SWT control construction.
It does not claim to test rendering or interactive behaviour.

Verification:

- All 52 focused look-through/Lens UI tests passed with the correction;
  Checkstyle passed.
- The same new regression test was run against the original optional-injection
  view and failed with the expected missing-backend assertion (one failure,
  zero errors). The corrected view was restored before committing.
- No core logic changed in this correction. The preceding 5,025-test core run
  remains the core verification evidence.
- `scripts/dev.sh app`: BUILD SUCCESS in 3:39 against `63f7fad`, with
  bundled-runtime macOS ARM64 packaging. App packaging skips test execution;
  the 52-test result above is from the separate focused test run. The initial
  packaging attempt was stopped to wrap the commit body correctly, then
  restarted against the final commit. The build is retained for manual testing.
- Strict OpenSpec validation and `git diff --check` passed.
- Diff review found no private identifiers, credentials or portfolio data.
  The user screenshot and local logs were not copied into repository artifacts.

Manual retest: launch from the macOS host with
`scripts/dev.sh run-app --webdav-copy`. Select the securities to include in a
securities view, then open Portfolio Lens. Current valuation and unresolved
categories should appear without waiting for a provider. Configure the personal
key in preferences when needed to check automatic/manual retrieval and status.
Verified company decomposition still depends on the open provider evidence gate;
the 100% objective and all publication restrictions remain unchanged.

## 2026-10-25: live test found a blocked refresh (task 5.2)

- Symptom: in the isolated app a click on "Composition data: refresh" changed
  nothing. The status pane showed the first fund with "no composition data" and
  the remaining funds without an attempt.
- Cause: an instrument-local provider answer (`UNAVAILABLE`, `UNSUPPORTED` or a
  composition that the validator rejected) was recorded through the shared
  request budget, which set an account-wide 15 minute failure backoff. Every
  following fund was deferred before its attempt, and the serial session
  (at most one pending request) never reached it. An individual stock in the
  selection was enough to stop the whole refresh.
- Fix, PP commit `c1e0e0e18`: instrument-local answers no longer touch the shared
  budget. The budget keeps transport, authentication, entitlement and rate-limit
  failures, which do affect the whole account. Covered by
  `testMissingInstrumentDoesNotDelayOtherFunds` and
  `testUnavailableAndUnvalidatedRowsDoNotStallSelection`.
- Fix, PP commit `db458b0c2`: a composition that the provider delivered but the
  validator rejected left the data status unchanged. The pane now shows the
  received source's provenance, freshness and declarations without admitting it
  to the calculation, moves attempt and retry next to the fund name and adds cell
  tooltips.
- Decision, user-approved: Portfolio Performance stores no fund classification
  (`online.SecurityType` exists only for search results and is not persisted, the
  legacy `Security.getType()` holds asset classes and is package-private). The
  provider decides instead of a name heuristic: PP commit `4db5adfbe` asks an
  instrument once per session and remembers a provider answer without a usable
  composition as `Disposition.NO_COMPOSITION`. Such an instrument is skipped for
  the rest of the session without a retry promise and never delays other funds. A
  restart clears the memory. `docs/portfolio-lens.md` states the rule.
- Verification: `CompositionRefreshCoordinatorTest` 18 tests green; the UI
  look-through suite 54 tests green with 0 Checkstyle violations.
- Still open: the interactive 5.2/5.4 check with a rebuilt app, and the actual
  provider decomposition of a fund (task 1.3 evidence gate).

## 2026-10-25: whole-portfolio scope and unverified display

The first integrated build showed a 100 percent unresolved view. Two causes were
corrected together; the strict path and the task 1.3 evidence gate are unchanged.

- Scope: `HeldSecurities` returns every security with a nonzero net position
  across all client portfolios, netting purchases and sales and ignoring
  transactions after the valuation date. `PortfolioLensCompositionService` uses
  it instead of `SelectionService`, so no prior selection is needed. An empty
  portfolio shows an explicit empty state instead of zero categories.
- Unverified display: `CompositionValidator.validateArithmetic` accepts
  nonnegative weights up to 100 percent without allocation semantics.
  `CompositionRefreshCoordinator` keeps such a source separately from validated
  data, never enriches or persists it, and does not set a retry backoff.
  `LookThroughEngine` expands it exactly one level into
  `Category.UNVERIFIED_HOLDING` rows; company aggregation and nested traversal
  are not used for it. Shortfalls stay unresolved and arithmetic-invalid
  sources leave the whole fund unresolved.
- Fund identity: `InstrumentEvidence.fundFromComposition` records the provider's
  own holdings answer as the fund classification. A composition is therefore
  sufficient evidence that the instrument is a fund; it says nothing about the
  allocation semantics.
- Presentation: the unverified category lists each position with fund path,
  note, value and share; the view shows a partial-coverage notice. Direct
  unresolved holdings are listed per instrument with a reason instead of only
  as an anonymous aggregate. Coverage stays partial.
- Documentation and labels: `docs/portfolio-lens.md` describes the whole-
  portfolio scope, the unverified category and the remaining limits. 13 new and
  4 changed labels were added in all 18 locale files and normalized with
  `portfolio-build-tools/sort-messages.sh`; the files stay pure ASCII with
  unicode escapes.

PP commit: `8898760a1` (`feat: show unverified fund positions`). Nothing was
pushed.

Verification:

- Focused core: `LookThroughEngineTest` 16, `CompositionValidatorTest` 16,
  `CompositionRefreshCoordinatorTest` 19, `HeldSecuritiesTest` 4; all green.
  Two pre-existing tests that expected unverified semantics to trigger a retry
  backoff were updated to the new display semantics.
- `scripts/dev.sh test`: 5,037 tests, zero failures/errors, one skipped;
  Checkstyle passed with zero violations.
- Focused UI reactor with REST and bootstrap bundles: 57 tests, zero
  failures/errors; Checkstyle passed. New coverage includes the unverified
  category and empty state in the presenter, and the coordinator retaining an
  unverified source for display.
- `git diff --check` passed before the commit. The diff contains no real
  identifiers, amounts or credentials.
- `scripts/dev.sh app`: BUILD SUCCESS against `8898760a1` (clean), macOS ARM64
  app with bundled runtime, build time 5:49. The manifest records the revision,
  source fingerprint and artifact digest; the packaged core jar contains
  `HeldSecurities` and the updated engine. Tests are not part of packaging; the
  results above come from separate runs.
- Task 7.4 (isolated-app confirmation) remains open; the app is launched for
  the user's check.

The provider evidence record is extended in `provider-gates.md`: 1266 rows
summing to 100 percent, `assetType` null throughout, 15 rows without identifier,
no holdings-effective date, and a row-value/AUM mismatch. A validated
decomposition is still not achieved.

## 2026-10-25: issuer x-ray via provider classification

The user requires a complete, functional x-ray, not an unresolved placeholder.
The provider does classify individual instruments, so the x-ray is built from
real provider data rather than a name heuristic.

- `InstrumentClassifier` and its Eulerpool implementation classify an instrument
  through `/equity/search` (stocks, ETFs, funds) with a `/bonds/list` fallback.
  A stock becomes a grouped equity keyed by its ISIN, an ETF or fund becomes
  traversable, a bond becomes other assets. Transport errors and unknown
  instruments leave the position unresolved.
- The coordinator now enriches the constituents of arithmetic-usable
  compositions as well as verified ones, and `LookThroughEngine` expands them
  into their classified children. Synthetic and derivative exposure stays
  unresolved. The terminal unverified-positions category is superseded by the
  issuer breakdown.
- `PortfolioLensSession` classifies the held instruments themselves and caches
  one answer per identifier for the whole session, shared across overlapping
  funds. The analysis resolves owned securities and constituents from this
  evidence and from the coordinator's resolutions.
- The presenter labels each company/instrument row with the provider-supplied
  issuer name and shows a weights-not-validated notice; coverage stays partial.
- `docs/portfolio-lens.md`, the capability specs, the provider evidence record
  and the design record the issuer-level x-ray, its share-class grouping limit
  and the unvalidated weights.

PP commit: `9588cc3ba` (`feat: classify fund constituents into issuers`).
Nothing was pushed.

Verification:

- Focused core: engine 16, validator 16, coordinator 19, provider 21; all green.
- `scripts/dev.sh test`: 5,037 tests, zero failures/errors, one skipped;
  Checkstyle zero violations.
- Focused UI reactor with REST and bootstrap bundles: 57 tests, zero
  failures/errors; Checkstyle passed.
- `git diff --check` passed; the diff contains no real identifiers or
  credentials.
- The isolated app is rebuilt and launched next for the user's check of
  task 8.3 (and the earlier 5.2/7.4 confirmations).

Remaining: a per-constituent request is issued serially, so the first x-ray of
a broad fund can take a few minutes; classification results appear progressively
and are cached for the session. The provider still reports no denominator,
completeness or holdings date, so task 1.3 stays open and coverage stays partial.

## 2026-10-25: completeness fix and loading feedback

The user reported that Apple appeared only from the MSCI World fund, although it
is also a NASDAQ 100 constituent. The NASDAQ 100 holdings were fetched but the
whole fund was rejected: its published weights sum to 100.00000001% because of
decimal rounding, and the exact overfull check made the snapshot unusable.

- `CompositionValidator` accepts at most one millionth above 100% as a
  published-weight rounding artefact, keeps every row unchanged and clamps the
  shortfall at zero. Larger overfull totals remain unusable. Evidence: a public
  UCITS fund returned 100.00000001%. This is a spec revision, recorded in the
  fund-compositions spec and the design.
- The provider reuses one HTTP client with a pooled connection manager instead of
  creating a client per request, so keep-alive and TLS session reuse speed up the
  per-constituent classification.
- The view shows a loading line while a refresh is running, with the number of
  funds completed. Without it a long classification pass looked stuck. The label
  is translated into all supported languages.

PP commit: `4b9cf7336` (`fix: accept rounding and show load progress`).

Verification: validator 17 tests, engine 16, coordinator 19, provider 21, held 4;
UI look-through suite 57 tests. Checkstyle zero violations.

Open: the Eulerpool preference page is functional but not structured like the
other API-key pages (task 8.5, low priority). The user confirms the full x-ray in
the isolated app (task 8.6).

## 2026-10-25: reconcile the accepted rounding excess

The first live pass with the rounding tolerance showed the x-ray and an
Internal Error (`IllegalArgumentException` in `LookThroughResult`). The accepted
overfull weights expanded to a hair more value than the fund position, so the
exact reconciliation failed on every recalculation.

`CompositionValidator` now removes the accepted excess proportionally (at most
one millionth) and puts the exact residual on the largest row, so the validated
weights sum to exactly one. Source rows stay unchanged, the shortfall is zero and
the decomposition reconciles with the fund value. Genuine overfull data is still
rejected and never rescaled.

PP commit: `27439e406` (`fix: reconcile accepted rounding excess`).
Verification: validator 17, engine 17, UI 57; Checkstyle zero violations.
The spec and design record the proportional correction instead of "no scaling".

## 2026-10-25: live acceptance of the issuer x-ray

The user ran the isolated app with their own key. The view showed the complete
portfolio and an issuer-level breakdown: Apple with a direct holding and
contributions from both the MSCI World and the NASDAQ 100 fund, plus the other
issuers. The accepted-rounding fix removed the repeated `IllegalArgumentException`;
the log shows no exception after the restart. The loading line showed the fund
count and disappeared quickly on the cached second pass, which is expected.

The user accepted the current state ("looks better now"). They did not perform an
exact numeric spot-check of one issuer total; the direct-plus-two-fund
aggregation is covered by the synthetic presenter test, and the decomposition
reconciles exactly to the portfolio value.

Task 8.6 is complete. Task 5.2 remains open only for the explicit cancel-refresh
check and task 5.4 for the re-read of the documented workflows; the core view,
loading feedback and the absence of an upload or mapping step were observed live.

## 2026-10-25: unresolved reasons, identity safety and bounded concurrency

The user's latest feedback was that "unresolved" looked like a defect, especially
when the category contained held ETFs. Review found distinct issues:

- The presenter ignored the contribution's decomposition failure reason and
  showed classification wording even for a known fund without a composition.
  It now distinguishes missing/unusable compositions, weight shortfalls and
  stopped traversal from missing identity/classification. Reasons are visible
  in a Note column; the category is labelled "Not yet decomposed".
- An interrupted earlier change treated all identifierless rows as other assets.
  That change was removed: absent identifiers do not establish cash or collateral.
- A single nonmatching search hit was previously accepted. Classification now
  requires an exact primary identifier, with an exact-ISIN equity-profile
  fallback. Similar tickers with a different ISIN do not establish equivalence.
- Provider evidence no longer asserts unverified aliases copied from a source
  row. It carries the matched primary identifier only. This prevents the same
  ISIN with different fund-specific ticker suffixes from producing conflicting
  alias evidence. The session classification cache is account/ISIN scoped.
- Constituent classification uses a separate eight-thread daemon pool. The
  coordinator admits distinct lookups in source order, preserves duplicate
  source occurrences, enforces its cap and shared budget, and discards late
  snapshot updates after cancellation. Queued work rechecks suspension/backoff.
  The wait checks cancellation without waiting for a blocked transport to finish.
- Classification transport failures remain uncached and carry sanitized auth,
  entitlement and Retry-After status. Eulerpool reserves at most three request
  units per classification, including bounded fallback requests; held-instrument
  classifications now also require budget admission. Reserved unused units are
  not refunded. No cold-start speed measurement is claimed yet.
- The preference page has a key link, clearer structure and masked active-key
  placeholder without retrieving a secret into the field. The navigation entry
  follows sibling report entries without its own icon. The status column is
  labelled Instrument rather than Fund.

The previous Go concurrency delegation exhausted its allowance before producing
working code. The user authorized ChatGPT-backed continuation, with economical
usage. Two bounded delegations use medium effort for concurrency and low effort
for translation. The orchestrator reviews and corrects their actual diffs and
runs all builds centrally. No paid API fallback or provider contact is used.

Verification in progress:

- Initial complete core run: 5050 tests, zero failures/errors, one skipped,
  Checkstyle zero violations.
- Follow-up core run after duplicate/cancellation/backoff fixes: 5052 tests,
  zero failures/errors, one skipped, Checkstyle zero violations.
- Final reviewed core, UI reactor, translation checks and packaging are recorded
  below when complete. Prior results do not establish those pending checks.

The official issuer downloads were re-fetched and compared independently;
provider-gates.md records the current dated results and corrects the stale
NASDAQ date in the earlier delegated report. This remains plausibility evidence,
not validated economic exposure. Task 1.3 and the publication permission gate
remain open. Task 6.4 is complete with explicit G1-G7 follow-up records in
coverage-follow-ups.md. Task 7.4's whole-portfolio/partial-display acceptance is
covered by the previously recorded task 8.6 live check; cancel/workflow acceptance
remains separate and open. No private scratch data is deleted by this milestone.

Reviewed verification:

- Complete core run after identity-safety fixes: 5053 tests, zero failures/errors,
  one skipped; Checkstyle zero violations.
- Coordinator regression rerun after strengthening the queued-auth and overlap
  assertions: 23 tests, zero failures/errors; Checkstyle passed.
- Focused UI reactor: 65 tests, zero failures/errors; Checkstyle passed. An initial
  run found missing policy setup in three newly added test fixtures, corrected
  before the successful rerun. It was not a production storage defect.
- Strict OpenSpec validation passed after splitting an overlong numerical rule
  into requirement/scenarios without changing the numerical contract.
- Native macOS UI automation is not enabled. No system permissions were changed;
  the interactive app acceptance remains pending rather than being inferred from
  the headless tests.
- Translation completion/resource validation and final app packaging are still
  pending. No updated app build or measured cold-start speed is claimed yet.

The user authorized pushing changes on 2026-10-25. Workspace planning/progress may
be pushed after privacy review. PP adapter publication still requires the recorded
provider gates; push authorization does not establish licensing rights. The user
also asked whether the translation agent was stuck. A targeted progress request
was sent to the same low-effort session; no completion report has arrived yet.

Workspace review milestone `819f92f` was pushed to
`origin/feature/automatic-portfolio-xray-cache-policy` under the user's new
authorization. The complete outgoing workspace range was checked against locally
retained credentials/private configuration, with no matches and no tracked
scratch files. No PP branch was pushed: its provider-publication gates remain
unpassed, and the current code milestone is still awaiting translations and
packaging. The translation session has not supplied a usable handoff; no crash
or active progress can be established from the available status tools. Avoid
parallel edits to its resource files until the session is stopped or completes.

## 2026-10-25: source-fork exception and complete issuer-data comparison

The user confirmed the proposed publication scope: experimental source-only
development-fork pushes are allowed with a clear notice, despite unverified
provider rights. This does not establish rights or transfer legal responsibility.
Official upstream integration and public binary releases still require their
separate review; persistence stays disabled. Proposal/design/spec/tasks,
provider-gates.md and AGENTS.md now distinguish these scopes.

PP commit `5153f7fca` adds the prominent experimental notice to README.md and was
pushed to `origin/feature/automatic-portfolio-xray`. This publishes the previously
accepted `27439e406` source baseline plus the notice, not the current uncommitted
review fixes. Those remain local pending translation handoff/resource validation
and packaging. The complete outgoing source range was privacy-reviewed against
retained credentials/private configuration and checked for scratch, OpenSpec,
generated build and `.project` artifacts. None was included. New local Java
language-server `.project` changes were excluded and not discarded. No upstream
PR, public binary release or provider contact was performed.

The user assigned independent data verification to the agent rather than asking
the user to validate weights. The issuer's actual product page/client request
contract was inspected. Unlike the simple CSV, its public dated holdings JSON
includes constituent ISINs, classifications, raw weights, market and notional
values. At issuer effective date 22 Oct 2026:

- World: all 1251 identified provider rows match unique issuer ISINs, and every
  paired weight agrees within combined raw rounding tolerance; maximum difference
  is 0.000005 percentage points. These are all 1250 equities plus a money-market
  holding.
- NASDAQ: all 101 identified rows match; every weight agrees within tolerance;
  maximum difference is 0.00000495 percentage points.
- No duplicate ISIN groups occur. The remaining 15/five provider rows have exact
  cash/collateral name candidates, not new verified identifier assertions.
- Four World futures and one NASDAQ future with zero market value but positive
  notional are omitted from the provider answer. An extra World zero-balance cash
  row explains the remaining row-count difference. Missing economic overlay is
  now a concrete diagnosed gap, not a speculative objection.
- Both issuer pages explicitly describe Physical structure. They distinguish
  fund/share-class net assets; current facts and historical holdings dates are not
  conflated. Dated keyFundFacts requests are unsupported (HTTP 400). A common
  market-value scale factor and the profile's GBP currency expose why the former
  naive AUM comparison was not valid evidence against the weights.

Workspace tooling milestone `500f6c8` adds the offline comparison utility,
synthetic tests and reproduction documentation. All 48 tooling tests passed in
Docker, including nine new comparison regressions; the nine were rerun after
review. A separate offline actual-data acceptance run asserts all 1352 identified
rows match within rounding and detects the omitted notional exposures. Full
payloads/reports remain in ignored scratch; none is a distributed fixture.
Strict OpenSpec validation and diff whitespace checks pass.

This materially advances task 1.3. Applying the issuer evidence in the app,
handling economic overlays and company grouping beyond ISIN remain unfinished;
the historical weight check is not falsely described as integrated full economic
coverage. The new evidence and concrete next gaps are recorded in provider-gates.md
and coverage-follow-ups.md. No new model delegation was used for this verification.

## 2026-10-25: translation handoff, settings polish and local review fixes

The translation subagent stopped responding twice and was cancelled by the user
after the TUI interrupt binding (`ctrl+d` in the composer's subagent list) was
explained. Its session produced no usable file changes, so the orchestrator
performed the translations directly in one pass over all 19 bundles.

- Six changed and two added labels are present in every locale:
  `LookThroughCategoryUnresolved` ("Not yet decomposed"), the four new
  decomposition reasons (missing composition, unusable composition, weight
  shortfall, stopped traversal), `LookThroughStatusColumnFund` ("Instrument"),
  `PrefEulerpoolAPIKeyLink` and `PrefEulerpoolKeyNotDisplayed`. The English
  `PrefEulerpoolDescription` again states that existing keys are never displayed,
  matching the actual page behaviour.
- Files were normalized with the repository's own
  `portfolio-build-tools` writer, so they stay pure ASCII with `\uXXXX` escapes,
  canonical spacing and sorted keys.
- A Docker resource check asserts ASCII encoding, absence of duplicate keys,
  presence and non-emptiness of every required key in all 19 files, and matching
  `Messages.java` fields. It reports `Validated 19 bundles`.
- Java language server artifacts are not part of this work. The generated
  `filteredResources` blocks in every tracked `.project` file were restored with
  `git restore`; a follow-up `git status` shows no modified `.project` file.

The Eulerpool preference page now offers a key link, a masked active-key
placeholder that never loads the stored secret, and a status hint only while a
key is active. Task 8.5 is complete. The navigation entry uses the same
icon-free presentation as its sibling report entries, and the data-status column
is labelled Instrument instead of Fund.

Local review corrections in this pass: provider classification evidence carries
only the matched primary identifier so two funds reporting the same ISIN with
different ticker suffixes no longer produce conflicting alias assertions; the
search path requires an exact primary identifier and never substitutes a
different ISIN; the equity-profile fallback requires the returned ISIN to match;
sanitized authentication/entitlement/rate-limit results stop the request chain;
session classification is keyed per account and ISIN; and reserved enrichment
permits are rechecked against suspension before a queued request executes.

Final verification for this milestone (all after the last code change):

- Core suite in Docker: 5053 tests, zero failures/errors, one skipped;
  Checkstyle zero violations.
- Focused UI reactor with REST and bootstrap bundles: 65 tests, zero
  failures/errors; Checkstyle zero violations.
- `scripts/dev.sh app`: BUILD SUCCESS in 3:26, macOS ARM64 app with bundled
  runtime. The manifest records revision `5153f7fca`, dirty state, source
  fingerprint and artifact digest. Packaging skips tests; the counts above come
  from separate runs. The artifact was built before the commit that carries the
  same working-tree content, so the recorded dirty state is expected.
- Resource validation over 19 bundles plus `Messages.java` passed; the files were
  normalized by `portfolio-build-tools`. `Messages.java` field order now mirrors
  the sorted properties.
- No modified `.project` file remained before the commit or after the build.
- Privacy review of the complete diff found no retained credential, private
  configuration value, scratch payload, portfolio data or provider fixture.

PP commit `7ad3b999b` (`fix: harden issuer classification and progress`) and the
earlier `5153f7fca` notice are pushed to the development fork only. No upstream
PR, binary release or provider contact was performed.

Remaining open work, deliberately not marked complete:

- Task 1.3: the historical weight and classification evidence is corroborated,
  but the app does not apply issuer evidence and economic overlays are missing.
- Task 5.2: the isolated app check for cancel/refresh behaviour is still pending.
  Native UI automation is unavailable on this machine, so this was not inferred
  from headless tests.
- Task 5.4: documentation is updated, but the manual workflow re-check is pending.
- Task 6.2: the synthetic end-to-end matrix in a managed launch is pending.
- Task 6.3: permissions and the publication checklist remain unverified; only the
  explicitly authorized experimental source fork exception applies.
- Task 6.5: publication preparation is done for this increment, but no official
  upstream publishing is authorized or ready.
