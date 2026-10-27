# Proposal

## Why

A company's headquarters country says little about where it earns its money: a US-headquartered company may
earn most of its revenue abroad. The provider offers revenue by geography per company (`equity/regions`,
taken from reported segment data). Allocating each company's exposure by that split shows the portfolio's
economic exposure to countries and regions, which is what "how exposed am I to the US" usually means.

## What Changes

- Revenue regions are fetched per company from the provider, largest exposures first, and cached for 90 days
  under the account's persistence policy.
- Each company's exposure is split by its latest reported revenue percentages. Reported members are
  normalized: country members map to countries, known region members (for example "Americas", "Europe")
  stay regions, everything else is "Other or unspecified".
- A new "Revenue region" option in the "Breakdown by" selector shows the split exposure; companies without
  revenue data form a "No revenue data" group, so totals still equal the company exposure.
- The data status reports how much of the company exposure has revenue data and the reporting periods used.

## Capabilities

### New Capabilities

- `revenue-exposure`: retrieving, normalizing and caching companies' revenue by geography and allocating
  exposure by it.

### Modified Capabilities

- `breakdown-view`: adds the revenue region grouping and its coverage notice.

## Impact

- Core: revenue region request and parser in the Eulerpool adapter, normalization and allocation service,
  cache next to the company enrichment cache.
- UI: grouping option, data status line.
- Delivery: one focused commit on `feature/revenue-regions`, stacked on `feature/breakdown-grouping`.

## Out of scope

- Business segments (`equity/segments`).
- Converting reported revenue amounts between currencies; only percentages are used.
- Estimating revenue splits for companies without reported data.
