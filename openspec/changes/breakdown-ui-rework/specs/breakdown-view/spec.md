# Spec Delta

## Purpose

Defines how the look-through result is presented and operated in the Breakdown view: layout, summary, charts,
onboarding states, refresh actions, data status and interaction behavior.

## ADDED Requirements

### Requirement: Summary before detail
The view SHALL open with a single header line naming the valuation date, followed by a summary of the securities value, the resolved share, the share of the ten largest companies and the number of decomposed funds out of held funds. Explanatory notices SHALL NOT appear as permanent paragraphs; they SHALL be reachable through an indicator with a tooltip or the information pane.

#### Scenario: Partial coverage with unvalidated weights
- **WHEN** the result is partial and contains compositions whose weights are not validated
- **THEN** the summary shows the resolved share, an indicator marks the unvalidated weights, and its tooltip explains the limitation without additional paragraphs above the table.

#### Scenario: Missing valuation
- **WHEN** a held security cannot be valued in the reporting currency
- **THEN** the summary withholds whole-portfolio percentages and the indicator names the missing valuation.

### Requirement: Coverage bar
The view SHALL show a horizontal bar that splits the securities value into company exposure, ungrouped equities, cash and other assets, and unresolved value. Segments SHALL be proportional to value, SHALL be labelled in a tooltip with amount and percentage, and SHALL NOT hide a nonzero unresolved remainder through rounding.

#### Scenario: Small unresolved remainder
- **WHEN** the unresolved value is nonzero but below one tenth of a percent
- **THEN** the unresolved segment remains visible with a minimum width and its tooltip shows the exact amount.

#### Scenario: Missing denominator
- **WHEN** the securities denominator cannot be established
- **THEN** the bar is replaced by a short notice that coverage cannot be computed.

### Requirement: Company charts
The view SHALL offer a treemap of companies sized by total exposure and a bar chart of the largest companies stacked by direct and indirect exposure. Charts SHALL show only company exposure; unresolved and other categories SHALL stay in the coverage bar. Each chart element SHALL show the company, amount and share in a tooltip.

#### Scenario: Company held directly and through funds
- **WHEN** a company is held directly and through two funds
- **THEN** its treemap tile shows the combined exposure, and its bar shows separate direct and indirect segments.

#### Scenario: No company exposure
- **WHEN** the result contains no company exposure
- **THEN** the chart area shows an empty-state message instead of empty axes.

### Requirement: Linked chart and table selection
Selecting a company in a chart SHALL select and reveal the same company in the table. Selecting a company in the table SHALL highlight it in the visible chart.

#### Scenario: Select a treemap tile
- **WHEN** the user clicks the tile of a company
- **THEN** the table selects that company row and scrolls it into view.

### Requirement: Stable selection across updates
Status updates, automatic refresh checks and recalculations SHALL preserve the selected rows, expanded rows and scroll position in the company table and in the data status table, as long as the selected items still exist.

#### Scenario: Automatic refresh check with no new data
- **WHEN** the periodic refresh check runs and no composition changed
- **THEN** neither table is rebuilt and the selection stays unchanged.

#### Scenario: New composition arrives
- **WHEN** a refreshed composition changes the result while a company row is selected and expanded
- **THEN** the same company stays selected and expanded after the update.

#### Scenario: Selected item disappears
- **WHEN** a selected company no longer appears in the new result
- **THEN** the selection is cleared without an error.

### Requirement: Responsive recalculation
Recalculation SHALL happen only when its inputs change: client data, valuation date, retained compositions or classifications. It SHALL run without blocking user interaction, and several changes in quick succession SHALL produce a single recalculation.

#### Scenario: Many fund results during one refresh
- **WHEN** a refresh delivers results for many funds in quick succession
- **THEN** the view stays responsive to scrolling and selection and recalculates once per burst instead of once per fund.

### Requirement: Single refresh action with inline progress
The view SHALL offer one refresh action. While a refresh runs, an inline progress indicator SHALL show completed and total lookups and offer a stop control. Starting or ending a refresh SHALL NOT move the summary, charts or table. The view SHALL NOT show a permanently visible cancel action.

#### Scenario: Refresh in progress
- **WHEN** the user starts a refresh for funds that need constituent lookups
- **THEN** the refresh action is disabled, the progress line shows the counts, and stopping it ends waiting without discarding results already applied.

#### Scenario: No layout shift
- **WHEN** the user starts a refresh and it later completes
- **THEN** the progress appears and disappears in place of the valuation date in the summary row, and no other element of the view changes position.

#### Scenario: Nothing to refresh
- **WHEN** no held fund needs a composition
- **THEN** the refresh action is disabled and no progress line is shown.

### Requirement: Onboarding and empty states
The view SHALL show one banner for the most relevant state: no API key configured, provider access suspended, no fund held, or empty portfolio. The no-key and suspended banners SHALL offer to open the provider's settings page. Direct holdings SHALL remain visible in all states that have holdings.

#### Scenario: No API key
- **WHEN** the portfolio holds funds and no API key is configured
- **THEN** a banner explains that funds can be broken down with an API key and opens the provider settings page on request, while directly held companies are shown.

#### Scenario: Authentication failure
- **WHEN** the provider rejected the configured key
- **THEN** the banner states that access is suspended and offers to open the provider settings page.

#### Scenario: No funds held
- **WHEN** the portfolio holds only direct securities
- **THEN** no key banner is shown and the view displays the direct breakdown.

### Requirement: Compact data status
The data status pane SHALL list each held fund, and each held security whose classification is still unknown, with its name, a status icon with a short status text, retrieval date and decomposed share. Securities classified as directly held shares SHALL NOT be listed. Attempt, retry, provider refresh, holdings date, freshness, source data and denominator details SHALL remain available in the row tooltip. The pane SHALL keep the session-only notice as a single line.

#### Scenario: Fund with failed refresh and retained data
- **WHEN** the latest refresh failed and an earlier composition from this session is used
- **THEN** the row shows a warning icon and the earlier retrieval date, and the tooltip names the failure and the original dates.

#### Scenario: Composition rejected by validation
- **WHEN** the provider returned a composition that validation rejects, for example because of negative weights or a total above 100 percent
- **THEN** the row states that the composition was rejected and names the reason in short text, the decomposed share shows a dash instead of zero, and the tooltip explains that the fund stays unresolved.

#### Scenario: Security not yet classified
- **WHEN** a held security has not been classified yet
- **THEN** the row states that it is being checked, and the row disappears once the security is classified as a directly held share.

### Requirement: Calculating state
Until the first result for the open portfolio is available, the view SHALL show a calculating state that is distinct from every empty state: placeholders in the summary and a calculating message in the chart area and the table. Empty-state messages SHALL appear only for a calculated result.

#### Scenario: Opening the view
- **WHEN** the user opens the view and the first calculation is still running
- **THEN** the summary shows placeholders and the chart area and table state that the breakdown is being calculated, without the "no company exposure" message.
