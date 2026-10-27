# Spec Delta

## MODIFIED Requirements

### Requirement: Compact persistence preference
The page SHALL show a confirmation that the user's provider plan allows local storage, the persistence preference as one checkbox, and a single status line. The confirmation SHALL be off by default and SHALL be stored only with Apply or OK. While it is off and provider policy is not verified, the persistence checkbox SHALL be disabled and the status line SHALL name the reason in one sentence. Once it is on, the checkbox SHALL be enabled and default to on.

#### Scenario: Persistence unverified
- **WHEN** the provider's persistence permission is unverified and the confirmation is off
- **THEN** the checkbox is disabled and the status line states that compositions are kept for the session only until local storage is confirmed.

#### Scenario: Local storage confirmed
- **WHEN** the user ticks the confirmation and presses OK
- **THEN** the persistence checkbox is enabled and on, and the status line states that provider data is stored on this computer.

#### Scenario: Confirmation withdrawn
- **WHEN** the user clears the confirmation and presses OK
- **THEN** the account's stored provider data is deleted, the checkbox is disabled, and analysis continues with session-only data.
