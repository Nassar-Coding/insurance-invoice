# Utilities

Everything the root [README](../README.md) asks you to run:

| Tool | What it does |
|---|---|
| `run_checks.py` | Runs the whole test suite and records its result. `python tools/run_checks.py local` |
| `validate_submission.py` | Re-reads the source invoices and checks `submission.csv` independently of the exporter. |
| `cost_scorer.py` | Scores Hospital 1 against its labels: true positives, misses, false positives, cost, amount exact match and calibration error. |
| `generalize.py` | Label-free portability: re-identified invoices, subsampled patients and perturbed descriptions must still produce a valid submission. |
| `generalize_recall.py` | The same perturbation, measured for recall loss and new false positives. |
| `decision_trace.py` | Per-invoice decision traces, withheld-reason histograms and the miss cross-tab. |
| `mine_decoy_proxies.py` | Mines and freezes the decoy proxy set that every gate is checked against. |
| `fit_confidence.py` | Fits the confidence tiers; its output is reviewed before it is frozen into `evaluation/confidence_policy.json`. |
| `register_baseline.py` | Appends a measured cost to `evaluation/baseline_cost.json`. Later gates append; it refuses to overwrite. |
| `render_decision_log.py` | Renders `reports/decision_log.md` to a one-page PDF. Optional, and the only tool here that needs `requirements-docs.txt`. |

## Acquisition

`acquisition/` preserves how the saved contract and mapping artifacts were
produced — extraction, review recording, acceptance, the mapping revision and
the confidence freeze. They are provenance, not steps in ordinary replay.
Running one may replace a reviewed artifact and would require a fresh technical
review, so do not run them to reproduce the submission.
