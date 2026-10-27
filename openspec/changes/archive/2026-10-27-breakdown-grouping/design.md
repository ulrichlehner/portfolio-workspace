# Design

## Context

The presenter builds `CompanyRow`s with contributions and a `ChartModel` of companies. The engehausen treemap
supports hierarchical models through `ITreeModel`; today the model is flat. PP ships taxonomy templates with
ISO country leaves (`country_XX`) for `regions` and `regions-msci`, and GICS sector labels in
`industry-gics-1st-level`, all translated.

## Goals / Non-Goals

**Goals:**
- One grouping mechanism that serves all attributes, so later groupings are a mapping function each.
- Stable selection keys across grouping changes and enrichment updates.

**Non-Goals:**
- Changing the calculation or the coverage bar.

## Decisions

- **Grouping as a presenter function.** `Grouping` maps a company plus its attributes to a group key and
  label. The presenter builds `GroupRow`s above `CompanyRow`s; Company grouping keeps today's flat rows.
  Alternative: grouping in the engine. Rejected, because grouping is presentation over the same result.
- **Row keys.** Group keys are `group:<grouping>:<code>`, so the existing `RowKey` restore keeps the selection
  when enrichment moves a company from Pending into its group.
- **Templates read, never instantiated.** Load the template definitions to build `country -> category` maps
  once; do not add taxonomies to the client file.
- **Treemap nesting.** Two-level `ITreeModel` (group, company); the renderer draws group tiles with a header
  label and company tiles inside. Clicking the group header area selects the group.
- **Selector.** A drop-down in the existing view toolbar next to the Top N menu; stored in the view
  preferences like the chart kind.

## Risks / Trade-offs

- [Provider sector names differ from GICS] → Unmatched names stay visible as delivered; the mapping table can grow later.
- [Many small groups (industries)] → The bar chart shows the top groups; the table lists all.
- [Pending group dominates on first run] → Value-ordered enrichment fills large companies first; the group label shows the count.
