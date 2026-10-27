# Spec Delta

## MODIFIED Requirements

### Requirement: Conservative numerical validation
The system SHALL preserve source rows and use decimal weights without general normalization. Malformed, nonfinite, negative or overfull weights SHALL make a snapshot unusable, except for an evidenced rounding excess of at most one millionth in fractional-weight units, and except for negative rows without a security identifier whose netting is described below. Accepted excess SHALL be removed proportionally with exact reconciliation. Positive shortfalls SHALL remain unresolved. Legitimate duplicate rows SHALL only be combined after validating their semantics. Within one snapshot, rows without a security identifier SHALL be netted against each other when no row with an identifier is negative; a zero or positive net SHALL stay unresolved as one netted amount, a negative net SHALL make the snapshot unusable. Netting SHALL NOT classify any row by its name, rescale any identified row or change the source rows, and SHALL be recorded as a non-fatal diagnostic.

#### Scenario: Signed or overfull response
- **WHEN** a response contains a negative allocation on a row with a security identifier, a negative net of rows without an identifier, or a total above 100% beyond the rounding tolerance
- **THEN** the system retains diagnostic source information and leaves the fund unresolved rather than dropping rows or rescaling it.

#### Scenario: Provider rounding excess
- **WHEN** published weights sum to 100.00000001% because of decimal rounding
- **THEN** the rows remain eligible for classification after a proportional correction within the tolerance, reconcile exactly to the fund value and keep a zero shortfall, while the original source rows remain unchanged.

#### Scenario: Tiny positive shortfall
- **WHEN** valid nonnegative weights sum to less than 100% by an amount that rounds to zero in the display
- **THEN** the exact shortfall remains unresolved and is not normalized away or treated as complete coverage.

#### Scenario: Legitimate duplicate positions
- **WHEN** two nonnegative positions represent the same verified instrument within a valid NAV composition
- **THEN** both contributions are retained in the calculation rather than discarding one by identifier.

#### Scenario: Negative cash and currency rows without identifier
- **WHEN** a composition sums to 100%, all identified rows are nonnegative, and its rows without an identifier are +0.05% and -0.015% of the fund
- **THEN** the identified rows keep their exact weights and are eligible for classification, the identifier-less rows become one unresolved amount of +0.035%, the fund reconciles exactly, the source rows stay unchanged, and a netting diagnostic is recorded.

#### Scenario: Negative net without identifier
- **WHEN** the rows without an identifier sum to a negative amount
- **THEN** the snapshot is unusable and the fund stays unresolved with the negative-weight reason.

#### Scenario: Short position with identifier
- **WHEN** a row with a security identifier has a negative weight
- **THEN** the snapshot is unusable even if identifier-less rows could absorb the amount.
