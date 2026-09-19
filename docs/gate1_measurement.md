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

## Step 2: decision trace and withholding

```bash
PYTHONPATH=src python -m insurance_audit audit --hospitals H2 H3 H4 H5
python tools/cost_scorer.py --submission reports/gate1/h1_predictions.csv --partition development --output reports/gate1/trace_development_score.json --trace reports/gate1/decision_trace.jsonl.gz
```

`--trace` observes all five current hospital runs, independently of the CSV being scored. The compressed JSONL has one decision per recoverable invoice identity and includes every linked physical source line. Quarantined or early-skipped lines have explicit posthoc lookup provenance. An orphan without a header stays in original input-quality accounting.

The four mapping states describe the existing reviewed records: MATCH is accepted, TIE has multiple reviewed candidates, WEAK has one unresolved candidate (or absent description), and NO_MATCH has no reviewed candidate. NO_MATCH is not a new confident unknown-service finding. The runtime's all-services uncertainty fallback is not presented as a semantic tie. No scored matcher is introduced.

Amount status `full` means an emitted total; `partial` means diagnostic supported-line pricing on a withheld invoice; `none` means no supported line pricing. Partial never becomes a submitted correction. Checks fired are those recorded by the existing execution, not newly invented checks on skipped lines.

`withheld_reasons.json` supplies exclusive first-runtime-reason histograms and overlapping distinct-invoice incidence for H1 development and H2–H5. `missed_development_crosstab.json` joins the 38 development misses to the supplied family coding; it supplies both versions and development IDs. `hospital_distributions.json` uses every unique source invoice as the flag-rate denominator.

H2 has zero rows: 1,110 invoices reach the existing submission-deadline/waiver uncertainty; 7 stop for conflicting reused IDs and 8 for quarantined required records. The existing policy does not regard invoice date as proof of actual submission or episode/waiver facts (H2 Article XIII.1–5 and Article II.5; `src/insurance_audit/audit.py`). This is an explanation of existing behavior, not a new contract interpretation. All H2–H5 rates remain below 3%; their named withholding reasons are recorded as the plan requires. Gate 1 investigates those rates without changing prediction behavior.

## Step 3: baseline register

```bash
python tools/register_baseline.py
```

This reads the committed scoring reports and registers `evaluation/baseline_cost.json`. It does not run prediction or generalization. Generalization is the explicitly carried-forward **full-history description control: 4 → 1 development detections, zero new false positives, 75% relative recall loss**. The original unpublished experiment logs were lost during workspace maintenance; the record labels the numbers as prior observations reaffirmed by the user, not new executed evidence. Its preserved protocol is in the baseline file. The experiment is not rerun here.

Later gates append entries rather than overwrite the baseline; the registration script refuses to overwrite later entries. Clean-checkout verification is deferred to the Final Gate. Tags are user-managed. The current implementation and measurement tests run with `python tools/run_checks.py gate1_rebuild`; all prediction modules, source data, mappings, schemas, confidence policy and the submission remain unchanged.
