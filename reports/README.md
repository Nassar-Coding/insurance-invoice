# Which report describes which state?

| Files | Interpretation |
|---|---|
| `publishing_preparation_report.md` | Current preparation outcome, actual final checks and pending external actions |
| `metrics.json`, `workload.json`, `evaluation_*.json`, `evaluation_report.md`, `release_manifest.json` | Audited deterministic results; README reproduction regenerates equivalent results (fresh attempt provenance varies) |
| `decision_log.md` / `.pdf`, `submission_writeup.md` / `.pdf`, `document_checks.json` | Current page-limited documents and their verified rendering |
| `implementation_report.md` | Current status addendum, followed by unchanged corrected author report |
| `H*_source_review.json`, `H*_candidate_closure.json` | Reviewed package inputs/evidence; preserve original paths and bytes |
| Acquisition, inventory, viability and mapping-review reports | Dated evidence of source examination and proposal/review history |
| `corrections/audit_1/` | Unchanged original audit counterexamples, before/after artifacts and author correction verification |
| `tests_*.json` / `.txt`, regression/provenance/reproduction/guarded/closure/delivery checks | Historical implementation checkpoints with their recorded code/artifact hashes; not new publication checks |
| `implementation_status.json`, `implementation_completion.json`, `gate_status.json` | Governing implementation ledger at correction checkpoint: 65 verified subtasks, four external BT11 tasks not completed |

Historical checks may reference the old document hashes and original attempt
paths; those exact documents and attempts remain recoverable in
`evidence/history/`. The original `document_checks.json` is additionally retained
under `evidence/audited_baseline/reports/`. A historical hash is not silently
relabelled as a check of a newly presented document.

`execution.json` at this level describes the original audited attempt IDs and
timing. The new clean-clone execution is recorded under
`evidence/publishing/final_reproduction/generated/reports/execution.json`.
The full result bytes match; attempt IDs and execution duration naturally differ.

Fresh publication execution logs, complete-output comparisons and document
checks live under `evidence/publishing/`. They are separate from historical
evidence. The generated evaluation report's final pending-stage sentence is
preserved as part of the audited release identity; the independent closure
report establishes the subsequent PASS status.
