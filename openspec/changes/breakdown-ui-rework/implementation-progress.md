# Implementation progress

Fork branch `feature/breakdown-ui-rework`, stacked on `feature/automatic-portfolio-xray`.
Commits are local until the first push is confirmed.

## Verification method

`scripts/dev.sh test` builds only the core modules. UI changes are verified through the
Docker UI reactor (core, REST, UI, bootstrap, UI tests, build-tools-check, Checkstyle on)
with the look-through and Eulerpool preference test classes, using a clean `git archive`
export where other work was still uncommitted. The helper used is
`scratch/ui-verify.sh <tree> <log>` (private, not committed).

## Increments

| Increment | Commit | Verification |
| :--- | :--- | :--- |
| B rename and placement | `b42b770cf` | core: 5080 tests, BUILD SUCCESS, Checkstyle clean; UI reactor: 72 tests passed |
| C settings page | `5073178f8` | UI reactor on B + C: 77 tests passed; restored a message key still used by the status pane |
| A responsiveness and selection | `7c2b119ff` | UI reactor: 86 tests passed, Checkstyle clean in 7 modules |
| D layout, onboarding, status pane | `c444a4b22` | UI reactor: 100 tests passed, Checkstyle and message checks clean; app build succeeded |

## Outstanding manual checks

- 2.4 selection and expansion survive a 60-second check and an incoming fund result.
- 3.3 German sidebar Vermögensaufstellung > Aufschlüsselung, view title.
- 4.4 disabled persistence checkbox with a one-sentence reason.
- 5.3 to 5.5 summary strip, coverage bar and banners in light and dark theme and at narrow
  widths; no-key banner opens the Eulerpool settings and disappears after a key is saved;
  stop control ends progress and keeps applied results.
- Computer-use access to the dev app was declined on 2026-10-26, so visual checks are done
  by the user.

## Notes for review

- Settings: a failed `replaceSecure` (storage unavailable) has already removed the previously
  stored key, because the core credential API deletes before it writes. Pre-existing behavior,
  not changed here; candidate follow-up.
- Settings: whitespace-only input is rejected as invalid rather than treated as empty.
- Status pane: `FundStatus` contains an age derived from the clock, so equal-model skipping
  rarely applies; selection is still kept by fund reference.
- Banner: without a key nothing is classified, so a portfolio with only direct shares shows the
  no-key banner until classifications exist. The spec scenario "No funds held" assumes known
  classification.
- Banner: after a new key is saved, the suspended banner stays until the next refresh replaces
  the failed attempt.
