# Proposal

## Why

The first use of the Breakdown view with a real portfolio showed four rough edges: clicking a treemap tile
selects the company row but leaves its contributions collapsed; the coverage legend and the chart legend use
the same blue and green for different meanings, so it is unclear which legend belongs to what; the treemap
draws hundreds of tiles too small to read, ending in a white sub-pixel area at the bottom right; and the data
status pane is not visually separated from the chart and table above.

## What Changes

- A click on a company in a chart selects, expands and reveals its table row.
- The coverage legend gets its own caption, lists only nonzero categories and no longer uses green; the
  treemap legend becomes a labelled direct-to-funds color scale, so green and blue in the chart only mean
  "held directly" and "held through funds".
- The treemap shows the largest companies as tiles and groups the rest into one neutral "Other companies"
  tile with count, amount and share in its tooltip; no area of the chart stays unpainted.
- The chart and table area is visually separated from the data status pane.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `breakdown-view`: requirements "Coverage bar", "Company charts" and "Linked chart and table selection"
  change; a requirement for the visual separation of the data status pane is added.

## Impact

- UI bundle only: `views/lookthrough/` (coverage bar, header, chart pane, treemap, view) and message files.
- Delivery: one focused commit on `feature/breakdown-chart-polish`, stacked on `fix/signed-cash-rows`.

## Out of scope

- Changes to PP's shared information pane used by other views.
- Calculation, provider or validation changes.
