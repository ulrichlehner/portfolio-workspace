# Repository and provider gates

Checked: 2026-10-23. Section 0 was committed as `1d3d0a9`.
This record contains public documentation evidence only. No portfolio was opened,
no authenticated provider request was made, no provider was contacted and no
subscription or persistent provider cache was created during this review.

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

## 1.2 Permission decision: not passed

This is a release-gate assessment, not a conclusion that all personal caching
is prohibited. The selected free personal desktop workflow lacks explicit
published permission for every required use.

| Required use | Public evidence | Decision |
| --- | --- | --- |
| Personal noncommercial display | The pricing and licensing pages describe free personal/evaluation use and public attribution requirements. | Supported in principle; preserve attribution requirements. |
| Local response caching and offline fallback on Free | The licensing FAQ expressly permits product caching on paid plans. It does not establish Free desktop caching rights. | Unresolved; no persistent provider storage implementation. |
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

No paid plan or alternate provider has been substituted. Tasks 4.3 and provider
release remain gated. Provider-independent synthetic models and calculations
in sections 2–3 can proceed separately.

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

Pause the affected provider/storage work. To pass these gates, obtain applicable
permission and perform a dated public physical-fund comparison covering the NAV
basis, supported exposure, classification and company identities. Do not silently
narrow the accepted behaviour to make the provider fit.
