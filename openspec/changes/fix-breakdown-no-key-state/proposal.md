# Proposal

## Why

Without provider credentials the breakdown view shows a permanent "Checking..." status for every held instrument and a banner that promises directly held companies are already visible. Neither is true: nothing is being checked, and no company attribution exists, because classification requires provider evidence. The view looks stuck and contradicts its own coverage statement of 100% unresolved.

## What Changes

- Add a terminal per-instrument status for "no provider credentials configured", so rows no longer claim progress that never started.
- Distinguish the transient "not retrieved yet" state from a running retrieval in the row text. The running retrieval already has its own state.
- Correct the no-key banner: funds and directly held shares both need the provider, so the banner must not promise direct company attribution without it.
- Correct the two specs that currently require the wrong behavior: direct holdings "visible" without a key, and a row that "states that it is being checked" while nothing checks it.

Out of scope:

- Hiding the view or its navigation entry when no key is configured.
- An onboarding panel replacing the empty chart area.
- Classifying direct holdings locally from names or labels without provider evidence.
- Any change to retrieval, caching, provider policy, quota handling or the portfolio file format.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `breakdown-view`: the onboarding banner and the data status pane no longer claim progress or direct company visibility when no API key is configured.
- `portfolio-look-through`: unresolved exposure names missing provider credentials as its reason and never presents a running check.

## Impact

- `name.abuchen.portfolio.ui` breakdown view: `LookThroughDataStatus`, `LookThroughStatusModel`, `LookThroughView`, and the message bundles in English plus 18 locales.
- No change to the model, composition store, provider adapter or file format.
- The view exists only in the fork, so the change targets the fork branch `fix/breakdown-no-key-state` and does not create an upstream pull request.
