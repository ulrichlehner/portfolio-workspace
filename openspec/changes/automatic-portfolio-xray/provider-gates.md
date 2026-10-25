# Repository and provider gates

## Current publication scope, confirmed 2026-10-25

The user explicitly permits source-only publication in their development fork
with an experimental-use notice, despite unresolved provider permissions and
data quality. This is the user's development-risk decision, not provider approval
or an assurance that a disclaimer transfers responsibility or grants rights.
It supersedes the earlier blanket restriction on source-fork pushes below.
No provider payloads, credentials or public binaries are distributed. Official
upstream integration and binary releases remain subject to task 6.3 review.
Real-data disk persistence stays disabled. Task 1.3 data validation continues.

**Latest data finding:** The full dated issuer-API comparison below supersedes the
earlier CSV-only limitation. All 1352 identified Eulerpool rows in the two public
examples match official issuer ISINs and raw weights within rounding. Historical
holdings weights are now corroborated across the complete identified lists, not
merely their top ten. Missing economic futures exposure and production use of this
independent evidence remain separate unfinished work.

Checked: 2026-10-23. Section 0 was committed as `1d3d0a9`.
This record contains public documentation evidence only. No portfolio was opened,
no authenticated provider request was made, no provider was contacted and no
subscription or persistent provider cache was created during this review.

Subsequent user decision on 2026-10-23: persistence is an opt-out preference per
provider/account where permitted, with session-only operation when disabled,
prohibited or unverified. This changes the delivery architecture, not the
permission findings below. See the current design, specs and tasks for the
effective storage rules; the review checkboxes are not newly completed.

## 1.1 Implementation checklist: complete

Reviewed the workspace `AGENTS.md`, upstream `portfolio/AGENTS.md`,
`portfolio/CLAUDE.md`, `portfolio/CONTRIBUTING.md`, the path scope of
`portfolio/.claude/rules/pdfextractors.md`, and the core, UI and core-test
bundles' `.settings/` compiler, formatter and encoding preferences.

- [x] Builds, tests and OpenSpec commands run in Docker through the wrappers.
- [x] Java 21, UTF-8, four spaces, next-line braces and the bundles' 120-column
  formatter settings apply to future Java edits. Use surrounding conventions
  and `var` where appropriate; do not reformat unrelated code.
- [x] Format-on-save remains disabled under the overriding workspace rule.
- [x] PDF rules are scoped to importer paths; this change does not touch them.
- [x] Keep new calculation/validation code independent of SWT, provider payloads
  and networking. Put it in the core domain; keep views and background UI jobs
  in the UI bundle. Follow existing ServiceLoader provider discovery and OSGi
  package/export conventions rather than changing quote-feed semantics.
- [x] Deterministic tests belong in the existing core test bundle, using
  synthetic inputs without live credentials. Use `scripts/dev.sh test` for
  core tests and Checkstyle, and `scripts/dev.sh app` for integrated UI builds.
- [x] Externalize new UI strings, follow contribution translation rules and
  existing image registration. Any new icons must meet the upstream rules.
- [x] Keep specs/tooling outside `portfolio/`. Future upstream increments remain
  focused: core composition/calculations, provider integration, then UI.
  The PP implementation branch is clean at `upstream/master` and remains
  `feature/automatic-portfolio-xray`; use focused scope suffixes as needed.
- [x] Use focused Conventional Commits, subjects at most 50 characters and
  bodies wrapped at 72. Review privacy and required checks before commits or
  pushes. No publishing is authorized by this gate review.

This checklist records implementation constraints, not tests of feature code
that has not yet been written.

## 1.2 Development assumption recorded; publication permission unverified

User-confirmed decision on 2026-10-23: assume runtime/personal display and
user-key adapter distribution permission for implementation and local development.
Task 1.2 now records this assumption, not completion of the permission research.
The evidence findings below remain unverified where indicated. Actual permission
verification is the mandatory pre-publish checklist in task 6.3, covering runtime,
display, source/binary adapter distribution, attribution/other obligations and
optional persistence/retention. Record authoritative sources, dates and decisions
before publishing. Real-data disk persistence remains disabled until permission
and retention are verified; local development uses session-only data. No provider
contact or purchase is authorized.

This is a release-gate assessment, not a conclusion that all personal caching
is prohibited. The selected free personal desktop workflow lacks explicit
published permission for every required use.

| Required use | Public evidence | Decision |
| --- | --- | --- |
| Personal noncommercial display | The pricing and licensing pages describe free personal/evaluation use and public attribution requirements. | Supported in principle; preserve attribution requirements. |
| Local response caching and offline fallback on Free | The licensing FAQ expressly permits product caching on paid plans. It does not establish Free desktop caching rights. | Unresolved; no activation of real-data disk persistence. Synthetic storage implementation may proceed. |
| Allowed cache retention | No applicable Free desktop retention period was established in the reviewed API terms. | Unknown, not zero or unlimited; do not invent a duration. |
| Open-source adapter distributed without data, using each user's own key | The reviewed documents do not explicitly resolve this distribution model. | Unresolved; provider release remains gated. |

Sources checked on 2026-10-23:

1. [Eulerpool data licensing](https://eulerpool.com/financial-data-api/licensing):
   personal/evaluation scope, attribution, caching FAQ and the statement that
   governing terms and an order form control the summary.
2. [API pricing](https://eulerpool.com/financial-data-api/pricing): the Free plan
   is described as noncommercial and provides individual API access. Endpoint
   access does not itself clear the storage/distribution questions.
3. [Terms of Service](https://eulerpool.com/terms-of-service), displayed update
   date 2026-10-22: API usage must comply with applicable restrictions; copying
   or exploitation requires permission. No specific Free cache retention or
   user-key open-source adapter grant was found.
4. [Eulerpool Excel add-in](https://eulerpool.com/financial-data-api/excel):
   Eulerpool describes its own free personal add-in and short caches. This
   product-specific example does not establish permission for a third-party
   holdings cache or its intended retention.

The summary's feature bullets lose included/excluded icon distinctions in text
extraction. Decisions above use the explicit FAQ prose, pricing scope and terms,
not an apparent permission inferred from a flattened bullet list.

No paid plan or alternate provider has been substituted. Activation of real
provider disk persistence remains gated. Generic session-only/persistent stores
can be implemented with synthetic providers. Session-only provider release does
not need disk-retention permission, but still needs runtime/display/distribution
permission and data-quality acceptance. Sections 2–3 remain independent.

### Clarification draft: prepared, not sent

We are considering an optional Eulerpool adapter for Portfolio Performance, a
free open-source desktop application. Each user would supply their own API key;
no shared key, portfolio upload, central data service or bundled holdings data
would be provided.

Does the Free plan permit personal holdings display, a local cache for daily
refresh and offline fallback, and distribution of this adapter's source and
binary code? What maximum retention, deletion-on-expiry and attribution rules
apply to raw responses and derived exposure results? Please distinguish Free
from paid-plan permissions and identify the governing terms.

Provider contact needs explicit user authorization. No message has been sent.

## 1.3 Data acceptance: not passed

The [holdings endpoint documentation](https://eulerpool.com/developers/api/etf/holdings)
describes top holdings and exposes weight and refresh fields in its example.
It does not, by itself, establish a total-fund NAV denominator, a separate
effective holdings date or complete supported economic exposure.

The [ETF product page](https://eulerpool.com/financial-data-api/etf-data) promises
complete constituent lists and replication metadata. That marketing description
conflicts with the narrower endpoint wording and does not validate a particular
snapshot. Neither a successful response nor a 100% sum closes this gate.

The earlier public issuer comparison in `design.md` remains preliminary:
rounded large-position agreement did not resolve derivative exposure or all
classification/company mappings. No new fund-level API comparison was completed
in this review. Task 1.3 stays unchecked; no fund is newly certified as useful
validated decomposition. Missing evidence remains in design gaps G1–G3.

### Measured evidence added 2026-10-25

A public accumulating UCITS equity fund was requested with an individual key.
This is a read-only check of one public identifier, not a portfolio-derived test:

- `/api/1/etf/holdings/{isin}` returned 1266 rows whose `percent` values summed
  to 100.0. `assetType` was null on every row, 15 rows carried no ISIN, and
  `share` summed to a different magnitude than `value`. The summed row `value`
  exceeded the profile `aum` by about three percent, so the rows are not a proven
  fraction of total fund NAV.
- `/api/1/etf/profile/{isin}` returned `assetClass` ("Equity"), `aum`, `nav`,
  `currency`, `isLeveraged`, `isInverse`, `trackingIndex`, `etfCompany`,
  `domicile`, `updated_at` and `tickers`. It supplies fund-level metadata and a
  fund-versus-non-fund signal, but no holdings-effective date and no constituent
  classification.
- `/api/1/equity/search?q={isin}` returned `name`, `isin`, `ticker`, `type`
  (`etf` for the fund, `stock` for a control equity), `currency`. It classifies
  an instrument, not its constituents.
- Response headers showed a very high provider limit for this account
  (`x-ratelimit-limit: 100000`, `x-ratelimit-remaining: 99996`). This is an
  observation, not an entitlement; the application budget stays a conservative
  placeholder.

Consequences recorded for the implementation:

- The provider cannot certify denominator, completeness or exposure basis through
  its API. Task 1.3 cannot be closed by endpoint evidence alone.
- The provider does classify individual instruments through `/equity/search`
  (stocks, ETFs, funds) and its bond list. A constituent and a held security can
  therefore be classified and grouped by security identifier into an issuer-level
  x-ray. That classification is real provider data, not a name heuristic; it does
  not validate the allocation semantics of the fund weights.
- Per-constituent company identity beyond the security identifier (for example a
  company graph merging share classes) is not available. Issuers stay grouped by
  their security identifier, which the view labels company / instrument.

Pause only work requiring an unpassed permission or data-quality gate. Obtain
runtime/display/distribution permission and a dated public physical-fund
comparison covering NAV, supported exposure, classification and company identity.
Resolve persistence permission before activating disk storage of real data;
otherwise use permitted session-only operation under the accepted storage design.

### Independent issuer recheck, 2026-10-25

The orchestrator fetched the official latest-holdings CSVs again rather than
treating a delegated summary as independently verified evidence:

- [World issuer CSV](https://www.ishares.com/uk/individual/en/products/251882/ishares-core-msci-world-ucits-etf/latest-holdings.csv)
- [NASDAQ 100 issuer CSV](https://www.ishares.com/uk/individual/en/products/253741/ishares-nasdaq-100-ucits-etf/latest-holdings.csv)

Both exports now state holdings effective **23 Oct 2026**. The previous delegated
NASDAQ comparison used a 22 Oct export; its maximum difference of 0.0049
percentage points is not the result against this newly retrieved export.

| Independent public example | API rows | API weight sum | Rows without ISIN | Issuer rows | Largest top-ten weight difference |
| --- | ---: | ---: | ---: | ---: | ---: |
| Core MSCI World UCITS ETF | 1266 | 99.99999996% | 15 | 1271 | 0.04191706 percentage points |
| NASDAQ 100 UCITS ETF USD (Acc) | 106 | 100.00000001% | 5 | 108 | 0.10491939 percentage points |

API row update dates are 25 Oct 2026, not an effective holdings date. Comparison
paired the top ten by exact ticker after removing the API's exchange suffix,
with a unique issuer row required. The issuer export has no constituent ISIN
column, so this is a plausibility comparison, not independent ISIN identity
verification. Issuer weights are rounded to two decimal places. Neither equal
row dates nor exact source vintages were established.

The World export includes equity, cash, collateral, money-market and futures
rows. The NASDAQ export includes equity, cash, collateral, FX and futures rows,
including a futures row with zero market value and positive notional value.
Row-count differences alone do not identify every omission, but demonstrate why
weight normalization and top-ten agreement cannot certify economic exposure.
Task 1.3 remains **not passed**. G1-G6 remedies and closure checks are retained
in [coverage-follow-ups.md](coverage-follow-ups.md).

### Pre-publish acceptance matrix, 2026-10-25

This is a release decision using the evidence above, not a new permission grant
or a claim that the provider's terms were independently cleared today.

| Gate | Result | Evidence / outstanding closure |
| --- | --- | --- |
| Runtime and personal desktop display | Unknown | Free personal use is supported in principle by the published pricing/licensing summary; applicable desktop-use obligations remain unverified |
| Adapter source distribution with individual keys | Unknown | No authoritative grant for this distribution model established |
| Adapter binary distribution with individual keys | Unknown | No authoritative grant for this distribution model established |
| Attribution and other applicable obligations | Unknown | Attribution is mentioned in the licensing summary; the applicable complete obligations have not been established |
| Optional real-data persistence | Unknown; disabled | No verified Free-plan permission established |
| Optional real-data retention | Unknown; disabled | No applicable retention period established |
| Public physical-fund economic-exposure acceptance (1.3) | Accepted for the identified physical sleeve under the documented rule | Two complete dated issuer comparisons (1251 and 101 exact-ISIN rows) agree within published rounding; issuer classifications available. Derivative overlay, completeness declaration, holdings-effective date and corporate grouping stay outside the accepted scope |
| Freshness transparency | Pass for representation, not source freshness | Missing holdings-effective dates remain unknown; retrieval/update dates are not substituted |
| Experimental source-only development fork | Authorized by user with notice | Explicitly confirmed on 2026-10-25; no rights verification, provider payloads, credentials or public binaries |
| Official upstream integration / binary releases | Blocked | Runtime/display/distribution/obligations and data-quality gates are not passed; the development-fork exception does not establish provider rights |

Provider contact remains unauthorized. Disk caching remains disabled. Further
local development can continue under the recorded development-only assumption.

### Full ISIN-keyed issuer comparison, 2026-10-25

The product page's own public data endpoint was inspected, not guessed from a
third-party data vendor. Its `holdings` component supplies a requested effective
date, parallel ISIN/classification/market-value/notional/weight arrays, and raw
weights with five decimal places. This corrects the earlier assumption that the
issuer has no available constituent ISINs: they are absent from the convenient CSV
but present in the issuer's public JSON.

Authoritative product pages:

- https://www.ishares.com/uk/individual/en/products/251882/ishares-core-msci-world-ucits-etf
- https://www.ishares.com/uk/individual/en/products/253741/ishares-nasdaq-100-ucits-etf

Observed endpoint:
`https://www.blackrock.com/varnish-api/uk-retail01-product-data/product-data/api/v2/get-product-data`

The page's `ProductPageAjaxUtils` supplies the query contract. The comparison used
`appSubType=ISHARES`, `appType=PRODUCT_PAGE`, `component=holdings`, `locale=en_GB`,
`targetSite=ishares-uk`, `userType=individual`, `excludeContent=true`,
`includeConfig=true`, `asOfDate=20261022`, and the product IDs above. Returned
`asOfDate.value` was checked independently; an update timestamp is never used as
a holdings-effective date.

| Public example, issuer effective 22 Oct 2026 | API rows | Issuer rows | Unique ISIN pairs | Pairs within raw rounding | Matched provider weight | Maximum difference, percentage points |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Core MSCI World UCITS ETF | 1266 | 1271 | 1251 | 1251 | 99.66376718% | 0.00000500 |
| NASDAQ 100 UCITS ETF USD (Acc) | 106 | 107 | 101 | 101 | 99.95872674% | 0.00000495 |

No duplicate ISIN groups occurred on either side. The World pairs comprise all
1250 equities plus one money-market holding; all 101 NASDAQ equity rows pair by
ISIN. The remaining 15 World and five NASDAQ source rows have no ISIN. Each has
one exact issuer-name candidate classified as cash or collateral. These candidates
are diagnostics, not new identifier assertions or classifications in the app.

The issuer additionally reports four World futures with zero market value but
positive aggregate notional of about 0.4263% of the issuer's total market value,
and one zero-market-value NASDAQ future with positive notional of about 0.0172%.
The World export also includes an additional zero-balance cash row. These exactly
explain the row-count differences for the dated comparison. Eulerpool has no
corresponding futures rows, so the source cannot establish full economic exposure.

The issuer page identifies World methodology as Optimised and NASDAQ as
Replicated; both explicitly declare `productStructure = Physical`. Both provide
full-fund and share-class net-asset fields separately. A request for dated
`keyFundFacts` at 22 Oct is explicitly rejected by the issuer with HTTP 400;
current 23 Oct net-asset facts are not silently substituted as 22 Oct facts.
All ISIN-paired market values share the same issuer/provider scale factor,
approximately 1.3374526876, in both examples. Issuer reporting currency is USD;
the provider's public World profile is GBP, while individual API rows declare no
value currency. The earlier naive comparison of row values with profile AUM does
not prove bad weights: currency, fund/share-class scope and dates must first align.
It is withdrawn as an invalidity argument. The ISIN/weight comparison is
dimensionless and is not affected by this currency ambiguity.

Verification tooling is `scripts/compare_fund_holdings.py`, with synthetic tests
in `scripts/tests/test_fund_comparison.py`. It rejects malformed numbers and
misaligned arrays, preserves duplicate groups, reports all unmatched rows and
does not certify names, dates or complete economic exposure. Nine synthetic
comparison tests and all 48 workspace tooling tests passed in Docker. An offline
Docker acceptance run against both downloaded public examples asserts that all
1352 identified source rows pair and agree within combined rounding tolerance
0.000005005 percentage points, with omitted positive-notional futures detected.
Raw issuer/provider payloads and detailed reports remain in ignored scratch
storage; none is distributed as a fixture.

This establishes reproducible historical holdings-weight and instrument-type
evidence, not a generic promise about later Eulerpool answers or a company graph.
The app currently does not retrieve or apply this issuer evidence. Task 1.3 still
requires a supported public decomposition using the corroborated evidence; the
economic-overlay and company-grouping limits must remain explicit. The complete
data objective is not replaced with acceptance of an unresolved placeholder.

### Additional provider probes, 2026-10-25 (public identifiers only)

Beyond the two equity funds, two further public funds were probed to test data
shapes the acceptance rule does not cover. No portfolio identifiers were used and
nothing private is recorded here.

| Public sample | Rows | Weight sum | Duplicate ISINs | Observation |
| --- | ---: | ---: | ---: | --- |
| iShares Core Global Aggregate Bond UCITS ETF (IE00BDBRDM35) | 40000 | 100.00000162% | 19603 | Same ISIN repeated with identical nominal amount but a different percent and value; two blocks of 20000 rows summing to 90.53930858% and 9.46069304% |
| Invesco S&P 500 UCITS ETF (IE00B3YCGJ38), swap-based | 502 | 99.99999953% | 0 | No futures, swap or forward rows; the substitute basket looks like a physical equity list |

Consequences:

- The bond response is internally inconsistent: identical instrument, identical
  nominal holding, two different weights and values. That cannot be one fund's NAV
  decomposition; it looks like merged share classes or vintages. Its total also
  exceeds the one-millionth rounding tolerance. The adapter now rejects an answer
  in which one ISIN appears with the same nominal amount and a different weight,
  as `MALFORMED_RESPONSE`, instead of summing the rows as two legitimate positions.
  Legitimate duplicates with different nominal amounts remain accepted.
- The swap-based fund would previously have been displayed as if its substitute
  basket were a physical portfolio. The provider declares neither exposure basis
  nor a replication method, so the application cannot distinguish it. It stays in
  the unvalidated, partial-coverage presentation, and G3 now records this concrete
  case rather than a hypothetical one.
- A non-browser client can receive HTTP 403 with body `error code: 1010` from the
  provider's CDN while the same request with a regular client succeeds. That is bot
  protection, not an entitlement result; the adapter treats 403 as an entitlement
  failure, so a misconfigured client is reported as suspended rather than retried.

A scale regression in `LookThroughEngineTest` now builds a 1266-row fund with 1250
identified equities and 16 identifierless rows. It asserts exact reconciliation,
1250 company rows and that identifierless rows stay unresolved rather than being
invented as cash.
