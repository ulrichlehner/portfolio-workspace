# development-portfolio-testing Specification

## Purpose

Enable private testing of local macOS Portfolio Performance builds against fresh WebDAV portfolio copies without changing the production portfolio.

## Requirements

### Requirement: Identifiable local macOS build
The workflow SHALL build PP in Docker with a bundled runtime and launch the matching local macOS application in an isolated development workspace. It SHALL identify the source revision and dirty state used for the build and reject missing, architecture-incompatible or outdated builds rather than silently testing another build.

#### Scenario: Source changed after build
- **WHEN** the source state differs from the recorded build state
- **THEN** managed launch requests a rebuild rather than silently starting that artifact.

### Requirement: One-way source protection
The managed workflow SHALL retrieve the configured WebDAV file using only GET and HEAD over verified HTTPS and a server-side read-only credential. It SHALL NOT upload, delete, rename or lock remote resources. The app SHALL receive a separate regular local copy, without WebDAV credentials, production mounts or production recent-file history.

#### Scenario: Local save
- **WHEN** the user edits and saves the managed development portfolio
- **THEN** only the local development copy changes and no write request is sent to WebDAV.

#### Scenario: Read-only access unavailable
- **WHEN** setup cannot establish server-side read-only access
- **THEN** managed WebDAV testing remains blocked without probing the source with write operations or using production write credentials.

### Requirement: Refresh before launch
Each managed online launch SHALL check the remote source and prepare a development copy from the latest successfully retrieved version. Conditional retrieval SHALL reuse only an untouched remote baseline, never an edited working copy. The workflow SHALL show last successful source-check time separately from download time and build identity.

#### Scenario: Remote unchanged but local edited
- **WHEN** the server reports unchanged content and the previous development copy contains local edits
- **THEN** the next working copy is created from the untouched baseline and previous edits remain recoverable.

### Requirement: Independent remote saves
Periodic saves by other applications SHALL be allowed. A coherent successfully
retrieved snapshot SHALL be sufficient for testing; equality between separate
remote downloads and continuous synchronization SHALL NOT be required.

#### Scenario: Remote automatically saved during local testing
- **WHEN** another application periodically saves the remote portfolio
- **THEN** the current local test copy remains fixed until the next managed
  refresh, subsequent coherent snapshots may differ, and this workflow sends
  no remote write requests.

### Requirement: Preserve previous test data
Successful refresh SHALL preserve the immediately preceding development portfolio and associated local settings/backups before activating its replacement. Older generations SHALL be pruned only after successful refresh under a disclosed retention policy, with an explicit option to retain a generation longer. Local test edits SHALL never be merged into the remote source.

#### Scenario: New remote version available
- **WHEN** a valid replacement is ready
- **THEN** the prior development generation remains recoverable and the new local copy reflects the remote version.

### Requirement: No replacement during testing
The workflow SHALL prevent concurrent managed launches and portfolio refresh while the development instance is running. A running instance SHALL keep its current local data until exit; freshness SHALL mean source state checked at launch, not continuous synchronization.

#### Scenario: Launch requested twice
- **WHEN** a managed test instance is still running
- **THEN** the second launch stops without replacing its portfolio or starting a competing instance.

### Requirement: Safe failed refresh
Failed authentication, TLS, transfer or file validation SHALL preserve the prior baseline and development generation and abort normal launch. Explicit offline launch SHALL use retained local data with a stale-data notice. The workflow SHALL support PP file containers and preserve encrypted data without persisting its password or claiming decrypted content validation before successful opening.

#### Scenario: HTML error response
- **WHEN** a download returns an error page instead of a supported portfolio file
- **THEN** it is rejected and neither the baseline nor the previous test copy is replaced.

#### Scenario: Encrypted portfolio cannot open
- **WHEN** PP cannot open a newly downloaded encrypted portfolio
- **THEN** the user can recover the prior local generation and no source data is modified.

### Requirement: Private configuration and cleanup
URLs, credentials, portfolios and private manifests SHALL stay outside tracked files and public logs. The workflow SHALL reject destination symlinks or paths escaping managed private storage and SHALL NOT forward credentials through redirects. Ordinary build cleanup SHALL preserve local portfolio generations; explicit test-data cleanup SHALL remove only managed private test data.

#### Scenario: Build cleaned
- **WHEN** build outputs and the development application workspace are cleaned
- **THEN** the retained portfolio generations remain available for the next test launch.

#### Scenario: Unsafe destination
- **WHEN** a configured destination resolves outside managed private storage or links to another file
- **THEN** refresh fails before writing it.
