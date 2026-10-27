# Proposal

## Why

The Breakdown only knows a company's name and identifiers, so it cannot answer "how much of my portfolio is
in US companies" or "how tech-heavy am I". The provider's company profile carries country, currency, sector,
industry and market capitalization, and the public GLEIF register carries each legal entity's headquarters
country, which is more accurate than the country prefix of an ISIN (for example a Cayman-registered holding
company whose headquarters is in Hong Kong).

## What Changes

- Each company in a Breakdown result gets attributes: headquarters country, currency, sector, industry and
  market capitalization, each with its source.
- Country is resolved in this order: GLEIF headquarters country, provider profile country, ISIN country
  prefix. The source used is kept per company and shown in the UI later.
- Profiles are fetched in order of portfolio value so the largest exposures are classified first, within the
  existing request budget; companies not yet enriched are reported as such.
- GLEIF records are fetched in batches by ISIN. GLEIF data is openly licensed and is stored on disk without
  the provider confirmation; provider profiles follow the account's persistence policy.
- Stored attributes are refreshed after 30 days.
- A preference allows switching GLEIF lookups off.

## Capabilities

### New Capabilities

- `company-enrichment`: resolving and caching descriptive attributes of companies (country, currency,
  sector, industry, size) from the fund composition provider and public registers.

### Modified Capabilities

None. The look-through calculation is unchanged; the attributes are added next to the result.

## Impact

- Core: new enrichment service and cache in `snapshot/lookthrough/` (or a sibling package), a profile request
  in `EulerpoolFundCompositionProvider`, a GLEIF client in `online/impl/`.
- UI: `LookThroughSession` schedules enrichment; settings page gets the GLEIF switch.
- New external endpoint: `api.gleif.org` (HTTPS, no key, CC0 data).
- Delivery: one focused commit on `feature/company-enrichment`, stacked on `feature/provider-cache-consent`.

## Out of scope

- Showing the attributes (planned in `breakdown-grouping`).
- Revenue by region (planned in `revenue-regions`).
- Enriching directly held securities through PP's own taxonomies.
