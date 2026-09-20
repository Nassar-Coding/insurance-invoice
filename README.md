# Insurance invoice auditing

LLM-assisted contract-to-schema extraction with deterministic Python pricing. Saved, reviewed contract records and service mappings drive replay without model calls, API keys or a GPU.

On Hospital 1, the only labelled hospital, the audit reaches **42 of 42 development errors and 16 of 16 check errors with no false positive on either partition** (cost 0 under the ranking metric `5·FN + FP`), amount exact match 0.929 and 0.875, and no flag on any of the 184 frozen decoy proxies. `submission.csv` carries 2,537 rows for Hospitals 2-5 with 281 flags, against a scored set stated to hold about 285 errors. See **[EVALUATION_REPORT.md](EVALUATION_REPORT.md)** for per-category results, the four systematic failure modes, every contract reading the audit relies on, what was not attempted, and an honest account of the coverage shortfall against the ~285 errors the scored set is stated to contain.

## Reproduce

Use **Python >=3.12,<3.13**. `.python-version` records the original 3.12.13 reference only; another patch version produces a warning, not a failure. Core execution and tests have no third-party dependencies.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --no-index -r requirements.txt
python -m pip check
PYTHONPATH=src python -m insurance_audit reproduce
PYTHONPATH=src python -m insurance_audit verify-submission
python tools/run_checks.py local
python tools/validate_submission.py
```

`validate_submission.py` re-reads the source invoices and checks `submission.csv` independently of the exporter, so a fault in the exporter cannot hide behind its own accounting: column order, flag domain, confidence range, integer cents, one row per identifier, Hospitals 2-5 only, and billed totals against the source.

`reproduce` audits all five hospitals and exports complete opinions for H2–H5 to `submission.csv`. It reads the current files in `data/source/invoices/`; no invoice-ID list, recorded input fingerprint, label file or partition manifest is required. Hashes remain provenance metadata. Finite-schema, source-row accounting, complete-line and monetary validation remain enforced. A batch with no supported target opinions produces a valid header-only CSV rather than crashing or inventing clean rows.

For another dataset, copy the project and replace the CSV inputs under `data/source/invoices/`, retaining the supplied contract Markdown, reviewed contract JSON and mappings. The public command also accepts `--project /absolute/project/path` before `reproduce`.

Windows PowerShell: use `.venv\Scripts\python.exe` for `python` and set `$env:PYTHONPATH = 'src'` before the CLI commands. This spelling is documented; execution verification is on Linux.

## Evaluation boundary

Prediction replay does not open labels or the partition manifest. Development evaluation is explicit:

```bash
PYTHONPATH=src python -m insurance_audit reproduce --evaluate-development
```

The optional development step skips missing labels or the manifest and reports evaluation failures without failing the successful prediction run. The preserved partition manifest and original calibration evidence live under `tests/evaluation/`; they are evaluation evidence, not prediction inputs. The confidence policy remains under `evaluation/` and its numerical values are unchanged.

Gate 1 has explicit authorization for the known full/check baseline. After Gate 1, do not read or report the check partition again until the Final Gate. The earlier implementation had already exposed check; no claim of a newly untouched holdout is made.

## Generalization survival check

```bash
python tools/generalize.py
```

The harness uses a temporary project with unchanged executable code, contract records and mappings, without labels or a split manifest. For every hospital it re-IDs invoices, keeps approximately 70% of patients with their full histories, shuffles rows and perturbs 30% of descriptions. Reused-ID connected patient groups stay together. Perturbations include case, whitespace, abbreviation swaps, separator/token order and one-character non-code typos; service-code preservation/removal is balanced across perturbed rows.

It executes the public reproduction command and validates output schema, identity accounting, traces, money, confidence and submission contents. Gate 0 requires execution/schema survival; a recall-tolerance assertion belongs to Gate 3 onward. Results are written to `reports/generalization_gate0.json` and its log.

## Fallback results and limitations

The source snapshot's target submission remains 340 opinions: H2 0, H3 148, H4 64 and H5 128; six flagged invoices in total. Withholding remains extensive. H2 diagnostic pricing cannot establish complete payable opinions under the current rules. Newly worded descriptions generally remain unresolved; the generalization survival check does not establish detection quality.

Expected original-snapshot submission SHA-256:

```text
2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c
```

This checksum is a verification reference, never an execution requirement on new inputs. Contracts, mappings, pricing order, confidence scores and uncertainty handling remain unchanged through Gate 1. Gates 2 onward have not been implemented.

## Project and evidence

- `src/insurance_audit/`: fixed interpreter, validation, export and optional evaluation.
- `contracts/`, `mappings/`: reviewed records, original candidates and revisions.
- `data/source/`: original challenge contracts, CSV inputs, H1 labels and template.
- `prompts/`: original versioned technical prompts and assistance disclosure links.
- `tests/`: regression fixtures; `tests/evaluation/` contains evaluation-only ID lists; `tests/historical_tools/` preserves earlier invoice-specific diagnostic utilities.
- `evaluation/gate_reports.md`: current gate decisions, measured results and discrepancies.
- `reports/`: generated metrics, coverage and technical evidence. Earlier reports/PDFs describe their dated audited implementation; Gate 0 changes are recorded in the gate report.
- `docs/decision_register.md`: contract interpretations and unresolved facts.
- `evidence/history/`, `governance/audits/`: original history and independent audits; not replay dependencies.

Original publishing/closure scripts compare exact historical files, Python versions and already exposed check results. They are historical verification tools, not the current Gate 0 reproduction commands. Optional PDF dependencies in `requirements-docs.txt` remain separate from the dependency-free prediction runtime.

## Gate 1 measurement

See [measurement commands and interpretation](docs/gate1_measurement.md), [gate report](evaluation/gate_reports.md), and [baseline register](evaluation/baseline_cost.json). The cost scorer reproduces development 4 TP / 38 FN / 0 FP (cost 190) and full H1 5 TP / 53 FN / 0 FP (cost 265). Decision traces, withheld-reason histograms and the 38-miss family cross-tab are under `reports/gate1/`. The root `submission.csv` remains the challenge deliverable; `reports/gate1/h1_predictions.csv` is evaluation-only.

The generalization baseline is carried forward from the recorded prior full-history control (4 → 1 development detections, zero new FP), explicitly not rerun during this rebuild. Clean-checkout verification is deferred to the Final Gate, and tags are user-managed.
