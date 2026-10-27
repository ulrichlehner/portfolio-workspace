# Implementation progress

Fork branch `fix/signed-cash-rows`, stacked on `feature/breakdown-ui-rework`.

| Task | Result |
| :--- | :--- |
| 2.1 to 3.1 | Commit `fa135ff9f`: non-fatal `NETTED_IDENTIFIERLESS_ROWS`, fatal-only usability, netting in `CompositionValidator`, tooltip note |
| 4.1 | `scripts/dev.sh test`: 5091 tests, 0 failures, Checkstyle clean; look-through core tests 184; UI reactor 114 tests, BUILD SUCCESS; diff scanned for private data |
| 4.2 | 2026-10-27, app from `fa135ff9f` with a private copy of the real portfolio: every held fund that was previously rejected for negative identifier-less rows shows OK with a decomposed share, the tooltip mentions the netting, and their constituents appear in the breakdown. Confirmed by the user. |

Identifier-less means an empty identifier map. The Eulerpool adapter adds ISIN, CUSIP and symbol
only when present and not blank; a literal "-" would count as an identifier and would not be
netted. No such value was observed.
