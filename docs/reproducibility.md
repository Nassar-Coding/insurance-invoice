# Reproduction during the improvement gates

Use the commands in the [README](../README.md) with Python >=3.12,<3.13. Prediction and tests require only the standard library. The Python patch recorded in `.python-version` is informational.

Normal replay needs current CSV inputs, finite contract and mapping records, the confidence policy and submission template. It does not read labels, partition IDs, historical results, source-review receipts or archived predictions. Recorded hashes describe the inputs actually read; they do not reject changed input batches or another Python patch version. Schema, monetary, source-row and completeness checks remain active.

Development evaluation is optional via `reproduce --evaluate-development`. Its split manifest is `tests/evaluation/split_manifest.json`. The check partition was opened once, at the Final Gate, and has not been reopened. Missing or invalid evaluation inputs do not invalidate a successful prediction run.

`tools/generalize.py` executes unchanged prediction code against temporary re-IDed, patient-sampled, shuffled and description-perturbed data for all hospitals, without labels or the split. It measures execution and schema validity; `tools/generalize_recall.py` measures detection retention under the same perturbation.

The original clean-clone and audit scripts compared against the pre-Gate-2 frozen baseline and were removed at the Gate 10 cleanup; they remain recoverable at the `gate9` tag. The current portability gates are the two `generalize` tools above. See [gate reports](../reports/gates/gate_reports.md) for the executed two-interpreter verification and its limitations. Fresh model extraction is a separate activity and is not promised to reproduce saved schemas.

`reports/decision_log.pdf` is rendered from the current `reports/decision_log.md` by `tools/render_decision_log.py`, and `reports/decision_log_render.json` records both files' hashes so a reader can confirm they match. The markdown is authoritative. Rendering is optional and uses `requirements-docs.txt`; those packages are not runtime dependencies.
