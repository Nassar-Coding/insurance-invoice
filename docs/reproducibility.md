# Reproducibility and evidence

Use CPython 3.12.13 and the commands in the [README](../README.md). Core execution and the 75-test suite use only the standard library. The source CSV/Markdown snapshot, reviewed schemas and mappings, confidence policy and patient-connected split are included. No model call, credentials or historical prediction is needed.

## Clean-clone check

`python publishing/check_reproduction.py` creates a fresh local Git clone and virtual environment, installs the empty runtime requirements, removes cached outputs, historical archives and saved predictions, then runs reproduction, submission validation, all tests and the three H1 evaluation commands. Only the source/candidate review reports required by the accepted bundles remain in the clone. The parent process retains the comparison hashes and reference CSV outside the pipeline.

The check compares all five complete hospital result files and their input-quality files, metrics, workload, evaluation details, generated report and manifest. It also verifies the submission's columns, identity set, contents, order and exact bytes. Fresh attempt identifiers and timing are expected; their exclusion from a comparison is explicit. Current checks are recorded in [final_reproduction_result.md](../reports/final_reproduction_result.md).

`evidence/publishing/baseline.json` contains the expected current file/manifest identities. Documentation-only edits change source/report fingerprints when a report template or prompt index is part of an identity. They do not authorize new predictions: the CSV, metrics, workload and full hospital/input-quality output hashes continue to match the original reference. The original comparison manifest is retained separately in `evidence/audited_baseline/reproduction_baseline.json`.

## Source review and history

The five `reports/H*_source_review.json` files are exact, hash-bound inputs to accepted bundles. Their descriptions record the original acquisition review. Preserve these files and the four original technical prompt versions. Raw candidates, rejected or revised mappings, source-review records and correction evidence remain available. Fresh LLM acquisition is a separate activity and is not guaranteed to recreate the saved records.

Historical audits and test records retain their original wording, paths and identities. They are evidence of the recorded state, not current status messages. See the [audit index](../governance/audits/README.md), [report index](../reports/README.md), and [history restoration instructions](../evidence/history/README.md). Restoring history is optional and must use a separate checkout.

## Documents

The one-page decision log and two-page write-up are generated from their current Markdown sources:

```bash
python -m pip install -r requirements-docs.txt
python publishing/render_delivery_documents.py
```

These optional PDF packages do not participate in pricing, evaluation or tests. The renderer checks page limits and extracted text; rendered pages are also inspected visually. The source challenge and its instructions remain unchanged under `data/source/`.
