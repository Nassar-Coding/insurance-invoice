# Insurance auditing

**LLM contract-to-schema with deterministic pricing**, implemented against the supplied synthetic five-hospital challenge. The authoring assistant interpreted contracts and reviewed service mappings in ChatGPT Work. Standard-library Python replays saved, reviewed JSON through a fixed interpreter. Prediction execution makes no model calls.

The independent closure verdict is **PASS — BOTH FINDINGS CLOSED, NO MATERIAL REGRESSIONS**. This repository preserves that corrected technical state; publication preparation changes documentation and packaging only. See the unchanged [closure report](governance/audits/independent_closure/Insurance_Auditing_Independent_Closure_Reaudit.md) and [current preparation/reproduction report](reports/publishing_preparation_report.md).

## Results and coverage

| Hospital | Unique invoice IDs | Complete opinions | Predicted errors | Withheld |
|---|---:|---:|---:|---:|
| H1 — labelled development | 913 | 250 | 5 | 663 |
| H2 | 1,125 | 0 | 0 | 1,125 |
| H3 | 932 | 148 | 5 | 784 |
| H4 | 835 | 64 | 1 | 771 |
| H5 | 1,050 | 128 | 0 | 922 |

The submission contains **340 target opinions: six predicted erroneous and 334 predicted correct**. Target accuracy is unknown. All five contracts and observed description keys were examined; inspected services do not imply complete invoice coverage.

H1 has **250/250 correct flag-and-exact-amount matches on emitted opinions**, **27.38% coverage**, and **5/58 = 8.62% population error recall**. The other 53 labelled errors are withheld. Development emits 169/622; the exposed check group emits 81/291. The check is now regression evidence, not a fresh holdout. [Evaluation](reports/evaluation_report.md) includes per-category metrics, denominators, confidence support and four systematic failure mechanisms with actual examples.

## Install and reproduce

After cloning the submitted repository, enter its root. Use **CPython 3.12.13**, recorded in `.python-version` and included in execution identity. There are **no third-party runtime or test packages**. `requirements.txt` is intentionally comments only. No API credentials, Work connection, GPU, database, network service or archived prediction is needed.

Linux/macOS shell:

```bash
python --version
python -m venv .venv
. .venv/bin/activate
python -m pip install --no-index -r requirements.txt
python -m pip check
PYTHONPATH=src python -m insurance_audit reproduce
PYTHONPATH=src python -m insurance_audit verify-submission
python tools/run_checks.py local
```

Windows PowerShell: after selecting Python 3.12.13 and running `python -m venv .venv`, use:

```powershell
.venv\Scripts\python.exe --version
.venv\Scripts\python.exe -m pip install --no-index -r requirements.txt
.venv\Scripts\python.exe -m pip check
$env:PYTHONPATH = 'src'
.venv\Scripts\python.exe -m insurance_audit reproduce
.venv\Scripts\python.exe -m insurance_audit verify-submission
.venv\Scripts\python.exe tools/run_checks.py local
```

The final verification was executed on Linux; the PowerShell spelling was not executed on Windows. Other Python versions are unverified and change execution identity.

`reproduce` recomputes **all five hospitals**, exports complete H2–H5 opinions and evaluates all three H1 partitions. It does not copy `submission.csv` or refit confidence. `verify-submission` needs a successful current run and release manifest, so run reproduction first in a new clone. The full suite contains **75 tests** and writes `reports/tests_local.json` and `.txt`.

Expected submission SHA-256:

```text
2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c
```

The 340 data rows use exactly these columns, in this order:

```text
invoice_id,flagged,error_category,expected_total_cents,billed_total_cents,confidence
```

To rerun H1 evaluation after reproduction:

```bash
PYTHONPATH=src python -m insurance_audit evaluate --partition development
PYTHONPATH=src python -m insurance_audit evaluate --partition check
PYTHONPATH=src python -m insurance_audit evaluate --partition full
```

Use `--project /absolute/project/path` before a subcommand when invoking elsewhere. [CLI details](docs/cli_contract.md) cover inventory, audit and export.

## Clean-state verification and generated files

The additional publication check creates a fresh local Git clone and virtual environment, installs the empty dependency set, removes saved predictions and archived history from the clone, executes the documented pipeline and all 75 tests, and compares complete hospital results and input-quality files with the audited hashes. It also compares the CSV, metrics, workload, evaluation report and release manifest. From a committed checkout:

```bash
python publishing/check_reproduction.py
```

Normal reproduction needs neither this helper nor historical restoration. Its output goes to `evidence/publishing/latest_reproduction/`; the supplied final verification is retained separately under `evidence/publishing/final_reproduction/`.

Before ordinary replay you may remove `runs/`, `submission.csv`, and generated `reports/metrics.json`, `reports/workload.json`, `reports/evaluation_*.json`, `reports/evaluation_report.md`, `reports/execution.json` and `reports/release_manifest.json`. **Keep the other review evidence:** accepted bundles require the exact five `reports/H*_source_review.json` files. New attempts live in `runs/attempts/`; `runs/current-H1.json` and `runs/current-H2-H3-H4-H5.json` locate them. Traces record opinions, omissions, services, dated rates, controlling clauses, arithmetic and uncertain context. Export checks full line coverage and policy consistency; failed or stale output cannot be promoted silently.

Prediction/report bytes match the audited baseline. Attempt IDs and timing are intentionally fresh. Each replay retains several hundred MB of detailed JSON; disk use grows with retained attempts. The final report records observed runtime and memory, not a scale guarantee.

## Project guide

| Path | Purpose |
|---|---|
| `data/source/` | Unchanged source CSV, Markdown, H1 labels and template; original challenge README retained |
| `src/insurance_audit/`, `tests/` | Frozen interpreter, data/uncertainty checks, evaluation/export and 75 tests |
| `contracts/`, `mappings/` | Finite rules, source-bound acceptance bundles, raw candidates and earlier revisions |
| `evaluation/` | Frozen patient-connected split, confidence policy and development support |
| `prompts/` | Unchanged extraction, mapping v1/v2, review, implementation and correction instructions |
| `docs/decision_register.md`, `docs/implementation_changes.md` | Interpretation history, failed expectations and corrections |
| `docs/ai_usage.md`, `docs/publishing_preparation.md` | Assistance disclosure, current status and packaging decisions |
| `reports/evaluation_report.md`, `metrics.json`, `workload.json` | Performance, failure examples, abstention workload and limitations |
| `reports/decision_log.md` / `.pdf` | Current one-page decision summary |
| `reports/submission_writeup.md` / `.pdf` | Current two-page accompanying write-up |
| `reports/implementation_report.md` | Corrected report with a separated closure/publication addendum |
| `reports/corrections/audit_1/` | Counterexamples, before/after evidence and author regression results |
| `governance/` | Governing workbook, gates, override and unchanged independent audits with evidence |
| `evidence/audited_baseline/`, `evidence/publishing/` | Reference artifacts, hashes, file dispositions and preparation evidence |
| `evidence/history/` | Compact original seven-commit history, including failures and full audited traces; see its README |
| `publishing/` | Packaging verification and document rendering; not imported by prediction code |

The source snapshot is commit `6fee1da60b74512156637a22be15d996a36627e1` of `majedzahrani3/insurance_auditing`. CSV and Markdown are the chosen supplied formats. OCR and a second JSONL loader are not ingestion requirements. All 66,097 source occurrences, including 35 quarantined lines, are accounted for.

## Interpretation and confidence limits

H2 has admission/discharge dates, but lacks actual submission dates, detailed episode/leave facts and possible written exceptions needed for invoice effectiveness. Invoice date is not assumed to be submission date. Its 07:00 Service Day is not proved by calendar dates. Pricing remains diagnostic and all full opinions are withheld.

Essential service qualifiers cannot be guessed from a unique catalog match or billed price. H1 development exposed a 43,650-cent over-correction; all 39 analogous mapping keys were withdrawn. Unknown quantity dimensions, conflicting IDs, missing context and nonunique allocations remain omissions. H3/H5 exclusion direction and exact boundaries remain qualified; H3 settlement protection uses the recorded chronology reading. H4 cumulative patient scope is bounded. H5 projects invoice facility onto lines as an explicit assumption; all 128 emitted H5 opinions have **0.65** confidence.

Confidence attaches to a complete supported opinion. H1 correct-row tiers use 0.95/0.90; sparse error tiers use 0.65 judgment. Reviewed targets use 0.80/0.70, with relevant interpretation or invariant-uncertainty caps. These are not demonstrated target probabilities. Lowering a score cannot replace a missing fact.

## History and document status

Frozen replay is reproducible from retained schemas/mappings. Fresh LLM acquisition is a distinct source-reviewed process; it is not promised to regenerate identical records. Historical acquisition, mapping, freeze, status and rendering helpers under `tools/` remain for traceability and are not prediction-reproduction commands.

The audited `prompts/README.md`, generated `reports/evaluation_report.md` and release-manifest scope still contain their original “closure pending” wording. Those bytes are retained to preserve the independently audited release. This README, the preparation report and the unchanged closure report establish the later status. Historical test/gate ledgers describe their dated checkpoints. Preparation does not falsely mark the four external BT11 tasks complete.

PDFs are provided and are not required for pricing/tests. Optional rendering of current Markdown uses unchanged pins in `requirements-docs.txt`:

```bash
python -m pip install -r requirements-docs.txt
python publishing/render_delivery_documents.py
```

The original exercise instructions and the later effort-limit override remain recorded without claiming compliance with the original cap. This is a synthetic-data batch prototype. Repository publication, assessor access and actual email delivery require later authorization; none has occurred. See [remaining external actions](docs/external_readiness.md).
