# Gate 2 — structural checks, term-window checks and the line-level decision layer

Published as `b886bb1` (steps 1–5) and `92eec96` (step 6); this report closes the gate.

## Exit criteria

| Criterion | Target | Result |
|---|---|---|
| Structural and term-window primary development invoices reported | ≥ 24 of 25 | **PASS — 25 of 25** (structural 23/23, term window 2/2) |
| False positives on the 580 clean development invoices | 0 | **PASS — 0** |
| Decoy-proxy flags | 0 | **PASS — 0 of 184** |
| Flag rate reported for H2–H5, H2 above 0% | H2 > 0% | **PASS — H2 3.91%, H3 4.94%, H4 4.55%, H5 4.10%** |
| Development cost and withheld-reason histogram | reported | below |

Development on Hospital 1: **26 TP, 16 FN, 0 FP, cost 80**, against the Gate 1
baseline of 4 TP, 38 FN, 0 FP, cost 190. Amount exact match on true positives
0.846 (22 of 26); mean absolute error 9,771 cents. Submission rows 340 → 512.

Per-category development detection is 100% for every structural category and for
`service_date_out_of_window`: `contract_number_mismatch` 4/4, `duplicate_invoice_id`
4/4, `invoice_total_mismatch` 5/5, `line_total_arithmetic` 3/3,
`malformed_service_date` 4/4, `service_date_after_invoice_date` 5/5,
`cross_invoice_duplicate` 2/2, `service_date_out_of_window` 4/4.

The generalization harness and the clean-checkout run were not re-run; both are
deferred to the Final Gate by instruction. The check partition was not read.

## What changed

Withholding an invoice because a required fact was unresolved was hiding errors
whose evidence *was* that unresolved fact. Gate 1 measured 14 of the 38 missed
development errors in exactly that position.

1. **A mapping-free findings layer** (`src/insurance_audit/findings.py`) reads the
   physical records plus the identifiers, term dates and express duplicate clause
   of each contract. A finding survives an unmapped line, an ambiguous rate or an
   unobservable submission date. Date and identifier findings are named in the
   plan's precedence: term window → reused identifier → after-invoice.
2. **Quarantined records are classified rather than treated as one blocker.** A
   malformed date or money field is a billing defect and is reported; a missing
   identifier or ragged row still only means the record cannot be attributed and
   stays an unresolved fact. Every quarantined record in all five snapshots is a
   malformed service date, so all 30 are now reported instead of withheld.
3. **Hospital 2's Article XIII** conditions effectiveness on a submission date the
   data never records. It is logged as unresolved on the trace and suppresses
   nothing. H2 emits rows for the first time.
4. **Cross-invoice duplicates** fire only where the contract expressly forbids
   billing a Service twice for one Patient and Service Date — H1 §11.4, H3 §10.3,
   H4 §11.3, H5 §10.3 each say so and H2's agreement does not, so H2 is excluded.
   Matching is on patient, Service Day, normalised service and quantity; the
   earliest invoice is left alone; a reused identifier is excluded because its
   lines cannot be attributed to one patient. Both development cases are found
   with no false positive, including on the two near-miss decoy proxies.
5. **The decision layer is line-level.** A confident finding is reported whatever
   else is unresolved; a clean assertion still requires every line priced;
   anything else is withheld with a named reason. Amounts are the full correction
   where every line priced and a partial correction otherwise: an unpriced line
   keeps its billed amount, an arithmetic line total is recomputed from its own
   quantity and unit price, and a line billed twice across invoices contributes
   nothing. A reused identifier reports the latest-dated record's total unchanged,
   which matches every labelled development case. A flagged row whose amount
   equals the billed amount records why.
6. **Decoy proxies** (`tests/evaluation/decoy_proxies.json`, 184 of 580 clean
   development invoices) are frozen and checked per pattern and overall.

## Withheld-reason histogram (exclusive first runtime reason)

| Reason | H1 dev | H2 | H3 | H4 | H5 |
|---|---:|---:|---:|---:|---:|
| `composite_dimension_unobserved` | 0 | 13 | 21 | 26 | 22 |
| `duplicate_service_day_allocation` | 1 | 0 | 3 | 2 | 1 |
| `multiple_supported_rate_outcomes` | 31 | 385 | 94 | 96 | 145 |
| `possible_duplicate_service_day` | 5 | 0 | 6 | 6 | 13 |
| `unobserved_service_day_cap_allocation` | 0 | 22 | 0 | 0 | 0 |
| `unresolved_exclusion` | 2 | 0 | 2 | 4 | 1 |
| `unresolved_service_mapping` | 392 | 654 | 617 | 600 | 697 |
| **Total withheld** | **431** | **1074** | **743** | **734** | **879** |

Every reason that was itself error evidence has gone: `conflicting_reused_invoice_id`,
`quarantined_required_source_record`, `service_date_after_invoice`,
`service_date_outside_term` and `unobserved_submission_deadline_and_waiver` no
longer withhold any invoice in any hospital. What remains is genuinely unresolved:
service mapping, rate ambiguity, same-day allocation, exclusion state and cap
allocation. Every withheld invoice still carries a named reason.

## The 16 remaining development misses

| Primary family | Withheld reason | Count |
|---|---|---:|
| mapping | `possible_duplicate_service_day` | 5 |
| mapping | `unresolved_service_mapping` | 3 |
| mapping | `unresolved_exclusion` | 1 |
| pricing | `unresolved_service_mapping` | 4 |
| pricing | `multiple_supported_rate_outcomes` | 1 |
| rule | `unresolved_service_mapping` | 1 |
| rule | `unresolved_exclusion` | 1 |

No structural or term-window error is missed. Nine of the sixteen are blocked by
the service mapping, which is Gate 3; the rest are Gates 4 and 5.

## Flag rates against the 7.2% scored base rate

| Hospital | Invoices | Rows | Flags | Flag rate | Band |
|---|---:|---:|---:|---:|---|
| H1 (unscored) | 913 | 281 | 36 | 3.94% | below 4% warning |
| H2 | 1,125 | 51 | 44 | 3.91% | below 4% warning |
| H3 | 932 | 189 | 46 | 4.94% | within band |
| H4 | 835 | 101 | 38 | 4.55% | within band |
| H5 | 1,050 | 171 | 43 | 4.10% | within band |

No hospital is below the 3% hard stop. The rates are close to one another and to
Hospital 1's, which is consistent with the plan's assumption that the scored
hospitals share Hospital 1's family mix, though that remains an assumption. The
gap to 7.2% is expected at this gate: the mapping, rule and pricing families are
not yet detected, and they account for 17 of Hospital 1's 42 development errors.

## Readings recorded

- **H2 cross-invoice duplicates are withheld, not flagged.** H2's contract carries
  no prohibition on billing a Service twice for one Patient and Service Date while
  the other four state one expressly. Seven H2 invoices match the pattern and are
  not reported. This is the decoy-strict reading and is the single most likely
  place to revisit at Gate 7.
- **`service_date_after_invoice_date` is enabled on H2** although H2's contract
  never defines `invoice_date`: a service cannot be invoiced before it happens.
- **A reused identifier's canonical record is the latest-dated one.** Every
  labelled development case agrees, for both the billed and the expected total.
- **H3's amendment keeps the base agreement's contract number**, so the
  contract-number check needs no date awareness; every mismatch in all five
  snapshots is another hospital's contract number.

## Scope

Prediction logic, the decision layer and the amount policy changed. Mappings,
schemas, the confidence policy and the pricing engine did not. 118 tests pass
(95 existing, 19 new findings tests, 4 decoy-proxy tests). Submission SHA-256
`ed65b5f7c6407a733111802f3d4d3f4ce1c80182e3fb113bb5afbbb83773d140`.
