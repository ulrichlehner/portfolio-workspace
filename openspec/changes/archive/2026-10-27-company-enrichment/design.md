# Design

## Context

Companies in `LookThroughResult` are keyed by an `Identifier`, usually an ISIN. The Eulerpool adapter already
calls `equity/profile/{isin}` for classification but discards the fields. The public API documentation
(fetched 2026-10-27) lists `country`, `currency`, `employees`, `sector`, `industry`, `ipo`, `mcap`, `shares`
for the profile; numbers are in millions; `country` is a name, not an ISO code. GLEIF's
`/api/v1/lei-records?filter[isin]=A,B` accepts several ISINs per request and returns
`entity.headquartersAddress.country` as ISO 3166 code (checked with two public example ISINs).

## Goals / Non-Goals

**Goals:**
- One enrichment model usable by every grouping (country, region, sector, industry, currency, size).
- Cheap repeat runs through caching; bounded first runs through value ordering.

**Non-Goals:**
- Fund-level allocations from the provider (`etf/countries`, `etf/sectors`); they may later serve as a
  cross-check for undecomposed value.

## Decisions

- **Separate enrichment service, not part of the engine.** The engine stays a pure calculation; enrichment is
  a keyed lookup `Identifier -> CompanyAttributes` filled asynchronously and joined in the presenter. This
  keeps recalculation fast and allows partial results.
- **Country codes.** Store ISO 3166 alpha-2. Profile country names are mapped through `java.util.Locale`
  display names in English; unmapped names count as unknown rather than guessed.
- **Ordering and batching.** Profiles: one request per company, highest value first, through the existing
  `CompositionRequestBudget`. GLEIF: batches of up to 200 ISINs with a small fixed pause between requests.
- **Cache.** One versioned file per source under the workspace state area, keyed by ISIN, with retrieval
  date. Provider profiles reuse the persistence policy from `provider-cache-consent`; GLEIF data is always
  stored. Entries older than 30 days are refetched when the company appears in a result.
- **GLEIF client.** Plain HTTPS GET with PP's existing HTTP utilities, no redirects, strict JSON parsing, and
  only `headquartersAddress.country`, `legalAddress.country` and the LEI kept.

## Risks / Trade-offs

- [First run with thousands of companies takes long] → Value ordering makes the top exposures available first; progress shows the pending count.
- [GLEIF rate limits] → Batching keeps the request count around one per 200 companies; on HTTP 429 back off and retry later.
- [Headquarters is not revenue exposure] → Labelled as headquarters country; revenue regions come in a separate change.
- [ISIN of a depositary receipt points to the depositary, not the company] → The register lookup usually resolves the issuer; otherwise the ISIN prefix source is visible.

## Open Questions

- Whether the provider profile request counts against a plan quota differently from holdings requests (the
  documentation tags endpoints with different weights). The budget treats every request as one until known.
