# Gate 1 measurement

This gate observes the unchanged Gate 0 predictor. User instructions close Gate 0, waive A3, require publishing after each numbered rebuild step, and defer clean-checkout verification to the Final Gate. Use the installed Python; no new interpreter is needed.

## Step 1: scorer

```bash
PYTHONPATH=src python -m insurance_audit audit --hospitals H1
python tools/cost_scorer.py --export-current-h1 reports/gate1/h1_predictions.csv --partition development --output reports/gate1/cost_development.json
```

The evaluation export includes H1 only; it must never replace the root `submission.csv`. `--submission FILE`, `--labels FILE` and `--families FILE` accept explicit inputs. Full/check partitions require `--allow-heldout-baseline` and are authorized only for this Gate 1 baseline or the Final Gate. After Gate 1, do not reopen check/full until the Final Gate.

Omitted errors count as false negatives. Clean omissions cost zero and carry no confidence. Amount metrics use true positives only. Five-bin reliability measures the existing correct-flag AND exact-amount event, not P(error). Category tables measure detection on invoices carrying each label; primary families are mutually exclusive. Hospital distributions describe only the supplied CSV, never secretly borrow predictions from other runs.

Measured results, input predictions and scorer test output are under `reports/gate1/`. No detection, mapping, pricing, confidence or withholding change is made.
