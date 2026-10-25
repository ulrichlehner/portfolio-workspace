# Complete-coverage follow-up register

Reviewed 2026-10-25. These are outstanding acceptance records, not completed
features or authorization to publish. The objective remains 100% validated
economic exposure of the declared portfolio scope. No private holdings or
provider credentials are recorded here.

The user separately authorized experimental source-only development-fork pushes
with a notice of unverified rights/data quality on 2026-10-25. G7 still gates
official upstream integration and binary releases; the notice does not verify
rights or constitute a legal transfer of responsibility. G1-G6 remain open.

| Record | Gap and affected category | Evidence still missing | Remedy | Closure check |
| --- | --- | --- | --- | --- |
| G1 | Allocation semantics for provider fund weights | Total-NAV denominator and complete supported exposure, not just a normalized sum | Obtain authoritative semantics and compare a dated independent issuer export, including non-equities and derivatives | A public physical fund reconciles by economic exposure and all exclusions are explained |
| G2 | Constituent classification and company grouping | Exact mappings for identifierless rows, changed identifiers, share classes and depositary receipts | Use licensed authoritative identifier/classification data and a company identity graph; never equate similar tickers or names | Public acceptance plus ambiguous/conflicting identifier tests; distinct instruments are not silently merged |
| G3 | Signed, synthetic and derivative exposure | Exposure rather than collateral/market-value weights | Design a supported economic-exposure contract with a verified source | Public derivative/synthetic cases reconcile with economic exposures; collateral is not substituted |
| G4 | Funds with no usable provider composition | Licensed automatic alternative or confirmed entitlement | Add a replaceable automatic source after permission and source-quality checks | Previously unavailable public example decomposes without uploads or guessed index substitution |
| G5 | Holdings-effective dates | Actual source effective date, distinct from retrieval/update time | Source dated issuer/provider evidence | UI preserves all three dates independently; missing dates stay unknown |
| G6 | Nested funds, cycles and depth limits | Automatically retrieved child compositions and evidence of branch completeness | Connect bounded recursive retrieval to the existing eight-edge/path-cycle engine | A public/synthetic nested case retrieves children automatically, preserves overlapping paths and stops only affected branches |
| G7 | Official integration and binary-release permissions | Runtime/display, source and binary adapter distribution, attribution obligations, optional retention | Resolve the checklist in provider-gates.md with authoritative terms or separately authorized provider contact | Explicit dated pass/fail/unknown record; no official integration or binary release on unknown permission; experimental source-fork exception stays labelled |

The current engine can traverse supplied nested compositions. That does not
establish that the production retrieval pipeline automatically fetches every
newly discovered child fund. G6 stays open until that integration is demonstrated.
The current issuer display is grouped by security identifier, not a verified
company graph; G2 stays open even when the display looks plausible.

Full issuer comparison on 2026-10-25 materially advances G1/G2: the issuer API
supplies dated ISINs and classifications absent from the simple CSV. All 1352
identified provider rows in the two public examples agree with issuer weights
within raw rounding at 22 Oct 2026. All unmatched issuer rows are now enumerated,
including omitted zero-market-value futures with positive notional. See the full
comparison in provider-gates.md and the reproducible Docker tooling in
docs/fund-data-validation.md at the workspace root. G1 still needs production
application of the evidence rather than a blanket assumption about future
provider payloads. G2 needs corporate grouping beyond security ISINs. G3 needs
supported economic overlay handling; known omissions are no longer merely
suspected. These are concrete implementation/evidence gaps, not a request for
the user to validate the weights manually.

Tasks 1.3 and 6.3 remain gated. Archive or synchronization must retain these
records and the durable complete-coverage requirement, not describe a partial
display as completion of the objective.
