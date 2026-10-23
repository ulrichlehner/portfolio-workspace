## Purpose

Provide automatic, replaceable sources of fund compositions with validated semantics, provenance and visible limitations for portfolio exposure analysis.

## ADDED Requirements

### Requirement: Automatic provider access
The system SHALL retrieve compositions automatically after individual credential configuration, initially through Eulerpool. Provider substitution SHALL preserve the exposure contract. Routine use SHALL NOT require file uploads, manual constituent mapping or a shared application key.

#### Scenario: Configured fund retrieval
- **WHEN** a configured user opens an analysis containing an eligible fund
- **THEN** the system schedules eligible retrieval and reports its status without requesting a holdings file.

### Requirement: Licensed local use
Provider release SHALL require verified permission for individual desktop display, adapter distribution with user-supplied keys, and the intended local retention. Persistent storage SHALL NOT be implemented before its permission is established. Incompatible terms SHALL require product review, without automatic subscription purchase.

#### Scenario: Free cache permission unresolved
- **WHEN** API access succeeds but free local caching permission remains unverified
- **THEN** persistent provider storage and provider release remain gated despite successful access.

### Requirement: Credential and portfolio privacy
The system SHALL keep credentials outside portfolio files, exports and logs, using secure local storage or session-only entry. Requests SHALL contain only identifiers needed for retrieval or bounded enrichment, never quantities, balances or transactions.

#### Scenario: Credential storage unavailable
- **WHEN** secure storage cannot be used
- **THEN** the system offers session-only entry without silently persisting the key in plaintext settings.

### Requirement: Independent provenance dates
Every composition SHALL identify its source, fund, retrieval time, available provider refresh time and available holdings-effective date. Missing dates SHALL remain unknown. Retrieval or provider refresh time SHALL NOT stand in for the holdings-effective date.

#### Scenario: Effective date absent
- **WHEN** a recently fetched response lacks a holdings-effective date
- **THEN** the result shows holdings date unavailable separately from retrieval and provider refresh times.

### Requirement: Verified allocation semantics
Only validated fractions of total fund NAV with a supported exposure basis SHALL enter exposure totals. Unknown denominators, normalized top-only weights, synthetic collateral substitutes and unsupported derivatives SHALL leave the affected fund unresolved. A weight sum of 100% SHALL NOT prove completeness.

#### Scenario: Top holdings normalized to 100 percent
- **WHEN** returned weights sum to 100% but their total-fund denominator is unverified
- **THEN** the entire fund remains unresolved in aggregated exposure, even if a separate source preview is available.

#### Scenario: Valid partial NAV fractions
- **WHEN** verified nonnegative rows account for 80% of total fund NAV
- **THEN** those rows are eligible for classification and the remaining 20% stays unresolved without normalization.

### Requirement: Conservative numerical validation
The system SHALL preserve source rows and use decimal weights without normalization. Nonfinite or malformed weights, totals exceeding 100%, and any negative allocation SHALL make a snapshot unusable for first-version exposure calculation. Legitimate duplicate instrument rows SHALL only be combined after validating their semantics. Positive shortfalls SHALL remain unresolved, regardless of display rounding.

#### Scenario: Signed or overfull response
- **WHEN** a response contains a negative allocation or a total above 100%
- **THEN** the system retains diagnostic source information and leaves the fund unresolved rather than dropping rows or rescaling it.

#### Scenario: Legitimate duplicate positions
- **WHEN** two nonnegative positions represent the same verified instrument within a valid NAV composition
- **THEN** both contributions are retained in the calculation rather than discarding one by identifier.

### Requirement: Bounded automatic identity resolution
The system SHALL attempt automatic classification and identity resolution within provider budgets. Missing or ambiguous identity SHALL remain explicit. Names alone SHALL NOT establish instrument equivalence or company grouping, and an ISIN alone SHALL NOT establish equity classification.

#### Scenario: Identity cannot be established
- **WHEN** permitted automatic resolution cannot establish a constituent's identity or asset type
- **THEN** its contribution remains unresolved with its source label and reason, without requiring user mapping.

### Requirement: Refresh scheduling and quota handling
Automatic refresh SHALL occur at most once per rolling 24 hours per fund while PP runs. Manual refresh SHALL respect provider quotas and coalesce concurrent requests. Redrawing a view SHALL NOT trigger retrieval. Rate limits SHALL cause backoff, and authentication or entitlement failures SHALL suspend requests until configuration changes.

#### Scenario: Manual refresh during rate limiting
- **WHEN** a user requests refresh before a provider retry deadline
- **THEN** the system reports the deferred status without sending another request or buying quota.

#### Scenario: Application closed
- **WHEN** PP is not running
- **THEN** no automatic refresh is performed by this feature.

### Requirement: Last valid data and retention
Failed retrieval or validation SHALL NOT replace an existing usable snapshot with empty or invalid data. Licensed retained data SHALL remain available with visible age and failure status only within permitted retention. Different sources or vintages SHALL NOT be silently blended.

#### Scenario: Failed refresh with retained data
- **WHEN** refresh fails and a previous valid snapshot is within permitted retention
- **THEN** the system uses that snapshot with a failed-refresh status and its original dates.

#### Scenario: Retention expires
- **WHEN** retained data reaches its permitted retention limit
- **THEN** the system deletes it and marks affected exposure unresolved until usable data is retrieved.
