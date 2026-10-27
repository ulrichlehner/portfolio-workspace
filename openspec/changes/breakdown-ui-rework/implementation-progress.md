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
| C settings page | `b2f79fb2c` | UI reactor on B + C: 77 tests passed; restored a message key still used by the status pane |
| A responsiveness and selection | `0a5ff3d00` | UI reactor: 86 tests passed, Checkstyle clean in 7 modules |
| D layout, onboarding, status pane | `c13bae600` | UI reactor: 100 tests passed, Checkstyle and message checks clean; app build succeeded |
| E charts | `258d18efa` | UI reactor: 103 tests passed, Checkstyle and message checks clean |

## Review

An Opus review of the stack found six issues, fixed and folded into their commits by
autosquash (hashes above are after the rebase): treemap click zoomed into a tile (library
navigation listener), Refresh enabled with nothing to refresh, coverage legend could read
100 % with a nonzero remainder (regression assertion added), status table rebuilt on every
push (now compared by visible content), persistence preference saved on click instead of
OK/Apply, session-only entry offered only after a failed OK. Final UI reactor on the rebased
stack: 103 tests passed, BUILD SUCCESS. The core bundle is unchanged by this change.

## First app check (2026-10-26/27)

Findings: initial state read as empty, status icons without meaning, layout shift on
refresh. Specs and tasks 7.1 to 7.3 were added. Fix commit `76adde874`: calculating state,
status text with validation reason, rows for directly held shares dropped, progress in the
summary row. UI reactor: 113 tests passed, BUILD SUCCESS. App rebuilt from `76adde874`.

The rejected funds were diagnosed with one provider request each: all negative rows are
identifier-less cash or currency-forward rows of at most -0.015 % of the fund. The current
validation rule rejects any negative weight, so the funds stay unresolved. A rule for such
rows is planned as a separate change.

## Manual verification

On 2026-10-27 the user confirmed all manual checks in the app built from `76adde874`
with a private copy of the real portfolio: navigation and German labels, summary strip,
coverage bar and indicator tooltip, calculating state, charts with tooltips, switcher and
restored layout, chart and table selection linking, selection kept across automatic checks,
refresh progress without layout shift, settings page and no-key banner. Computer-use access
was declined, so these checks were done by the user. Task 7.4: the fixes were committed as a
separate focused commit instead of being folded into increment D, because they also touch
files introduced by increment E.

## Notes for review

- Settings (open): a failed `replaceSecure` (storage unavailable) has already removed the previously
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
