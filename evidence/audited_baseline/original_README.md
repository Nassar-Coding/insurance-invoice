# Insurance auditing - implementation candidate

This project implements **LLM contract-to-schema with deterministic pricing** against the supplied synthetic insurance-auditing data. The Work-session assistant interpreted the contracts and reviewed saved service mappings. A fixed Python interpreter replays those accepted JSON artifacts; it makes no LLM calls.

The current submission contains **340 complete opinions**: H3 148, H4 64, H5 128. H2 has diagnostic pricing but **no submission opinions**, because its invoice-effectiveness conditions require facts absent from the files. These are predicted opinions, not established target accuracy. H1 produces 250/913 opinions, with 250 exact flag-and-amount matches, 27.38% coverage and 8.62% population error recall. Low recall is a material limitation.

## Reproduce from a clone

After cloning this project, enter its root and select **Python 3.12.13**. That exact interpreter was verified; `.python-version` records it and replay checks it. There are **no third-party execution or test dependencies**. `requirements.txt` intentionally contains no packages. No API keys, Work connection, GPU, database, or network access are needed for the commands below.

```bash
python --version
PYTHONPATH=src python -m insurance_audit reproduce
PYTHONPATH=src python -m insurance_audit verify-submission
python tools/run_checks.py local
```

On Windows PowerShell, set `$env:PYTHONPATH = 'src'` before running `python -m insurance_audit reproduce` and `python -m insurance_audit verify-submission`.

`reproduce` reads the source CSVs and accepted contract/mapping bundles, recomputes all five hospitals, exports complete target opinions, evaluates H1, and regenerates the stable metrics and evaluation report. It does **not** copy a saved submission or fit the confidence policy. You can delete `submission.csv`, `runs/`, and the generated files `reports/metrics.json`, `reports/workload.json`, `reports/evaluation_*.json`, `reports/evaluation_report.md`, `reports/release_manifest.json`, and `reports/execution.json` before replay. Keep the other reviewed source and acquisition evidence: bundles bind several `reports/H*_source_review.json` files as required inputs. Historical regression tools additionally use the retained historical runs; ordinary replay does not.

Expected submission SHA-256:

```text
2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c
```

`reports/metrics.json`, `reports/workload.json`, and `reports/evaluation_report.md` are deterministic report outputs. Attempt IDs, execution duration and recovery records intentionally vary. The corrected supplied-data replay measured approximately 38 seconds and 468 MiB peak process RSS in Work; these are observations, not a scale or performance guarantee. Retained historical traces make the working tree substantially larger than the required source data. Disk grows with each retained run.

## Outputs and traceability

- `submission.csv`: exactly the six template columns; only complete H2-H5 opinions are eligible. Money uses integer cents.
- `reports/evaluation_report.md`: development category metrics, explicit denominators, confidence support and systematic failure analysis.
- `reports/decision_log.md` and `.pdf`: one-page decision summary. `reports/submission_writeup.md` and `.pdf`: at most two pages for the requested accompanying write-up.
- `runs/attempts/<attempt>/H*.json`: opinions, omissions and line traces, including selected services, source references, exact arithmetic stages and context bounds. Recover an attempt through `runs/current-H1.json` or `runs/current-H2-H3-H4-H5.json`.
- `runs/current-submission.json`: validated local submission pointer. Its referenced manifest binds source execution, counts, line reconciliation and CSV checksum. `verify-submission` rejects changed bytes, inputs or incomplete promotion. Old successful attempts remain historical after changes; a failed command has an explicit failed status and a nonzero exit.
- `reports/release_manifest.json`, `reports/final_regression.json`, `reports/provenance_check.json`, and `reports/reproduction_check.json`: current input/output identities and implementation evidence. `reports/implementation_status.json` maps the governing subtasks to evidence; `reports/gate_status.json` records gate dispositions.

The source snapshot is commit `6fee1da60b74512156637a22be15d996a36627e1` of `majedzahrani3/insurance_auditing`. `data/source/README.md` is unchanged. CSV and Markdown are the chosen supplied formats; OCR, PDFs and a second JSONL invoice loader are not part of ingestion. All raw occurrences, including quarantined lines, are retained in accounting and relevant context. Conflicting invoice IDs are not split using guessed ID patterns.

## Commands and change handling

```bash
PYTHONPATH=src python -m insurance_audit inventory --hospitals H1 H2 H3 H4 H5
PYTHONPATH=src python -m insurance_audit audit --hospitals H1
PYTHONPATH=src python -m insurance_audit evaluate --partition development
PYTHONPATH=src python -m insurance_audit audit --hospitals H2 H3 H4 H5
PYTHONPATH=src python -m insurance_audit export
```

Use `--project /absolute/project/path` **before** the subcommand when needed. The final target batch intentionally runs H2 to retain diagnostic/omission evidence; H2 is inactive for submission. H1 labels are read only by evaluation. The check partition has already been exposed; later reruns are regressions, not fresh held-out estimates.

Changes to governing sources, mappings, schemas or semantics require source review and rebinding before execution. Never update acceptance hashes merely to silence rejection. Changed invoice history needs a new audit of the supplied snapshot; omitted invoice opinions remain in relevant history. The current manifest then changes. Confidence-support changes require explicit development evidence or withdrawal of the affected tier. See `docs/implementation_changes.md` and the tests for these boundaries.

Frozen replay is distinct from **fresh LLM extraction**. The latter uses the versioned instructions in `prompts/`, the source documents, retained raw candidates, and source review. It is not promised to be bit-reproducible or automated by a hidden API. Acquisition scripts are historical aids; do not run them as part of replay or overwrite accepted artifacts casually.

## Documentation rendering and stage boundary

The PDFs are retained deliverables. Reproducing the submission and evaluation does not need a PDF library. Optional re-rendering uses the pinned packages in `requirements-docs.txt` and `python tools/render_documents.py`; its Markdown and rendered page counts are checked separately.

The first independent implementation audit returned PASS WITH CORRECTIONS. This revision fixes its two findings: recoverable ownership from quarantined headers remains context evidence, and bundle traces cite their controlling clause and applicability context. `reports/corrections/audit_1/` retains the baseline, source-rule counterexample, corrected results and all-hospital before/after comparison. `python tools/verify_audit_corrections.py` reruns those author checks using the retained baseline attempts; ordinary replay does not need historical attempts. The result is awaiting independent closure re-audit.

No external repository was created/published, assessor access granted, or email sent. `docs/external_readiness.md` tracks those later actions. No production service, real-patient compliance certification or external clinical/legal truth is claimed. The user's execution override removed the source exercise's effort constraints; the original source instructions and override are retained without claiming compliance with the original cap.
