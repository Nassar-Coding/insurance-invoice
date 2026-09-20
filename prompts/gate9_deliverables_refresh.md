# Gate 9 — graded deliverables refresh

Status: **verbatim**, as received through the `/goal` mechanism. Documentation
only; this gate changed no code and no prediction.

---

Complete Gate 9 (graded deliverables refresh) below. Met only when shown here: the new decision log with its word count (one page, ≤ ~600 words), the prompt files added, the consistency check result, proof submission.csv is unchanged (SHA-256 09a48b06852eda729cb7171044901bf0afd480de6298b2ee0a283bfe9ea4ca0f), and the final commit hash. No code or prediction changes.

STATE: gate8 = cb9d679 on main. Dev 42/0/0, check 16/0/0, 281 H2–H5 flags. reports/decision_log.md is stale (last updated before Gate 2): it still says all H2 opinions are withheld and that H2's 07:00 Service Day is not established. prompts/ stops at Gate 1.

1. Rewrite reports/decision_log.md as a one-page log (regenerate decision_log.pdf if the repo has a tool for it): assumptions, ambiguities found and not resolved, and the decision for each. Cover: H2 Service Day = calendar date, adopted by the population-consistency test (98.23% vs 42.70%, §2.2); H4 patient scope and H5 facility left ambiguous (below 98% / tied); H2 invoice_date undefined but after-invoice check kept (H1 evidence 12/12); line-level volume discounts in all hospitals (H2 §3.5); inclusive exclusion boundary; H3 exclusion direction via every-reading; strict-majority threshold for ambiguous lines (142/143 clean on dev); reused-ID attribution via line identifiers + total reconciliation (29/31); billed price NOT used for mapping, incl. the declined TIE shortcut (925 lines) and why; confidence = confidence in the whole row incl. amount; unknown services keep billed amount.
2. Add prompts/gate2 … gate8 files with the prompts you received, verbatim where available; mark reconstructed text as reconstructed. Update prompts/README.md to list the sequence and what changed between iterations, including the plan document that drove them.
3. Update docs/ai_usage.md: tools used (Codex for Gates 0–1, Claude Code for Gates 2–8, research assistance for diagnosis and planning), the plan → gated prompt → review workflow, and that work continued in the organiser-granted revisit window after the original submission.
4. EVALUATION_REPORT.md and README: confirm current numbers everywhere (dev 42/0/0, check 16/0/0, 281 flags, amount exact 0.929); keep the 3–4 systematic failure modes with an example each; keep the honest caveat that 281 ≈ 285 in count does not prove the same invoices, and that H1 is the only labelled hospital; add a short "what I would do next" section (e.g., TIE-line resolution without price evidence, H4 patient scope, H5 facility).
5. Consistency check: grep README, EVALUATION_REPORT, decision log and docs for contradictions or stale numbers (e.g., "withheld", "not established", 249, cost 10); fix text only.
6. Push to main; report hash. Tags blocked — I tag gate9.

RULES: no code changes; lean context. Stop after Gate 9.
