# Insurance invoice auditing

LLM-assisted contract-to-schema extraction with deterministic Python pricing. Saved, reviewed contract records and service mappings drive replay without model calls, API keys or a GPU.

On Hospital 1, the only labelled hospital, the audit reaches **42 of 42 development errors with no false positive** (cost 0 under the ranking metric `5·FN + FP`), at amount exact match 0.929 and with no flag on any of the 184 frozen decoy proxies. The check partition was read once, at the Final Gate, where it scored 16 of 16 with no false positive; that figure is the code as it stood then, and the partition has not been reopened since. `submission.csv` carries 2,537 rows for Hospitals 2-5 with 281 flags, against a scored set stated to hold about 285 errors. See **[EVALUATION_REPORT.md](EVALUATION_REPORT.md)** for per-category results, the four systematic failure modes, every contract reading the audit relies on, what was not attempted, and an honest account of the coverage shortfall against the ~285 errors the scored set is stated to contain.

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

Gate 1 had explicit authorization for the known full/check baseline. The check partition was then closed until the Final Gate, read once there, and has not been read since; every gate in between was tuned on development alone. The earlier implementation had already exposed check, so no claim of a newly untouched holdout is made — it is regression evidence, and the check column of the evaluation report is the Final Gate measurement rather than a figure for the current code.

## Generalization survival check

```bash
python tools/generalize.py
```

The harness uses a temporary project with unchanged executable code, contract records and mappings, without labels or a split manifest. For every hospital it re-IDs invoices, keeps approximately 70% of patients with their full histories, shuffles rows and perturbs 30% of descriptions. Reused-ID connected patient groups stay together. Perturbations include case, whitespace, abbreviation swaps, separator/token order and one-character non-code typos; service-code preservation/removal is balanced across perturbed rows.

It executes the public reproduction command and validates output schema, identity accounting, traces, money, confidence and submission contents. Results are written to `reports/generalization_gate0.json` and its log.

Recall under the same perturbations is measured separately:

```bash
python tools/generalize_recall.py
```

Perturbing 30% of Hospital 1's descriptions, and leaving every identifier, quantity, date and amount untouched, costs a **9.5% relative recall drop with no new false positive**. An early version of the matcher failed this badly — 478 false positives, because a typo makes a token unexplained and an unexplained token was indistinguishable from an absent service. The rebuilt matcher scores coverage of the *billed* tokens and guards drift with a contract-vocabulary check, a canonical token multiset and a single-character repair rule.

## Coverage and limitations

`submission.csv` carries **2,537 rows across Hospitals 2-5, 281 of them flagged** (H2 76, H3 69, H4 61, H5 75), at flag rates of 6.76%, 7.40%, 7.31% and 7.14% against a scored base rate near 7.2%. 1,405 invoices are withheld rather than opined on, the largest blocks being ambiguous service mapping (657), a composite dimension the record does not observe (339) and a rate still ambiguous after the consistency test (299).

Matching counts is not the same as matching invoices: some flags may be false positives offsetting misses elsewhere, and Hospital 1 stays the only place any of this can be checked. [EVALUATION_REPORT.md](EVALUATION_REPORT.md) sets out the four systematic failure modes, one known defect found while writing it up, and what would be done next.

Current submission SHA-256:

```text
09a48b06852eda729cb7171044901bf0afd480de6298b2ee0a283bfe9ea4ca0f
```

The original pre-Gate-2 snapshot hashed to `2a208c62…5c99c` and produced 340 opinions with six flags; that checksum survives in the history as a provenance reference. Neither checksum is an execution requirement on new inputs.

## Project and evidence

- `src/insurance_audit/`: fixed interpreter, validation, export and optional evaluation.
- `contracts/`, `mappings/`: reviewed records, original candidates and revisions.
- `data/source/`: original challenge contracts, CSV inputs, H1 labels and template.
- `prompts/`: every prompt the work was done under, verbatim — the four acquisition prompts and one per gate — with the sequence and what changed between iterations in [prompts/README.md](prompts/README.md).
- `tests/`: regression fixtures; `tests/evaluation/` contains evaluation-only ID lists; `tests/historical_tools/` preserves earlier invoice-specific diagnostic utilities.
- `evaluation/gate_reports.md`: current gate decisions, measured results and discrepancies.
- `reports/`: generated metrics, coverage and technical evidence, with one summary per gate under `reports/gate<N>/`. [reports/decision_log.md](reports/decision_log.md) is the one-page record of every contract ambiguity and what was decided. Earlier reports describe their dated audited implementation.
- `docs/decision_register.md`: contract interpretations and unresolved facts.
- `evidence/history/`, `governance/audits/`: original history and independent audits; not replay dependencies.

Original publishing/closure scripts compare exact historical files, Python versions and already exposed check results. They are historical verification tools, not the current reproduction commands. Optional PDF dependencies in `requirements-docs.txt` remain separate from the dependency-free prediction runtime, and `reportlab` is not available in this environment: `reports/decision_log.pdf` therefore still renders the pre-Gate-9 decision log. **The markdown is authoritative**; regenerating the PDF needs `pip install -r requirements-docs.txt` and `python publishing/render_delivery_documents.py`.

## How it got here

The first submission placed 29th at a cost of 1395. The work since was run in gates, one instruction at a time, each with a numeric exit criterion that had to be shown before the next began. Development cost by gate:

| Gate | What it changed | Development cost |
|---|---|---|
| 1 | measurement rebuilt; no prediction change | 190 |
| 2 | structural and term-window checks decoupled from mapping; line-level decision layer | 80 |
| 3-4 | four-state matcher, `unknown_service`, unit basis, reviewed cap and exclusion clauses | 10 |
| 5-7 | pricing order and rounding, amount policy, confidence tiers, decoy and distribution audit | 10 |
| Final | check read once, submission validator, fresh-clone reproduction, freeze | 10 |
| 8 | ambiguous clauses settled by how the parties performed them | **0** |
| 9 | deliverables refreshed; no code and no prediction change | 0 |

See [measurement commands and interpretation](docs/gate1_measurement.md), [gate report](evaluation/gate_reports.md), [baseline register](evaluation/baseline_cost.json), and the per-gate summaries under `reports/`. The cost scorer reproduces the Gate 1 baseline of development 4 TP / 38 FN / 0 FP (cost 190) and full H1 5 TP / 53 FN / 0 FP (cost 265) from that commit; the root `submission.csv` remains the challenge deliverable, and `reports/gate1/h1_predictions.csv` is evaluation-only. Tags are user-managed.
