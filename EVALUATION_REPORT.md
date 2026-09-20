# Evaluation report

Deterministic contract-to-invoice auditing. Reviewed contract records and service
mappings drive replay; no model calls, API keys or GPU. All figures below are
produced by `tools/cost_scorer.py` against Hospital 1's labels.

The ranking metric is `cost = 5·FN + 1·FP` over Hospitals 2–5. Hospital 1 is
labelled and unscored; it is the only place accuracy can be measured at all.

## Headline

| | Development | Check |
|---|---|---|
| Erroneous invoices | 42 | 16 |
| Clean invoices | 580 | 275 |
| True positives | **40** | **16** |
| False negatives | 2 | 0 |
| False positives | **0** | **0** |
| **Cost (5·FN + FP)** | **10** | **0** |
| Amount exact match on TPs | 0.925 | 0.875 |
| Expected calibration error | 0.0322 | 0.0293 |

The check partition was read **once**, at this gate, and nothing was changed as
a result, so it remains genuinely held out rather than regression evidence.

Rows emitted: 444 of 622 development, 217 of 291 check. 0 flags on all 184
frozen decoy proxies, and 0 on every pattern taken separately.

## Per-category results

| Category | Development | Check |
|---|---|---|
| bundle_not_applied | 3/3 | 2/2 |
| contract_number_mismatch | 4/4 | 1/1 |
| cross_invoice_duplicate | 2/2 | 2/2 |
| daily_cap_exceeded | 2/2 | 2/2 |
| duplicate_invoice_id | 4/4 | 1/1 |
| exclusion_window_violation | 3/3 | 1/1 |
| invoice_total_mismatch | 5/5 | 1/1 |
| line_total_arithmetic | 3/3 | 3/3 |
| malformed_service_date | 4/4 | 2/2 |
| premium_incorrectly_applied | 5/5 | 1/1 |
| **premium_omitted** | **2/3** | — |
| service_date_after_invoice_date | 5/5 | — |
| service_date_out_of_window | 4/4 | 1/1 |
| **unit_price_mismatch** | **6/7** | 3/3 |
| unknown_service | 9/9 | 3/3 |
| volume_discount_incorrectly_applied | 3/3 | 1/1 |
| volume_discount_omitted | 3/3 | 1/1 |
| wrong_unit_basis | 6/6 | 5/5 |

By primary family: development structural 23/23, term_window 2/2, mapping 10/10,
rule 2/2, **pricing 3/5**; check is complete in every family.

## Systematic failure modes

**1. A pricing error alone, on an invoice with nothing else wrong.** Both
remaining development misses are here: one `unit_price_mismatch` and one
`premium_omitted`, each the only error on its invoice and each on a line the
engine could not price to a single outcome, so the invoice is withheld rather
than reported. Every other family is complete on both partitions. This is the
narrowest remaining gap and the only one that costs anything.

**2. A rate that is ambiguous under the contract's own terms.** By far the
largest source of withheld invoices. Hospital 2 alone withholds 773 invoices for
`multiple_supported_rate_outcomes`, because its Service Day begins at 07:00 and
the records carry dates without times, so whether a service falls on a Business
Day cannot be settled and both the uplifted and un-uplifted rate remain
supportable. The audit reports the uncertainty instead of choosing.

**3. A description that names more than one contracted service.** 421 invoices
across Hospitals 2–5 are withheld for `ambiguous_service_mapping`. Each line is
priced under every candidate reading; where the readings agree the verdict is
reported, and where they disagree the invoice is withheld. On development, 143
invoices sit at an error fraction of exactly 0.5 and **142 of them are clean**,
which is why flagging a split reading was measured and rejected.

**4. An amount the record cannot determine.** Where a billed quantity exceeds a
daily cap, the contract fixes what is billable but nothing shows how many units
were actually delivered below the cap. The corrected amount is the capped
quantity, the row is qualified, and the quantity is never guessed. Both
development cap invoices are detected and both keep an inexact amount by design;
they are 2 of the 3 remaining amount misses.

## Assumptions, per hospital

These are readings of ambiguous or silent clauses. Each is applied uniformly and
recorded in the traces.

| Reading | Where | Basis |
|---|---|---|
| Volume discounts are **line-level** everywhere | all five | H1 2.4, H2 2.7 and 3.5, H3 6.1, H4 8.3–8.5, H5 8: the discount applies to *a line item* whose utilisation *prior to that line* exceeds the threshold, and not to the line that crosses it. H2 8.3's "each subsequent Unit" says which units are discounted; 3.5, in the calculation article, fixes how it is applied, and the calculation clause governs. **No line straddles a threshold.** |
| A reused invoice identifier's lines are **attributable** | all five | A line identifier embeds the record number that raised it. Used only where it reconciles: each group's billed total must match one header's exactly. Holds for 29 of 31 reused identifiers; the other 2 fall back to reporting the canonical billed total unchanged. This reconciles from billed totals deliberately — it is accounting, not identification, and two tests assert no mapping moves under price perturbation. |
| The canonical record of a reused identifier is the **latest-dated** one | all five | Every labelled development case agrees, for both the billed and the expected total. |
| An exclusion window **includes** its boundary day | all five | "Not billable within N days" covers a Service Date exactly N days away: the ordinary meaning of "within", making the boundary the last day inside the window. |
| Exclusion direction, where the clause is silent, uses **every reading** | H2, H3, H5 | H1 10.1 and H4 measure in either direction. Where the clause does not fix the direction, only an anchor the readings agree on is reported — for H3 and H5, an anchor on the Service Date itself. |
| **Service Day = the calendar date** | H2 | H2 2.2 defines 07:00–06:59, but the records carry no times, so nothing can be shown to cross the boundary, and 2.2 places a service delivered wholly within a calendar day on that date. Used for caps and for the after-invoice check. |
| The **submission deadline is unobservable**, and blocks nothing | H2 | Article XIII conditions effectiveness on a submission date the data never records. Logged as unresolved; it suppresses no other check. |
| A **cross-invoice repeat is reported even where no clause forbids it** | H2 | H1 11.4, H3 10.3, H4 11.3 and H5 10.3 forbid billing a Service twice for one Patient and Service Date. H2's agreement is silent, but silence is not permission, and on the only labelled hospital every invoice this exact pattern matches is a labelled error. |
| A service date **after** the invoice date is reported | H2 | H2 never defines `invoice_date`, but a service cannot be invoiced before it happens. |
| An **unknown service has no contracted rate** | all five | Its billed amount stands; only the naming is reported. Pricing it against whichever service it resembles would put a fabricated figure on the row. |
| Ambiguity is flagged only on a **strict majority** of readings | all five | Swept 1/6 to 1 on development: every threshold at or below 0.5 costs 147 against 10. |
| Caps and exclusion windows are **unamended** | H3 | Amendment No. 1 clause A1.4.1 states they are unchanged and apply to the substituted rates in the same way. |
| H4's volume utilisation is **patient-scoped where unstated** | H4 | Its clause never says whether utilisation aggregates across patients, so a different patient's history leaves the rate undetermined rather than assumed. |

## What was not attempted

- **The two remaining development misses.** Both need a rate the engine cannot
  reduce to one outcome. Forcing a choice would trade 2 misses for an unknown
  number of false positives, and the measured cost ratio does not support it.
- **Hospital-specific tuning.** No rule keys off an invoice identifier, a record
  count or an input fingerprint; every fix is a general rule.
- **Calibration beyond the stated bar.** Calibration is measured by the
  organisers but is not part of the ranking cost, so fitting stopped once
  confidence was monotone with accuracy and ECE ≤ 0.08.
- **Resolving H2's Service Day.** It would need service times the records do not
  contain. Inferring them would be invention.

## Coverage: an honest limitation

The submission flags **249** invoices across Hospitals 2–5 (H2 63, H3 67, H4 54,
H5 65). The scored set is stated to contain about **285** erroneous invoices, so
on the face of it roughly **36 errors are not being reported** — about 13% of
them, costing about 180 under 5·FN + FP if the shortfall is real.

Two things qualify that figure, in opposite directions. Flag rates are 5.60%,
7.19%, 6.47% and 6.19% against a scored base rate near 7.2%, so the shortfall is
concentrated rather than uniform — Hospital 2 is the outlier, and its 992
withheld invoices are dominated by the Service Day ambiguity above. Against
that, Hospital 1 is the only hospital where accuracy is measurable at all, and
the assumption that the other four share its error mix is untested; the true
shortfall could be larger or smaller. No attempt was made to close the gap by
lowering the evidence bar, because on development every such attempt that was
measured cost more in false positives than it saved in misses.

## Reproduction

Fresh clone of `main`, Python 3.11.15 (outside the declared 3.12 range, which
warns rather than fails):

- `python -m insurance_audit reproduce` — exit **0**
- `python -m insurance_audit verify-submission` — exit **0**
- `python tools/run_checks.py local` — **175 tests, 0 failures**
- `submission.csv` byte-identical to the working copy,
  SHA-256 `c94dc630882dbbfc66b34fbc31dc7d6f2a5a2a52aa1fe6f2c8d8c90a0d53574a`,
  1,977 rows

`tools/generalize.py` exits 0 with a valid schema on all five hospitals under
re-identified invoices, subsampled patients and perturbed descriptions.
`tools/generalize_recall.py` measures a **10.0% relative recall drop with 0 new
false positives** when 30% of Hospital 1's descriptions are perturbed and every
identifier, quantity, date and amount is left untouched.

`tools/validate_submission.py` re-reads the source invoices and checks the CSV
independently of the exporter: column order, flag domain, confidence range,
integer cents, one row per identifier, Hospitals 2–5 only, and billed totals
against the source. All seven pass.
