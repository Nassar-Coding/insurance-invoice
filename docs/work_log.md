# Technical changelog

## Input handling and initial execution

The first ingestion test incorrectly assumed every H1 line had a valid date. It was corrected to reconcile accepted and quarantined records: 11,409 typed H1 lines plus six malformed dates, with 35 malformed-date lines across all hospitals. Raw invalid values remain available to uncertainty handling. The initial CLI run also exposed a three-value bundle return unpacked into two variables; fixing the caller allowed execution of all 913 H1 identities. The failed attempt is retained in the historical Git bundle.

## Mapping revision and evaluation

Initial H1 execution emitted 579 opinions. Development invoice INV-H1-000236 exposed a 43,650-cent over-correction caused by an unsupported specialty assignment. Mapping revision 2 withdrew all 39 analogous missing-essential-qualifier keys. With the revised mappings and fixed confidence policy, H1 emits 250 opinions: development 169/622 and check 81/291, all with correct flags and exact cents. Full error recall is 5/58 (8.62%); 53 labelled errors remain withheld. The check is exposed and subsequent evaluations are regressions.

## All-hospital execution and deterministic traces

All five contract packages were implemented. H2 remains diagnostic-only because actual submission and required episode/exception evidence are absent. Complete target opinions total 340: H3 148, H4 64 and H5 128. A full-snapshot permutation check initially failed because conflicting-header trace lists followed input order even though all opinion fields were unchanged. Canonical source-row ordering fixed the trace difference. The initial failure and successful all-hospital regression are retained.

## Uncertainty and source-trace corrections

AUD-01 preserves quarantined-header patient ownership in cross-invoice context; missing or conflicting identity remains uncertain. AUD-02 records controlling bundle clauses and the partner context establishing applicability. The original 61 tests and 14 added regressions pass. The corrections preserve all supplied-data opinion fields, confidence values, omission reasons and arithmetic. All 352 emitted bundle substitutions and 5,605 base/bundle stages were checked against source/context evidence. Before/after records are under `reports/corrections/audit_1/`.

## Reproducibility

Independent verification confirmed 75 passing tests, clean replay and an unchanged 340-row CSV. Guarded execution observed no label access during prediction/export and no network access. Full-hospital permutation and result-hash comparisons passed. [final_reproduction_result.md](../reports/final_reproduction_result.md) records the latest documented-command verification. Earlier failures, mapping versions and audit records remain historical evidence, including the older H2 archive discrepancy explained in [the history index](../evidence/history/README.md).
