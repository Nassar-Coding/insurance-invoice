# Report index

Everything here is evidence for a number stated in the root [README](../README.md)
or in [EVALUATION_REPORT.md](../EVALUATION_REPORT.md), or provenance for how the
reviewed contract and mapping artifacts were produced. Nothing here is read by a
prediction: `python -m insurance_audit reproduce` writes into this folder and
never depends on what it finds.

| Path | Purpose |
|---|---|
| `decision_log.md` | **Graded deliverable.** One page: every contract ambiguity found and what was decided. |
| `submission_writeup.md` | **Graded deliverable.** Two pages: how results were measured, where the work was uncertain and why, and what another week would go on. |
| `decision_log.pdf`, `submission_writeup.pdf` | The same two documents rendered by `tools/render_documents.py`; `document_render.json` records each one's page count, body point size and both files' hashes, so a reader can tell a PDF matches its markdown. The markdown is authoritative. |
| `gates/gate_reports.md` | Gate decisions, measured results and discrepancies across the whole sequence. |
| `gates/gate<N>/` | One folder per gate: the scorer output, withheld-reason histogram, miss cross-tab, decision-trace summary and a short written summary for that gate. |
| `gates/final/` | The Final Gate: development and check scorer output, submission validation, generalization and its recall measurement, withheld reasons. The check figures quoted in the evaluation report come from here. |
| `gates/gate8/` | The population-consistency tables behind the adopted Service Day reading, and the tie-line diagnostic that was measured and deliberately not used. |
| `gates/gate0/` | Prediction-input independence and label-free preservation findings; `development_and_preservation.json` is read by `tools/decision_trace.py`. |
| `acquisition/` | How the reviewed artifacts were produced: source reviews, candidate closures, acquisition manifests, inventories, viability and mapping-review records, and the H1 mapping revision behind `prompts/map_v2.md`. |

Records under `acquisition/` are retained as written. Their status wording and
counts describe the version they were recorded against, not the current run.
Current coverage comes from the evaluation report and from `workload.json` and
`metrics.json` after a reproduction.

Generated outputs of a reproduction — `metrics.json`, `workload.json`,
`evaluation_*.json`, `evaluation_report.md`, `release_manifest.json`,
`execution.json`, `inventory_*.json`, `input_quality*.json` and `tests_*` — are
not committed: the frozen inputs reproduce them exactly.
