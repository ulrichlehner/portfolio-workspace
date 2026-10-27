# Spec Delta

## ADDED Requirements

### Requirement: Revenue region grouping
The "Breakdown by" selector SHALL offer "Revenue region". It SHALL show the exposure allocated by revenue per country or region, companies without revenue data in their headquarters country marked as fallback, a "No revenue data" group for companies with neither, and a notice with the shares of company exposure allocated by revenue, by headquarters fallback and without data, plus the range of reporting periods.

#### Scenario: Partial revenue data
- **WHEN** companies covering 80 percent of the company exposure have revenue data
- **THEN** the remaining 20 percent are allocated to headquarters countries as marked fallback where known, and the notice states 80 percent by revenue, the fallback share and the share without data.

#### Scenario: Headquarters and revenue differ
- **WHEN** the user switches between Country and Revenue region
- **THEN** both groupings keep the same total, and the labels make clear that one shows headquarters and the other revenue.
