# Gates 3 and 4 — mapping, then contract rules

Status: **verbatim**, as received through the `/goal` mechanism, which held the
instruction as a stop condition until every exit criterion was shown.

---

Complete Gate 3 and then Gate 4 of the plan, as specified below, in order. Met only when ALL gates' exits are met AND shown here (printed tools/cost_scorer.py dev output, decoy-proxy count, H2–H5 flag rates, commit hash per gate). OR stop with a blocker report if any gate's exit can't be met after 3 attempts — never start the next gate if the current one fails.

STATE: gate2 = 1af65e4 on main. Dev 40 TP / 2 FN / 0 FP, cost 10. Remaining 16 dev misses are mapping/rule/pricing only.

GATE 3 (mapping)
Step 0 — H2 cross-invoice duplicates: flag the 7 H2 pattern matches as cross_invoice_duplicate. Evidence: the same exact pattern (same patient, service date, normalised service, quantity, different invoices) matches 4 invoices in H1 — all 4 labelled real cross_invoice_duplicate errors — and exactly 4 in each of H3/H4/H5. Under cost 5·FN + FP, flag whenever P(error) > 1/6. Exempt a specific match only for a concrete H2 contract clause or data fact making it legitimate; report any exemption.
1. Four-state matcher: MATCH / NO_MATCH / WEAK / TIE. Start MIN_SCORE 0.60, MIN_MARGIN 0.08; set NO_MATCH_FLOOR by sweep on dev.
2. NO_MATCH → flag unknown_service, only after confirming no match in any contract document for that hospital incl. amendments/appendices. Target dev unknown_service ≥8/9.
3. Remove all price features from matching; unit test that price perturbation changes no mapping.
4. Unit-basis check on MATCH lines only. Target dev wrong_unit_basis ≥5/6.
5. Reopen the 39 withdrawn mapping keys one at a time; keep only keys adding 0 new FP and not reintroducing the 43,650-cent over-correction.
6. TIE/WEAK lines: price under every candidate reading; all readings error → flag; mixed → mark ambiguous with the error fraction (threshold decided at Gate 6).
7. Rerun tools/generalize.py on dev with description perturbation; report relative recall drop (target ≤10%).
Gate 3 exit (dev): cumulative ≥33/42, 0 FP on clean dev, 0 decoy-proxy flags, H2–H5 flag rates (none <3%), generalization drop reported. Report the Gate 3 final hash.

GATE 4 (contract rules) — only if Gate 3 exit passed
1. Extract daily caps and exclusion windows per hospital into reviewed JSON with clause citations and effective dates (amendments included); schema-validate.
2. Daily cap: sum quantity per patient, service, day ACROSS invoices using retained history; flag when over cap. H2: "day" = Service Day (07:00–06:59), aggregate across all lines (H2 §3.4). Target dev daily_cap_exceeded 2/2.
3. Exclusion window: flag services inside an excluded window per each clause's anchor; record direction/boundary per hospital; H3 exclusion direction is ambiguous → use every-reading method. Target dev exclusion_window_violation ≥3/3.
Gate 4 exit (dev): cumulative ≥35/42, 0 FP on clean dev, 0 decoy-proxy flags, H2–H5 flag rates. Report the Gate 4 final hash.

SAVING: push directly to main after each step and report the hash. Tags are blocked — I tag gate3 and gate4 myself from the hashes you report.
RULES: dev partition only; never read the check partition; no Python installs (stop if setup >10 min); revert any change that adds FP on clean dev or decoy proxies; lean context. No invoice IDs, record counts or input hashes in runtime logic — every fix must be a general rule that would apply to unseen invoices. Stop after Gate 4.
