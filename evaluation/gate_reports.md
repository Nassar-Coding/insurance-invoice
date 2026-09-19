# Implementation gate reports

## Gate 0 — Survive the grader — 2026-09-19

**Technical exit: PASS (0.1–0.5). Gate 1 has not started.**

Governing source: `docs/Revised_Plan_Rank29_to_Top3.md`, Gate 0. The background corrections memo is subordinate to that plan. Baseline working-repository commit: `b3291da61658a8781f351622c249ab42da98659a`. Tested implementation commit: `3ac49083192350c4876666672d3bdb7b68befbe8`. Subsequent delivery changes contain documentation and executed evidence only; the clean-clone receipt records hashes of every tested source/test file. Delivery tag: `gate0` (resolve its final delivery commit with `git rev-parse gate0^{commit}`).

### Changes and decisions

- Replaced the Python 3.12.13 exception with a warning. `.python-version` remains reference documentation; README declares `>=3.12,<3.13`.
- Removed stored input/source/artifact fingerprint equality as a prediction precondition. Fingerprints remain provenance. Current source identity, finite contract schema, accounting, complete-line, monetary, confidence and output-content validation remain enforced.
- Moved the split manifest and original development calibration evidence to `tests/evaluation/`. Moved the invoice-specific historical mapping-review and correction-verification utilities to `tests/historical_tools/`. No prediction path reads an invoice-ID allowlist.
- `reproduce` is prediction-only by default. `--evaluate-development` explicitly opts into development evaluation, skips absent evaluation inputs, and records evaluation failures without failing prediction. It never invokes check/full evaluation. Reports tolerate evaluation being absent. A target batch with zero supported opinions exports a valid header-only CSV.
- Added the label-free, all-hospital `tools/generalize.py` harness and the two-interpreter `tools/verify_gate0.py` clean-clone check. Added nine regression tests; updated three former fingerprint-lock assertions to the new documented contract.
- Contracts, mapping records, pricing/check/decision algorithms, numerical confidence policy, source data and the six submission fields were not changed. Full hospital result files and input-quality outputs match the audited baseline byte-for-byte.
- Preserved genuine historical provenance. Explicit offline bundle-acceptance review checks and old snapshot-verification scripts remain historical tools, not reproduction dependencies. They are not invoked by the README reproduction path, and were not used to inspect check results. This is the distinction between an acquisition-review check and a runtime input lock; see `evaluation/gate0/input_independence_review.json`.

### Exit criteria and evidence

| Criterion | Result | Measured evidence |
|---|---|---|
| 0.1 Exact-patch gate removed | PASS | Original 3.12.14 run raised `RuntimeError`; revised 3.12.13 and 3.12.14 replays exit 0. Other-patch warning and informational version file are covered by tests. |
| 0.2 Input independence and invoice-specific runtime artifacts | PASS | Requested directory review covers 81 text files. No prediction invoice-ID literals or fixed dataset-count gates. Clean runs succeed after removing labels, the split/calibration fixtures, saved predictions, reports, governance and historical evidence. Source/artifact hash differences no longer gate replay. |
| 0.2 Optional H1 evaluation | PASS | Default path does not open labels/split. Tests cover missing labels, missing manifest and an evaluation exception; prediction remains successful. Explicit development replay also completes successfully. |
| 0.3 Two fresh-clone reproductions | PASS | Separate clean clones and virtual environments on 3.12.13 and 3.12.14: install, dependency check, reproduction, submission verification and test commands all exit 0. Submissions, all five hospital result files and all five input-quality files are byte-identical. |
| 0.4 All-hospital generalization survival | PASS | All H1–H5 inputs re-IDed, patient-sampled, row-shuffled and description-perturbed; unchanged pipeline exits 0, all five result schemas validate, and target CSV validates. No labels or split copied into the temporary project. |
| 0.5 Dependency hygiene | PASS | `pip install --no-index -r requirements.txt` and `pip check` succeed in both new environments. No third-party runtime dependencies. |
| Regression tests | PASS | 84/84 pass on each interpreter, 0 failures, 0 errors, 0 skipped. |
| Fallback preservation | PASS | 340 target rows, 6 flags. Submission bytes and all ten hospital result/input-quality files match the audited baseline. |

Clean-clone commands, return codes, interpreter versions and file fingerprints: `evaluation/gate0/clean_reproduction/verification.json` and sibling logs. Original version failure: `evaluation/gate0/before_version_failure.log`. Current development evaluation: `reports/evaluation_development.json`. Preservation receipt: `evaluation/gate0/development_and_preservation.json`. Stress-test details: `reports/generalization_gate0.json` and `.log`. Prompt record: `prompts/gate0_implementation_v1.md`.

Submission SHA-256: `2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c`.

### Development cost and false positives

Development population: **622 invoices**, **42 erroneous**, **580 clean**. Existing evaluator: **4 TP, 38 FN, 0 FP**; **cost = 5 × 38 + 0 = 190**. Recall 4/42 = 9.52%; 169 emitted opinions and 453 withheld. **False positives on clean development invoices: 0/580.** These are unchanged baseline results, not improved detection. The scored target file remains identical, so the external initial cost remains the reported **1395**; no hidden target labels were available to rescore it independently.

**Decoy-proxy flags: not measured.** The frozen clean-development proxy set is established at Gate 2.6. No zero-decoy claim is made at Gate 0. Real check labels/results were not inspected or evaluated during this gate. Unlabelled invoice history is processed for prediction and stress testing; this is not held-out scoring. The historical implementation had already exposed check, so this is not a newly untouched holdout.

### H2–H5 distribution (unchanged fallback)

Flag rate uses all unique invoice IDs, including withheld invoices.

| Hospital | Unique invoices | Emitted rows | Flags | Withheld | Flag rate |
|---|---:|---:|---:|---:|---:|
| H2 | 1,125 | 0 | 0 | 1,125 | 0.0000% |
| H3 | 932 | 148 | 5 | 784 | 0.5365% |
| H4 | 835 | 64 | 1 | 771 | 0.1198% |
| H5 | 1,050 | 128 | 0 | 922 | 0.0000% |

All are below 3%. Gate 0 explicitly ships the unchanged fallback; it does not require detection expansion. The flag-rate investigation requirement begins in Gate 1 and is not waived for that gate. The plan's family-mix extrapolation would give approximately `5 × 285 × (1 − 4/42) = 1289.29`, before projected false positives. It differs from the observed external cost 1395 and is only an unsupported distribution assumption, not a new scoring result.

### Generalization measurements and qualifications

| Hospital | Patients kept / original | Descriptions perturbed | Output opinions | Flags | Withheld |
|---|---:|---:|---:|---:|---:|
| H1 | 158 / 226 | 2,428 | 5 | 0 | 645 |
| H2 | 195 / 278 | 3,097 | 0 | 0 | 805 |
| H3 | 164 / 234 | 2,373 | 2 | 0 | 634 |
| H4 | 144 / 206 | 2,162 | 4 | 1 | 572 |
| H5 | 180 / 257 | 2,834 | 4 | 0 | 749 |

Sampling rounds 70% to whole patients. Patients linked through a reused invoice ID are retained together to avoid losing physical-record history or line links. About 30% of retained descriptions are perturbed, with half assigned to preserve service codes and half to remove them. Some original descriptions have no code; the receipt separates assigned code policy from actual removals. The harness emits 10 target opinions. This sparse result exposes the frozen matcher's fragility; Gate 0 tests survival, not recall preservation. The 10% relative-recall limit starts at Gate 3 and has not been measured here.

### Discrepancies and boundaries

1. The background memo gives H2's physical-header count, whereas the revised plan correctly uses unique invoice IDs. Observed unique counts match the revised plan; retained physical rows remain source evidence.
2. Python 3.12.14 reproduced the exact-version failure locally. Two available patch versions, 3.12.13 and 3.12.14, were verified; the plan's 3.12.3 was an example. The leaderboard's actual exit-1 cause remains unproven, as the background memo states.
3. Historical reports and verifier scripts were written against the original exact-patch/hash-lock workflow. They are retained as dated evidence; current README commands and Gate 0 receipts supersede that execution requirement. Prediction succeeds without those historical files.
4. Gate 1 text asks for check/full measurements, while the plan's global instruction forbids reading check before the Final Gate. The global prohibition was honored here; the conflict must not be resolved by reading check in Gate 1.
5. Delivery capability: the GitHub integration can create commits and update branches, but exposes no tag-creation operation; shell `git push --dry-run` fails because GitHub HTTPS credentials are unavailable. The local `gate0` tag is prepared on the final delivery commit. Publishing that tag to GitHub requires an authenticated `git push origin refs/tags/gate0` or equivalent user action. This does not invalidate the executed 0.1–0.5 results; it is an outstanding remote-tag delivery step.

No Gate 1 scorer, decision layer, structural detector, mapping threshold, rule or pricing expansion has been implemented. Stop after this Gate 0 delivery and wait for the user's instruction to continue.
