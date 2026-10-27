# Spec Delta

## MODIFIED Requirements

### Requirement: Percent signs outside percent columns
Shares SHALL carry a percent sign wherever they are shown: in the summary, the coverage legend and tooltips, the chart labels, treemap group headers and tooltips, and the share column of the table.

#### Scenario: Summary and legend
- **WHEN** the summary shows the assigned share and the top ten share and the coverage legend shows its categories
- **THEN** each share is followed by a percent sign, as are the values in the table's share column.

## ADDED Requirements

### Requirement: Table columns
The table SHALL name its first column after the selected grouping, show a rank for top-level company or group rows by total, and show each contribution's source in the first column below its company. Rows whose total rounds to zero in the currency SHALL be hidden and not ranked.

#### Scenario: Ranked groups
- **WHEN** the user groups by sector
- **THEN** the first column reads "Sector / company", sectors carry ranks 1, 2, 3 by total, and Unknown, Pending and coverage category rows carry no rank.

### Requirement: Grouping selector
The view SHALL offer a "Breakdown by" selector with Company, Country, Region, Market classification, Sector, Industry and Currency. Company SHALL be the default. The selection SHALL be remembered per view and SHALL NOT trigger provider requests.

#### Scenario: Switch to country
- **WHEN** the user selects Country
- **THEN** the table, treemap and bar chart show countries, using the current result and stored attributes only.

### Requirement: Group rows
For every grouping except Company, the table SHALL show one row per group with direct, indirect and total value and share. A group row SHALL expand into its companies, and the companies SHALL keep their contributions. The group totals SHALL add up to the company exposure of the result.

#### Scenario: Country totals
- **WHEN** the result contains companies headquartered in two countries
- **THEN** each country row shows the sum of its companies, and both rows together equal the company exposure.

### Requirement: Unknown and pending groups
Companies without the selected attribute SHALL be shown in an "Unknown" group, and companies whose enrichment is still pending in a "Pending" group. Both groups SHALL show their count in the label.

#### Scenario: Enrichment running
- **WHEN** the user groups by sector while enrichment of the smaller companies is still running
- **THEN** the enriched companies appear in their sectors, the others in "Pending", and the groups update as enrichment completes without losing the selection.

### Requirement: Grouped charts
For every grouping except Company, the treemap SHALL show groups as tiles with their companies nested inside, and the bar chart SHALL show the largest groups split into direct and indirect value with amount and share next to each bar. Selecting a group in a chart SHALL select and expand it in the table.

#### Scenario: Select a country tile
- **WHEN** the user clicks the area of a country in the treemap outside any labelled company
- **THEN** the table selects and expands that country row.

### Requirement: Standard classifications
Regions and market classification SHALL use PP's region taxonomy templates, mapping each country code to its template category. Sectors SHALL map provider sector names to PP's GICS sector template by name; unmatched names SHALL be shown as delivered. The country source SHALL be visible in the country tooltip.

#### Scenario: Country not in template
- **WHEN** a company's country is not listed in the region template
- **THEN** the company appears in the "Unknown" region group and keeps its country in the country grouping.
