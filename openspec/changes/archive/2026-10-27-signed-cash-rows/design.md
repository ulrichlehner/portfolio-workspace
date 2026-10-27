# Design

## Context

See proposal.md for motivation. `CompositionValidator.check` adds `NEGATIVE_WEIGHT` for every negative row and
returns an unusable result when any diagnostic exists. Rows without an identifier (empty
`CompositionInstrument.identifiers()`) already end up `UNRESOLVED` in `LookThroughEngine`, because the existing
spec forbids treating a missing identifier as cash evidence. A live probe of rejected public index funds showed
that all their negative rows lack an identifier and that the identifier-less rows of each fund net to a positive
amount between +0.04 % and +0.97 %, with no negative identified row.

## Goals / Non-Goals

**Goals:**
- Accept such compositions with exact reconciliation and unchanged identified weights.
- Keep the netted remainder visible as unresolved.

**Non-Goals:**
- Name-based cash or currency detection, acceptance of short or leveraged positions.

## Decisions

### D1 Net identifier-less rows inside the validator
In `check`, split rows into identified and identifier-less. A negative identified row keeps producing
`NEGATIVE_WEIGHT`. Negative identifier-less rows no longer produce it; instead their sum with the positive
identifier-less rows is computed. A negative net produces `NEGATIVE_WEIGHT` (snapshot-level). A zero or positive
net replaces the identifier-less validated rows by one netted row: weight = net, source = the first
identifier-less row with the largest positive weight (for provenance), source index of that row. The total and
the existing rounding-excess logic run on the netted rows, so overfull data is still rejected.
*Alternative:* keep all positive identifier-less rows and reduce them proportionally. Rejected: it fabricates
per-row values; one netted amount is honest and still reconciles.

### D2 Non-fatal diagnostic
Add `Reason.NETTED_IDENTIFIERLESS_ROWS` as an informational diagnostic. `CompositionValidationResult` already
carries diagnostics; usability must be derived from fatal reasons only, so introduce an explicit fatal set
(all existing reasons) and keep `NETTED_IDENTIFIERLESS_ROWS` out of it. Check every place that treats
"diagnostics non-empty" as unusable (validator, refresh coordinator, UI status) and switch it to the fatal set.

### D3 UI hint
The data status tooltip of a fund with the netting diagnostic adds one sentence ("Cash and currency rows
without identifier were netted; the remainder stays unresolved."), translated in all message files. No new
column or icon.

## Risks / Trade-offs

- [A provider could label a real security without identifier and a negative weight] → it is netted into an
  unresolved amount, never attributed to a company, so no exposure is overstated; a negative net still rejects.
- [Diagnostics semantics change from "any" to "fatal"] → covered by validator and coordinator tests for each
  existing reason.

## Migration Plan

No persisted data is affected (persistence is disabled). Session data is revalidated on the next refresh.
