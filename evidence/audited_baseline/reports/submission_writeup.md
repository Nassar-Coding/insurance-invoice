# Insurance auditing - implementation write-up
LLM contract-to-schema with deterministic pricing | Local implementation candidate

## What was implemented
All five supplied contract sources were inspected and represented in finite, source-referenced JSON: H1 108 services, H2 76, H3 120, H4 98 and H5 84. The Work-session assistant interpreted definitions and conditions, proposed mappings, wrote code and tests, and performed author source review. Deterministic transcription aided extraction. Versioned instructions, raw candidates, revisions and accepted artifacts are retained. No programmatic model/API, local GPU or external compute was used.

One fixed Python interpreter selects service-date versions, assembles retrospective usage and executes bundles, facility/tier multipliers, premiums, weekend uplifts, deepest qualifying discounts and caps with exact staged half-up cents. It checks supported unit, arithmetic, contract-reference and eligibility faults. It emits a complete invoice opinion only when all necessary lines and context support the amount. Other invoices remain explicit omissions with source and reason traces.

## How results were measured
H1 has 913 unique invoice IDs, partitioned into 622 development and 291 check IDs using frozen patient-connected groups. Shared legitimate global usage remains in context across groups. Labels were used for development and evaluation, never as prediction inputs or answer-key mappings. The check was first opened after mapping revision 2 and confidence freeze. Current check results are regression evidence after that exposure; full H1 is development-inclusive.

Development emits 169/622 opinions with 169 correct flags and exact amounts. Check emits 81/291 with 81 joint successes. Full H1 emits 250/913 (27.38% coverage), with 250 joint successes, five true error flags and zero false flags. Error recall across all 58 erroneous IDs is 8.62% and F1 is 0.1587. The other 53 errors are withheld. High conditional accuracy therefore accompanies low recall; it is not a claim of broad accuracy.

The separate evaluation report gives every original label's support/detection and per-family precision, recall and F1 through an explicit crosswalk. Abstentions are missed positives for population recall and excluded from conditional accuracy; they are never correct negatives. Joint success means flag plus exact expected cents, with billed totals and complete traces separately verified. Free-text diagnostic correctness is measured separately. Undefined denominators are not filled with perfect scores.

## Target output
The validated six-column submission has 340 opinions: H3 148/932 (five flagged), H4 64/835 (one flagged) and H5 128/1,050 (none flagged). H2 has zero/1,125. Every source occurrence and unique opinion identity is accounted for. All source services were attempted; remaining omissions reflect missing evidence and unsupported corrections. There are no H2-H5 labels, so target accuracy is unknown.

<!-- PAGEBREAK -->

# Uncertainty, reproducibility and next work

## Where uncertainty matters
An initial mapping accepted generic outpatient radiotherapy as a metabolic service. Development invoice INV-H1-000236 exposed a 43,650-cent over-correction. The correction withdrew all 39 analogous missing-essential-qualifier keys, rather than patching that invoice or learning a billed price as identity. Coverage fell substantially. Current systemic omissions arise from insufficient description evidence, conflicting identities or damaged dates, and uncertain cross-invoice context or allocation. The report gives actual examples; these omissions are distinguished from observed emitted errors.

H3 service-date amendment precedence is explicit; settlement protection uses a recorded valid-invoice chronology interpretation. H3/H5 exclusion direction and exactly-N-day boundaries remain uncertain. H4 instance-to-unit equivalence is explicit, but patient scope of cumulative usage is bounded. H5 line facility is unavailable, so invoice facility is an explicit contextual projection, never a claimed observed line field. All 128 emitted H5 rows have an outcome-relevant projection and .65 confidence.

H2 was fully inspected, including definitions and all 76 rate clauses. Article XIII conditions invoice effectiveness on actual submission within 60 days of episode discharge, with possible written exceptions. Admission/discharge dates are supplied; actual submission, detailed episode/leave and possible written-exception evidence are absent. The CSV invoice date cannot prove submission. Its 07:00 Service Day also lacks timestamps or qualifying duration evidence. Pricing is available diagnostically, but no complete payable H2 opinion is claimed.

## Confidence and verification
Development supported correct-row tiers use conservative .95/.90 scores; sparse error tiers use .65 judgment. Novel reviewed target rows use .80/.70; relevant interpretation or invariant-uncertainty qualifications cap .65. These are explicitly limited scores, not proven target probability calibration. No number substitutes for missing necessary facts.

The 75 tests cover schema rejection, dates/amendments, exact arithmetic, thresholds, cross-invoice rules, uncertainty, metrics and failed/stale export. The first independent audit required two corrections: quarantined-header patient ownership now remains uncertain context, and applied bundles cite their controlling clause and partner evidence. Author regressions preserve the failing fixtures and compare all hospitals before/after; no submission, metric or confidence value changed. All 352 emitted bundle substitutions were checked against source/context. Full permutation, label isolation and clean replay were rerun. Independent closure re-audit remains pending.

## Reproduction and further work
Clone the project, select Python 3.12.13, and run the README's reproduce command. It recomputes the source CSVs through retained accepted schemas/mappings, then exports and evaluates. Core execution/tests use only the standard library, without model keys or Work state. Outputs can be removed before replay; historical attempts are not required. PDF rendering alone has separately pinned optional dependencies. Fresh LLM acquisition is a distinct process and is not promised to regenerate identical schemas.

For further development, first obtain authoritative service aliases and the absent H2 submission/episode facts; resolve H3/H5 direction and H4 scope with the contract owner. Then expand source-derived fixtures and validate the changed mappings/rules on new labelled examples, including withheld invoices. Evaluate confidence on independent target evidence and measure the unresolved review workload before scaling. More compute alone does not resolve missing source facts. External publishing, assessor access, final presentation and actual email delivery remain separate, unperformed stages.
