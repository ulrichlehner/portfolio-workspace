# Spec Delta

## MODIFIED Requirements

### Requirement: Coverage bar
The view SHALL show a horizontal bar that splits the securities value into company exposure, ungrouped equities, cash and other assets, and unresolved value. Segments SHALL be proportional to value, SHALL be labelled in a tooltip with amount and percentage, and SHALL NOT hide a nonzero unresolved remainder through rounding. Its legend SHALL carry a caption naming it as coverage, SHALL list only nonzero categories and SHALL NOT reuse the colors that the charts use for direct and indirect holdings.

#### Scenario: Small unresolved remainder
- **WHEN** the unresolved value is nonzero but below one tenth of a percent
- **THEN** the unresolved segment remains visible with a minimum width and its tooltip shows the exact amount.

#### Scenario: Missing denominator
- **WHEN** the securities denominator cannot be established
- **THEN** the bar is replaced by a short notice that coverage cannot be computed.

#### Scenario: Zero categories
- **WHEN** ungrouped equities and cash or other assets are zero
- **THEN** the coverage legend lists only companies and the remaining nonzero categories.

### Requirement: Company charts
The view SHALL offer a treemap of companies sized by total exposure and a bar chart of the largest companies stacked by direct and indirect exposure. Charts SHALL show only company exposure; unresolved and other categories SHALL stay in the coverage bar. Each chart element SHALL show the company, amount and share in a tooltip. The treemap SHALL group companies too small for a readable tile into one neutral "other companies" tile, SHALL leave no area unpainted, and its legend SHALL be a labelled scale from directly held to held through funds.

#### Scenario: Company held directly and through funds
- **WHEN** a company is held directly and through two funds
- **THEN** its treemap tile shows the combined exposure, and its bar shows separate direct and indirect segments.

#### Scenario: No company exposure
- **WHEN** the result contains no company exposure
- **THEN** the chart area shows an empty-state message instead of empty axes.

#### Scenario: Many small companies
- **WHEN** the result contains hundreds of companies with tiny exposure
- **THEN** the treemap shows the largest companies as tiles and one "other companies" tile whose tooltip names the number of companies, their amount and share, and the chart area contains no blank region.

### Requirement: Linked chart and table selection
Selecting a company in a chart SHALL select, expand and reveal the same company in the table. Selecting a company in the table SHALL highlight it in the visible chart.

#### Scenario: Select a treemap tile
- **WHEN** the user clicks the tile of a company whose row is collapsed
- **THEN** the table selects that company row, expands it to show its contributions and scrolls it into view.

## ADDED Requirements

### Requirement: Separated data status pane
The chart and table area SHALL be visually separated from the data status pane, so that the pane reads as a distinct section rather than a continuation of the table.

#### Scenario: Pane below the table
- **WHEN** the data status pane is open below the chart and table
- **THEN** a visible boundary and spacing separate the two areas in light and dark theme.
