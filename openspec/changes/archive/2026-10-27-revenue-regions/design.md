# Design

## Context

The provider documentation (fetched 2026-10-27) describes `equity/regions/{isin}` as an array of
`period`, `unit`, `axis`, `label`, `value`, `percentage`, `member` (for example `country_US`) and `symbol`.
Entries come from reported segment data, so members mix countries and regions and periods vary between
companies. The endpoint carries a higher documented weight tag than the profile.

## Goals / Non-Goals

**Goals:**
- Honest economic exposure with visible coverage, no estimates.

**Non-Goals:**
- Filling gaps with fund-level allocations or headquarters countries.

## Decisions

- **Latest period only.** Take the newest `period`; if several axes exist for it, prefer the geographical axis
  with the most entries.
- **Normalization.** `country_XX` members map to ISO codes. A small fixed table maps common region members and
  labels (Americas, Europe, EMEA, Asia Pacific, Rest of world) to region keys aligned with PP's `regions`
  template where possible; everything else is "Other or unspecified". Unknown labels are logged once.
- **Allocation in the presenter.** Revenue grouping is one more grouping function, but it splits a company
  across several groups; group rows list the company with its allocated part.
- **Cost control.** Requests share the enrichment queue after profiles, value ordered, so the largest
  companies get revenue data first.

## Risks / Trade-offs

- [Region members overlap countries (US and Americas both reported)] → Within one axis and period, entries are treated as a partition; overlapping axes are not combined.
- [Reporting differences between companies] → Coverage and period range are shown; no blending of periods inside one company.
- [Request weight] → Value ordering and the 90-day cache bound the cost; the coverage notice shows what is missing.

## Open Questions

- The exact meaning of the documented weight tags and whether revenue requests reduce a plan quota faster.
  The budget counts each request as one until verified with real responses.
