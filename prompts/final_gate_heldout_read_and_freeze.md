# Final Gate — held-out read, validation, reproduction, freeze

Status: **verbatim**, as received through the `/goal` mechanism.

---

Complete the plan's Final Gate as specified below. Met only when all items are done AND shown here: check-partition scorer output, submission validator result, generalization output, fresh-clone reproduction exit code and SHA-256, report updated, final commit hash. OR stop with a blocker report if an item can't be completed after 3 attempts.

STATE: gate7 = d0565c0 on main. Dev 40/2/0, cost 10, amount exact 0.925, ECE 0.032. Submission SHA c94dc630…574a, 1,977 rows. H2–H5 flags: 63/67/54/65 = 249.

F.1 Read the check partition ONCE with tools/cost_scorer.py: report TP/FN/FP, cost, amount exact-match, per-category results. If check cost ≤ 30: change nothing. If > 30: identify the failing rule class, fix it as a GENERAL rule (never per-invoice), rerun dev (must stay 0 FP, cost not worse) and check, and state in the report that check is now regression evidence, not held-out.
F.2 Run tools/validate_submission.py: exact columns (invoice_id, flagged, error_category, expected_total_cents, billed_total_cents, confidence); flagged 0/1; confidence in [0,1]; integer cents; one row per invoice_id; only H2–H5 IDs; billed_total_cents matches source.
F.3 Rerun tools/generalize.py on dev (no tuning): report relative recall drop and new FP.
F.4 Fresh clone from GitHub main; run the README reproduction on the Python already available (no installs); report exit code and SHA-256 — must match the submission.
F.5 Diagnostic only, no changes: withheld-reason histogram for each of H2–H5 at the current state.
F.6 Update EVALUATION_REPORT.md and README: per-category dev and check results; 3–4 systematic failure modes with examples; per-hospital assumptions (incl. H2 line-level discount per §3.5, reused-ID attribution via line identifiers, inclusive exclusion boundary, H2 Service Day = calendar date, strict-majority ambiguity threshold); what was not attempted; honest note that H2–H5 flags (249) are below the ~285 expected errors.
F.7 Push to main; report final hash and submission SHA-256.

RULES: no Python installs (stop if setup >10 min); no invoice IDs, record counts or input hashes in runtime logic; lean context. Stop after the Final Gate.
