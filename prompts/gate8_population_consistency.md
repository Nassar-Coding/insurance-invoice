# Gate 8 — population-consistency resolution of rate ambiguity

Status: **verbatim**, as received through the `/goal` mechanism.

The EVIDENCE block names specific Hospital 2 invoices. They appear here only as a
historical record of the instruction, and were used only to check the
implementation against an independent analysis. No invoice identifier from this
block reaches runtime logic; the consistency test recomputes itself from
whatever data is present.

---

Complete Gate 8 below. Met only when shown here: per-hospital consistency-test tables, readings adopted (with clause refs) or rejected, dev and check scorer outputs, decoy-proxy count, H2–H5 flag rates and new flags per hospital, validator result, generalize.py exit code, fresh-clone SHA-256, final commit hash. OR stop with a blocker report after 3 failed attempts.

STATE: final = 90cd065 on main. Dev 40/2/0 (cost 10), check 16/0/0. H2–H5 flags 63/67/54/65 = 249 vs 285 scored errors, so ≥36 errors are unflagged. Most H2–H5 withholds are multiple_supported_rate_outcomes (H2 773, H3 18, H4 177, H5 78) and unobserved_service_day_cap_allocation (H2 41).

EVIDENCE (independent analysis of the gate7 trace + raw H2 data): H2's rate ambiguity comes from the 07:00 Service Day envelope, driving weekend_uplift, bundle and daily_premium readings. Reading A — Service Day = calendar service_date (H2 §2.2: a service wholly within one calendar day is on the Service Day bearing that date; already used at Gate 4 for caps) — is confirmed by H2's own billing: daily_premium lines 1,352/1,361 consistent (99.3%), weekend lines 1,248/1,255 (99.4%), bundle pairs consistent except 8 withheld lines billed base while the partner is billed the same date. Withheld H2 invoices deviating under A: INV-H2-000238, 000325, 000852, 001109 (bundle), 000610, 000743, 000900 (premium), plus 1 weekend line. Use these only to check your implementation — never in runtime logic.

GATE 8 (population-consistency resolution of rate ambiguity)
1. General rule: when a hospital's contract admits more than one reading for a rate stage (weekend, daily premium, bundle, cap allocation, discount envelope), compute for each reading the share of that hospital's supported lines for that stage whose billed rate it explains. Adopt a reading only if (a) it is consistent with the contract text and (b) it explains ≥98% of those lines and every other reading explains less. Lines deviating under the adopted reading become findings with the specific category. Otherwise leave the stage ambiguous.
2. Apply to H2 first (expected: reading A adopted for weekend, premium, bundle, cap allocation), then run the same test on H3, H4, H5 and on H1 dev. Print one table per hospital: stage, readings, % explained, adopted or not.
3. Guards (revert per hospital/stage if any fails): dev stays 40/2/0 cost ≤10; check stays 16/0/0 (regression evidence); decoy proxies 0; each hospital's flag rate ≤12%. No invoice IDs, record counts or input hashes in runtime logic.
4. Diagnostic only, no changes: for ambiguous_service_mapping / TIE lines in H2–H5, count how many have exactly one candidate whose contracted rate (under adopted readings) equals the billed rate, per hospital.
5. Regenerate submission; run tools/validate_submission.py; run tools/generalize.py (exit 0, report drop and new FP); fresh clone from GitHub main, reproduce, exit 0, matching SHA-256; add the readings and consistency tables to EVALUATION_REPORT.md.
6. Push to main after each step; report hashes. Tags blocked — I tag gate8.

RULES: no Python installs (stop if setup >10 min); lean context. Stop after Gate 8.
