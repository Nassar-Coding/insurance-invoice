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
| True positives | **42** | **16** |
| False negatives | **0** | **0** |
| False positives | **0** | **0** |
| **Cost (5·FN + FP)** | **0** | **0** |
| Amount exact match on TPs | 0.929 | 0.875 |
| Expected calibration error | 0.0332 | 0.0293 |

The development column is measured on the current code. **The check column is
the Final Gate measurement**, taken before the consistency change below, and has
not been re-measured: the check partition is authorised to be read at the Final
Gate only, and Gate 9 changed no code, so re-reading it would buy nothing and
spend the discipline. Its figures therefore describe the code as it stood at the
Final Gate, not as it stands now.

Nor is the check partition an untouched holdout in the first place. The earlier
implementation opened it after mapping revision 2 and the confidence freeze, so
it is regression evidence. What can be said of the gated rebuild is narrower and
still worth saying: it was read once, at the Final Gate, and nothing was changed
as a result.

Every labelled error in both partitions is reported, with no false positive on
either. Rows emitted: 446 of 622 development, 217 of 291 check. 0 flags on all 184
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
| premium_omitted | 3/3 | — |
| service_date_after_invoice_date | 5/5 | — |
| service_date_out_of_window | 4/4 | 1/1 |
| unit_price_mismatch | 7/7 | 3/3 |
| unknown_service | 9/9 | 3/3 |
| volume_discount_incorrectly_applied | 3/3 | 1/1 |
| volume_discount_omitted | 3/3 | 1/1 |
| wrong_unit_basis | 6/6 | 5/5 |

By primary family: both partitions are complete in every family.

## Settling an ambiguous clause by course of dealing

Several agreements admit more than one reading of a pricing stage. Recording
every supported outcome and withholding the invoice is right when the readings
genuinely disagree about a hospital's billing, and wasteful when they do not.

Each admissible reading is therefore tested against the hospital's **own
supported lines**, and adopted only when the contract text admits it, the stage
covers at least 50 lines, it accounts for at least **98%** of every relevant
line, and every other reading accounts for strictly less. The denominator is
every relevant line, not the subset a reading chooses to price: a reading that
leaves a line ambiguous has not accounted for it either. That distinction
decides the test — scored only on the lines it settles, Hospital 2's unobserved
envelope reaches 99.7% by declining to price 2,912 of 5,094 lines.

This uses the billed **population** to choose between readings of a clause,
which is how a course of dealing settles an ambiguous term. It is not the billed
price being used as evidence of which service a line names: the matcher never
sees a price, and its own tests assert that.

| Hospital | Stage | Reading | Accounted for | Adopted |
|---|---|---|---|---|
| H1 | — | no ambiguous stage declared | — | — |
| **H2** | weekend uplift, daily premium, bundle presence, cap allocation | **calendar Service Day** (clause 2.2) | **5,004 / 5,094 = 98.23%** | **yes** |
| H2 | " | 07:00 envelope (clause 2.2) | 2,175 / 5,094 = 42.70% | no |
| H3 | — | no ambiguous stage declared | — | — |
| H4 | cumulative volume discount | utilisation across all patients | 304 / 322 = 94.41% | no — below 98% |
| H4 | " | same patient only (clause silent) | 82 / 322 = 25.47% | no |
| H5 | facility multiplier | no facility multiplier | 12,542 / 12,900 = 97.22% | no — below 98%, and see the caveat |
| H5 | " | invoice facility projected onto lines | 12,542 / 12,900 = 97.22% | no — below 98%, and see the caveat |

Only Hospital 2's Service Day clears the bar. Hospital 4's better reading falls
short at 94.4%, so its stage stays ambiguous and those invoices stay withheld.
Adopting the calendar Service Day settles four Hospital 2 stages at once and
cuts Hospital 2's withheld invoices from 992 to 451.

**Hospital 5's row does not mean what it appears to mean, and is reported here
rather than quietly left.** Its two readings score identically in *every* cell —
same matched, same differing, same left-ambiguous — because `facility_source`
only sets a qualification label in the pricing engine; the multiplier keyed by
the invoice's facility code is applied under both readings alike. The "no
facility multiplier" reading was therefore never actually exercised, so what the
table shows is not two readings the billing cannot separate but one reading
measured twice. The outcome is unaffected — the stage was not adopted, and those
invoices stay withheld either way — but the *reason* recorded is below-the-bar,
not tied, and the comparison itself is vacuous. Fixing it is the first item
under **What I would do next**.

A line that resolved to one service and priced to one rate under the adopted
readings now carries its own finding, on the same principle Gate 2 applied to
structural evidence: an unrelated unresolved line elsewhere on the invoice does
not make an established rate difference any less established.

## Systematic failure modes

**1. A description that names more than one contracted service.** Now the
largest remaining source of withheld invoices: 925 ambiguous lines across
Hospitals 2-5. A Hospital 2 line reading `admin ophth anaes` is the shape of it:
the agreement contracts both *Intermittent* and *Postoperative* Ophthalmic
Anaesthesia Administration, at different rates, and the abbreviation drops the
one word that would separate them. Each is priced under every candidate reading; where the readings
agree the verdict is reported, where they disagree the invoice is withheld. On
development, 143 invoices sit at an error fraction of exactly 0.5 and **142 of
them are clean**, which is why flagging a split reading was measured and
rejected.

*A tempting shortcut, deliberately not taken.* Every one of those 925 lines has
**exactly one** candidate whose contracted rate equals the billed rate — a
perfect disambiguation signal on its face. It is not used. Picking the service
whose rate matches what was billed is precisely using price as mapping evidence,
and on a line whose rate is *wrong* it would select the service that makes the
error disappear. The one signal that would close this gap is the one that would
silently hide the errors being looked for.

**2. A rate still ambiguous after the consistency test.** Hospital 4's volume
discount stays unresolved because its better reading accounts for 94.4%, below
the 98% bar. Hospital 5's facility multiplier stays unresolved too, but for the
weaker reason set out above: its alternative reading was never exercised, so
nothing has yet been shown about whether its billing chooses. These invoices are
withheld rather than decided on a guess.

**3. An amount the record cannot determine.** Where a billed quantity exceeds a
daily cap, the contract fixes what is billable but nothing shows how many units
were actually delivered below the cap. The corrected amount is the capped
quantity, the row is qualified, and the quantity is never guessed. Both
development cap invoices are detected and both keep an inexact amount by design.

**4. A composite dimension the record does not observe.** 339 invoices across
Hospitals 2-5 are withheld for `composite_dimension_unobserved`, where a rate
depends on a dimension the snapshot does not carry at all. Telemetry Monitoring
is the case in every hospital: it is contracted **per hour per item**, and each
line carries a single quantity, so hours and items cannot be separated and no
expected amount follows from the record. No reading of the
contract resolves this; it is an evidence limit rather than a missing check.

The full withheld picture across the scored hospitals, 1,405 invoices:
ambiguous service mapping 657, composite dimension unobserved 339, rate still
ambiguous 299, unresolved mapping 62, same-day allocation 39, exclusion 9.

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
| **Service Day = the calendar date** | H2 | H2 2.2 defines 07:00–06:59, but the records carry no times, so nothing can be shown to cross the boundary, and 2.2 places a service delivered wholly within a calendar day on that date. **Adopted by the consistency test above at 98.23% against 42.70%**, and applied to the weekend uplift, daily premium, bundle presence, cap allocation and the after-invoice check. |
| The **submission deadline is unobservable**, and blocks nothing | H2 | Article XIII conditions effectiveness on a submission date the data never records. Logged as unresolved; it suppresses no other check. |
| A **cross-invoice repeat is reported even where no clause forbids it** | H2 | H1 11.4, H3 10.3, H4 11.3 and H5 10.3 forbid billing a Service twice for one Patient and Service Date. H2's agreement is silent, but silence is not permission, and on the only labelled hospital every invoice this exact pattern matches is a labelled error. |
| A service date **after** the invoice date is reported | H2 | H2 never defines `invoice_date`, but a service cannot be invoiced before it happens. |
| An **unknown service has no contracted rate** | all five | Its billed amount stands; only the naming is reported. Pricing it against whichever service it resembles would put a fabricated figure on the row. |
| Ambiguity is flagged only on a **strict majority** of readings | all five | Swept 1/6 to 1 on development: every threshold at or below 0.5 costs 147 against 10. |
| Caps and exclusion windows are **unamended** | H3 | Amendment No. 1 clause A1.4.1 states they are unchanged and apply to the substituted rates in the same way. |
| H4's volume utilisation is **patient-scoped where unstated** | H4 | Its clause never says whether utilisation aggregates across patients, so a different patient's history leaves the rate undetermined rather than assumed. |

## What was not attempted

- **Flagging a split reading.** Where the candidate readings of a line disagree
  exactly evenly, the invoice is withheld rather than flagged. On development
  143 invoices sit at that split and 142 of them are clean, so flagging them
  would cost 147 to save 10 at the measured 5:1 ratio.
- **Hospital-specific tuning.** No rule keys off an invoice identifier, a record
  count or an input fingerprint; every fix is a general rule.
- **Calibration beyond the stated bar.** Calibration is measured by the
  organisers but is not part of the ranking cost, so fitting stopped once
  confidence was monotone with accuracy and ECE ≤ 0.08.
- **Observing H2's Service Day directly.** The clause was settled by how the
  parties performed it, not by reading the boundary off the records: the records
  carry no service times, and inferring them would be invention.

## What I would do next

**1. Make Hospital 5's facility comparison real.** `facility_source` currently
only attaches a qualification; the `none` reading needs to actually suppress the
multiplier before the consistency test can say anything about Hospital 5. The
test then either separates the readings or honestly reports a tie, and the fix is
small and local. This is the one known defect in the work, and it is first for
that reason.

**2. Resolve TIE lines without price evidence.** 925 lines, the largest single
block of withheld invoices. The Gate 8 idea transfers from pricing to mapping:
where an abbreviation is ambiguous, ask whether the hospital's *unabbreviated*
lines name only one of the candidates over the term, and adopt that candidate on
the same decisive-margin test. `admin ophth anaes` resolves if the hospital only
ever writes out *Postoperative Ophthalmic Anaesthesia Administration*. It uses
the population of descriptions, never a price, so it does not reintroduce the
shortcut rejected above — and, like the pricing test, it must count a line it
cannot settle against itself.

**3. Hospital 4's patient scope: enumerate more readings, not more lines.** The
bar is a share, so additional lines will not lift 94.4%. Only two readings were
tried — all patients over the term, and same patient only. The clause also admits
aggregation reset per contract year, and aggregation across patients within an
admission. If one of those accounts for ≥98% where neither of the tried readings
does, the stage resolves on the same test with no new machinery.

Each is measurable on development before it ships, against the standing rule that
anything adding a false positive on clean development or on the frozen decoy
proxies is reverted.

## Coverage

The submission flags **281** invoices across Hospitals 2–5 (H2 76, H3 69, H4 61,
H5 75) against a scored set stated to contain about **285** erroneous invoices.
Before this gate it flagged 249; settling Hospital 2's Service Day and reporting
established rate differences on partially resolved invoices added 32.

Flag rates are **6.76%, 7.40%, 7.31% and 7.14%** against a scored base rate near
7.2%, all inside the 4–12% band and now tightly clustered around it.

That closeness is worth stating carefully rather than claiming as a result. The
counts agreeing does not mean the *same* invoices agree: some flags may be false
positives offsetting misses elsewhere, and Hospital 1 remains the only hospital
where any of this can be checked. What can be said is that on Hospital 1 both
partitions are now complete with no false positive, that no decoy proxy is
flagged, and that the count and the rate on all four scored hospitals are
consistent with the stated base rate rather than short of it.

## Reproduction

Fresh clone of `main`, Python 3.11.15 (outside the declared 3.12 range, which
warns rather than fails):

- `python -m insurance_audit reproduce` — exit **0**
- `python -m insurance_audit verify-submission` — exit **0**
- `python tools/run_checks.py local` — **175 tests, 0 failures**
- `submission.csv` byte-identical to the working copy,
  SHA-256 `09a48b06852eda729cb7171044901bf0afd480de6298b2ee0a283bfe9ea4ca0f`,
  2,537 rows

`tools/generalize.py` exits 0 with a valid schema on all five hospitals under
re-identified invoices, subsampled patients and perturbed descriptions.
`tools/generalize_recall.py` measures a **9.5% relative recall drop with 0 new
false positives** when 30% of Hospital 1's descriptions are perturbed and every
identifier, quantity, date and amount is left untouched.

`tools/validate_submission.py` re-reads the source invoices and checks the CSV
independently of the exporter: column order, flag domain, confidence range,
integer cents, one row per identifier, Hospitals 2–5 only, and billed totals
against the source. All seven pass.
