## Purpose

Explain current company exposure across direct securities and fund constituents while preserving traceable contributions and the objective of complete validated coverage.

## ADDED Requirements

### Requirement: Feature identity
The analysis SHALL be presented as Portfolio Lens within Portfolio Performance. It SHALL retain the existing PP application identity and portfolio compatibility rather than requiring a separately branded application.

#### Scenario: Open the analysis
- **WHEN** a user navigates to the look-through analysis
- **THEN** the feature is labelled Portfolio Lens within the existing PP application.

### Requirement: Current securities scope
The analysis SHALL use current PP valuations in the reporting currency for selected positive-value securities. Percentages SHALL use that selected securities value as denominator, explicitly excluding account cash. Zero positions SHALL contribute nothing. Unsupported negative positions SHALL be disclosed as excluded rather than silently changing the denominator.

#### Scenario: Accounts and closed positions
- **WHEN** the selection contains positive securities, an account cash balance and a zero position
- **THEN** only positive securities enter the denominator, and the view labels the account-cash exclusion.

#### Scenario: Negative position
- **WHEN** the selection includes a negative position
- **THEN** the view identifies the excluded unsupported position and does not claim complete coverage of the entire selection.

### Requirement: Missing valuation visibility
Missing valuation or currency conversion SHALL make the analysis explicitly incomplete. The system SHALL NOT substitute zero or show a whole-selection coverage percentage when its denominator cannot be established.

#### Scenario: Missing exchange rate
- **WHEN** a selected security cannot be valued in the reporting currency
- **THEN** the system identifies the missing valuation and withholds whole-selection percentages while allowing clearly labelled valued-subset results.

### Requirement: Company aggregation and provenance
The system SHALL aggregate verified direct and indirect contributions by company and show their separate and combined values and percentages. Indirect contributions SHALL equal parent value multiplied by validated weights along the contribution path. Users SHALL be able to inspect originating holdings and composition provenance without creating owned securities for constituents.

#### Scenario: Direct share and fund overlap
- **WHEN** a verified company is held directly and through two funds
- **THEN** its combined exposure includes all three contributions, with each source inspectable and no additional parent-fund exposure counted.

### Requirement: Unresolved exposure conservation
Unavailable or unusable compositions SHALL leave the entire affected fund unresolved. Usable partial compositions SHALL retain their unresolved remainder. Unknown identity or classification SHALL leave the affected contribution unresolved. The system SHALL NOT normalize resolved contributions to conceal missing exposure.

#### Scenario: Mixed coverage
- **WHEN** a synthetic selection consists of 60% fully resolved direct equity and 40% a fund with only half its NAV validated and grouped
- **THEN** resolved company exposure is 80% and unresolved exposure is 20% of the full securities denominator.

### Requirement: Separate coverage categories
The view SHALL reconcile selected value across verified company contributions, identified equities with unverified company grouping, validated cash/other assets and unresolved portions. Unknown asset types SHALL remain unresolved. Coverage and composition freshness SHALL be reported separately; rounding SHALL NOT turn a nonzero unresolved remainder into a complete-coverage claim.

#### Scenario: Fund cash and ungrouped shares
- **WHEN** a fund contains verified cash and an identified equity whose company grouping is unknown
- **THEN** cash remains cash/other assets, the equity remains ungrouped, and neither is reported as fully grouped company exposure.

### Requirement: Bounded nested look-through
Nested funds SHALL be decomposed only with usable compositions. Cycles and branches beyond eight composition edges SHALL stop at the affected branch and preserve its value as unresolved. Repeated legitimate paths SHALL remain distinct contributions before company aggregation.

#### Scenario: Cyclic fund branch
- **WHEN** a nested composition refers to a fund already present on its current path
- **THEN** only that branch becomes unresolved with a cycle reason and all other validated branches remain usable.

### Requirement: Visible analysis limitations
The view SHALL state that current valuations are combined with available composition dates. It SHALL show unresolved exposure alongside results, provide per-source reasons and refresh status, and remain usable without manual uploads. Unsupported economic exposure SHALL NOT be substituted with collateral or a similar index fund.

#### Scenario: Unsupported synthetic fund
- **WHEN** only a synthetic fund's collateral basket is available
- **THEN** its value remains unresolved with an unsupported-exposure reason, while other validated holdings remain visible.

### Requirement: Durable complete-coverage objective
The ultimate objective SHALL remain 100% validated coverage of the declared scope. A partial first release SHALL NOT close it. Every outstanding coverage gap SHALL retain its category, missing evidence, proposed remedy and verification criterion in a maintained register. Release and archive review SHALL carry unresolved gaps into linked follow-up records and preserve this requirement in durable specs.

#### Scenario: Partial release accepted
- **WHEN** a first release passes its partial-coverage acceptance checks with unresolved funds or unverified company grouping
- **THEN** the release can be accepted as partial only, with the gaps retained and linked to follow-up records before archive.

#### Scenario: Complete coverage claimed
- **WHEN** all selected value is numerically allocated but some identities, classifications or exposure bases remain unverified
- **THEN** the system does not claim 100% validated coverage.

### Requirement: Existing portfolio compatibility
Enabling, disabling or removing look-through SHALL NOT modify transactions, owned securities or the portfolio file format. Unavailable or incompatible derived data SHALL be safely discarded and shown as unavailable until retrieved again.

#### Scenario: Cache incompatible after update
- **WHEN** existing derived composition data cannot be read by the current version
- **THEN** the portfolio remains usable, the incompatible data is discarded, and affected exposure is unresolved until a usable replacement is obtained.
