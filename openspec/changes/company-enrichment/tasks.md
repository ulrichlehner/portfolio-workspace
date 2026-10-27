# Tasks

## 1. Setup

- [x] 1.1 In `portfolio/`, create `feature/company-enrichment` from `feature/provider-cache-consent`; verify with `git log --oneline -1`

## 2. Core

- [x] 2.1 Add the attribute model (country with source, currency, sector, industry, market cap, retrieval date) and country-name-to-ISO mapping; verify with unit tests including an unmapped name
- [x] 2.2 Parse and return the profile fields from the Eulerpool adapter; verify with a synthetic JSON fixture test
- [x] 2.3 Add the GLEIF client with batched ISIN lookups and strict parsing; verify with synthetic fixture tests for found, not found and malformed responses (no live calls in tests)
- [x] 2.4 Implement country resolution order and ISIN-prefix fallback; verify with tests for register, profile and prefix sources
- [x] 2.5 Implement the enrichment service with value ordering, budget accounting, pending count and the 30-day refresh; verify with tests using a fake clock and fake sources
- [x] 2.6 Implement the versioned enrichment cache honouring the account policy for profiles and always storing register data; verify with round-trip and withdrawal tests

## 3. UI wiring

- [x] 3.1 Schedule enrichment from `LookThroughSession` after each result and expose attributes and pending count to the presenter; verify with a session test
- [x] 3.2 Add the register on/off switch to the provider settings page with translations; verify with a preference page test

## 4. Verification and commit

- [x] 4.1 Run `scripts/dev.sh test` and the Docker UI reactor tests with Checkstyle, scan the diff for private data and create one focused commit (fork 3bf54a19d; 5122 core and 123 UI tests pass)
- [ ] 4.2 With the user's private portfolio copy, check aggregated counts only (companies enriched, by source) and confirm that a restart needs no new requests

## Notes

- GLEIF records do not name the ISIN they matched, so a batch that returns records is resolved with one
  request per ISIN; only empty batches save requests. The first run with thousands of companies therefore
  takes about one request per second (GLEIF data is free and stored permanently); later runs need none.
- Profiles are requested for every constituent with an ISIN, value ordered; "not found" answers are cached for
  30 days. Profile failures from authentication, entitlement or rate limits pause all provider requests.
- Country names from the profile map through JDK English names plus a small alias table (Hong Kong, South
  Korea and similar).
- Switching register lookups off ignores stored register data without deleting it (open data).

## Fixes after the first real-data check (2026-10-27)

- Bar chart resize loop (StackOverflowError), table without source column, "Streuung" wording, title per grouping.
- Enrichment in independent lanes with incremental storage, scoped register lookups (largest 500, typical holding domiciles or deviating profile country), throttled off-thread presentation, backoff and a data status line; companies are pending only while loading continues.
- Request accounting: constituents classified profile-first, profiles shared with enrichment, unused reservations released, revenue keeps headroom for profiles. Estimated first launch about 8 000 to 8 500 budget units instead of about 20 000. Profile-first assumes the profile endpoint returns no sector for funds (unverified).
- Feedback round 3: holdings asset type as classification evidence (fork 861a65bd0), 1:1 split, percent signs, grouping-aware column heading, rank column, overlap as lower triangle, effective number dropped, clickable coverage legend (fork 29352dd7d).
- Round 4: compositions stored as unverified (strict validation rejected all provider compositions), store pruning once per hour and backend/status off the UI thread, rank column filled, effective number restored as "N von M", constituents with ISIN and no classification assumed as companies unless the name indicates a fund/cash/derivative. The holdings assetType field is always empty in real responses, so that change was dropped.
