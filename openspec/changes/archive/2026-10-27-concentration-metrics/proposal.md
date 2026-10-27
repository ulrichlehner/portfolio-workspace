# Proposal

## Why

The summary shows the top-ten share, but not how concentrated the portfolio is overall or whether a single
company dominates it after looking through funds. Both follow from the existing result.

## What Changes

- The summary adds the effective number of companies (the inverse of the sum of squared company shares of the
  company exposure), with a tooltip explaining it in one sentence.
- The summary adds the largest single company with its share of the portfolio value.
- When one company exceeds 10 percent of the portfolio value, the existing attention indicator names it.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `breakdown-view`: adds a concentration requirement to the summary.

## Impact

- UI bundle: presenter summary and header; messages.
- Delivery: one focused commit on `feature/concentration-metrics`, stacked on `feature/fund-overlap` in one linear stack;
  independent of the enrichment changes.

## Out of scope

- A configurable threshold (fixed at 10 percent for now).
- Concentration by country or sector (possible later on top of `breakdown-grouping`).
