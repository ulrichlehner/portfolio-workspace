# Tasks

Unchecked boxes describe work remaining after the completed milestones. Task 1.2 records the confirmed development-only permission assumption; implementation and local development can proceed. Actual permission verification is required by the task 6.3 pre-publish checklist. Real provider data stays session-only until persistence permission and retention are verified. Task 1.3 gates validated exposure claims. Stop only the affected work when a gate fails. Do not silently substitute a paid plan or another provider.

## 0. Local macOS testing foundation

- [x] 0.1 Create a workspace tooling branch following the generic branch convention and keep PP implementation on feature/automatic-portfolio-xray (or focused scope-suffixed branches) from upstream/master; verify repository, base and branch before editing. Record that workspace tooling never goes into upstream PP.
- [x] 0.2 Extend macOS build metadata and architecture selection in scripts/dev.sh; verify the Docker-built app includes its runtime, identifies revision plus source-content fingerprint, and rejects missing, mismatched or stale artifacts. Add script tests in the container and document rebuild/launch commands.
- [x] 0.3 Implement private WebDAV setup and a GET/HEAD-only downloader with verified HTTPS, no redirects and a read-only credential; test against a synthetic mock server in Docker, asserting no mutating requests, no credentials in output and safe rejection of auth/TLS/redirect failures. Document local configuration without real URLs or credentials.
- [x] 0.4 Implement untouched baseline, staging validation, atomic generation activation and previous-copy preservation under scratch/pp-dev-data; test changed/unchanged remote files, locally edited copies, interrupted downloads, error bodies, XML/ZIP/encrypted containers, unsafe links and paths. Verify ordinary clean preserves generations and explicit private-data cleanup removes only managed data; document retention and keep/recovery options.
- [x] 0.5 Implement managed launch locking and correct local-file opening in the separate development process; verify on macOS that concurrent launch/refresh is rejected, stale locks recover safely, saves/backups remain local and production recent files/settings are not restored. Verify explicit offline launch reports stale data and default launch aborts on failed refresh.
- [x] 0.6 After synthetic isolation checks pass, configure the real server privately with its file URL, read-only authentication and format; launch a local build against the downloaded copy, test local save/reopen and next-launch refresh, and verify that this workflow performs no remote writes using read-only evidence. Periodic external source saves are expected; a coherent local snapshot is sufficient and byte equality between separate remote downloads is not required. Keep contents and identifiers out of reports, and remove private test data explicitly when testing is finished.

## 1. Repository and provider gates

- [x] 1.1 Recheck workspace and upstream AGENTS.md, CLAUDE.md, CONTRIBUTING.md, applicable path rules and target bundle formatting settings; record an implementation checklist confirming Docker-only builds, no unrelated formatting, core/UI boundaries and focused upstream increments.
- [x] 1.2 Record the user-confirmed development-only assumption of Eulerpool runtime/display and user-key adapter distribution permission, without claiming verified rights. Move actual verification to the task 6.3 pre-publish checklist. Keep real-data disk persistence disabled until permission and retention are verified; local development uses session-only data. Provider contact needs separate explicit authorization.
- [ ] 1.3 Establish Eulerpool NAV denominator, completeness and exposure-basis evidence for at least one independent public physical-fund example; document issuer comparison, classification and company-mapping evidence and remaining gaps. Verify a useful validated decomposition, not merely endpoint success or a 100% sum; keep unsupported funds unvalidated. Recorded on 2026-10-25: a public UCITS fund returned 1266 rows summing to 100%, `assetType` was null on every row, 15 rows had no identifier, and the row `value` sum differed from the reported fund AUM. The provider exposes no holdings-effective date and no per-constituent classification. A validated decomposition therefore remains unachieved; arithmetic-usable provider weights are displayed only as unverified positions (task 7.2), never as validated coverage.

## 2. Composition foundations

- [x] 2.1 Add lightweight composition/provenance/result models and a dedicated provider contract with per-provider/account persistence policy and retention using existing online discovery conventions. Verify substitution with two offline providers, independent policies and no creation of owned constituent securities. Document result and policy states beside the contract.
- [x] 2.2 Implement decimal validation, unknown-denominator rejection, explicit shortfalls, duplicate-row handling and first-version signed/overfull rejection; add synthetic tests for missing/nonfinite weights, tiny residuals, valid duplicates and normalized top-only data, and run them through scripts/dev.sh test.
- [x] 2.3 Add evidence-backed instrument classification and separate company grouping, with bounded resolution outcomes; verify ambiguous names, share classes, depositary receipts, missing identifiers and unknown asset types through offline core tests. Document the distinction between ungrouped and unresolved.

## 3. Exposure engine

- [x] 3.1 Integrate current ClientSnapshot valuations and reporting-currency conversion with the selected positive-securities denominator; test account cash exclusion, zero/negative positions, empty selection and missing valuations/conversion using synthetic inputs through scripts/dev.sh test.
- [x] 3.2 Implement direct/indirect aggregation and inspectable contribution paths; test direct-plus-multiple-fund overlap, duplicate legitimate paths and no parent double counting. Verify the four coverage categories reconcile to selected value before display rounding.
- [x] 3.3 Implement partial-composition residuals and unsupported-fund states; test missing funds, unknown denominator, unknown classification, ungrouped equity and unsupported synthetic exposure. Verify the specification's 80% resolved / 20% unresolved example exactly.
- [x] 3.4 Implement nested traversal with path-specific cycle detection and an eight-edge limit; test boundary depth, cycles and repeated funds on independent paths. Verify only affected branches become unresolved and document the limit.

## 4. Eulerpool and automatic retrieval

- [x] 4.1 Implement the Eulerpool adapter with injectable transport, identifier lookup, Bearer authentication and explicit provenance mapping; verify sanitized synthetic response fixtures for success, empty response, nullable fields and malformed data. Do not commit private or unlicensed payloads; usable-exposure claims depend on 1.3.
- [x] 4.2 Implement provider-wide request budgeting, bounded enrichment, coalescing, rolling 24-hour automatic refresh and quota-aware manual refresh; verify with a fake clock/transport that redraws cause no requests, Retry-After is honoured and authentication/entitlement errors suspend retries until configuration changes. Document refresh semantics.
- [x] 4.3 Implement interchangeable session-only and versioned persistent composition stores with identical validation/calculation semantics. Gate real-data disk activation per provider/account on verified persistence permission and retention under 6.3, not the 1.2 development assumption; test both modes with synthetic providers. Cover atomic replacement, retention, last-valid fallback, corruption, restart/offline behaviour, provider isolation, policy withdrawal and pending writes after deletion without modifying portfolio files.
- [x] 4.4 Verify secure-storage availability in the target platform and implement secure credentials or session-only fallback; test redaction, key replacement/removal and request contents. Confirm no key enters URLs, portable settings, logs or exports; document individual setup and deletion.
- [x] 4.5 Add a local persistence opt-out per provider/account, defaulting on only where permitted; expose effective session-only/persistent mode and policy restrictions. Verify toggling without restart, immediate affected-cache deletion, pending-write invalidation, unchanged other-provider settings, and eligible repopulation only when preference and policy both allow it. Document preserved analysis and restart/offline limitations.

## 5. Reporting UI

- [x] 5.1 Add the Portfolio Lens view under the existing PP namespace using the lookthrough internal domain term with company/direct/indirect/total columns, source expansion and clearly labelled denominator; verify a synthetic portfolio shows overlaps, cash/other, ungrouped and unresolved categories and never labels rounded residuals complete. Follow existing view and image-registration conventions; verify the feature name is externalized and existing application/bundle identifiers are unchanged.
- [ ] 5.2 Connect cancellable background jobs and data-status UI for provenance, missing dates, stale data, storage mode/restart limitations, excluded positions, unverified provider positions and provider failures; verify responsive refresh/cancel behaviour, no requests on redraw and no required upload or mapping flow in an isolated app. The view must open on the complete portfolio without a prior selection and show an explicit empty state when there is no holding.
- [x] 5.3 Externalize and translate new UI labels according to CONTRIBUTING.md, including setup, limitations and missing-date states; verify resource keys and translations and build changed UI bundles in Docker via scripts/dev.sh app. Check any icons against CC0, iconmonstr, SVG sizing and Images registration rules.
- [ ] 5.4 Document current-value scope, credential setup, refresh, per-provider persistence opt-out/policy enforcement, session-only restart/offline limitations, partial coverage and local data removal; verify each workflow against the isolated app and preserve the full-coverage objective.

## 6. Integration and release review

- [x] 6.1 Run scripts/dev.sh test for core tests and Checkstyle and scripts/dev.sh app for integrated UI compilation; record results and review changed code against bundle formatting/contribution rules. Do not require live credentials in ordinary tests.
- [ ] 6.2 Use scripts/dev.sh run-app with synthetic portfolios/providers to verify mixed coverage, identical analysis in both stores, offline retained-data fallback, session-only restart/failed retrieval, per-provider opt-out and policy changes during refresh, quota/auth failures, cache reset, feature removal and reopening without X-ray. Confirm portfolio integrity, then quit and run scripts/dev.sh clean.
- [ ] 6.3 Complete the pre-publish checklist before publishing the adapter: verify Eulerpool runtime/personal display, user-key adapter source/binary distribution, applicable attribution and other obligations, and separately optional persistence/retention for the applicable plan using authoritative terms or an authorized provider response. Record source, date and pass/fail/unknown per permission; development assumptions do not pass this checklist. Keep real-data persistence disabled unless permitted with verified retention. Verify the task 1.3 public physical-fund acceptance evidence and produce a pass/fail acceptance record distinguishing validated coverage from freshness. Private portfolio checks remain local and never become public fixtures or artifacts. Provider contact requires separate explicit authorization.
- [x] 6.4 Review gaps G1-G6 in design.md and any newly discovered gaps; deliver linked follow-up backlog records for unresolved items with evidence, remedy and closure criteria. Verify the durable-spec synchronization will retain the 100% objective and that partial delivery is not described as objective completion.
- [ ] 6.5 Review the complete diff for secrets and real portfolio data and prepare focused upstream increments from upstream/master under workspace contribution rules; verify specs remain outside portfolio/, each increment includes its tests, and required checks pass before any separately authorized publishing. Create focused Conventional Commits for completed workspace tooling and upstream increments after checks and privacy review; record commit references. Push and open PRs when authorized, recording any outstanding publishing steps.

## 7. Whole-portfolio scope and unverified display revision

The user rejected the selection-based scope: Portfolio Lens is the x-ray of the
complete portfolio. The earlier design made the strict provider gate reject every
real fund, so the view showed no usable result. These tasks correct that while
keeping validated coverage separate.

- [x] 7.1 Replace the selection scope with every security that has a nonzero net position across the client's portfolios, without a prior selection; verify cross-portfolio netting, sold positions, future-dated transactions, client order and the empty-portfolio state.
- [x] 7.2 Add an arithmetic-only composition path that accepts nonnegative weights up to 100% without verified semantics, displays them as unverified provider positions with fund path, note and partial coverage, never aggregates them into company exposure and never traverses them recursively; verify shortfall, overfull, negative and missing weights with synthetic inputs.
- [x] 7.3 Update the user documentation, capability specs and task 1.3 record so a validated decomposition is not claimed and the unverified category is described as display-only; translate changed and new labels into all supported languages.
- [x] 7.4 Rebuild the isolated macOS app and have the user confirm that opening Portfolio Lens shows the complete portfolio with visible unverified fund positions and an explicit partial-coverage notice. Record the outcome; keep tasks 5.2 and 5.4 open until the interactive checks pass.

## 8. Issuer x-ray via provider classification

Section 8 supersedes the intermediate display-only category in tasks 7.2-7.4.
The whole-portfolio/partial-display acceptance of 7.4 was observed in the isolated
app and recorded with task 8.6 in implementation-progress.md. This closes neither
weight validation nor the separate cancel and workflow checks in 5.2/5.4.

The user requires a complete, functional x-ray. The provider does classify
individual instruments (`/equity/search` for stocks, ETFs and funds, and its
bond list for bonds), and the holdings list already carries each holding's
identifier, ticker and name. These are combined into an issuer-level x-ray.

- [x] 8.1 Add provider-backed instrument classification and use it to resolve held instruments and fund constituents to issuers, funds, bonds and other assets; cache one answer per identifier per session.
- [x] 8.2 Expand arithmetic-usable compositions into their classified constituents even when the allocation semantics are unvalidated; keep synthetic and derivative exposure unresolved, keep coverage partial and show an issuer-level company/instrument breakdown with a weights-not-validated notice.
- [x] 8.3 Accept a provider rounding excess of up to one millionth above 100%, proportionally correcting accepted weights to reconcile exactly while retaining unchanged source rows, with evidence from a public fund whose weights sum to 100.00000001%; keep larger overfull totals unusable.
- [x] 8.4 Show a loading line with completed fund count while a refresh or classification pass runs, and translate the label into all supported languages.
- [ ] 8.5 Align the Eulerpool preference page with the other API-key pages (masked key field, key link, simpler structure); low priority, no functional change.
- [x] 8.6 Update the documentation, capability specs and provider evidence record to describe the issuer-level x-ray, its share-class grouping limit and its unvalidated weights; rebuild the isolated app and have the user confirm the x-ray.

## Workflow follow-up

- After implementation and review, use the archive workflow to synchronize the capability deltas into durable specs and archive this change.
- Verify the durable coverage objective and linked unresolved-gap records survive archive; archive of a partial release does not mean 100% coverage has been achieved.
