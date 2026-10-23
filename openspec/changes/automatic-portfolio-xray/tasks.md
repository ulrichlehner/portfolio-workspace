# Tasks

Planning only. All boxes describe future work after a separate apply request. The local testing work in section 0 and sections 2 and 3 can proceed independently of provider permission using synthetic fixtures. Task 1.2 gates persistent provider storage and provider release; task 1.3 gates treating tested funds as validated exposure. If either gate fails, stop the affected work and revise planning. Do not silently substitute a paid plan or another provider.

## 0. Local macOS testing foundation

- [ ] 0.1 Create a workspace tooling branch following the generic branch convention and keep PP implementation on feature/automatic-portfolio-xray (or focused scope-suffixed branches) from upstream/master; verify repository, base and branch before editing. Record that workspace tooling never goes into upstream PP.
- [ ] 0.2 Extend macOS build metadata and architecture selection in scripts/dev.sh; verify the Docker-built app includes its runtime, identifies revision plus source-content fingerprint, and rejects missing, mismatched or stale artifacts. Add script tests in the container and document rebuild/launch commands.
- [ ] 0.3 Implement private WebDAV setup and a GET/HEAD-only downloader with verified HTTPS, no redirects and a read-only credential; test against a synthetic mock server in Docker, asserting no mutating requests, no credentials in output and safe rejection of auth/TLS/redirect failures. Document local configuration without real URLs or credentials.
- [ ] 0.4 Implement untouched baseline, staging validation, atomic generation activation and previous-copy preservation under scratch/pp-dev-data; test changed/unchanged remote files, locally edited copies, interrupted downloads, error bodies, XML/ZIP/encrypted containers, unsafe links and paths. Verify ordinary clean preserves generations and explicit private-data cleanup removes only managed data; document retention and keep/recovery options.
- [ ] 0.5 Implement managed launch locking and correct local-file opening in the separate development process; verify on macOS that concurrent launch/refresh is rejected, stale locks recover safely, saves/backups remain local and production recent files/settings are not restored. Verify explicit offline launch reports stale data and default launch aborts on failed refresh.
- [ ] 0.6 After synthetic isolation checks pass, configure the real server privately with its file URL, read-only authentication and format; launch a local build against the downloaded copy, test local save/reopen and next-launch refresh, and verify the server file remains unchanged using read-only evidence. Keep contents and identifiers out of reports, and remove private test data explicitly when testing is finished.

## 1. Repository and provider gates

- [ ] 1.1 Recheck workspace and upstream AGENTS.md, CLAUDE.md, CONTRIBUTING.md, applicable path rules and target bundle formatting settings; record an implementation checklist confirming Docker-only builds, no unrelated formatting, core/UI boundaries and focused upstream increments.
- [ ] 1.2 Resolve Eulerpool free personal display, local caching/retention and user-key adapter distribution permissions using authoritative published terms or an explicitly authorized provider response; record source, date, allowed retention and a pass/fail decision. Do not implement persistent provider storage until passed; provider contact needs separate explicit authorization.
- [ ] 1.3 Establish Eulerpool NAV denominator, completeness and exposure-basis evidence for at least one independent public physical-fund example; document issuer comparison, classification and company-mapping evidence and remaining gaps. Verify a useful validated decomposition, not merely endpoint success or a 100% sum; keep unsupported funds unresolved.

## 2. Composition foundations

- [ ] 2.1 Add lightweight composition/provenance/result models and a dedicated provider contract in the core bundle using existing online discovery conventions; verify provider substitution with two offline test providers and confirm constituents do not become owned securities. Document result states beside the contract.
- [ ] 2.2 Implement decimal validation, unknown-denominator rejection, explicit shortfalls, duplicate-row handling and first-version signed/overfull rejection; add synthetic tests for missing/nonfinite weights, tiny residuals, valid duplicates and normalized top-only data, and run them through scripts/dev.sh test.
- [ ] 2.3 Add evidence-backed instrument classification and separate company grouping, with bounded resolution outcomes; verify ambiguous names, share classes, depositary receipts, missing identifiers and unknown asset types through offline core tests. Document the distinction between ungrouped and unresolved.

## 3. Exposure engine

- [ ] 3.1 Integrate current ClientSnapshot valuations and reporting-currency conversion with the selected positive-securities denominator; test account cash exclusion, zero/negative positions, empty selection and missing valuations/conversion using synthetic inputs through scripts/dev.sh test.
- [ ] 3.2 Implement direct/indirect aggregation and inspectable contribution paths; test direct-plus-multiple-fund overlap, duplicate legitimate paths and no parent double counting. Verify the four coverage categories reconcile to selected value before display rounding.
- [ ] 3.3 Implement partial-composition residuals and unsupported-fund states; test missing funds, unknown denominator, unknown classification, ungrouped equity and unsupported synthetic exposure. Verify the specification's 80% resolved / 20% unresolved example exactly.
- [ ] 3.4 Implement nested traversal with path-specific cycle detection and an eight-edge limit; test boundary depth, cycles and repeated funds on independent paths. Verify only affected branches become unresolved and document the limit.

## 4. Eulerpool and automatic retrieval

- [ ] 4.1 Implement the Eulerpool adapter with injectable transport, identifier lookup, Bearer authentication and explicit provenance mapping; verify sanitized synthetic response fixtures for success, empty response, nullable fields and malformed data. Do not commit private or unlicensed payloads; usable-exposure claims depend on 1.3.
- [ ] 4.2 Implement provider-wide request budgeting, bounded enrichment, coalescing, rolling 24-hour automatic refresh and quota-aware manual refresh; verify with a fake clock/transport that redraws cause no requests, Retry-After is honoured and authentication/entitlement errors suspend retries until configuration changes. Document refresh semantics.
- [ ] 4.3 After 1.2 passes, implement the separate versioned local cache with atomic replacement, approved retention, validation-version checks and last-valid fallback; test refresh failures, expired retention, corruption and incompatible versions without modifying portfolio files.
- [ ] 4.4 Verify secure-storage availability in the target platform and implement secure credentials or session-only fallback; test redaction, key replacement/removal and request contents. Confirm no key enters URLs, portable settings, logs or exports; document individual setup and deletion.

## 5. Reporting UI

- [ ] 5.1 Add the Portfolio Lens view under the existing PP namespace using the lookthrough internal domain term with company/direct/indirect/total columns, source expansion and clearly labelled denominator; verify a synthetic portfolio shows overlaps, cash/other, ungrouped and unresolved categories and never labels rounded residuals complete. Follow existing view and image-registration conventions; verify the feature name is externalized and existing application/bundle identifiers are unchanged.
- [ ] 5.2 Connect cancellable background jobs and data-status UI for provenance, missing dates, stale data, excluded positions and provider failures; verify responsive refresh/cancel behaviour, no requests on redraw and no required upload or mapping flow in an isolated app.
- [ ] 5.3 Externalize and translate new UI labels according to CONTRIBUTING.md, including setup, limitations and missing-date states; verify resource keys and translations and build changed UI bundles in Docker via scripts/dev.sh app. Check any icons against CC0, iconmonstr, SVG sizing and Images registration rules.
- [ ] 5.4 Document the current-value scope, credential setup, refresh behaviour, partial coverage and local data removal in the repository's applicable user documentation; verify each described workflow against the isolated app and preserve the full-coverage objective in the wording.

## 6. Integration and release review

- [ ] 6.1 Run scripts/dev.sh test for core tests and Checkstyle and scripts/dev.sh app for integrated UI compilation; record results and review changed code against bundle formatting/contribution rules. Do not require live credentials in ordinary tests.
- [ ] 6.2 Use scripts/dev.sh run-app with a synthetic portfolio to verify mixed coverage, offline fallback within permitted retention, quota/auth failures, cache reset, feature disablement and reopening with a build without X-ray; confirm portfolio transactions, securities and format remain intact, then quit and run scripts/dev.sh clean.
- [ ] 6.3 Recheck the public physical-fund acceptance evidence and provider permission gates before release; produce a pass/fail acceptance record distinguishing validated coverage from data freshness. Private portfolio checks, if performed within existing authorization, remain local and never become public fixtures or artifacts.
- [ ] 6.4 Review gaps G1-G6 in design.md and any newly discovered gaps; deliver linked follow-up backlog records for unresolved items with evidence, remedy and closure criteria. Verify the durable-spec synchronization will retain the 100% objective and that partial delivery is not described as objective completion.
- [ ] 6.5 Review the complete diff for secrets and real portfolio data and prepare focused upstream increments from upstream/master under workspace contribution rules; verify specs remain outside portfolio/, each increment includes its tests, and required checks pass before any separately authorized publishing. Create focused Conventional Commits for completed workspace tooling and upstream increments after checks and privacy review; record commit references. Push and open PRs when authorized, recording any outstanding publishing steps.

## Workflow follow-up

- After implementation and review, use the archive workflow to synchronize the capability deltas into durable specs and archive this change.
- Verify the durable coverage objective and linked unresolved-gap records survive archive; archive of a partial release does not mean 100% coverage has been achieved.
