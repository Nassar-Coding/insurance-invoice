# Insurance Auditing — Independent Closure Re-audit

Date: 8 September 2026  
Selected solution: **LLM contract-to-schema with deterministic pricing**

**Both original findings are Closed.** The corrected code resolves the demonstrated uncertainty defect and the observed bundle-trace defect. Independent execution and comparisons found no material regression in the previously verified behavior.

This is a closure check of **AUD-01 and AUD-02**, using the supplied original independent audit as the acceptance reference. It does not replace that audit or expand its claims about target accuracy. Execution took place in isolated copies; the supplied checkpoint, schemas, submission and report were not modified. No implementation fixes or publishing actions were performed.

## Review basis and identification

| Item | State checked |
|---|---|
| Previously audited implementation | Git commit `d468718711de952be5300906ee09a85d3d35ec2c` |
| Corrected checkpoint | Git commit `ebc3f05fd42bd84584cc5455dc7c0b74a2c8bc8c` |
| Functional correction commit | `e5efadf4af7fe58ca1b75d904aac9c426093109d`; subsequent changes are evidence/status/packaging changes, with runtime and tests unchanged |
| Original acceptance reference | Supplied `Insurance_Auditing_Independent_Implementation_Audit(1).md`, byte-identical to the retained original audit |
| Source challenge snapshot | `majedzahrani3/insurance_auditing`, commit `6fee1da60b74512156637a22be15d996a36627e1` |
| Runtime actually executed | Python **3.12.13** |

The corrected ZIP's 874 manifest entries matched their recorded hashes. The separately supplied implementation report and submission matched their checkpoint copies. The original audit also matched the copy retained in the checkpoint. Before/after comparisons used results recovered from the previously audited Git commit, with their hashes checked against that commit's run manifests; the owner's comparison summaries were not the sole baseline.

Source contracts/data, accepted contract packages, service mappings, confidence policy and evaluator are unchanged from the previously audited commit. The corrections preserve the selected solution.

### Original Finding 1 — Major uncertainty handling

**Original issue — AUD-01.** A quarantined invoice header could lose its recoverable patient ownership. In the original source-rule fixture, invoice I2 had conflicting P1/P2 headers. Changing only the P2 header's date to impossible `2024-02-30` removed P2 from dependent context. I1's exclusion then became falsely certain: the engine emitted a zero expected amount with confidence 0.65, and result validation accepted it. With both conflicting headers valid, I1 correctly abstained.

**Correction inspected.** `src/insurance_audit/context.py` now separates accepted typed headers from header ownership evidence. Recoverable patient IDs and source locations from quarantined headers participate in ownership decisions. `possibly_owned` and `certainly_owned` are used in patient-scoped daily, presence, duplicate, exclusion and relevant prior-volume calculations.

`io.py::Loaded.invoice_identities` retains recoverable invoice IDs even when their only header is quarantined. `audit.py`, `batch.py::verify_accounting` and `submission.py::validate_result` account for those identities and prevent their own unresolved records from being emitted. A missing patient remains unbounded ownership; a header without a recoverable invoice ID triggers explicit batch-wide withholding. The latter is deliberately conservative and does not affect this supplied snapshot.

**Evidence checked.** I executed the original auditor counterexample, unchanged, against corrected code. It reaches loading, pricing, confidence assignment and result validation. I also ran and inspected the new ownership regression tests and the owner's before/after verification harness.

| Original fixture variant | Corrected I1 result | I2 disposition | Result validation |
|---|---|---|---|
| Both conflicting headers have valid dates | No opinion; `unresolved_exclusion` | Explicit abstention | 0 opinions, 2 traces, 0 supported lines checked |
| P2 header has impossible invoice date | No opinion; `unresolved_exclusion` | Explicit abstention | 0 opinions, 2 traces, 0 supported lines checked |

For the malformed variant, the retained dependency evidence identifies candidate patients **P1 and P2**, **0 certain / 1 possible** anchor records, and both source-header rows. The invalid date no longer establishes that the anchor belongs to P1.

The additional executed cases demonstrate that:

- Malformed amount/admission/discharge fields and reordered CSV columns preserve the conflict.
- Missing patient IDs remain uncertain; a recoverable ID with only a quarantined header receives an explicit disposition.
- A malformed header with the same recoverable patient does not invent a new ownership conflict; known unrelated patients do not block I1.
- Possible ownership propagates through daily-premium, duplicate-service, bundle and H4 patient-scope bounds. All-patient historical usage remains known where patient ownership is irrelevant.
- Missing invoice identity fails closed, and shuffled fixture records produce identical results.

**Closure verdict: Closed.** The fix addresses the lost-evidence mechanism, rather than reducing confidence on the same unsupported opinion. It is demonstrated through the same final validation path that accepted the original counterexample. Both I1 variants now withhold, and I2 remains accounted for.

The original supplied snapshot has no quarantined invoice headers; its quarantines concern line items. Consequently, an unchanged submission is consistent with this correction. The fixture establishes the required invalid-header behavior; neither it nor the enlarged test suite proves every imaginable malformed-input combination.

### Original Finding 2 — Moderate traceability

**Original issue — AUD-02.** Bundle substitutions had supported numeric amounts, but their calculation-stage `source` field cited standalone service rates instead of the controlling bundle clause. The observed gap covered **352 emitted lines across 151 invoices**, including **252 target lines across 103 target invoices**.

**Correction inspected.** `src/insurance_audit/pricing.py::rate_for` now records the dated base version and each relevant bundle's zero-based rule index, source clause, service/partner IDs, substituted cents, applicability state and index into the calculation's context evidence. Source selection distinguishes a present partner, an absent partner and unresolved applicability. This changes calculation evidence without changing the arithmetic operators or rule values.

**Evidence checked.** I independently checked all **5,605 emitted base/bundle stages** against accepted rule records. For bundle rules, a separate audit script used source CSV rows and retained mapping records to reconstruct partner service/date/patient membership, check the recorded applicability and context-member digest, and verify the referenced source text and cents. It did not import the implementation's pricing or context functions.

All **352 actual substitutions** now identify their controlling clauses and supporting partner context:

| Hospital | Applied bundle lines checked | Invoices |
|---|---:|---:|
| H1 | 100 | 48 |
| H2 | 0 | 0 |
| H3 | 76 | 33 |
| H4 | 84 | 28 |
| H5 | 92 | 42 |
| **Total** | **352** | **151** |

The original example, **INV-H4-000583**, now records:

| Line | Bundle-stage cents | Controlling record | Supporting partner line |
|---|---:|---|---|
| H4-L00583-03 | 1,250 | H4 bundle index 4; contract line 216 | H4-L00583-04 |
| H4-L00583-04 | 111,675 | H4 bundle index 4; contract line 216 | H4-L00583-03 |

Both point to `data/source/contracts/hospital_4/conditional_reimbursement_agreement.md#L216`. The dated standalone rates remain recorded as base-rate evidence, rather than being presented as the authority for substituted amounts.

The four new bundle tests assert applied-clause/partner context, absent-partner base provenance, unresolved applicability with both possible sources and withholding of unequal outcomes, and effective-date provenance across an H3 amendment. The rerun verification harness also rejected deliberately incorrect source citations, context indices and substituted cents. These are substantive trace checks; the generic submission validator alone is not an independent proof of clause semantics.

**Closure verdict: Closed.** The actual affected traces now carry the missing controlling rule and applicability chain. The original example and the complete observed set pass source/context checks. Refreshed output and release identities correspond to the corrected code.

### Regression verification

#### Tests

| Execution | Tests run | Failures | Errors | Skipped |
|---|---:|---:|---:|---:|
| Isolated working clone | 75 | 0 | 0 | 0 |
| Clean clone after replay | 75 | 0 | 0 | 0 |

**Verified by execution.** All nine original test modules are byte-identical to the previously audited versions, retaining the original **61** tests. `tests/test_audit_corrections.py` adds **10 ownership/context tests and 4 bundle-trace tests**. The two fresh runs tested identical source/test file hashes. No previously passing test failed.

The count represents top-level unittest methods, several with multiple cases. Closure rests on their assertions, the original counterexample and actual-output comparisons—not on the increased count alone.

#### Clean replay

**Verified by execution on the supplied final commit.** I created a separate local Git clone and removed `runs/`, `reports/corrections/`, `submission.csv`, generated evaluation JSON, metrics, workload, evaluation text, execution report and release manifest. The replay therefore had neither retained run results nor correction before/after caches available.

With Python 3.12.13, a sanitized environment and no inherited model/API credentials, the documented commands succeeded:

```bash
PYTHONPATH=src python -m insurance_audit reproduce
PYTHONPATH=src python -m insurance_audit verify-submission
python tools/run_checks.py independent_closure_clean
```

There are no third-party runtime/test dependencies to install. Replay regenerated the five hospital results, evaluation and submission. All five complete `H*.json` results and five input-quality files match the corrected checkpoint byte-for-byte. The corrected evaluation report and release manifest also reproduce byte-for-byte. Detailed evaluation JSON differs from the corrected checkpoint only at `/provenance/attempt`, as expected for a fresh attempt.

Fresh audit attempts were `0a8f51db2ceb43cda476e2d9c930de6c` for H1 and `2de35f67b8814669bb41ebc537820187` for H2–H5. This verifies local cloning and deterministic replay, not external publishing or fresh LLM extraction.

#### Hospital 1 metrics

**Independently recomputed** directly from the actual H1 CSV labels and regenerated opinion records, without importing the implementation's evaluator:

| Population | Invoice IDs | Emitted opinions | Exact flag-and-amount matches | Coverage | Detected / labelled errors | Error recall |
|---|---:|---:|---:|---:|---:|---:|
| Development | 622 | 169 | 169 | 27.17% | 4 / 42 | 9.52% |
| Previously exposed check group | 291 | 81 | 81 | 27.84% | 1 / 16 | 6.25% |
| **Full H1** | **913** | **250** | **250** | **27.38%** | **5 / 58** | **8.62%** |

These are unchanged. Full H1 has **663 abstentions**, including **53 labelled errors**. The 250/250 result establishes agreement on emitted opinions; it does not establish complete-population accuracy. This rerun is regression evidence, not a newly untouched evaluation split.

#### Prediction counts and submission

| Target hospital | Opinions | Flagged opinions | Abstentions |
|---|---:|---:|---:|
| H2 | 0 | 0 | 1,125 |
| H3 | 148 | 5 | 784 |
| H4 | 64 | 1 | 771 |
| H5 | 128 | 0 | 922 |
| **Total** | **340** | **6** | **3,602** |

**Verified by execution and independent CSV parsing.** Regenerated `submission.csv` contains 340 unique target invoice IDs and exactly the six template columns, in order. Every serialized flag, category, expected total, billed total and confidence matches its current opinion. Billed totals match unique source headers, and emitted traces account for their source lines. No H1 rows or duplicate invoice IDs appear.

The regenerated CSV, the separately supplied `submission(2).csv`, the corrected checkpoint CSV and the previously audited CSV are **byte-identical**. **No prediction changed.** Their shared SHA-256 is:

```text
2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c
```

#### Confidence, omissions and arithmetic

Every field of every opinion across all five hospitals is identical to the pre-correction result, including confidence tier, score, mapping evidence, interpretation qualifications and outcome-invariance indicator. H2 remains fully withheld. No confidence threshold or support evidence was refitted.

A recursive comparison of the entire results found changes only in the bundle-stage provenance fields `source`, `before`, `base_rate` and `rules`. After excluding exactly those fields, the complete results are identical. This includes accounting, omitted invoice IDs, reason categories, context bounds and arithmetic outcomes.

The intentional metadata change affects **4,784 invoice traces** and **1,898 abstention detail records**, including nested diagnostics and base-rate stages. This larger number does not imply additional changed predictions. Independent checks also verified the added base-rate and bundle metadata on every emitted stage.

#### Artifact consistency

**Verified.** All **82 distinct paths** bound by the corrected release manifest's prediction-input, evaluation/test/documentation-input and stable-output maps match their hashes. The independently regenerated release manifest matches the checkpoint's manifest.

| Artifact | Relationship to previously audited state |
|---|---|
| Submission, metrics and workload | Byte-identical |
| All opinion records and accounting | Identical |
| Trace and nested diagnostic provenance | Intentionally corrected; arithmetic unchanged |
| Evaluation report text | Intentionally clarifies H2's available admission/discharge dates and records the audit/correction stage |
| Run/release identities | Refreshed for corrected code and traces; consistent across clean replay |
| Implementation report | Attached and checkpoint copies identical; checked closure/regression claims supported |

The corrected release-manifest SHA-256 is `b6a52c763c3964fc105241f9993d352c4d0b5bb102897d1f5882eb399c4868c0`. Its change from the earlier release is expected; retaining the old manifest would have misidentified the corrected technical state.

#### Affected quality gates

The status files explicitly attach corrected tests and before/after evidence to the affected tasks and gates. I checked those references against the work actually executed:

| Original gate concern | Closure evidence and assessment |
|---|---|
| QG02 / QG03 — input integrity and identity | Recoverable quarantined-header ownership and invoice accounting tested; original lost-ownership defect closed |
| QG07 / QG09 — dependent uncertainty and fail-closed opinions | Original exclusion fixture withheld through confidence/result validation; related daily, duplicate, bundle and prior-context cases pass |
| QG11 — decision lineage | Actual 352 substitutions source/context checked; added metadata and release evidence consistent |
| QG10 / QG12 / QG13 — evaluation, reproduction and regression | Independent metrics, unchanged full opinion records, 75 passing tests in both clones, and matching clean replay |
| QG16 — snapshot revision behavior | New input-ownership cases and unchanged existing revision tests pass; revised code generates new run identities |

The original objections to ST02.03–ST02.04, ST05.02/ST05.05 and ST09.04 are therefore closed to the extent they arose from AUD-01/AUD-02. This is not a fresh certification of unrelated operational gates.

No material issue introduced by the corrections was found. Existing limits—unlabelled target accuracy, low H1 coverage/recall, disclosed contractual interpretations and judgment-based target confidence—remain unchanged and do not constitute a new regression.

## Evidence retained for this re-audit

The companion ZIP includes the auditor's execution logs and independent comparison outputs under `closure_reaudit/execution/`, separate from the implementation. They include the original counterexample output, both test runs, clean replay/validation logs, independently recomputed H1/CSV checks and all 352 bundle source/context comparisons. The project evidence checked includes `reports/corrections/audit_1/`, the current run pointers/results, `reports/release_manifest.json`, `reports/gate_status.json` and `reports/implementation_status.json`.

For exact handover identification, the corrected ZIP SHA-256 is `c3b49e516b335d9a2cd424279df3b983e66d6f23946a87fda6bbace61ade891e`; the updated implementation report SHA-256 is `950da8b3322ae0cd1b9ea2b6038341d12336fed981d9b0f93402dae4213b9b20`.

### Final verdict

**PASS — BOTH FINDINGS CLOSED, NO MATERIAL REGRESSIONS**
