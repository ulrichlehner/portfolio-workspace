# Spec Delta

## MODIFIED Requirements

### Requirement: Licensed local use
Official upstream integration and binary releases SHALL require verified desktop-use and adapter-distribution permissions. An explicitly authorized experimental source-only development fork MAY be published with a notice of unverified rights and data quality; the notice SHALL NOT claim to grant rights or transfer legal responsibility. Real-data persistence SHALL require either verified permission or the user's explicit confirmation for the provider account that local storage is allowed. Without either, persistence SHALL remain disabled.

#### Scenario: Free cache permission unresolved
- **WHEN** API access succeeds, local caching permission is unverified and the user has not confirmed local storage for the account
- **THEN** persistence remains disabled, session-only operation is available under the recorded development assumption, and official integration or binary release still requires the separate permission and data-quality gates.

#### Scenario: User confirms local storage
- **WHEN** the user confirms for a provider account that local storage is allowed and keeps the persistence preference on
- **THEN** validated compositions and classifications of that account are stored on disk and are available after a restart without new provider requests.

### Requirement: Development permission assumption
Implementation and local development MAY proceed under an explicitly recorded development-only assumption of runtime/display and adapter distribution permission. That assumption SHALL NOT establish verified permission or satisfy the pre-publish permission checklist. Real-data disk persistence SHALL follow the user's per-account confirmation, not the assumption itself.

#### Scenario: Development permission assumed
- **WHEN** development proceeds under the recorded permission assumption and the user has not confirmed local storage
- **THEN** real provider data remains session-only, and official integration or binary release remains blocked until runtime/display, adapter distribution and applicable attribution obligations are verified.

#### Scenario: Authorized experimental source fork
- **WHEN** the user explicitly authorizes source-only publication of the development fork before provider clarification
- **THEN** the fork includes an experimental-use notice, distributes no provider payloads or credentials, and leaves permission and data-quality gates open; the notice does not assert that provider rights are verified or responsibility has legally transferred.
