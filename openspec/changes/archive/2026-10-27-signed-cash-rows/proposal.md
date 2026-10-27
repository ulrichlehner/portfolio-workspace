# Proposal

## Why

Broad index funds publish a few tiny negative rows without a security identifier, such as cash balances
and currency forwards. The current validation rejects a whole composition for any negative weight, so
major funds stay completely unresolved in the Breakdown view although every security row is clean. In
live provider data for broad public index funds, the negative rows were between
-0.00000001 % and -0.015 % of the fund, and each fund also had larger positive rows without an identifier.

## What Changes

- Within one fund composition, rows without a security identifier are netted against each other. When the
  net is zero or positive and no row with an identifier is negative, the composition is no longer rejected.
- The netted identifier-less amount stays unresolved, exactly as identifier-less rows are treated today. No
  row is classified as cash by its name, and no security weight is rescaled.
- Rejection stays for negative rows with an identifier (short positions), a negative net of identifier-less
  rows, missing or invalid weights and totals above 100 % beyond the existing rounding tolerance.
- The fund's source rows stay unchanged for diagnostics, and the netting is recorded so the data status can
  say that identifier-less rows were netted.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `fund-compositions`: the requirement "Conservative numerical validation" accepts netted identifier-less
  rows instead of rejecting every negative weight.

## Impact

- Core bundle: `snapshot/lookthrough/CompositionValidator`, `CompositionValidationResult` (a non-fatal
  netting diagnostic), and possibly `LookThroughEngine` for how the netted row is expanded; tests in
  `name.abuchen.portfolio.tests`.
- UI: the data status tooltip mentions the netting; no layout change.
- Delivery: one focused commit on a branch stacked on `feature/breakdown-ui-rework`, because it changes
  behavior the Breakdown view displays. It becomes part of the look-through upstream split later.

## Out of scope

- Classifying identifier-less rows as cash or currency by their names.
- Accepting short positions, leveraged or synthetic funds, or any other negative row with an identifier.
- Changes to the rounding tolerance, provider access or the UI layout.
