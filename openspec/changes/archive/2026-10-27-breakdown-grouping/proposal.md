# Proposal

## Why

With company attributes available (change `company-enrichment`), the Breakdown can answer questions such as
"how much EUR and what share of my portfolio is in US companies", "how large is my emerging markets share"
or "how much is information technology". Today it can only list companies.

## What Changes

- A "Breakdown by" selector in the view toolbar: Company (default), Country, Region, Market classification,
  Sector, Industry and Currency. The choice is remembered.
- For every grouping except Company, the table shows one row per group with direct, indirect and total value
  and share; a group expands into its companies, and companies still expand into their contributions.
- Treemap and bar chart show groups instead of companies; the treemap nests companies inside their group.
- Companies without the attribute form an "Unknown" group; companies whose enrichment is still pending form a
  "Pending" group, so the groups always add up to the company exposure.
- Regions and market classification use PP's existing region taxonomy templates (continents and MSCI market
  classification), sectors map to PP's GICS sector template by name; industries and currencies are shown as
  delivered.
- The country column and tooltips name the country source (register, provider, ISIN).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `breakdown-view`: new requirements for the grouping selector, group rows, grouped charts and the unknown
  and pending groups.

## Impact

- UI bundle: `views/lookthrough/` presenter, view, chart pane, treemap, bar chart; messages.
- Reads PP's taxonomy templates `regions`, `regions-msci` and `industry-gics-1st-level` without creating
  taxonomies in the user's file.
- Delivery: one focused commit on `feature/breakdown-grouping`, stacked on `feature/company-enrichment`.

## Out of scope

- Grouping by company size (market capitalization currency and buckets are not settled).
- Revenue regions (change `revenue-regions`), fund overlap and concentration metrics.
- Writing groups into the user's taxonomies.
