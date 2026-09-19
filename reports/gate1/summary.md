# Gate 1 — lean rebuild result

All three measurement steps are complete. Step 1 published as `7c20498d09311f92ee9ddac1f816b03fc03849b0`; step 2 as `413fd4fc7c336d2342099bafea9613d3ad851775`. The step 3 commit introducing this report completes the baseline register; no tags are created.

| Criterion | Result | Evidence |
|---|---|---|
| Development scorer | PASS — 4 TP / 38 FN / 0 FP; cost 190 | `cost_development.json` |
| Full H1 scorer | PASS — 5 TP / 53 FN / 0 FP; cost 265 | `cost_full.json` |
| All-invoice trace and named withholding | PASS — 4,855 traces; 4,265 named withheld decisions | `trace_summary.json`, `decision_trace.jsonl.gz` |
| Histograms and missed-error cross-tab | PASS — five scopes; exactly 38 development misses | `withheld_reasons.json`, `missed_development_crosstab.json` |
| Baseline registration | PASS — measured H1/target distributions and external cost 1395 registered | `evaluation/baseline_cost.json` |
| Generalization baseline recording | PASS — prior 4 → 1 dev detections; 0 new FP; not rerun | Baseline provenance explicitly marks carried-forward evidence |
| Measurement-only invariant | PASS — 340 submission rows, 6 flags, identical bytes and all ten runtime outputs | `final_verification.json` |
| Regression tests | PASS — 92 tests (84 existing + 8 measurement tests) | `reports/tests_gate1_rebuild.json` |

Submission SHA-256: `2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c`.

## Withheld-reason histograms

Exclusive first-runtime-reason counts. Overlapping any-reason invoice incidence is retained separately in JSON.

| Reason | H1 dev | H2 | H3 | H4 | H5 |
|---|---:|---:|---:|---:|---:|
| `composite_dimension_unobserved` | 0 | 0 | 21 | 28 | 22 |
| `conflicting_reused_invoice_id` | 4 | 7 | 7 | 5 | 7 |
| `duplicate_service_day_allocation` | 1 | 0 | 3 | 2 | 1 |
| `multiple_supported_rate_outcomes` | 31 | 0 | 95 | 97 | 146 |
| `possible_duplicate_service_day` | 6 | 0 | 9 | 8 | 17 |
| `quarantined_required_source_record` | 4 | 8 | 6 | 6 | 8 |
| `service_date_after_invoice` | 3 | 0 | 3 | 1 | 2 |
| `service_date_outside_term` | 2 | 0 | 3 | 1 | 1 |
| `unobserved_submission_deadline_and_waiver` | 0 | 1110 | 0 | 0 | 0 |
| `unresolved_exclusion` | 2 | 0 | 2 | 5 | 1 |
| `unresolved_service_mapping` | 400 | 0 | 635 | 618 | 717 |
| **Total** | 453 | 1125 | 784 | 771 | 922 |

H2 zero rows are fully accounted for: 1,110 submission-deadline/waiver uncertainties, 7 conflicting reused IDs, 8 quarantined records. The H2 policy is unchanged.

## Cross-tab: all 38 missed development errors

| Primary family | Withheld reason | Count |
|---|---|---:|
| mapping | `possible_duplicate_service_day` | 5 |
| mapping | `unresolved_exclusion` | 1 |
| mapping | `unresolved_service_mapping` | 3 |
| pricing | `multiple_supported_rate_outcomes` | 1 |
| pricing | `unresolved_service_mapping` | 4 |
| rule | `unresolved_exclusion` | 1 |
| rule | `unresolved_service_mapping` | 1 |
| structural | `conflicting_reused_invoice_id` | 4 |
| structural | `quarantined_required_source_record` | 4 |
| structural | `service_date_after_invoice` | 3 |
| structural | `service_date_outside_term` | 1 |
| structural | `unresolved_service_mapping` | 8 |
| term_window | `possible_duplicate_service_day` | 1 |
| term_window | `service_date_outside_term` | 1 |

All 38 misses are withheld, rather than emitted-clean decisions. Family totals: structural 20, term_window 2, mapping 9, rule 2, pricing 5.

H2–H5 flag rates remain 0%, 0.5365%, 0.1198%, 0%. All below-3% rates have named-reason investigations; this measurement gate does not raise the rates. The plan's family-mix extrapolation remains an unverified assumption, not measured target performance.

Decoy-proxy flags are not measured: the proxy set is defined at Gate 2.6. Clean-development FP is 0/580. The carried-forward full-history generalization result has a 75% relative recall drop; it does not satisfy the future Gate 3 <=10% tolerance. The earlier sampled/re-ID test changed utilisation context and is not the same baseline. Original experiment logs were lost; no new experiment or log is claimed.

No clean-checkout verification was performed. A3 is waived and Gate 0 is closed by user instruction. After this Gate 1 baseline, do not read or report the check partition again until Final Gate. No prediction logic, mappings, schemas, confidence or uncertainty behavior changed. Gate 2 has not started.
