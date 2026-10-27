# Tasks

## 1. Setup

- [ ] 1.1 In `portfolio/`, create `feature/company-enrichment` from `feature/provider-cache-consent`; verify with `git log --oneline -1`

## 2. Core

- [ ] 2.1 Add the attribute model (country with source, currency, sector, industry, market cap, retrieval date) and country-name-to-ISO mapping; verify with unit tests including an unmapped name
- [ ] 2.2 Parse and return the profile fields from the Eulerpool adapter; verify with a synthetic JSON fixture test
- [ ] 2.3 Add the GLEIF client with batched ISIN lookups and strict parsing; verify with synthetic fixture tests for found, not found and malformed responses (no live calls in tests)
- [ ] 2.4 Implement country resolution order and ISIN-prefix fallback; verify with tests for register, profile and prefix sources
- [ ] 2.5 Implement the enrichment service with value ordering, budget accounting, pending count and the 30-day refresh; verify with tests using a fake clock and fake sources
- [ ] 2.6 Implement the versioned enrichment cache honouring the account policy for profiles and always storing register data; verify with round-trip and withdrawal tests

## 3. UI wiring

- [ ] 3.1 Schedule enrichment from `LookThroughSession` after each result and expose attributes and pending count to the presenter; verify with a session test
- [ ] 3.2 Add the register on/off switch to the provider settings page with translations; verify with a preference page test

## 4. Verification and commit

- [ ] 4.1 Run `scripts/dev.sh test` and the Docker UI reactor tests with Checkstyle, scan the diff for private data and create one focused commit
- [ ] 4.2 With the user's private portfolio copy, check aggregated counts only (companies enriched, by source) and confirm that a restart needs no new requests
