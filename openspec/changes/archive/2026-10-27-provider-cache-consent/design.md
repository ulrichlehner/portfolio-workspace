# Design

## Context

`CompositionPersistencePolicy` already models permitted, prohibited and unverified persistence, and
`VersionedCompositionStore` implements generation-safe disk storage with withdrawal cleanup. The Eulerpool
provider returns a hardcoded unverified policy, and `LookThroughSession` always creates a
`SessionCompositionStore`. Classification evidence is cached in memory inside the session.

## Goals / Non-Goals

**Goals:**
- Turn on the existing disk path with the smallest change, driven by an explicit user confirmation.
- Keep every existing guarantee: withdrawal deletes data, pending jobs cannot recreate it, other providers stay independent.

**Non-Goals:**
- A new storage format or cache for enrichment data.
- Any statement that the provider's terms are verified.

## Decisions

- **Confirmation as a preference, not as a constant.** Stored per provider account next to the existing
  persistence preference. The provider's `getPersistencePolicy` reads it: confirmed means `PERMITTED`
  without a maximum age, otherwise `UNVERIFIED`. Alternative considered: hardcoding `PERMITTED` in the fork.
  Rejected, because the upstream code must not claim a permission for every user.
- **Always construct the versioned store.** `LookThroughSession` uses `VersionedCompositionStore` under PP's
  workspace state location (`.metadata/.plugins/<ui bundle>/lookthrough-cache`). Session-only behaviour is
  already what that store does while the effective mode is session-only, so no second code path is needed.
- **Classifications use the same store.** Instrument evidence is stored with the compositions so that a
  restart does not repeat classification requests. If the store's codec cannot hold evidence yet, add it to
  `CompositionCacheCodec` with its own record type and version.
- **Wording.** The confirmation text names the user's own responsibility ("My Eulerpool plan allows storing
  data locally"); no legal claim.

## Risks / Trade-offs

- [The user's plan may not allow storage] → Off by default, explicit per account, wording places the decision with the user.
- [Cache corruption or a format change] → The versioned codec rejects unknown versions and the data is fetched again.
- [Stale compositions] → Existing refresh scheduling and visible provenance dates stay in force.

## Migration Plan

No migration: existing users have no stored data. Rollback is removing the confirmation, which deletes the cache.
