# Proposal

## Why

Investors often hold several broad funds and do not know how much they duplicate each other, for example a
world fund and a technology index that share most of their largest companies. The Breakdown already holds the
decomposed constituents of every fund, so the overlap can be computed without new data.

## What Changes

- For every pair of decomposed funds, the overlap is computed as the sum over shared companies of the smaller
  of the two weights, plus the number of shared companies.
- A new chart kind "Overlap" in the chart pane shows a fund-by-fund matrix with the overlap percentage per
  cell; the tooltip lists the largest shared companies.
- Selecting a cell selects the largest shared company in the table.

## Capabilities

### New Capabilities

- `fund-overlap`: pairwise overlap of decomposed funds by shared companies.

### Modified Capabilities

- `breakdown-view`: adds the overlap chart kind.

## Impact

- Core or presenter: overlap calculation from the look-through contributions.
- UI: chart pane gets a third chart kind drawn with SWT (no new library).
- Delivery: one focused commit on `feature/fund-overlap`, stacked on `feature/revenue-regions` in one linear stack;
  independent of the enrichment changes.

## Out of scope

- Overlap of funds the user does not hold.
- Suggestions to sell or switch funds.
