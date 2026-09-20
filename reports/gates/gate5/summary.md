# Gate 5 — pricing and amounts

## Exit criteria (development partition)

| Criterion | Target | Result |
|---|---|---|
| Cumulative detection | ≥ 40 of 42 | **PASS — 40 of 42** |
| False positives on the 580 clean development invoices | 0 | **PASS — 0** |
| Decoy-proxy flags | 0 | **PASS — 0 of 184** |
| Amount exact match on true positives | ≥ 0.90 | **PASS — 0.925** (37 of 40) |
| Flag rates H2–H5 | reported | 5.60 / 7.19 / 6.47 / 6.19 % |

Dev cost 10 (40 TP, 2 FN, 0 FP), unchanged from Gate 4. Amount exact match rose
0.775 → 0.925; mean absolute error 3,634 cents. Submission rows 1,881 → 1,977.

## The discount model, read from each contract

The brief specified Hospital 2 as **unit-level** ("each subsequent Unit", a line
straddling the threshold priced in two parts). **Its own calculation clause says
otherwise and was followed instead.** H2 clause 3.5: *"A cumulative volume
discount applies to a line item where cumulative utilisation of the Service
prior to that line item exceeds the stated threshold."* Clause 8.3's "each
subsequent Unit" describes which units are discounted; clause 3.5, in the
calculation article, fixes how that is applied — per line item, on prior
utilisation. Where a general calculation clause and a rate clause appear to
differ, the clause that expressly addresses the mechanics governs.

All five hospitals are therefore **line-level**, each stating it directly:

| Hospital | Clause | Scope |
|---|---|---|
| H1 | 2.4 — "up to but excluding the line item being priced" | all patients, whole term |
| H2 | 2.7, 3.5 — as above | all patients, whole term |
| H3 | 6.1 — "up to but excluding the line item being priced" | all patients, whole term |
| H4 | 8.3–8.5 — "does not apply to the line item on which the threshold is first crossed" | **patient scope unstated** |
| H5 | 8 — "discount on subsequent units" | all patients, whole term |

Ties are broken in ascending line-identifier order within a Service Date (H2 3.5,
H3 6.1, H4 8.5). The deeper tier replaces the shallower one and they do not
compound. H4's clause never says whether utilisation aggregates across patients,
so a different patient's history leaves its rate undetermined rather than
assumed — there is a test for that.

## What changed

**An unknown service has no contracted rate.** A line naming a service the
contract does not sell was being priced against whichever service it most
resembled, putting a fabricated figure on the row. It now keeps its billed
amount and only the naming is reported. `unknown_service` joins the
amount-neutral findings.

**A reused identifier's lines are separable, and the data proves it.** These
snapshots number a line after the invoice record that raised it, so a line
identifier says which physical record it belongs to. The split is used only
when it reconciles: each group's billed total must match one header's exactly.
That holds for 29 of the 31 reused identifiers across all five hospitals; the
two that do not reconcile fall back to reporting the canonical billed total
unchanged. Once attribution holds, the owning patient is known rather than
merely possible, which lets the exclusion, cap and duplicate checks reach a
verdict on those invoices at all.

*This uses billed totals, deliberately.* It is reconciliation, not
identification: no line's mapping moves. The price-independence test now asserts
that line by line, and a second test asserts that only a reused identifier can
change which lines are audited.

**An unreadable description is no longer a possible duplicate of everything.**
An unresolved description inherited *every* service in the contract as a
candidate, so it became a possible same-day duplicate of every other line for
that patient, withholding whole invoices over one unreadable line. Candidates
now come from the matcher. This alone moved amount exact match 0.85 → 0.925 and
released 9 more invoices.

**A wrong rate is named after the adjustment that explains it.** If applying one
of the service's own adjustments to the billed rate reaches the contracted rate,
the provider omitted it (`premium_omitted`, `volume_discount_omitted`,
`bundle_not_applied`); if applying it the other way reaches the billed rate,
they applied one the contract does not give. Anything no adjustment explains
stays `unit_price_mismatch`.

**Daily-cap amounts — one rule, everywhere.** The contract caps what is
billable, but nothing in the record shows how many units were actually delivered
below that cap. The corrected amount is the capped quantity and the row carries
the qualification `capped_quantity_substituted_for_an_unobserved_one`, which
Gate 6 turns into a confidence penalty. The quantity the data omits is never
guessed. Both development cap invoices are detected; both keep an inexact
amount by design, and they are 2 of the 3 remaining amount misses.

## Hand-computed tests

19 tests in `tests/test_pricing_clauses.py`, every figure worked out from the
quoted clause rather than read back from the engine: half-up rounding including
exact halves and negatives; the H2 threshold-crossing line (59 → 9675, 60 →
9675, 61 → 8708, 180 → 8708, 181 → 7740) and a line that would straddle 60
priced whole; the H4 crossing line (80 → 157150, 81 → 133578, 240 → 133578,
241 → 110005) and non-compounding tiers; the cap at and above its limit; the six
adjustment-naming cases; and the declared adjustment order in all five
contracts.

168 tests pass. The check partition was not read.
