# Report index

| Files | Purpose |
|---|---|
| `implementation_report.md` | Implemented method, audit corrections, observed effects and limitations |
| `final_reproduction_result.md` | Latest documented-command verification |
| `metrics.json`, `workload.json`, `evaluation_*.json`, `evaluation_report.md`, `release_manifest.json`, `execution.json` | Regenerated results and their input identities; fresh attempt/timing fields vary |
| `decision_log.md` / `.pdf`, `submission_writeup.md` / `.pdf`, `document_checks.json` | Current page-limited deliverables and rendering checks |
| `H*_source_review.json`, `H*_candidate_closure.json` | Original reviewed package inputs/evidence; exact paths and bytes are required by accepted bundles |
| Acquisition, inventory, viability and mapping-review reports | Historical evidence of source examination, candidate decisions and mapping revisions |
| `corrections/audit_1/` | Original counterexamples, before/after artifacts and regression results for AUD-01/AUD-02 |
| Earlier `tests_*.json` / `.txt`, regression, provenance and reproduction checks | Historical verification records, identified by their recorded file hashes and attempts |

Historical source-review records and technical evidence are retained verbatim. Their model/session descriptions and earlier status wording are not current operational statements. Earlier viability and mapping counts describe their recorded versions. Current coverage comes from `metrics.json` and `workload.json` after reproduction.

Old attempts and documents referenced by historical records are recoverable in a separate checkout using [the history archive](../evidence/history/README.md). Current reproduction uses neither those outputs nor the old test receipts. The clean-clone checks and current comparison manifest are under `evidence/publishing/`; the original pre-cleanup reference is under `evidence/audited_baseline/`.
