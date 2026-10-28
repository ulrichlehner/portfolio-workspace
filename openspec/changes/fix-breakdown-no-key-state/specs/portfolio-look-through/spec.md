# Spec Delta

## MODIFIED Requirements

### Requirement: Visible analysis limitations
The view SHALL state that current valuations are combined with available composition dates. It SHALL show unresolved exposure alongside results, provide per-source reasons and refresh status, and remain usable without manual uploads. Unsupported economic exposure SHALL NOT be substituted with collateral or a similar index fund.

#### Scenario: Known fund has no usable composition
- **WHEN** an instrument is classified as a fund but its composition is unavailable or unusable
- **THEN** its value remains in the not-yet-decomposed category, with a visible reason distinguishing missing composition, unusable composition and a weight shortfall from missing instrument classification.

#### Scenario: Missing identifier is not cash evidence
- **WHEN** a source row has no usable identifier and no verified asset classification
- **THEN** its value remains unclassified rather than being assigned to cash or other assets merely because an identifier is absent.

#### Scenario: Unsupported synthetic fund
- **WHEN** only a synthetic fund's collateral basket is available
- **THEN** its value remains unresolved with an unsupported-exposure reason, while other validated holdings remain visible.

#### Scenario: Session-only composition storage
- **WHEN** persistent caching is disabled by preference or provider policy
- **THEN** the same validated compositions produce the same exposure results, while the data-status UI explains that reopening PP needs retrieval and offline fund analysis may be unavailable after restart.

#### Scenario: No provider credentials
- **WHEN** no provider credentials are configured
- **THEN** every unclassified position remains in the not-yet-decomposed category with a reason naming the missing credentials, and no row or banner presents a retrieval or a check that has not started.
