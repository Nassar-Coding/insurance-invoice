# Reproduction during the improvement gates

Use the commands in the [README](../README.md) with Python >=3.12,<3.13. Prediction and tests require only the standard library. The Python patch recorded in `.python-version` is informational.

Normal replay needs current CSV inputs, finite contract and mapping records, the confidence policy and submission template. It does not read labels, partition IDs, historical results, source-review receipts or archived predictions. Recorded hashes describe the inputs actually read; they do not reject changed input batches or another Python patch version. Schema, monetary, source-row and completeness checks remain active.

Development evaluation is optional via `reproduce --evaluate-development`. Its split manifest is `tests/evaluation/split_manifest.json`. Do not open check/full until the Final Gate. Missing or invalid evaluation inputs do not invalidate a successful prediction run.

`tools/generalize.py` executes unchanged prediction code against temporary re-IDed, patient-sampled, shuffled and description-perturbed data for all hospitals, without labels or the split. Gate 0 measures execution and schema validity, not detection retention.

Original clean-clone and audit scripts under `publishing/` and historical tools record the earlier frozen baseline, including exact fingerprints and prior check exposure. Do not use those scripts as the current portability gate. See [gate reports](../evaluation/gate_reports.md) for the executed two-interpreter verification and its limitations. Fresh model extraction is a separate activity and is not promised to reproduce saved schemas.

The existing PDFs remain the earlier audited documents. Rendering them is optional and uses `requirements-docs.txt` and `publishing/render_delivery_documents.py`; PDF packages are not runtime dependencies.
