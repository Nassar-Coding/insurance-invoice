# Gate 2 — structural checks, term-window checks, line-level decision layer

Status: **verbatim**, as received. Delivered with `Revised_Plan_Rank29_to_Top3.md`,
`Corrections_and_Reprioritized_Plan.md`, `h1_primary_family_coding.csv` and the
leaderboard PDF attached, together with the STATE and KEY FINDING blocks below.

---

STATE
- First get the latest main (Gate 1 is tagged gate1 = 6e1b9dc).
- Gate 0 DONE (tag gate0 = 7a020c2). Gate 1 DONE (tag gate1 = 6e1b9dc). Read reports/gate1/summary.md for the full baseline.
- Baseline: dev 4 TP / 38 FN / 0 FP (cost 190). Submission 340 rows, 6 flags. Flag rates H2 0%, H3 0.54%, H4 0.12%, H5 0%. Scored cost is 5·FN + FP over H2–H5 (285 errors, 158 decoys); H1 is not scored.
- Tools exist: tools/cost_scorer.py, --trace decision trace, withheld-reason histograms, evaluation/baseline_cost.json.

KEY FINDING FROM GATE 1 (drives this gate)
Of the 38 missed dev errors, 14 are withheld for a reason that IS the error: service_date_after_invoice (3), service_date_outside_term (2), conflicting_reused_invoice_id (4), quarantined_required_source_record (4), plus 1 term-window case. Another 8 structural errors are withheld only because of unrelated unresolved_service_mapping. H2's 1,110 invoices are all withheld for unobserved_submission_deadline_and_waiver.

GATE 2 — follow the plan's Gate 2, in this order:
1. Convert error-evidence withholds into flags: service_date_after_invoice → flag service_date_after_invoice_date; service_date_outside_term → flag service_date_out_of_window; conflicting_reused_invoice_id → flag duplicate_invoice_id; quarantined_required_source_record → inspect the quarantine cause and flag when it is a structural error (malformed date, arithmetic, etc.); keep withholding only for genuinely non-error quarantine causes. Use the plan's category precedence (out_of_window > duplicate_invoice_id > service_date_after_invoice_date).
2. Decouple structural and term-window checks from mapping: they run and emit flags regardless of unresolved_service_mapping or rate ambiguity.
3. H2: unobserved_submission_deadline_and_waiver must never block a structural finding. Read H2's deadline/waiver clauses; if the deadline can't be evaluated from the data, log it as unresolved and let every other check proceed normally.
4. possible_duplicate_service_day: flag cross_invoice_duplicate only when structural evidence is clear (same patient, same Service Day, same normalised service, same quantity, on different invoices, and no contract clause permitting repeats). Otherwise keep withholding. This is decoy-sensitive — be strict.
5. Line-level decision layer and amount policy (plan 2.4–2.5): flag on any confident finding; partial correction for resolved lines; never expected == billed on a flagged row unless the error doesn't affect the amount.
6. Decoy proxies (plan 2.6) mined from the 580 clean dev invoices; every check must produce 0 flags on them.

EXIT (dev partition only)
- ≥24 of 25 structural + term-window primary dev invoices flagged
- 0 FP on 580 clean dev invoices; 0 decoy-proxy flags
- H2–H5 flag rates reported; H2 > 0%
- report dev cost and the updated withheld-reason histogram

SAVING WORK (mandatory)
- After each numbered step, commit and push immediately and tell me the commit hash and branch. Push to main if permitted; if your environment only allows a separate branch, push there and tell me its name — I'll merge it.
- Never hold unpushed work.
- At the end of Gate 2, push tag gate2 if permitted; otherwise tell me the final hash and I'll tag it.

RULES
- Stop after Gate 2; wait for "continue".
- Never install or build Python versions. If any setup exceeds 10 minutes, stop and tell me.
- No clean-checkout or generalization re-runs until the Final Gate.
- Tune on dev only; never read the check partition.
- Any change that adds a false positive on clean dev or decoy proxies is reverted.
- Keep reports short; keep context use lean (no large file/log dumps).
