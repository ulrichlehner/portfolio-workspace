# Design

## Context

Exploration record, last investigated 2026-10-23. See proposal.md for motivation and scope. This design completes planning and records explicit gates for dependent implementation and release. Eulerpool is selected as the initial provider. Transparent partial coverage is accepted for the first release, with 100% validated coverage retained as the ultimate objective. The current-value denominator and refresh defaults are accepted; licensing and data-validation gates remain unresolved.

Confirmed product direction: current exposure, automatic retrieval, no required manual uploads, preference for free or affordable individual subscriptions, and extensibility beyond the first provider.

Confirmed provider decision: proceed with Eulerpool first, based on working free-account access and the low-friction setup observed. Leeway remains a documented alternative; its activation process and unverified holdings access are not blockers for this change.

Observed PP integration points in the local checkout:

- `portfolio/name.abuchen.portfolio/src/name/abuchen/portfolio/snapshot/ClientSnapshot.java`: dated positions and valuations in the reporting currency.
- `portfolio/name.abuchen.portfolio/src/name/abuchen/portfolio/model/Classification.java`: weighted classification assignments, but not a dedicated dated fund-composition model.
- `portfolio/name.abuchen.portfolio/src/name/abuchen/portfolio/online/Factory.java`: ServiceLoader discovery of quote/dividend/search providers.
- `portfolio/name.abuchen.portfolio.ui/src/name/abuchen/portfolio/ui/views/taxonomy/TaxonomyModel.java`: weighted valuation and chart infrastructure worth reusing selectively.

## Goals / Non-Goals

**Goals:** Keep network/source handling separate from deterministic calculations; retain provenance and incomplete-data states; make one-time credential setup sufficient for routine use.

**Non-Goals:** Turning every constituent into an owned PP security; silently mapping uncertain names to companies; normalizing partial holdings to imply complete coverage; committing provider payloads or private portfolio examples.

## Decisions

### Feature name and package identity

The accepted user-facing name is **Portfolio Lens**, a feature within Portfolio Performance, not a separately branded application. Use `lookthrough` as the stable internal domain term under PP's existing namespaces: proposed core package `name.abuchen.portfolio.snapshot.lookthrough` and UI package `name.abuchen.portfolio.ui.views.lookthrough`, with provider implementations following the existing online package conventions. Confirm exact placement against surrounding code during implementation. Do not rename existing bundles, application identifiers, portfolio formats or the `automatic-portfolio-xray` OpenSpec change. Externalize the display name using PP's normal translation conventions. This decouples presentation wording from internal compatibility; it is a project naming decision, not a claim of trademark exclusivity.

### Accepted coverage objective and release boundary

The first release may display explicitly incomplete results. This is a delivery milestone, not a reduction of the ultimate 100% coverage objective. Complete coverage means all positions in the declared analysis scope are accounted for with validated economic exposure and identity/classification, including correctly represented cash and other non-equity assets. It does not mean forcing every position into an equity, normalizing known rows, or merely receiving weights that sum to 100%. Freshness remains a separately reported quality dimension.

The capability specs preserve this distinction for synchronization into durable specifications. Track each remaining gap by reason, affected instrument category, missing evidence, proposed remedy and verification criterion. Public records must use synthetic or independent public examples; private acceptance checks must not expose the user's portfolio. Provider expansion, identity resolution, composition validation and synthetic exposure are routes toward complete coverage, not reasons to silently exclude difficult instruments.

Before closing or archiving the first release, review the coverage gaps and explicitly carry unresolved work into durable specs and linked follow-up changes/backlog records. Do not mark the full-coverage objective achieved while unresolved exposure or unverified company grouping remains. Do not promise universal provider coverage that has not been demonstrated. No follow-up change is scaffolded during this planning step.

### Repository rules and enforcement

Read and apply the workspace `AGENTS.md`, then `portfolio/AGENTS.md`, `portfolio/CLAUDE.md` and `portfolio/CONTRIBUTING.md`, plus any more specific instructions in files being changed. The workspace rules take precedence where they conflict. Recheck these sources at implementation time rather than treating this research summary as a replacement for them.

Future implementation tasks must include explicit evidence for the relevant gates:

- Code review against the target bundles' Eclipse `.settings/`, surrounding Java conventions and OSGi/core/UI boundaries; no unrelated formatting changes. Keep format-on-save disabled under the workspace rule, despite upstream editor setup suggestions.
- Focused deterministic tests for exposure calculations, incomplete/invalid compositions, identifiers, dates, signed weights and provider failures. Place core tests in the existing core test bundle. Ordinary tests must not require API keys or live network access.
- Run `scripts/dev.sh test` for core tests and Checkstyle. The wrapper explicitly re-enables Checkstyle despite using the local-dev profile. This does not establish UI compilation or translation validation: include appropriate container builds/checks for changed UI bundles and externalized/translatable strings. Follow upstream UI test guidance; it does not require blanket UI test creation.
- Review labels, translations, existing image registration and any new icons against CONTRIBUTING.md. Verify UI behaviour with an isolated local build where needed, using a synthetic portfolio or a private copy.
- Apply the workspace contribution and privacy checks before commits/pushes; keep specs outside the fork, use focused upstream contributions and verify required checks before publishing. Clean generated build output when implementation verification finishes.

The existing PDF-extractor rule is path-scoped and is not applicable to the planned X-ray code. If later work touches an importer, its additional requirements become applicable. These are acceptance gates for future tasks, not checks claimed to have run during this documentation-only turn.

### Proposed architecture

```text
Provider adapters --> validated composition snapshots --> identity resolution
                                                            |
PP current valuations ------------------------------> look-through engine
                                                            |
                                               contributions and coverage UI
```

Use a dedicated composition-provider interface, following existing feed discovery conventions. Prefer an aggregated API initially to limit issuer-specific maintenance. Retain the option of automatic issuer adapters where API coverage fails; manual uploads are not the fallback workflow.

Store lightweight constituents separately from the user's owned securities. A snapshot needs provider/fund identity, available holdings-effective date, provider refresh time, retrieval time, exposure basis and completeness status. Unknown dates remain unknown. Local storage and retention are conditional on the selected provider's terms.

Compute indirect exposure by multiplying current position value by constituent weight. Preserve contribution paths and an explicit unresolved remainder. Distinguish instrument identity from company grouping, including share classes and depositary receipts. Do not merge by name alone. Nested compositions require cycle detection and bounded traversal; unsupported branches remain unresolved.

Eulerpool is the initial provider, not a permanent dependency of the calculation model. Prefer one validated source per fund snapshot rather than silently blending incompatible snapshots. Cache mappings and refresh results where licensed, retain last valid data on failures, show stale status, and never trigger a network refresh for every chart redraw. Credentials belong in local secure configuration, not portfolio exports or logs. No shared embedded API key or central portfolio upload is proposed.

### Provider comparison

Prices and entitlements are a dated research snapshot, not a purchase recommendation. All candidates need actual fund-level acceptance checks; price/ticker coverage does not establish composition coverage.

| Provider | Personal access and cost observed | Evidence and assessment |
| --- | --- | --- |
| Eulerpool | Advertises free non-commercial access with 100,000 requests/month | Selected initial provider. Authenticated free access tested; identity, exposure-basis, effective-date and caching gates remain. [Pricing](https://eulerpool.com/financial-data-api/pricing), [holdings API](https://eulerpool.com/developers/api/etf/holdings). |
| Leeway | Public pages advertise 50 free units/day; account UI instead offers 50 free test requests by email. Recurrence unconfirmed. Paid data API EUR 69.95/month billed annually, VAT included | Deferred alternative. Tests returned HTTP 429 with a zero limit. Fundamentals cost ten documented units per call; full constituents only for selected ETFs. [ETF API](https://leeway.tech/data-api/etfs), [fundamentals costs](https://leeway.tech/data-api/fundamentals). |
| EODHD | Fundamentals USD 59.99/month or USD 599.90/year; free plan excludes fundamentals | Paid fallback. Documents worldwide ETF data and a full Holdings field, but completeness is instrument-specific. No authenticated test performed. [Pricing](https://eodhd.com/pricing), [fundamentals](https://eodhd.com/financial-apis/stock-etfs-fundamental-data-feeds). |
| Financial Modeling Prep | Ultimate USD 99/month billed annually on the consulted personal pricing page | Global coverage and ETF/fund holdings listed in Ultimate. Relatively expensive for this scope; no authenticated UCITS test. [Pricing](https://site.financialmodelingprep.com/pricing-plans). |
| Alpha Vantage | General free allowance of 25 requests/day; endpoint entitlement needs checking | Documents ETF_PROFILE holdings, but required UCITS coverage is unverified. Secondary candidate, not a confirmed substitute. [API](https://www.alphavantage.co/documentation/), [limits](https://www.alphavantage.co/premium/). |
| Twelve Data | Individual plans exist; ETF metrics listed in Ultra, advertised from USD 329/month | Low priority due to cost and unverified full UCITS holdings coverage. Confirm exact composition endpoint entitlement before any evaluation purchase. [Pricing](https://twelvedata.com/pricing). |

### Eulerpool: measured evidence

Authenticated read-only requests succeeded on a free account. Evaluated fund responses were nonempty, contained substantially more than ten constituents for broad funds, and included numeric weights totaling approximately 100%. This demonstrates usable access, not proven completeness or coverage of all funds. Portfolio-derived identifiers and per-fund results are intentionally absent from this public record.

Observed limitations: assetType was null throughout the evaluated responses; some equities lacked ISINs; two ticker-based equity-profile enrichment attempts returned errors; duplicate identifiers and negative weights occurred. Such records need deliberate handling, not removal or naive deduplication.

A separate public DAX example returned identified equities and cash/collateral. Its largest weights agreed with the issuer's rounded download. The provider refresh was two days later than the issuer's effective holdings date. Zero-market-value derivative rows in the issuer export were absent from the API response. Consequently, NAV weights are not automatically a complete economic-exposure representation. [Public issuer export](https://www.ishares.com/de/privatanleger/de/produkte/251464/ishares-core-dax-ucits-etf-de/latest-holdings.csv).

Documentation also conflicts: the [marketing page](https://eulerpool.com/financial-data-api/etf-data) promises complete lists, while the endpoint describes top holdings. The [schema](https://api.eulerpool.com/api/1/documentation/yaml) documents nullable identifiers and a refresh timestamp, not a separate holdings-effective date. No explicit replication-method field was observed in tested profiles. The [licensing FAQ](https://eulerpool.com/financial-data-api/licensing) discusses free personal use but explicitly grants caching on paid plans; free desktop caching needs clarification.

### Leeway: free-tier feasibility

Leeway documents ISIN lookup followed by a symbol/exchange fundamentals request. Its public DAX example displays ten positions; this is not evidence that a live response is complete.

Read-only tests on 2026-10-23 used an unrelated public DAX ETF, not portfolio-derived identifiers. Bearer authentication on `general/dailyrequestsleft` returned HTTP 401, with a message requiring an apitoken. Using the documented `apitoken` query parameter returned HTTP 429 with a zero-requests-per-day limit on both `general/dailyrequestsleft` and `fundamentals/EXS1.XETRA`. No holdings were retrieved. This does not establish that the credential is invalid, that free access is unavailable to everyone, or that a daily reset will fix the problem. Account entitlement, activation or provider configuration needs clarification; do not retry repeatedly or purchase a plan automatically.

The [fundamentals page](https://leeway.tech/data-api/fundamentals) explicitly documents ten API-call units per request. This corrects the earlier provisional one-unit budget assumption. If fifty free daily units are enabled and this endpoint is included, at most five fundamentals calls fit in a day before mapping, quota inspection or other usage. Actual unit decrements could not be measured because requests were rejected.

Subsequent account-UI evidence explicitly requests an email to activate fifty free test requests. This explains the onboarding obstacle, but does not establish a recurring daily allowance. No screenshot, credential or account detail is retained in these artifacts. Investigation is deferred by the provider decision; no support request has been sent.

Illustrative request budget, unrelated to any real portfolio: twelve funds require 120 documented units per complete composition refresh, excluding mapping and enrichment. That needs at least three daily quota windows at fifty units per day. Staggered weekly refreshes might fit, but the application must display differing source/refresh dates and cannot promise every fund refreshes daily on this allowance. Constituent enrichment, retries, quota checks and other PP features also consume the allowance; avoid one lookup per constituent per refresh.

Use budget-aware scheduling, bounded retries, backoff and cached identities. Permit gradual automatic enrichment across days. Do not automatically purchase quota or repeatedly retry entitlement errors.

Leeway's [analysis-plan page](https://leeway.tech/payment/plans?data=api) distinguishes web-app plans without API access from API packages. Its [general API page](https://leeway.tech/data-api) contains inconsistent free-allowance wording. Verify actual free-account entitlements and quota decrement rather than assuming every marketing limit applies. The accessible [terms PDF](https://leeway.tech/assets/AGB.pdf) is headed for business customers; establish which terms govern individual API use, local display and caching.

### Remaining blockers and their scope

Confirmed development decision on 2026-10-23: assume runtime/display and
user-key adapter distribution permission for implementation and local development.
This is a working assumption, not a verified grant. Task 1.2 records this decision;
actual permission verification moves to the pre-publish checklist in task 6.3.
Do not publish the adapter until that checklist passes. Real provider data must
remain session-only until persistence permission and retention are verified.
No provider contact or paid plan is authorized by this decision.

Implementation review on 2026-10-23: `provider-gates.md` records the repository
checklist and current permission decision. Free personal display is supported
in principle, but local cache retention and distribution of a user-key adapter
remain unverified. The permission evidence and task 1.3 are not passed; activation of persistence
for real provider data remains gated. Session-only release still requires the
display/distribution and data-quality gates. The provider-independent work in sections
2–3 remains available. Clarification questions are prepared but have not been
sent; no provider contact is authorized by this record.

| Question | What it blocks | Required resolution |
| --- | --- | --- |
| Free personal display and distribution with individual keys | Provider release in either storage mode | Establish permission for runtime use and adapter distribution; API access alone does not resolve all release rights. |
| Per-provider/account persistence and retention | Enabling disk storage of that provider's data | Establish applicable permission and retention. Otherwise use permitted session-only operation; do not require payment or block the analysis merely because disk caching is unavailable. |
| Weight denominator, completeness and physical versus synthetic exposure | Treating a particular fund as decomposed economic exposure | Validate issuer examples and provider semantics. A 100% sum is insufficient. Until validated, leave that fund unresolved in the exposure totals. |
| Reliable identification of asset type and issuer/company | Correct aggregation of affected constituent rows | Establish automatic, evidence-backed mappings. Unsupported rows can remain unresolved; complete global identifier coverage is not a prerequisite to the engine. |
| Public physical-fund acceptance example | Shipping a useful initial adapter | Demonstrate at least one independent public example with validated weight basis, asset classes and company identities. Passing parser tests alone is insufficient. |

Not global blockers under the accepted partial-coverage approach: missing effective dates, temporarily unavailable funds, unresolved individual constituents, unavailable historical data, and Leeway activation. Unknown dates must stay visible. Synthetic support can be incremental, but an unknown replication/exposure basis cannot be silently assumed physical. These gaps still matter to the ultimate coverage objective.

Provider selection is settled for the initial adapter. It does not certify every fund, resolve licensing, or authorize implementation.

### First-version behaviour: accepted defaults

Accepted: show useful validated results with explicit unresolved exposure, without abandoning the full-coverage objective. The capability specs define the observable contract; the following table explains its application.

Use current portfolio values and the latest available compositions. Label the result as current values combined with the available composition dates, not a real-time holdings feed. Use a positive-value securities view initially, explicitly labelled as a percentage of selected securities value; exclude account cash from that denominator and explain this in the view. Short/leveraged portfolio semantics need separate design before support. Within funds, retain cash and other non-equity allocations rather than assigning them to companies.

The main view should show company, direct contribution, contribution through funds and combined contribution. Expanding a company reveals the source funds. A status summary should keep unresolved exposure and data limitations visible beside the result. Provider details belong in a data-status panel rather than the main flow.

| Condition | Recommended visible behaviour |
| --- | --- |
| Missing fund or failed first retrieval | Keep its full value as unresolved with a reason. Show other usable positions normally; do not ask for a file upload. |
| Partial composition with weights known to be fractions of total fund NAV | Include only validated contributions; retain the remaining NAV portion as unresolved. Never scale known rows to 100%. |
| Possibly normalized/top-only composition, or unverified denominator | Leave the entire fund unresolved in economic-exposure totals. Optional source preview must be separate from aggregated results. Do not invent a numerical missing fraction. |
| Missing constituent identity | Try bounded automatic resolution. Otherwise retain an unresolved row under its source fund, preserving the reported label for inspection. No manual mapping is required to use the view. |
| Instrument known but company grouping unverified | Show an explicitly ungrouped instrument; do not guess that different share classes or depositary receipts are the same company. Distinguish identified instruments from fully grouped company exposure. |
| Unknown asset type | Keep the affected contribution unclassified; an ISIN alone does not prove it is an equity. |
| Synthetic or otherwise unsupported exposure basis | Keep that fund unresolved. Do not substitute its collateral basket or another fund tracking a similar index. |
| Effective holdings date absent | Show "Holdings date unavailable" and separately show provider refresh and local retrieval dates. A recent refresh is not evidence of recent holdings. |
| Refresh fails with a valid licensed local snapshot | Keep the last valid snapshot with a visible failed-refresh/age status. Do not silently replace it with an empty result. |
| User opts out or persistence is prohibited/unverified | Use session-only results with identical analysis; remove the affected disk cache and disclose restart/offline limitations. |
| Refresh fails in session-only mode | Keep any permitted valid in-memory snapshot for this session with its dates and failure status. After exit, fund analysis needs retrieval again. |
| Rate limit or expired key | Back off or stop the relevant requests; show an actionable status and preserve existing results where storage is allowed. No repeated prompts, silent provider switch or automatic purchase. |
| Duplicate identifiers or signed weights | Preserve source rows during validation. Sum legitimate separate positions only after checking semantics; reject incompatible/malformed snapshots rather than dropping negatives or deduplicating blindly. |

Coverage should describe how much selected value is accounted for by validated company contributions, identified-but-ungrouped instruments, cash/other assets and unresolved portions. Freshness is a separate dimension. Do not advertise "100% complete" merely because weights reconcile. Use decimal arithmetic and preserve signed source rows. Version one resolves only nonnegative, unleveraged NAV allocations with verified semantics; a negative allocation makes the entire fund unsupported, with signed source rows retained for diagnostics. Do not normalize overfull totals. A shortfall remains unresolved even if tiny; round only for display. Invalid/nonfinite weights or totals above 100% make a snapshot unusable. This conservative rule avoids concealing uncertainty with a tolerance; any later provider-specific rounding tolerance requires evidence and a spec revision.

Schedule automatic retrieval at most once per rolling 24 hours per fund while PP runs, plus manual refresh respecting provider limits. Coalesce concurrent requests; a chart redraw never schedules a fetch. Use a provider-wide budget, honour Retry-After, and stop authentication/entitlement retries until configuration changes. No background process runs when PP is closed. This does not promise daily source publication.

### Implementation sequence and unresolved gates

After apply authorization, models, storage abstractions, offline calculations and the adapter can proceed under the confirmed development-only permission assumption. Real provider persistence requires verified permission and retention; local development uses session-only real data until then. Provider publication still requires runtime/display/distribution permission and data-quality evidence under task 6.3. If verified terms contradict the development assumption, revisit affected work rather than silently imposing payment. No contact with a provider is authorized by this plan.

Before claiming usable fund decomposition, validate denominator, exposure basis, classification and identity against independent public examples. Unknown effective dates remain permitted and visible. Unsupported funds do not block the whole view, but a release consisting only of unresolved funds fails the public physical-fund acceptance gate.

### Storage, credentials and integration

Accepted storage decision on 2026-10-23: persistent caching is optional and
defaults on where permitted, with an opt-out preference for each provider/account.
The provider contract exposes persistence policy independently from the user's
preference: permitted with applicable retention, prohibited, or unverified.
Effective persistence requires both preference and policy approval. An unknown
policy does not imply permission; it selects session-only operation if runtime
use is allowed. This applies to Eulerpool and later providers without coupling
their storage modes or settings. Existing permission findings are not cleared
by choosing this architecture.

Both modes feed the same composition validation and look-through engine.
Session-only mode retains compositions, enrichment mappings and derived exposure
results in memory while PP runs, discarding them at exit. It writes no provider
payloads to caches, portfolio files, portable settings or diagnostic logs.
Existing portfolio storage, secure credentials and the local preference are
independent. Valid in-memory results can survive refresh failures in the same
session within permitted use; after restart, initial retrieval is needed and
offline fund exposure is unresolved until data becomes available. A redraw
never triggers a request, and initial retrieval still respects quotas/backoff.

Observed `ClientInput.getPreferenceStoreFile` can place settings beside a
portfolio or in plugin state; `PortfolioPlugin.getStateLocation` supplies local
application storage. When persistence is effective, use a separate versioned,
disposable cache in plugin state, never the portfolio or its portable settings.
Cache records contain one provider snapshot per fund, provenance and validation
version, with atomic replacement and approved retention. Do not blend providers
or vintages. The common storage contract and synthetic providers let tests
compare identical calculations under both modes without storing real payloads.

Opting out or withdrawing permission stops disk reads/writes and removes the
affected provider/account's retained compositions, mappings and derived results.
Invalidate pending persistence operations so a completed refresh cannot recreate
deleted data. Reduced retention removes expired entries, including when refresh
fails. Other providers' permitted caches and the portfolio remain intact.
Permitted session results may continue in memory. Re-enabling persistence can
store only validated eligible results within approved retention; it does not
restore expired or previously forbidden files.

Use local secure credential storage, with session-only entry if secure storage is unavailable; never fall back to plaintext portfolio preferences. Verify Equinox secure-storage availability in the target platform before adding the UI integration. No shared key ships with PP. Bearer headers keep secrets out of URLs; redact errors and logs. Send fund identifiers only, never quantities, values, transactions or the portfolio file.

Use cancellable background jobs following the existing UI jobs pattern, with injected provider transport and clock for deterministic core tests. Keep the calculator independent of SWT, network calls and provider payloads. Reuse `ClientSnapshot` valuations and conversion; report missing valuation/conversion as an incomplete analysis, not zero exposure. Existing online feed tests and snapshot tests provide nearby conventions. Add a dedicated provider service contract rather than overloading quote feeds or classifications, because composition provenance and completeness are different data contracts.

Traverse nested funds to a maximum of eight composition edges per path, detect cycles per path, and leave only the affected branch unresolved. Aggregate repeated legitimate paths without double counting the parent fund itself. Bounded identity enrichment shares the provider budget and must never merge by name alone.

### Isolated macOS testing with WebDAV refresh

Accepted workflow: refresh before every managed test launch, preserve the previous local test copy, and never replace a portfolio while the development app is running. This is workspace tooling, independent of Eulerpool gates. Implement it early so each useful X-ray increment can be tested locally.

Acceptance clarification during implementation on 2026-10-23: the production
portfolio is saved automatically and periodically by an external process, which
cannot be paused for this workflow. A coherent plausible local snapshot is
sufficient; continuous synchronization and byte equality between separate
remote downloads are not acceptance criteria. Verify source protection through
the confirmed read-only credential, GET/HEAD-only transport and absence of local
test edits in later downloads. Independent remote saves must not replace or
invalidate a running local copy. Failed/incoherent downloads still fail closed,
with explicit offline launch available for retained valid data.

Observed `scripts/dev.sh app` builds through Docker and selects a macOS aarch64 app with bundled Java. `run-app` uses `open -n` with a separate `scratch/pp-dev-workspace`; it currently neither downloads nor selects a portfolio. `clean` removes build outputs and that workspace. `scratch/` is ignored. `ClientFactory` supports XML, ZIP and encrypted formats; copying only XML would be an incorrect assumption. No WebDAV integration was found in the inspected source trees.

Extend the wrapper with a dedicated opt-in managed launch, proposed as `scripts/dev.sh run-app --webdav-copy`. Keep ordinary synthetic testing available. Build separately with `scripts/dev.sh app`; launch must identify the build revision and refuse a missing or incompatible app. Preserve a build manifest outside disposable target directories. Do not silently launch an older build when source revision or working-tree state differs. Architecture detection must select a matching packaged macOS runtime or fail clearly; the current aarch64 constant is not a universal macOS target.

Use one configured HTTPS WebDAV file URL, not a mounted production share or a bidirectional sync folder. A downloader in the dev container receives private configuration via a read-only secret file and writes only to `scratch/pp-dev-data/`. Allow only GET and HEAD; no upload, remote deletion, locking or directory mutation. Require a server-side read-only account/token for the managed workflow. Do not probe permissions by attempting a write. Reject redirects by default, verify TLS, and never forward credentials to another origin. URL, user name and credential stay outside tracked files, logs and command arguments. The desktop process receives neither WebDAV credentials nor a source path. It opens only a regular local file, never a symlink or hardlink to production storage. This protects the managed workflow; it is not an OS sandbox against deliberately opening an unrelated file manually.

Private setup is a later implementation prerequisite: obtain the file URL, authentication method, read-only credential and portfolio format locally, plus an encryption password if required by PP. Do not request these in public artifacts or infer them from unrelated credentials. If the server cannot supply read-only access, stop setup and revisit isolation rather than quietly using production write credentials. No server access is needed or performed during planning.

Acquire one launcher lock before refresh and hold it through the development process lifetime. Refuse refresh or another managed launch while that instance runs; do not trust a stale PID alone. Download to a uniquely named staging file with restrictive permissions, bounded time/size, and verify successful complete transfer and a supported file container. For encrypted portfolios, preserve encryption and let PP request the password; do not label content validated until PP can open it. Reject HTML/error bodies and malformed containers. Never replace the active or previous copy on failed download or preflight validation.

Keep an untouched downloaded baseline and a separate writable development copy. Conditional GET may reuse an unchanged baseline, but must not reuse the locally edited working file as the remote baseline. Record check time, download time, validator if supplied, local digest and build revision in a private manifest. Without reliable validators, fetch the full file each launch. The guarantee is the latest successfully retrieved server version at launch, not changes made after the download.

After successful staging, preserve the previous development portfolio and its adjacent backup/settings files in a generation directory, then atomically activate the new baseline and working copy. Retain the immediately preceding generation by default; disclose that older generations are pruned only after successful refresh, with an explicit local keep option for experiments that must survive longer. Keep copies and generation backups outside `pp-dev-workspace` so ordinary build cleanup does not erase them. A separate explicit data-cleanup action removes only managed private test data when testing is finished.

Use the isolated Eclipse workspace with no imported production recent-file history or preferences. Verify the chosen mechanism for opening the local portfolio in the development process; do not assume a URL or generic file association targets the correct PP instance. Label the file as a development copy. Local saves and autosaves remain local. Test startup, reopen, backup paths and recovery from an encrypted-file/password error before real use. On failure, abort the normal launch and retain the previous copy; an explicit offline launch can use it with a stale-data notice. Never silently fall back to the production file. Initial acceptance uses a mock WebDAV server and a synthetic portfolio, followed by a private real-portfolio check without publishing any contents.

### Coverage gap register

| ID | Gap | Remedy and closure evidence |
| --- | --- | --- |
| G1 | Unverified provider completeness/denominator | Authoritative semantics plus independent issuer comparisons; accepted fractions of total NAV, no normalized top-only data |
| G2 | Missing asset classification or company identity | Evidence-backed automatic mappings; offline ambiguous-name and share-class tests plus public acceptance sample |
| G3 | Synthetic, signed or derivative exposure | Follow-up economic-exposure contract and validated data; never use collateral as a proxy |
| G4 | Unavailable funds or provider entitlements | Additional licensed automatic adapter or confirmed entitlement; verified coverage, no manual-upload requirement |
| G5 | Missing holdings-effective dates | Provider or issuer date evidence; distinguish this freshness gap from exposure accounting |
| G6 | Cyclic/deep nested funds | Validated traversal/data remedy; preserve reconciliation and visible branch gaps |

For each remaining gap, release review must retain missing evidence, affected category, remedy and verification criterion and link a follow-up backlog record. These generic records contain no private holdings. The local view supplies per-fund reasons. Partial first-release acceptance cannot close these gaps or the ultimate objective automatically.

Suggested provider questions, prepared but not sent: Does the free tier include complete UCITS holdings? What does each request cost? Are underlying identifiers and holdings-effective dates available? What is returned for synthetic funds? Are signed weights and derivatives included? May an individual cache responses locally for offline use in PP, and for how long? Does distributing an adapter with user-supplied keys require a separate agreement?

## Risks / Trade-offs

- Incomplete or normalized responses -> preserve unknown exposure and validate against issuer disclosures.
- Missing/ambiguous identifiers -> use validated provider mappings and show unresolved identities; do not substitute guesses.
- Cash and derivative rows without asset types -> do not infer stock exposure from a nonempty name or ISIN alone.
- Provider refresh mistaken for effective date -> retain separate fields and label unavailable effective dates.
- Synthetic substitute basket mistaken for intended exposure -> require an explicit exposure basis before treating the decomposition as economic exposure.
- Free quotas or contracts changing -> interchangeable adapters, bounded refresh budgets and visible provider failures.
- Local cache prohibited or unverified -> use permitted session-only operation with the same analysis; disclose restart/offline limits without silently requiring a paid plan.

## Migration Plan

Planning only. After apply authorization and the relevant gates, deliver focused core, provider and UI increments. Do not change the portfolio serialization format. A missing, incompatible or corrupt cache is discarded and retrieved again, with unavailable data shown explicitly meanwhile. Disabling the feature cancels jobs and leaves portfolio transactions and securities intact; removal can delete only its own derived cache and credential entry. Enforce the approved retention policy on startup and refresh. Verify opening and saving a synthetic portfolio with the feature disabled, and rollback to a build without the feature, before release.
