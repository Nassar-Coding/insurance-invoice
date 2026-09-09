# Insurance auditing - correction and regression implementation report

**CORRECTIONS COMPLETE — READY FOR INDEPENDENT CLOSURE RE-AUDIT**

Both substantive findings in the supplied first independent audit were reproduced, accepted and corrected. The corrected implementation was executed for all five hospitals, evaluated on Hospital 1, tested and reproduced in a clean local clone. This is author correction/regression verification; independent closure re-audit remains pending. No publishing, assessor access change or sending has occurred.

The selected solution remains **LLM contract-to-schema with deterministic pricing**. The governing Ready workbook and pinned challenge source commit `6fee1da60b74512156637a22be15d996a36627e1` are unchanged. Contract schemas, mappings, source inputs and the frozen confidence policy are unchanged by these fixes. The original audit is retained unchanged in `governance/audits/independent_implementation_1/`. Historical reports/results remain under `reports/corrections/audit_1/before/` and their original attempt directories.

## Findings, decisions and before/after evidence

| Finding | Audit concern and reproduced original behavior | Author decision and implemented correction | Corrected behavior and evidence |
|---|---|---|---|
| AUD-01 - Major uncertainty handling | I2 has P1/P2 conflicting headers. Making only P2's invoice date impossible removed P2 from context ownership. Dependent I1 changed from `unresolved_exclusion` to an emitted zero-cent opinion, flagged 1 at confidence .65; result validation accepted it. | **Accept.** Separate valid typed headers from complete recoverable raw-header ownership evidence. Preserve every candidate patient and its source row; missing patient identity stays unbounded. All patient-dependent context operations use this evidence. An invalid date is never rewritten or treated as proof that its patient is false. | Both original fixture variants now withhold I1 for `unresolved_exclusion`, including through confidence assignment and result validation. I2 retains an explicit omission. Exact before/after probe output and complete corrected fixture traces are retained. |
| AUD-02 - Moderate traceability | Bundle prices were numerically supported, but the calculation's source field cited standalone service rates. All 352 emitted substitutions across 151 invoices had this gap; 252 lines/103 invoices are in target scope. | **Accept.** Record the dated base version plus each relevant bundle-record index/source, partner service, substituted cents, presence state and context index. Applied clauses supply the source; absent partners use the base source; uncertain alternatives retain both. | All 5,605 emitted base/bundle stages reconcile to accepted records and recomputed raw context, including all 352 substitutions. The H4 example and all applicable source table rows were checked. Deliberately wrong source, context and bundle cents are rejected by the verification harness. |

AUD-01's original fixture uses accepted H1 services H1-S004 (9,200 cents) and H1-S100, governed by the seven-day exclusion. Quarantine cannot settle the anchor's disputed patient. A lower confidence score would not repair that missing evidence, so the corrected outcome is omission. On malformed-header inputs, recoverable invoice IDs with no valid header now receive explicit dispositions; quality and result accounting use the same identity set. If a quarantined header has no recoverable invoice ID, all complete opinions are withheld with an explicit unlinked-header reason. These input-contract cases are covered by regressions. Known unrelated patients remain irrelevant, same-patient evidence is retained, and contract-wide all-patient prior usage is not arbitrarily weakened.

There are **zero quarantined invoice headers in the supplied snapshot**. Its 35 quarantines are line items. AUD-01 therefore changes the demonstrated malformed-input behavior, not any current submission row. This limitation on the observed impact is accepted from the audit and confirmed directly.

For AUD-02, actual invoice `INV-H4-000583` line `H4-L00583-03` uses **1,250 cents**, and partner `H4-L00583-04` uses **111,675 cents**, from `conditional_reimbursement_agreement.md#L216`. Their old source pointers led to standalone **1,425** and **126,900**-cent rows. The regenerated stage now identifies bundle record 4, that controlling source and the same-patient/day partner context. The numerical rates and invoice total did not change.

Before/after records:

- `reports/corrections/audit_1/before/baseline_manifest.json`: preserved original file/code hashes and attempts; original Git state `d468718711de952be5300906ee09a85d3d35ec2c`.
- `before/auditor_aud01_reproduction.py` and `.txt`: the auditor's exact supplied probe and actual failing output, relative to the correction evidence directory.
- `after/auditor_aud01_reproduction.txt`, `after/aud01_valid_conflict.json`, and `after/aud01_malformed_conflict.json`: corrected execution, validation, omissions and raw ownership provenance.
- `before/bundle_trace_inventory.json`, `after/bundle_trace_inventory.json`, and `after/aud02_H4_example.json`: actual old/new clauses, cents and applicability evidence.
- `tests/test_audit_corrections.py`: 14 new source-rule regression methods; `docs/implementation_changes.md` D016-D018 records expectations, contradictions, decisions and qualifications.

## Current executed outputs

| Hospital | Unique invoice IDs | Complete opinions | Flagged opinions | Withheld |
|---|---:|---:|---:|---:|
| H1 | 913 | 250 | 5 | 663 |
| H2 | 1125 | 0 | 0 | 1125 |
| H3 | 932 | 148 | 5 | 784 |
| H4 | 835 | 64 | 1 | 771 |
| H5 | 1050 | 128 | 0 | 922 |

The freshly generated, template-validated `submission.csv` contains **340 target opinions**: six predicted erroneous and 334 predicted correct invoices; no H1 rows. The columns remain exactly `invoice_id,flagged,error_category,expected_total_cents,billed_total_cents,confidence`. Money is serialized as integer cents. Expected/billed totals, full line coverage and confidence-policy consistency were revalidated before local export.

| H1 population | IDs | Opinions | Correct flag + exact cents | Coverage | Error recall over all labelled errors | F1 |
|---|---:|---:|---:|---:|---:|---:|
| development | 622 | 169 | 169/169 | 27.17% | 4/42 (9.52%) | 0.1739 |
| check | 291 | 81 | 81/81 | 27.84% | 1/16 (6.25%) | 0.1176 |
| full | 913 | 250 | 250/250 | 27.38% | 5/58 (8.62%) | 0.1587 |

Full H1 has 245 labelled-correct emitted opinions and five detected errors, with no emitted flag/amount errors. **53 of 58 labelled errors remain withheld.** Perfect matches on the emitted subset do not establish broad accuracy. The check partition was already exposed: this rerun is regression evidence, not a fresh holdout. No H2-H5 labels or accuracy estimates exist. Category-family metrics and their explicit crosswalk are retained in `reports/evaluation_report.md` and `reports/metrics.json`.

All **66,097 raw occurrences** still reconcile: 4,886 headers and 61,211 lines, including the 35 quarantined malformed-date lines; 4,855 unique invoice IDs. No record multiplication or guessed patient allocation was introduced.

## Explicit downstream comparison

Every opinion record across all hospitals is exactly unchanged, including flag, expected/billed cents, category, confidence, confidence tier, mapping grade, invariant-uncertainty flag and interpretation qualifications. All omitted identities, omission reason categories, accounting totals and H1 development/check/full metrics are unchanged. `submission.csv`, `metrics.json` and `workload.json` are independently verified byte-for-byte identical to the preserved originals.

| Hospital | Confidence value: opinion count | Changed scores |
|---|---|---:|
| H1 | 0.65: 5, 0.9: 77, 0.95: 168 | 0 |
| H2 | No opinions | 0 |
| H3 | 0.7: 27, 0.8: 121 | 0 |
| H4 | 0.7: 14, 0.8: 50 | 0 |
| H5 | 0.65: 128 | 0 |

The result files are **not** byte-identical: the intended source/trace metadata enrichment affects 4,784 invoice traces and 1,898 abstention records containing nested calculation diagnostics. This includes standalone stages that now explicitly retain their dated base source. Comparing all result fields after excluding exactly the declared bundle metadata changes found no other difference; all intermediate arithmetic outcomes remain identical. Omission IDs, reason categories and behavior did not change on the supplied data. Before/after counts and hashes are in `reports/corrections/audit_1/correction_verification.json`.

Run identities, trace hashes and release identity changed because the interpreter and evidence changed. The evaluation report's prose now distinguishes H2's present admission/discharge dates from absent actual submission, detailed episode/leave and possible written-exception evidence. It also records the completed first audit and pending closure re-audit. Those documentation changes do not change evaluation numbers.

Current submission SHA-256: `2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c`.

## Regression and reproducibility actually verified

- **75 tests passed**, zero failures/errors/skips, in both the corrected working project and the clean clone. All original 61 methods remain; 14 added methods address ownership propagation and clause-level bundle traces. Test records bind the exact source/test bytes. The new tests include missing patient identity, only-quarantined headers, invalid fields/reordered columns, unrelated and identical patients, daily premium/duplicate/bundle context, H4 bounded scope, all-patient usage, permutation and amended standalone provenance.
- Full five-hospital result objects reproduce under deterministic permutation of loaded headers, lines and dispositions. Frozen H1 opinion fields and every development/check/full metric still match. Current results also match the immediately pre-audit baseline on all substantive fields, not merely counts.
- Guarded all-hospital execution observed **zero label opens during pricing/export** and **zero network attempts** with socket creation/connections blocked. Evaluation read H1 labels only after decisions/export. No LLM API, credentials, GPU or external compute were used. Retained schemas/mappings, not hidden Work state, drive replay.
- A clean local Git clone at **`e5efadf4af7fe58ca1b75d904aac9c426093109d`** removed every old run, generated output and the correction before/after output caches. It used a sanitized environment and actually ran the README reproduction command, submission validation and all 75 tests. The CSV, metrics, workload, evaluation report and full release manifest matched. **All five regenerated hospital trace and input-quality files also matched by hash.** No copied prediction file supplied the result.
- The current decision log remains one page and the existing write-up two pages. Their factual correction/stage updates were rendered and all three pages visually checked; hashes and page images are retained. These remain implementation drafts, not final assessor-facing polish.

The guarded corrected replay measured **37.66 seconds** and **467.73 MiB** peak process RSS in this run (previous observation: 29.50 seconds/421.78 MiB). These are separate measurements, not a controlled performance comparison or scale guarantee. Core replay/tests still require only Python 3.12.13 and its standard library. PDF dependencies remain optional. Fresh LLM extraction is not claimed bit-reproducible.

Clean replay's commit identifies the executed code/input state. Later report/status/checkpoint commits may have different IDs; the recorded source/test, release-input and output hashes establish whether they remain the same tested implementation. Current local attempts are H1 `a1ee1b9f209f4f41913349e165fe8a26` and targets `4d449a6fc6fc49399da2cd567bdb1b51`.

## Gates, limitations and remaining work

The implicated ingestion, context, complete-opinion, confidence/evaluation, export, traceability and reproduction tasks were reopened. Closure now requires current test hashes, current attempts, correction evidence, permutation equality, document hashes and clean replay identity; an old passing report cannot satisfy those checks. `reports/implementation_status.json` maps all 69 governing subtasks to evidence. **65 implementation subtasks are Completed and verified**; BT01-BT10 and all 17 applicable implementation quality gates are addressed. QG02/QG03/QG07/QG09/QG10/QG11/QG12/QG13/QG16 explicitly cite the correction/regression evidence. The four BT11 publishing/delivery tasks and QG18 remain Not started. QG19-QG22 retain the governing exclusions as mandatory requirements.

No unresolved audit correction, implementation blocker or required user action remains for this implemented scope. Limitations remain:

- H2 has no supported complete payable opinion. All 1,132 headers have admission/discharge dates, but actual submission dates, detailed episode/leave evidence and possible written exceptions are not supplied. Invoice date is not renamed submission date; 07:00 Service Day facts are also incomplete. Diagnostic pricing is implemented, with all 1,125 full opinions withheld.
- Other unresolved mappings, compound unit dimensions, allocations and context remain explicit omissions. H3 settlement chronology, H3/H5 exclusion direction, boundary inclusivity and H4 patient aggregation keep their documented interpretations/limits. H5 invoice facility is a disclosed projection, not an observed line attribute; all 128 H5 opinions retain .65 confidence.
- There is no target accuracy or target confidence-calibration claim. Source-derived fixtures and current-data regressions do not prove all arbitrary malformed inputs or every rule combination. The ordinary result validator checks accounting, provenance structure and confidence; it is not a general semantic proof. The additional source/context verification is author evidence and does not replace independent closure re-audit.

The correction report, its tests, all before/after evidence, refreshed traces, current submission and replay instructions are organized within this one repository-ready project. Source-rule extraction was not redesigned or rerun, and no original/reviewer work was overwritten. Publication, assessor permissions and actual email delivery remain later actions.
