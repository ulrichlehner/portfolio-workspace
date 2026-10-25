# Complete-coverage follow-up register

Reviewed 2026-10-25. These are outstanding acceptance records, not completed
features or authorization to publish. The objective remains 100% validated
economic exposure of the declared portfolio scope. No private holdings or
provider credentials are recorded here.

| Record | Gap and affected category | Evidence still missing | Remedy | Closure check |
| --- | --- | --- | --- | --- |
| G1 | Allocation semantics for provider fund weights | Total-NAV denominator and complete supported exposure, not just a normalized sum | Obtain authoritative semantics and compare a dated independent issuer export, including non-equities and derivatives | A public physical fund reconciles by economic exposure and all exclusions are explained |
| G2 | Constituent classification and company grouping | Exact mappings for identifierless rows, changed identifiers, share classes and depositary receipts | Use licensed authoritative identifier/classification data and a company identity graph; never equate similar tickers or names | Public acceptance plus ambiguous/conflicting identifier tests; distinct instruments are not silently merged |
| G3 | Signed, synthetic and derivative exposure | Exposure rather than collateral/market-value weights | Design a supported economic-exposure contract with a verified source | Public derivative/synthetic cases reconcile with economic exposures; collateral is not substituted |
| G4 | Funds with no usable provider composition | Licensed automatic alternative or confirmed entitlement | Add a replaceable automatic source after permission and source-quality checks | Previously unavailable public example decomposes without uploads or guessed index substitution |
| G5 | Holdings-effective dates | Actual source effective date, distinct from retrieval/update time | Source dated issuer/provider evidence | UI preserves all three dates independently; missing dates stay unknown |
| G6 | Nested funds, cycles and depth limits | Automatically retrieved child compositions and evidence of branch completeness | Connect bounded recursive retrieval to the existing eight-edge/path-cycle engine | A public/synthetic nested case retrieves children automatically, preserves overlapping paths and stops only affected branches |
| G7 | Publication permissions | Runtime/display, source and binary adapter distribution, attribution obligations, optional retention | Resolve the checklist in provider-gates.md with authoritative terms or separately authorized provider contact | Explicit dated pass/fail/unknown record; no publication on unknown permission |

The current engine can traverse supplied nested compositions. That does not
establish that the production retrieval pipeline automatically fetches every
newly discovered child fund. G6 stays open until that integration is demonstrated.
The current issuer display is grouped by security identifier, not a verified
company graph; G2 stays open even when the display looks plausible.

Tasks 1.3 and 6.3 remain gated. Archive or synchronization must retain these
records and the durable complete-coverage requirement, not describe a partial
display as completion of the objective.
