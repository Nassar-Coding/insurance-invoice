# Hospital 1 evaluation and implementation limitations

These are executed results from the current deterministic pipeline. Hospital 1 is development data. The patient-group check was first opened after the mapping and confidence freeze; the current check is a regression after that exposure, not a new holdout. Full H1 includes development. No target labels or target accuracy estimates exist.

| Partition | All IDs | Opinions | Coverage | Flag + exact cents on opinions | Error precision | Error recall, all IDs | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| development | 622 | 169 | 27.17% | 169/169 | 100.00% | 9.52% | 0.1739 |
| check | 291 | 81 | 27.84% | 81/81 | 100.00% | 6.25% | 0.1176 |
| full | 913 | 250 | 27.38% | 250/250 | 100.00% | 8.62% | 0.1587 |

Abstentions are excluded from conditional accuracy and counted as missed positives in population recall. They are never correct negatives. The joint event is a correct binary flag and exact corrected cents; billed cents, identity, and complete line provenance are separately validated. Free-text category correctness is measured by a disclosed many-to-one family crosswalk, not folded into that joint event. Undefined denominators remain undefined. High conditional accuracy with low recall is a substantial limitation.

## Per-category development performance

Family precision/recall use the explicit crosswalk in `src/insurance_audit/evaluation.py`. Broad pricing diagnostics do not establish which particular premium or discount caused a rate mismatch.

| Family | Positive labels | TP | FP | Misses incl. abstentions | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| date | 12 | 0 | 0 | 12 | undefined | 0.00% | 0.0000 |
| duplicate | 2 | 0 | 0 | 2 | undefined | 0.00% | 0.0000 |
| eligibility | 3 | 0 | 0 | 3 | undefined | 0.00% | 0.0000 |
| identity | 7 | 1 | 0 | 6 | 100.00% | 14.29% | 0.2500 |
| invoice_arithmetic | 5 | 1 | 0 | 4 | 100.00% | 20.00% | 0.3333 |
| line_arithmetic | 3 | 1 | 0 | 2 | 100.00% | 33.33% | 0.5000 |
| mapping | 9 | 0 | 0 | 9 | undefined | 0.00% | 0.0000 |
| pricing | 21 | 2 | 0 | 19 | 100.00% | 9.52% | 0.1739 |
| quantity | 2 | 0 | 0 | 2 | undefined | 0.00% | 0.0000 |
| unit | 6 | 2 | 0 | 4 | 100.00% | 33.33% | 0.5000 |

Original-label detection is also reported below. This table measures detection on invoices carrying each label, not category-specific precision. An invoice can carry multiple labels.

| Original label | Support | Covered | Flagged | Exact amount | Joint successes | Detection recall |
|---|---:|---:|---:|---:|---:|---:|
| bundle_not_applied | 3 | 0 | 0 | 0 | 0 | 0.00% |
| contract_number_mismatch | 4 | 1 | 1 | 1 | 1 | 25.00% |
| cross_invoice_duplicate | 2 | 0 | 0 | 0 | 0 | 0.00% |
| daily_cap_exceeded | 2 | 0 | 0 | 0 | 0 | 0.00% |
| duplicate_invoice_id | 4 | 0 | 0 | 0 | 0 | 0.00% |
| exclusion_window_violation | 3 | 0 | 0 | 0 | 0 | 0.00% |
| invoice_total_mismatch | 5 | 1 | 1 | 1 | 1 | 20.00% |
| line_total_arithmetic | 3 | 1 | 1 | 1 | 1 | 33.33% |
| malformed_service_date | 4 | 0 | 0 | 0 | 0 | 0.00% |
| premium_incorrectly_applied | 5 | 1 | 1 | 1 | 1 | 20.00% |
| premium_omitted | 3 | 0 | 0 | 0 | 0 | 0.00% |
| service_date_after_invoice_date | 5 | 0 | 0 | 0 | 0 | 0.00% |
| service_date_out_of_window | 4 | 0 | 0 | 0 | 0 | 0.00% |
| unit_price_mismatch | 7 | 1 | 1 | 1 | 1 | 14.29% |
| unknown_service | 9 | 0 | 0 | 0 | 0 | 0.00% |
| volume_discount_incorrectly_applied | 3 | 0 | 0 | 0 | 0 | 0.00% |
| volume_discount_omitted | 3 | 0 | 0 | 0 | 0 | 0.00% |
| wrong_unit_basis | 6 | 2 | 2 | 2 | 2 | 33.33% |

## Confidence support

Confidence scores were frozen from development evidence before check exposure. Correct-row groups use conservative bounded scores; sparse error groups use .65 policy judgment. Targets use .80 (explicit) or .70 (generic noun elision); outcome-invariant uncertainty and outcome-relevant invoice facility projection are capped at .65. These are conservative judgments, not demonstrated target probability calibration. Missing necessary facts cause whole-invoice omission.

| Development tier | n | Joint successes | Mean confidence | Brier score |
|---|---:|---:|---:|---:|
| h1_supported:elided:0 | 43 | 43 | 0.9000 | 0.0100 |
| h1_supported:explicit:0 | 122 | 122 | 0.9500 | 0.0025 |
| sparse:explicit:1 | 4 | 4 | 0.6500 | 0.1225 |

## Four systematic failure mechanisms

1. **Overconfident service identity (observed and corrected).** Initial mapping assigned generic `Fract Outpatient Radiotherapy` to a metabolic service without evidence of the specialty. Development invoice INV-H1-000236 had a corrected amount overstated by 43,650 cents. All 39 analogous missing-essential-qualifier keys were withdrawn, with initial results preserved. This fixed an observed emitted error at a substantial coverage cost; it is not an invoice-specific answer patch.

2. **Insufficient description evidence (current abstention mechanism).** Unknown, ambiguous, or essentially incomplete descriptions prevent a complete invoice opinion and can also make related usage uncertain. Example `INV-H1-000002` was withheld for `unresolved_service_mapping`; its development truth is flagged=1. See that invoice's current trace.

3. **Damaged source identity or dates (current abstention mechanism).** Conflicting reused invoice IDs and malformed dates cannot be corrected into a unique supported invoice total. Example `INV-H1-000068` was withheld for `conflicting_reused_invoice_id`; its development truth is flagged=1. See that invoice's current trace.

4. **Unobservable rule context (current abstention mechanism and target applicability risk).** Unresolved related rows, exclusion boundary/direction, or duplicate allocation can change the result. Example `INV-H1-000151` was withheld for `multiple_supported_rate_outcomes`; its development truth is flagged=1. See that invoice's current trace. H2 supplies admission/discharge dates, but actual submission dates, detailed episode/leave evidence and possible written exceptions remain unobserved under Articles II and XIII, so all its full opinions are withheld. H4 patient scope is bounded; H5 invoice facility projection is explicitly qualified.

Only the first mechanism is an observed emitted wrong amount during development. The others explain observed omissions or unlabelled target risks, not invented scored failures. After the correction the current emitted H1 joint event has no observed errors; that does not establish accuracy outside the covered subset.

## Target coverage and unresolved workload

| Hospital | Unique IDs | Opinions | Flagged | Withheld | Coverage | Unresolved mapping keys |
|---|---:|---:|---:|---:|---:|---:|
| H2 | 1125 | 0 | 0 | 1125 | 0.00% | 137 |
| H3 | 932 | 148 | 5 | 784 | 15.88% | 85 |
| H4 | 835 | 64 | 1 | 771 | 7.66% | 108 |
| H5 | 1050 | 128 | 0 | 922 | 12.19% | 76 |

Every raw CSV occurrence is accounted for. All five source contracts and all observed mapping keys were examined; complete invoice coverage remains limited by evidence. `workload.json` records overlapping omission causes and review items. The system audits the supplied historical snapshot, not an unseen complete claims feed. Late or corrected records require a new run and context recomputation.

Replay uses retained reviewed schemas/mappings and standard-library Python. Repeating fresh LLM extraction is a different activity and is not claimed bit-reproducible. Quarantined-header ownership propagation (AUD-01) and controlling bundle citations (AUD-02) are covered by regression tests; before/after evidence is retained under reports/corrections/audit_1.
