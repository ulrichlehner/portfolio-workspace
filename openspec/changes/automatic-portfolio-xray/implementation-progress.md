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
