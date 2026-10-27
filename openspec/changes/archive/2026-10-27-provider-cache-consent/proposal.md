# Proposal

## Why

Fund compositions and instrument classifications are fetched again in every PP session, because the
provider policy is hardcoded as "unverified" and the session only uses the in-memory store. The disk store,
its versioning and the opt-out preference already exist but are never used. The user decided on 2026-10-27
that provider data shall be stored locally on their own machine (recorded in AGENTS.md). The planned company
enrichment needs thousands of provider requests and is only practical with a local cache.

## What Changes

- The provider settings page gets a confirmation per account: "My plan allows storing provider data locally".
  It is off by default and stored with OK or Apply.
- With the confirmation set, the account's persistence policy is "permitted"; without it, it stays
  "unverified". The existing persistence checkbox becomes enabled and defaults to on.
- The Breakdown session uses the existing versioned disk store in PP's workspace state area, so validated
  compositions and instrument classifications survive a restart. Session-only operation stays unchanged when
  the confirmation or the preference is off.
- Withdrawing the confirmation or switching the preference off deletes the account's stored data, as the
  existing withdrawal requirement demands.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `fund-compositions`: "Licensed local use" and "Development permission assumption" allow real-data
  persistence after the user's explicit per-account confirmation instead of requiring verified permission.
- `composition-provider-settings`: "Compact persistence preference" gains the confirmation control.

## Impact

- Core: provider policy derived from the confirmation; classification cache made storable.
- UI: `EulerpoolPreferencePage`, `LookThroughSession`, `LookThroughCompositionService`, messages.
- Delivery: one focused commit on `feature/provider-cache-consent`, stacked on `feature/breakdown-chart-polish`.

## Out of scope

- Company profile and GLEIF caches (planned in `company-enrichment`).
- Retention limits other than the provider's; no maximum age is introduced.
- Verifying the provider's terms; distributing provider payloads.
