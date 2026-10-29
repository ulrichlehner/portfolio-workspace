# Spec Delta

## ADDED Requirements

### Requirement: Immediate restore from the last result

Within one session, when the view opens for a portfolio whose earlier opening produced a result, the view SHALL show that result immediately instead of the calculating state, also when the portfolio has unsaved changes. It SHALL replace the result when the background calculation finishes. The slot of the valuation date SHALL indicate that an update runs. Without an earlier result, the calculating state stays.

#### Scenario: Return to the view

- **WHEN** the user leaves the view and returns to it without changing the portfolio
- **THEN** the previous result, charts and summary appear at once, the date slot shows that an update runs, and the table is not replaced by the calculating message.

#### Scenario: Updated result arrives

- **WHEN** the background calculation finishes after a return
- **THEN** the new result replaces the shown one and the update indicator disappears.

#### Scenario: Unsaved changes

- **WHEN** the portfolio has unsaved changes and an earlier result exists
- **THEN** the earlier result is shown and replaced when the calculation finishes.

#### Scenario: Other portfolio

- **WHEN** the view opens for a portfolio without an earlier result in this session
- **THEN** the view shows the calculating state.

### Requirement: Stable header controls

The refresh action SHALL stay visible when the grouping or chart selection changes and when the window is narrow. Changing a selection SHALL NOT move the refresh action; only the selectors may collapse into the overflow menu. The grouping selector SHALL name the current grouping in its label and menu.

#### Scenario: Long grouping name

- **WHEN** the user selects a grouping with a long label in a narrow window
- **THEN** the refresh action stays visible and only the selectors move or collapse.

#### Scenario: Switching grouping

- **WHEN** the user switches the grouping back and forth
- **THEN** the grouping selector shows the new grouping, the refresh action keeps its position and no overflow marker appears for the refresh action.

## MODIFIED Requirements

### Requirement: Responsive recalculation

Recalculation SHALL happen only when its inputs change: client data, valuation date, retained compositions or classifications. It SHALL run without blocking user interaction, and several changes in quick succession SHALL produce a single recalculation. A view that opens with a shown earlier result SHALL run one calculation in the background to bring that result up to date.

#### Scenario: Many fund results during one refresh
- **WHEN** a refresh delivers results for many funds in quick succession
- **THEN** the view stays responsive to scrolling and selection and recalculates once per burst instead of once per fund.

#### Scenario: Return with an earlier result
- **WHEN** the view opens with a result from an earlier opening
- **THEN** it shows that result and runs exactly one background calculation for the current inputs.

### Requirement: Compact data status

The data status pane SHALL list each held fund, and each held security whose classification is still unknown, with its name, a status icon with a short status text, retrieval date and decomposed share. Securities classified as directly held shares SHALL NOT be listed. Attempt, retry, provider refresh, holdings date, freshness, source data and denominator details SHALL remain available in the row tooltip. When storage is persistent, the pane SHALL show the storage mode, the company data state and the assumed-company count in one line, and the details of that line SHALL stay in its tooltip. A limitation of persistence SHALL remain a separate, visible warning line.

#### Scenario: Persistent storage and completed company data

- **WHEN** data is stored on this computer and company data is loaded
- **THEN** one line names the storage and the company data with the assumed-company count, and the pane keeps its height with the fund rows visible.

#### Scenario: Session-only storage

- **WHEN** compositions are kept for this session only
- **THEN** a separate warning line names the limitation and the summary line keeps the company data state and the assumed-company count.

#### Scenario: Fund with failed refresh and retained data
- **WHEN** the latest refresh failed and an earlier composition from this session is used
- **THEN** the row shows a warning icon and the earlier retrieval date, and the tooltip names the failure and the original dates.

#### Scenario: Composition rejected by validation
- **WHEN** the provider returned a composition that validation rejects, for example because of negative weights or a total above 100 percent
- **THEN** the row states that the composition was rejected and names the reason in short text, the decomposed share shows a dash instead of zero, and the tooltip explains that the fund stays unresolved.

#### Scenario: Security without provider credentials
- **WHEN** a held security is unclassified and no API key is configured
- **THEN** the row states that no API key is configured and that the security is not broken down, without any progress text, and the row disappears once the security is classified as a directly held share.

#### Scenario: Security not yet classified
- **WHEN** an API key is configured and the first pass has not reached the security yet
- **THEN** the row states that it was not retrieved yet, and the row disappears once the security is classified as a directly held share.

## MODIFIED Requirements

### Requirement: Table columns

The table SHALL show a rank column first for top-level company or group rows by total and name the second column after the selected grouping. Contributions SHALL show their source in the second column below their company. Rows whose total rounds to zero in the currency SHALL be hidden and not ranked.

#### Scenario: Ranked groups

- **WHEN** the user groups by sector
- **THEN** the first column is the rank, the second reads "Sector / company", sectors carry ranks 1, 2, 3 by total, and Unknown, Pending and coverage category rows carry no rank.
