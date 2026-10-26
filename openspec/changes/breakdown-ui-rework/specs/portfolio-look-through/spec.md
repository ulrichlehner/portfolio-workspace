# Spec Delta

## MODIFIED Requirements

### Requirement: Feature identity
The analysis SHALL be presented as Breakdown (German: Aufschlüsselung) within Portfolio Performance, as a sub-item of Statement of Assets (German: Vermögensaufstellung), with the view title Breakdown by Company (German: Aufschlüsselung nach Unternehmen). It SHALL retain the existing PP application identity and portfolio compatibility rather than requiring a separately branded application.

#### Scenario: Open the analysis
- **WHEN** a user navigates to the look-through analysis
- **THEN** the feature is listed as Breakdown under Statement of Assets within the existing PP application, and the view is titled Breakdown by Company.

#### Scenario: German user interface
- **WHEN** PP runs with the German language
- **THEN** the sidebar shows Aufschlüsselung under Vermögensaufstellung and the view is titled Aufschlüsselung nach Unternehmen.
