# Spec Delta

## ADDED Requirements

### Requirement: Revenue region grouping
The "Breakdown by" selector SHALL offer "Revenue region". It SHALL show the allocated exposure per country or region, a "No revenue data" group for unallocated companies, and a notice with the share of company exposure that has revenue data and the range of reporting periods.

#### Scenario: Partial revenue data
- **WHEN** companies covering 80 percent of the company exposure have revenue data
- **THEN** the groups show the allocated amounts, "No revenue data" holds the remaining 20 percent, and the notice states the 80 percent coverage.

#### Scenario: Headquarters and revenue differ
- **WHEN** the user switches between Country and Revenue region
- **THEN** both groupings keep the same total, and the labels make clear that one shows headquarters and the other revenue.
