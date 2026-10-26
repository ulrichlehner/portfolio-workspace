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

## Outstanding manual checks

- 2.4 selection and expansion survive a 60-second check and an incoming fund result.
- 3.3 German sidebar Vermögensaufstellung > Aufschlüsselung, view title.
- 4.4 disabled persistence checkbox with a one-sentence reason.

## Notes for review

- Settings: a failed `replaceSecure` (storage unavailable) has already removed the previously
  stored key, because the core credential API deletes before it writes. Pre-existing behavior,
  not changed here; candidate follow-up.
- Settings: whitespace-only input is rejected as invalid rather than treated as empty.
- Status pane: `FundStatus` contains an age derived from the clock, so equal-model skipping
  rarely applies; selection is still kept by fund reference.
