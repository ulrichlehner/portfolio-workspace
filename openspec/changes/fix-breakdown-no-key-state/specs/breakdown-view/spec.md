# Spec Delta

## MODIFIED Requirements

### Requirement: Onboarding and empty states
The view SHALL show one banner for the most relevant state: no API key configured, provider access suspended, no fund held, or empty portfolio. The no-key and suspended banners SHALL offer to open the provider's settings page. Holdings SHALL remain listed with their value in every state; without provider credentials the view SHALL NOT claim that any value is attributed to companies.

#### Scenario: No API key
- **WHEN** the portfolio holds funds or directly held securities and no API key is configured
- **THEN** a banner states that funds and directly held securities are broken down by company only with an API key and opens the provider settings page on request, while the coverage states that no value is attributed to companies.

#### Scenario: Authentication failure
- **WHEN** the provider rejected the configured key
- **THEN** the banner states that access is suspended and offers to open the provider settings page.

#### Scenario: No funds held
- **WHEN** the portfolio holds only directly held securities and an API key is configured
- **THEN** no banner is shown and the view displays the direct breakdown.

### Requirement: Compact data status
The data status pane SHALL list each held fund, and each held security whose classification is still unknown, with its name, a status icon with a short status text, retrieval date and decomposed share. Securities classified as directly held shares SHALL NOT be listed. Attempt, retry, provider refresh, holdings date, freshness, source data and denominator details SHALL remain available in the row tooltip. The pane SHALL keep the session-only notice as a single line.

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
