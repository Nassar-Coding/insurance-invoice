# Insurance invoice auditing — write-up

LLM-assisted contract-to-schema interpretation, deterministic pricing, explicit abstention. Repository `Nassar-Coding/insurance-invoice`, commit `7ac7f74`.

## Approach and sequencing

All five contracts were represented as finite, source-referenced JSON (H1 108 services, H2 76, H3 120, H4 98, H5 84). One deterministic interpreter replays them: it selects the service-date version, assembles retrospective usage, then applies bundles, multipliers, premiums, uplifts, the deepest qualifying discount and caps, in that order, in exact staged half-up cents. Replay makes no model call.

The order followed what each layer depends on. **Structural checks first** — duplicate identifiers, malformed dates, line arithmetic, a service date after its invoice date, cross-invoice repeats — because none needs to know which service a line names. **Then a per-line decision layer**, deciding separately for each line whether its evidence supports a finding, a clean verdict, or neither. **Then mapping**, a four-state matcher (match / no-match / weak / tie) that never sees a price. **Then contract rules**, then **pricing and amounts**. Each stage was measured on Hospital 1 before the next began, and any change adding a false positive on clean development invoices or the frozen decoy set was reverted.

That order is a correction, not a plan I got right first time. The first submission was precise but silent: 340 opinions out of 3,942 and six flags, none for Hospital 2. It withheld invoices whose *own evidence was the error*: a malformed service date is a finding, but the first version read it as a reason the invoice could not be priced and said nothing. Hospital 2 was silent end to end because Article XIII conditions an invoice's effectiveness on a submission date the data never records — one unresolvable fact suppressed every other check on 1,125 invoices. The revision fixed abstention before adding a single new check — an unresolved fact now blocks only what depends on it, and evidence that is itself the error is always reported. That alone took development cost from 190 to 80.

## How I measured

Hospital 1 is the only labelled hospital and so the only place accuracy is measurable. Its 913 identifiers were split into 622 development and 291 check by frozen patient-connected groups. Every iteration was tuned on development alone; the check partition was read **once**, at the final gate, and nothing changed as a result. The objective was the ranking metric, `cost = 5·FN + 1·FP`, which puts the flag threshold at P(error) > 1/6 and makes a miss five times costlier than a false alarm.

Three measurements guard against fitting the labels, all from `tools/`: **decoy proxies**, 184 clean Hospital 1 invoices carrying the surface patterns an error would have, frozen and re-checked every iteration; **generalization**, re-identified invoices with 30% of descriptions perturbed and quantities, dates and amounts untouched; and **calibration**, since stated confidence is scored.

| | Development | Check |
|---|---|---|
| True positives / false negatives / false positives | **42 / 0 / 0** | **16 / 0 / 0** |
| Cost (5·FN + FP) | **0** | **0** |
| Amount exact match on true positives | 0.929 | 0.875 |
| Expected calibration error | 0.0332 | 0.0293 |

`submission.csv` carries 2,537 rows across Hospitals 2–5 with **281 flags** against a scored set stated to hold about **285** errors, at flag rates of 6.76%, 7.40%, 7.31% and 7.14% against a base rate near 7.2%. No decoy proxy is flagged. Perturbation costs a 9.5% relative recall drop with no new false positive. 175 tests pass and a fresh clone reproduces `submission.csv` byte for byte.

The limits matter as much as the figures. The evidence is Hospital 1 only. **The counts agreeing does not mean the same invoices agree** — some of the 281 may be false positives offsetting misses elsewhere, and nothing here can tell. The check column is regression evidence rather than an untouched holdout: the earlier implementation had already opened that partition, and the column was measured at the final gate, before the last change.

## Where I was uncertain, and why

**H2's Service Day** (clause 2.2) defines 07:00–06:59, but the records carry no times, and the same clause places a service delivered wholly within a calendar day on that date. Each admissible reading was tested against H2's own billing: the calendar reading accounts for 5,004 of 5,094 relevant lines (**98.23%**), the 07:00 envelope for 2,175 (**42.70%**), so the calendar reading was adopted. The denominator is every relevant line, not the subset a reading chooses to price — scored the other way, the envelope "wins" at 99.7% by declining to price 2,912 lines.

**H4's patient scope** — whether volume utilisation aggregates across patients — is never stated. Its better reading reaches 94.4%, below the 98% bar, so the stage stays ambiguous and those invoices stay withheld.

**H5's facility multiplier is a defect I found while writing the evaluation report, and am reporting rather than quietly leaving.** Both readings score identically in every cell because `facility_source` only sets a qualification label in the pricing engine; the alternative was never actually exercised. Predictions are unaffected — the stage was not adopted either way — but the comparison is vacuous, and the reason recorded is below-the-bar, not tied.

**925 ambiguous lines** name more than one contracted service. Every one has exactly **one** candidate whose contracted rate equals the billed rate — a perfect disambiguation signal on its face, deliberately refused. Choosing the service whose rate matches what was billed is using price as identity evidence, and on a line whose rate is *wrong* it selects the service that makes the error vanish: the one signal that would close this gap is the one that would hide what I am looking for. These lines are priced under every candidate and reported only on a strict majority; on development, every lower threshold flags 143 invoices of which 142 are clean.

**Some amounts the record cannot determine.** Where a billed quantity exceeds a daily cap, the contract fixes what is billable but nothing shows how many units were delivered; the corrected amount is the capped quantity and the row is penalised in confidence rather than guessed. Telemetry Monitoring is contracted per hour per item and each line carries one quantity, so no expected amount follows. Of 1,405 invoices withheld: ambiguous mapping 657, composite dimension 339, rate still ambiguous 299, and 110 across three smaller reasons. Confidence is confidence in the **whole emitted row**, flag and corrected amount together, not in the flag alone.

## What I would do differently with another week

**1. Make H5's facility comparison real.** The alternative reading must actually suppress the multiplier before the test can say anything. Small, local, and first because it is the one known defect.

**2. Resolve the 925 tie lines without price evidence.** Move the consistency idea from pricing to mapping: where an abbreviation is ambiguous, ask whether the hospital's *unabbreviated* lines name only one candidate over the term, and adopt on the same decisive-margin test — `admin ophth anaes` resolves if the hospital only ever writes out *Postoperative Ophthalmic Anaesthesia Administration*. That uses the population of descriptions, never a price.

**3. H4's patient scope: enumerate more readings, not more lines.** The bar is a share, so extra lines cannot lift 94.4%. Only two readings were tried; the clause also admits aggregation reset per contract year, or within an admission.

Three process lessons matter more. **Trace withheld reasons from day one**: I could not see that one Article XIII fact was silencing 1,125 invoices until a withheld-reason histogram existed, and building it was the highest-value hour of the exercise. **Treat error evidence as a flag, never as a reason to withhold** — precision that comes from silence is not precision. **Decouple structural checks from mapping earlier**, since duplicate identifiers and malformed dates never needed to know what a line meant.

## Time and AI use

The original submission was completed by the original deadline; everything after it was done in the revisit window the organisers granted, as gated iterations each with a numeric exit criterion. AI assistance was used throughout — OpenAI and Anthropic models, for research and diagnosis, planning, contract interpretation, code and tests — and is disclosed in `docs/ai_usage.md`. Every prompt used to drive the implementation, one per gate included, is in `prompts/` verbatim, with what changed between iterations in `prompts/README.md`.
