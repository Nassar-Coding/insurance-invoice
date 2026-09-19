# Revised Implementation Plan: Rank 29 → Top 3

This plan is written for an implementation agent working in `Nassar-Coding/insurance-invoice`. Work through the gates in order. Do not start a gate until the previous gate's exit criteria pass. Every gate from Gate 2 onward ends in a shippable submission.

---

## 0. Target and fixed facts

**The ranking metric** is `cost = 5·FN + 1·FP`.

- It is computed over 3,942 scored invoices from Hospitals 2–5. There is one row per unique `invoice_id`: H2 has 1,125, H3 932, H4 835 and H5 1,050.
- The scored set contains 285 erroneous invoices and 158 decoys. A decoy is an odd-looking invoice that is actually correct.
- Top 3 means a cost of 0.
- Hospital 1 is **not scored**. Use it only for development.

**What is missing, and what is not:**

- An erroneous invoice with no row counts as a miss (FN) and costs 5.
- A clean invoice with no row costs 0.

**The flagging threshold** is estimated P(error) > 1/6. Below this, a flag costs more in expected false positives than it saves in misses.

**Current state** (rank 29, cost 1395):

- 6 of 285 errors found, 0 false positives.
- 340 rows emitted. H2 has 0 rows.
- The Reproduction and Generalization runs are marked "exited 1". One demonstrated cause is the exact-patch Python check in `pipeline.reproduce()`.

**Grader runs:** every candidate is run three times.

- *Initial*: the submitted file.
- *Reproduction*: your code on the same invoices, from a fresh clone.
- *Generalization*: your code on unseen invoices under byte-identical contracts.

Other candidates lost their runs for three reasons: hard-coded record counts, committed files that name specific invoices, and non-zero exit codes.

### Hospital 1 development data (from `h1_primary_family_coding.csv`)

The development/check split is the existing patient-hash split in `evaluation/split_manifest.json`.

- **Tune only on development.**
- **Read check only at the Final Gate.**

| Partition | Invoices | Erroneous | Clean |
|---|---|---|---|
| development | 622 | 42 | 580 |
| check | 291 | 16 | 275 |

**Primary-family counts.** Each erroneous invoice is assigned to one family, in the priority order structural → term_window → mapping → rule → pricing.

| Family | Categories | Dev | Check |
|---|---|---|---|
| structural | duplicate_invoice_id, cross_invoice_duplicate, contract_number_mismatch, service_date_after_invoice_date, malformed_service_date, line_total_arithmetic, invoice_total_mismatch | 23 | 8 |
| term_window | service_date_out_of_window | 2 | 1 |
| mapping | unknown_service, wrong_unit_basis | 10 | 3 |
| rule | daily_cap_exceeded, exclusion_window_violation | 2 | 2 |
| pricing | unit_price_mismatch, premium_*, volume_discount_*, bundle_not_applied | 5 | 2 |

**Per-category counts.** An invoice can carry more than one category. Use these counts for per-check recall; use the family counts above only for cumulative recall.

| Category | Dev | Check |
|---|---|---|
| unknown_service | 9 | 3 |
| unit_price_mismatch | 7 | 3 |
| wrong_unit_basis | 6 | 5 |
| invoice_total_mismatch | 5 | 1 |
| premium_incorrectly_applied | 5 | 1 |
| service_date_after_invoice_date | 5 | 0 |
| contract_number_mismatch | 4 | 1 |
| duplicate_invoice_id | 4 | 1 |
| malformed_service_date | 4 | 2 |
| service_date_out_of_window | 4 | 1 |
| bundle_not_applied | 3 | 2 |
| exclusion_window_violation | 3 | 1 |
| line_total_arithmetic | 3 | 3 |
| premium_omitted | 3 | 0 |
| volume_discount_incorrectly_applied | 3 | 1 |
| volume_discount_omitted | 3 | 1 |
| cross_invoice_duplicate | 2 | 2 |
| daily_cap_exceeded | 2 | 2 |

**Projection used at every gate.** This assumes Hospitals 2–5 have a similar family mix to Hospital 1, and that assumption is checked in each gate's distribution report.

`projected scored cost ≈ 5 × 285 × (1 − dev recall) + projected FP`

---

## Gate 0 — Survive the grader

**Purpose.** The Reproduction and Generalization runs must exit with code 0 and produce correct output. Nothing else counts until this works.

**0.1 Remove the exact-version gate.**

- In `src/insurance_audit/pipeline.py`, `reproduce()` raises `RuntimeError` unless the interpreter is exactly 3.12.13. Change it to a warning.
- Keep `.python-version` as documentation only.
- Declare `>=3.12,<3.13` in the README.

**0.2 Remove input locks and invoice-specific artifacts.**

Search `src/`, `tools/`, `evaluation/`, `mappings/`, `governance/` and `runs/` for:

- Invoice ID literals, meaning the patterns `INV-H[1-5]-`.
- Hard-coded record counts: 913, 918, 1125, 1132, 932, 939, 835, 840, 1050, 1057, 622, 291, 58, 285.
- `assert len(`.
- Any runtime comparison against the stored `input_hashes` or `source_hashes`. Check `batch.py`: `decision_identity` and `canonical_hash` are applied to source files.

Rules:

- **Hashes** may be *recorded* in outputs, but must never *gate* execution.
- **Invoice-ID lists** that ship in runtime paths must be deleted or moved under `tests/`. This includes the partition manifest if the pipeline reads it at prediction time.
- **The H1 evaluation step** inside `reproduce()` must not run when labels or the manifest are absent, and it must never cause a non-zero exit.

**0.3 Fresh-clone reproduction.**

- Clone the repo into a temporary directory.
- Run the README commands under **two** interpreters, for example 3.12.3 and 3.12.13.
- *Exit:* exit code 0 on both runs, and a byte-identical `submission.csv` across the two runs.

**0.4 Generalization harness (`tools/generalize.py`).** This builds fake "unseen" inputs from Hospital 1 and from each of Hospitals 2–5, then runs the **unmodified** pipeline on them. For each source hospital:

- Re-ID every invoice (new prefix and new numbers), and keep the line → invoice links consistent.
- Subsample 70% of patients, keeping each patient's full history together, and shuffle the row order.
- Perturb 30% of descriptions:
  - change the case;
  - collapse or expand whitespace;
  - swap common abbreviations in either direction (for example Procedure ↔ Proc, Routine ↔ Rtn);
  - reorder tokens around separators;
  - insert one-character typos in non-code tokens.

  Keep service codes such as `/NG-3022` unchanged in half of the perturbed cases and removed in the other half.
- Write the results into a temporary data root with the same file layout.

This matters because your mappings replay frozen, reviewed JSON. On genuinely unseen invoices, new description wording is the most likely failure point, not new IDs.

- *Exit:* exit code 0, a valid schema, and no crash.
- *Exit, tracked from Gate 3 on:* on perturbed Hospital 1 development invoices, recall falls by no more than 10% relative to unperturbed, and there are no new false positives.

**0.5 Repository hygiene.** The repo has no third-party dependencies, so there is nothing to pin. Confirm that `requirements.txt` still installs cleanly with `--no-index`.

**Gate 0 exit:** 0.1 through 0.4 pass. Tag the commit `gate0` and ship it as the fallback submission. It will score the same cost as today, but it will reproduce.

---

## Gate 1 — Measurement

**1.1 Cost scorer (`tools/cost_scorer.py`).**

Inputs:

- the submission file;
- `labels/hospital_1_labels.csv`;
- `h1_primary_family_coding.csv`;
- `--partition development|check|full`.

It should report:

- TP, FN and FP, and cost = 5·FN + FP.
- Recall per category and cumulative recall per family.
- FP on clean invoices, listed by `invoice_id` and error category, so every false positive can be inspected.
- Amount exact-match rate and mean absolute error on true-positive rows.
- A reliability table with 5 bins, plus the expected calibration error (ECE).
- A per-hospital report for **any** hospital present in the submission:
  - row count, flag count and flag rate;
  - category mix;
  - withheld count;
  - confidence histogram.

*Exit:* it reproduces today's Hospital 1 figures (5 TP, 53 FN, 0 FP, cost 265 on the full set) and reports the development/check breakdown.

**1.2 Decision trace (`--trace`).** For every invoice in every hospital, emit one JSON line with:

- the decision: `flag`, `clean`, or `withhold`;
- the checks that fired;
- the unresolved facts (line IDs plus the reason);
- the mapping state of each line: `MATCH`, `NO_MATCH`, `TIE`, or `WEAK`;
- the amount status: `full`, `partial`, or `none`.

*Exit:* every withheld invoice has a named reason.

**1.3 Baseline file.** Write `evaluation/baseline_cost.json` containing:

- the Hospital 1 figures for development, check and full;
- rows and flags per hospital for Hospitals 2–5;
- the leaderboard cost of 1395.

Every later gate appends its own entry to this file.

**1.4 Flag-rate band.** The scored base rate is 285 / 3,942 ≈ 7.2%, and Hospital 1's is 6.4%. Report each hospital's flag rate against these figures.

- **Warning below 4% or above 12%.**
- **Hard stop below 3%:** investigate the withheld reasons for that hospital before continuing. Under a 5:1 cost ratio, under-flagging is the expensive direction.

---

## Gate 2 — Structural checks, term-window checks, and the line-level decision layer, on all five hospitals

**2.1 Loader hardening (one loader for everything).**

- Money is integer cents only.
- Date parsing is strict: an unparseable value becomes `None` plus a malformed marker, and never raises an error.
- Keep **all** physical rows. Scoring has one row per `invoice_id`, but reused-ID history is evidence for duplicate checks and for cumulative pricing.
- Check that the CSV and JSONL files load identically.

**2.2 Structural checks (`checks/structural.py`).** Each check returns line-level or invoice-level findings, together with evidence.

| Check | Rule | Caution |
|---|---|---|
| duplicate_invoice_id | The `invoice_id` appears on more than one physical record. **Flag the ID once**, because the submission has one row per ID. | Use the latest-dated record for `billed_total_cents`. Log the choice. |
| cross_invoice_duplicate | The same patient, service date, normalised service and quantity is billed on two different invoices. Flag the later invoice. | Match on the *normalised* service, not the raw description. Same-day repeats allowed by the contract are **not** duplicates. |
| contract_number_mismatch | The contract number is not the contract (or valid amendment) for that hospital on that date. | Hospital 3 has amendments, so check it by date. |
| service_date_after_invoice_date | The service date is strictly later than `invoice_date`. | **Enabled for all five hospitals, including Hospital 2.** Hospital 2's contract never defines `invoice_date`; its Article 7 is circular filler. But a service cannot be invoiced before it happens. On Hospital 1, all 12 invoices with a line dated after the invoice date are labelled erroneous (0 false positives). Hospital 2 has 15 such invoices. For reused IDs, join each line to its correct physical record: in Hospital 1 the 70+ day gaps all came from lines joined to the wrong record. |
| malformed_service_date | The date is unparseable or impossible. | Distinguish a malformed date from an unusual but valid format. |
| line_total_arithmetic | `quantity × unit_price_cents ≠ line_total_cents`. | Integer arithmetic only. |
| invoice_total_mismatch | The sum of line totals ≠ `invoice_total_cents`. | Compute this after loading every line of the canonical record. |

**Category precedence for date findings.** On Hospital 1, only 5 of those 12 invoices are labelled `service_date_after_invoice_date`; the rest carry other date or ID labels. When several date or ID findings fire on one invoice, name the category in this order:

1. `service_date_out_of_window`, if the date is outside the contract term.
2. `duplicate_invoice_id`, if the ID is reused.
3. `service_date_after_invoice_date`, otherwise.

This affects only category accuracy, not cost.

**Hospital 2 Service Day.** Hospital 2 defines a Service Day as 07:00–06:59 (clause 2.2). The data has dates only, so treat `service_date` as the Service Day date. The boundary cannot create a false after-invoice finding.

**2.3 Term-window check (`checks/term_window.py`).** Flag a service date outside the contract term, taking amendments into account. This needs only the contract's term dates, so extract those per hospital into a small reviewed JSON file with a clause citation.

**2.4 Line-level decision layer (`decision.py`).** This replaces "any unresolved line means withhold the whole invoice".

- **Flag** if any check produces a confident finding, whatever the state of the other lines.
- **Clean** only if every line is resolved and priced, and every check passes.
- **Otherwise withhold.**

Built now, this layer lets every later gate plug in its own checks, so its gains show up in Gates 3–5.

**2.5 Amount on flagged rows.**

- **When all lines are resolved,** use the fully corrected total.
- **When some lines are resolved,** use the *partial correction*: fix the resolved lines and keep the billed amounts for the unresolved lines.
- **Never** emit `expected_total_cents == billed_total_cents` on a flagged row unless the error has no effect on the amount (for example a reused ID with correct pricing). In that case, log the reason.

**2.6 Decoy proxies from real data (`tests/decoy_proxies.py`).**

- Mine the 580 clean Hospital 1 development invoices for odd-looking but correct patterns:
  - same-day repeats of a service;
  - multiple invoices for the same patient;
  - amended rates;
  - boundary dates;
  - zero or unusual quantities;
  - rare descriptions.
- Freeze this set.
- Every check must produce **0 flags** on it.
- Rerun the set at every later gate.

**2.7 Run on Hospitals 1–5.**

*Exit:*

- Development: **≥ 24 of 25** structural and term-window-primary invoices flagged.
- **0 false positives** on the 580 clean development invoices.
- 0 decoy-proxy flags.
- A flag-rate report exists for each of Hospitals 2–5.
- The generalization harness passes.

*Ship point:* `gate2`. Development recall ≈ 0.57, so projected scored cost is ≈ 610 plus FP. That is less than half of today's cost.

---

## Gate 3 — Mapping

**3.1 Four-state matcher (`mapping.py`).** The matcher returns one of four states:

- `MATCH`: the score is at least `MIN_SCORE` and the margin to the second candidate is at least `MIN_MARGIN`.
- `NO_MATCH`: the best score is below `NO_MATCH_FLOOR`.
- `WEAK`: the score falls between the floor and `MIN_SCORE`.
- `TIE`: the score is at least `MIN_SCORE` but the margin is below `MIN_MARGIN`.

Start with `MIN_SCORE = 0.60` and `MIN_MARGIN = 0.08`. These values come from a documented competitor starting point, so treat them as a starting point, not a truth. Set `NO_MATCH_FLOOR` by a sweep on development.

**3.2 A confident no-match is the error.**

- `NO_MATCH` → flag `unknown_service`.
- `unknown_service` is the most common category, and it is currently hidden by abstention.
- Before flagging, confirm that the description does not match any service in *any* contract document for that hospital, including amendments and appendices.
- *Exit:* development `unknown_service` recall **≥ 8 of 9**, with 0 new false positives.

**3.3 Billed price is never evidence.**

- Remove every price feature from the matcher.
- Add a unit test: perturbing `unit_price_cents` or `line_total_cents` must not change any mapping.

**3.4 Unit-basis check (`checks/unit_basis.py`).**

- Flag when `unit_basis_as_billed` differs from the contracted unit basis of the mapped service.
- Only fire on `MATCH` lines.
- *Exit:* development `wrong_unit_basis` recall **≥ 5 of 6**.

**3.5 Reopen the 39 withdrawn mapping keys, one at a time.** For each key:

1. Add the key.
2. Rerun development.
3. Confirm there are 0 new false positives.
4. Confirm the invoice behind the 43,650-cent over-correction now prices correctly or is withheld.
5. Commit the key only if all of these pass. Otherwise log why and leave it withdrawn.

**3.6 Ties and weak matches: price under every reading.**

For a `TIE` or `WEAK` line, compute the audit result under every candidate service.

- **All readings show an error:** flag, with high confidence.
- **Some readings show an error:** mark the line `ambiguous`, and record the fraction of readings that show an error.
- **No reading shows an error:** the line is clean.

Gate 6 decides the threshold for ambiguous lines.

**3.7 Generalization check.** Rerun the harness. The perturbed-description recall drop must stay at or below 10% relative.

*Gate 3 exit:*

- Development cumulative **≥ 33 of 42**.
- 0 false positives on development clean invoices.
- 0 decoy-proxy flags.
- Flag rates for Hospitals 2–5 reported, with none below 3%.

*Ship point:* `gate3`. Development recall ≈ 0.79, so projected cost ≈ 300.

---

## Gate 4 — Contract rules

**4.1 Rule extraction.**

- For each hospital, extract daily caps and exclusion windows into reviewed JSON.
- Each entry carries a clause citation and an effective date range, taking amendments into account.
- Validate the JSON against a schema.

**4.2 Daily cap (`checks/daily_cap.py`).**

- Sum the quantity per patient, per service and per day **across invoices**, using the retained history.
- For Hospital 2, "day" means the Service Day. Caps and threshold premiums are judged on the patient's total for that Service Day across all lines, not per line (clause 3.4).
- Flag when the total exceeds the cap.
- *Exit:* development `daily_cap_exceeded` recall **2 of 2**.

**4.3 Exclusion window (`checks/exclusion.py`).**

- Flag a service billed inside an excluded window. The anchor might be an admission, a prior service or a procedure, according to the clause.
- Record the direction and boundary you chose for each hospital. Hospital 3's exclusion direction is a known ambiguity; send it through the every-reading method from 3.6.
- *Exit:* development `exclusion_window_violation` recall **≥ 3 of 3**.

*Gate 4 exit:*

- Development cumulative **≥ 35 of 42**.
- 0 false positives.
- 0 decoy-proxy flags.

*Ship point:* `gate4`. Projected cost ≈ 240.

---

## Gate 5 — Pricing and amounts

**5.1 Pricing engine (`pricing.py`).**

- Apply the steps in this order: bundle substitution → facility multiplier → plan-tier multiplier → premium or uplift (including weekend and non-business-day) → cumulative volume discount.
- Round half-up to integer cents after each step.
- If a line cannot be priced, **raise an error**. Never let it silently contribute 0.
- **Verified in all five contracts** (clause 3.2 in H1, H2, H3; 4.1 in H4; 3.1 and 3.3 in H5). Half-up rounding after each step is also stated in all five (clause 3.1 in most; 4.2 in H4).
- Hospital 5 clause 3.4: apply the rounding step even when a multiplier is 1.0.
- Hospital 4 clause 8.2 says the discount comes last "except as provided in Section 8.3". Section 8.3 only defines thresholds and changes nothing about the order. Treat it as no exception, and log the reading.
- Hospital 2 "Business Day" (used for the weekend or non-business-day premium) depends on the day the Service Day *starts* (clause 2.4).

**5.2 Cumulative volume discounts.** The discount threshold counts prior utilisation *across invoices*, using retained history, not just the current invoice. Reused IDs must not be double-counted.

**The discount granularity differs between hospitals.** Read it from each contract and implement it per hospital; do not assume one rule.

- **Hospital 4 (clauses 8.3–8.5): line-level.**
  - The discount applies to a line only when utilisation *before* that line already exceeds the threshold. It does not apply to the line that crosses the threshold.
  - Utilisation is counted in service-date order; lines on the same date are counted in ascending line ID order.
  - Where a service has more than one threshold, the deeper discount applies once its threshold is exceeded.
- **Hospital 2 (e.g., clause 8.3): unit-level.**
  - The discount applies to "each subsequent Unit", so a single line can straddle the threshold. Price the units before and after the threshold separately.
  - Utilisation is counted across all patients over the whole contract term.
- **Hospitals 1, 3 and 5:** confirm which of these two models their discount clauses use before implementing, and log the clause.
- Add a hand-computed unit test for each model, including a line that straddles the threshold (Hospital 2) and a line that crosses it (Hospital 4).

**5.3 Pricing detections.** Flag when the recomputed total differs from the billed total on fully resolved lines. Map the difference to the specific category (for example `premium_omitted` rather than a generic mismatch).

**5.4 Daily-cap amounts.**

- **When billed quantity exceeds the cap,** correct the amount to the capped quantity.
- **When the correct quantity below the cap is unobservable,** flag the invoice, emit the capped-quantity amount, and apply a confidence penalty.

Apply one rule everywhere and document it.

**5.5 Hand-computed unit tests.** Write at least two per rule family, taken from the actual contract clauses.

*Gate 5 exit:*

- Development cumulative **≥ 40 of 42**.
- 0 false positives on development clean invoices.
- Amount exact-match **≥ 0.90** on development true positives.
- 0 decoy-proxy flags.

*Ship point:* `gate5`. Projected cost ≈ 70 plus FP.

---

## Gate 6 — Ambiguity threshold and confidence (keep short)

**6.1 Ambiguity threshold.**

- For invoices whose only findings are `ambiguous` lines, sweep the error-fraction threshold from 1/6 to 1.
- Choose the value that minimises development cost, 5·FN + FP.
- If development has too few ambiguous cases to fit, default to **flagging when a majority of readings show an error**, and log it.

**6.2 Confidence tiers.**

- Fit the tiers to development accuracy per tier:
  - structural;
  - `MATCH` with full pricing;
  - `NO_MATCH`;
  - ambiguous;
  - partial amount;
  - clean.
- Cap confidence for Hospitals 2–5 below the fitted Hospital 1 values, because there is no labelled calibration data for them.
- Calibration is measured by the organisers but is **not part of the ranking cost**. Stop once confidence rises monotonically with accuracy and ECE ≤ 0.08.

---

## Gate 7 — Decoy and distribution audit

**7.1** Rerun the decoy proxies. There must be 0 flags.

**7.2** For each of Hospitals 2–5, sample 15 flagged invoices and 15 withheld invoices, and inspect their traces.

- **A flag with thin evidence** means the check needs a tighter rule.
- **A withheld invoice that shows an obvious error** means there is an abstention leak. Fix it, then rerun Gates 2–5 on development.

**7.3** Flag rates for all four hospitals are within 4–12%, or any deviation is explained in the trace.

---

## Final Gate — Held-out read, reproduction, freeze

**F.1 Read the check partition once.** Report the check-partition cost.

- If it is **far worse than development** (a check-partition cost above 30 while development is near 0), there is overfitting. Find the rule that fails on check and fix it *generally*, never by invoice.
- After any fix, the check partition becomes regression evidence and is no longer held-out. State this honestly in the report.

**F.2 Validate the submission (`tools/validate_submission.py`).**

- Exact column order: `invoice_id, flagged, error_category, expected_total_cents, billed_total_cents, confidence`.
- `flagged` is 0 or 1.
- `confidence` is between 0 and 1.
- Money is integer cents only.
- One row per `invoice_id`, with no duplicates.
- IDs are drawn only from Hospitals 2–5.
- `billed_total_cents` matches the source data.

**F.3 Rerun the generalization harness.** It must exit with code 0, and perturbed recall must stay within tolerance.

**F.4 Fresh-clone reproduction.** Use two interpreters. The output must be byte-identical, and the exit code must be 0.

**F.5 Update the reports.** Update `EVALUATION_REPORT.md`:

- per-category development and check results;
- the three or four systematic failure modes, each with an example;
- the assumptions made for each hospital;
- what was not attempted.

**F.6 Freeze and submit.** Record the SHA-256 of `submission.csv`, then submit.

---

## Non-negotiable rules

1. No invoice IDs, record counts or input hashes in runtime logic.
2. Every gate runs on all five hospitals. No gate is complete until Hospitals 2–5 have been re-emitted and their flag rates reported.
3. Tune on development only. Read the check partition once, at the Final Gate.
4. A change that adds a false positive on development clean invoices or on the decoy proxies is reverted unless it removes at least one development miss. Five false positives cost the same as one miss, but decoy resistance is required for top 3, so prefer rules that achieve both.
5. Never use billed price as mapping evidence.
6. Never emit a clean assertion for an invoice that has not been fully audited.
7. A flagged row's amount is the full or partial correction, never a fabricated figure.
8. Commit and tag at every ship point: `gate0`, `gate2`, `gate3`, `gate4`, `gate5`.

## Suggested 48-hour budget (2-day revisit window)

| Hours | Work |
|---|---|
| 0–3 | Gate 0. Ship the reproducible `gate0` tag. |
| 3–6 | Gate 1: scorer, trace, baseline. |
| 6–16 | Gate 2 on all five hospitals. Ship `gate2`, the largest single cost drop. |
| 16–28 | Gate 3: mapping, including reopening the 39 keys. Ship `gate3`. |
| 28–33 | Gate 4: contract rules. Ship `gate4`. |
| 33–41 | Gate 5: pricing and amounts. Ship `gate5`. |
| 41–43 | Gate 6: ambiguity threshold and confidence. |
| 43–45 | Gate 7: decoy and distribution audit. |
| 45–48 | Final Gate. Keep this slot even if earlier gates overrun; cut Gate 6 first. |

## Stopping points

| Stop after | Development recall | Projected scored cost | Rough rank band |
|---|---|---|---|
| Gate 0 | same as now | 1395 (but reproducible) | 29 |
| Gate 2 | ~0.57 | ~610 + FP | ~15–20 |
| Gate 3 | ~0.79 | ~300 + FP | ~11–13 |
| Gate 4 | ~0.83 | ~240 + FP | ~11–12 |
| Gate 5 | ~0.95 | ~70 + FP | ~8–10 |
| Gate 7 plus Final Gate | ~1.00, 0 FP | ~0 | top band |

The projections assume Hospitals 2–5 have Hospital 1's family mix, and each gate's distribution report tests that assumption. The rank bands come from the leaderboard PDF: cost 47–50 sat at ranks 8–9, 138 at rank 10, 225 at rank 11, and 1110 at rank 24.

## Open items to confirm before investing heavily

- ~~Time cap~~ **Resolved:** the top 30 have a 2-day revisit window with no hour cap. Assume the new commit will be re-run through Reproduction and Generalization, so Gate 0 and the Final Gate still apply in full. Record the revisit in `EVALUATION_REPORT.md`: what changed, and why.
- **Tie-breaking at cost 0.** The PDF does not say how ties at cost 0 are broken. It is not generalization cost, and not strictly amount accuracy.
- ~~Hospital 2 dates~~ **Resolved:** `invoice_date` is undefined in the contract, but the after-invoice check stays enabled on evidence from Hospital 1 (see Gate 2.2).
- ~~Pricing order~~ **Resolved:** the order is identical in all five contracts. The volume-discount granularity differs between hospitals (see Gate 5.1 and 5.2).
