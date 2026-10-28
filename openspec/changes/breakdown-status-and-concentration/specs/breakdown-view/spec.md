# Spec Delta

## ADDED Requirements

### Requirement: Data status summary row

An always-visible status row SHALL separate the table from the data status pane, SHALL open and close the pane when activated, and SHALL state the current refresh situation in plain words.

#### Scenario: Toggle

- **WHEN** the user activates the row
- **THEN** the data status pane opens or closes, and the row keeps showing the current state.

### Requirement: Status row wording

The row SHALL distinguish running lookups from waiting ones and answered results from usable data. It SHALL NOT describe a running or waiting lookup as loaded or available.

#### Scenario: Refresh running

- **WHEN** a refresh is running and some funds wait for the rate limit
- **THEN** the row states how many lookups run, how many wait and how many are answered, and the pane stays closed if the user closed it.

#### Scenario: Settled

- **WHEN** no lookup is running
- **THEN** the row states how many funds have data and how many have no composition.

### Requirement: Status row warning

When a lookup failed or a composition was rejected, the row SHALL carry a warning marker, name the problem and, when known, state the time of the next attempt.

#### Scenario: Failure

- **WHEN** at least one lookup failed or a composition was rejected
- **THEN** the row shows a warning marker and names the problem and the next attempt time.

## MODIFIED Requirements

### Requirement: Separated data status pane

The chart and table area SHALL be visually separated from the header above and from the data status pane below, so that each reads as a distinct section. The pane SHALL start collapsed unless the user has opened or closed it before; an explicit user choice SHALL be remembered per view and SHALL NOT be overridden by the view. A visible status row SHALL remain between the table and the pane in both states.

#### Scenario: Pane below the table

- **WHEN** the data status pane is open below the chart and table
- **THEN** a visible boundary and spacing separate the two areas in light and dark theme.

#### Scenario: Header above the charts

- **WHEN** the view shows a result
- **THEN** a visible boundary separates the summary and coverage legend from the chart and table.

#### Scenario: First opening

- **WHEN** the view is opened in a workspace that has no stored state for the pane
- **THEN** the pane is collapsed and the status row is visible.

#### Scenario: Stored state

- **WHEN** the user opened or closed the pane earlier
- **THEN** the view restores that state and the status row stays visible.

### Requirement: Concentration summary

The summary SHALL show the concentration as the approximate number of equally sized companies, computed as one divided by the sum of squared shares of each company in the company exposure, together with the number of companies that the value is based on. Its tooltip SHALL explain the calculation with a worked example, state that a smaller value means higher concentration, and name the basis. The summary SHALL also show the largest company with its share of the portfolio value. When a single company exceeds 10 percent of the portfolio value, the attention indicator SHALL name that company and its share.

#### Scenario: Evenly spread

- **WHEN** the company exposure is split evenly across 100 companies
- **THEN** the summary shows a concentration of about 100 companies out of 100 companies.

#### Scenario: Uneven split

- **WHEN** three companies hold 50, 25 and 25 percent of the company exposure
- **THEN** the summary shows a concentration of about 2.67 companies, and the tooltip shows the same calculation next to the evenly split example.

#### Scenario: Dominant company

- **WHEN** one company accounts for 12 percent of the portfolio value
- **THEN** the summary shows it as the largest company and the attention indicator names it with its 12 percent share.
