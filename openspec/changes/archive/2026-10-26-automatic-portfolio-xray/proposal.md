# Proposal

## Why

Portfolio Performance should reveal current company exposure across directly held shares and fund constituents. Automatic composition retrieval would make this useful without recurring file uploads, while replaceable providers would avoid dependence on a single data vendor.

## What Changes

- Name the feature **Portfolio Lens** within Portfolio Performance. Retain the existing OpenSpec change identifier and PP application identity.
- Introduce current portfolio look-through with direct and indirect contributions and visible unresolved exposure.
- Accept transparent partial coverage for the first release while retaining 100% validated coverage as the ultimate objective. Outstanding gaps must remain tracked through later changes rather than being dismissed when the first release is complete.
- Retrieve fund compositions automatically using individually configured provider credentials; prioritize free or affordable personal access.
- Separate provider adapters, composition validation, instrument identity resolution and exposure calculations.
- Make persistent composition caching an opt-out preference per provider/account where permitted. Keep analysis functional with session-only data when the user disables persistence or provider policy prohibits it or leaves permission unverified; disclose restart and offline limitations.
- Show source, available dates, coverage and failures without treating a successful response or a 100% weight sum as proof of completeness.
- Use Eulerpool as the initial provider, as selected during exploration. Retain Leeway and paid alternatives in the research record and keep the provider interface replaceable. Selection does not waive remaining licensing or data-quality release gates.
- Analyze current positive-value securities, excluding account cash from the clearly labelled denominator. Refresh automatically at most once per day per fund while PP runs, with a quota-aware manual refresh.
- Define testable incomplete-data behaviour and gated implementation tasks. Permission is assumed for development only. The user permits experimental source-only publication in their development fork with an explicit notice; this does not verify provider rights. Official upstream integration and binary releases still require permission and data-quality review. Real-data disk persistence stays disabled until permission and retention are verified.
- Provide local macOS test builds with an isolated development portfolio refreshed from WebDAV before each test launch. Preserve the previous local copy and never write back to the source.

Out of scope for the first release: historical exposure reconstruction, manual uploads as a required workflow, a centrally operated redistribution service, trading recommendations, and general derivatives risk analytics. Sector/country and overlap views are potential follow-ups rather than confirmed first-release scope.

## Capabilities

### New Capabilities

- `fund-compositions`: Automatic provider retrieval, validation, provenance, freshness and coverage of fund compositions.
- `portfolio-look-through`: Current direct and indirect company exposure with traceable contributions and explicit unresolved portions.
- `development-portfolio-testing`: Local macOS testing against a safely refreshed, private WebDAV copy, with source protection and recoverable local test changes.

### Modified Capabilities

None. The existing OpenSpec capability inventory is empty.

## Impact

Expected integration areas are the core model, online provider infrastructure, portfolio snapshots and reporting UI. Existing ClientSnapshot valuations and ServiceLoader-based feed discovery are useful foundations; weighted classifications are not a substitute for dated composition records.

Plan focused upstream increments: composition/calculation foundations, a validated provider integration, then reporting UI. Additional providers should be separate contributions. This change currently authorizes planning only.

Repository coding and contribution rules remain binding throughout planning, implementation and review. The design records the applicable sources and validation gates; OpenSpec does not replace them.

The test launcher, WebDAV retrieval and their tests/documentation belong in this workspace, not upstream PP. Reuse the Docker build and bundled-runtime macOS launch flow. Bidirectional synchronization, production portfolio editing, and live replacement during a test session are out of scope.
