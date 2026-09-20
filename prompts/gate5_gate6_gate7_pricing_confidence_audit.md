# Gates 5, 6 and 7 — pricing and amounts, confidence, decoy and distribution audit

Status: **verbatim**, as received through the `/goal` mechanism. An earlier draft
of this instruction exceeded the 4,000-character goal limit and was shortened by
the author before being accepted; the accepted text is the one below.

---

Complete Gates 5, 6, 7 of the plan below, in order. Met only when ALL three gates' exits are met AND shown here (printed tools/cost_scorer.py dev output, amount exact-match, decoy-proxy count, H2–H5 flag rates, commit hash per gate, final submission SHA-256 and rows/flags per hospital). OR stop with a blocker report if any gate's exit can't be met after 3 attempts — never start the next gate if the current one fails.

STATE: gate4 = 1dd10ca on main. Dev 40 TP / 2 FN / 0 FP, cost 10. Misses: INV-H1-000151 (unit_price_mismatch), INV-H1-000619 (premium_omitted). Flag rates H2 5.60%, H3 7.19%, H4 6.47%, H5 6.00%.

GATE 5 (pricing and amounts)
1. Pricing: bundle substitution → facility multiplier → plan-tier multiplier → premium/uplift (incl. weekend/non-business-day) → cumulative volume discount; half-up rounding to integer cents after each step (verified in all 5 contracts; H5 §3.4: round even at multiplier 1.0). Unpriceable line raises, never contributes 0. H4 §8.2 "except 8.3" changes nothing. H2 Business Day follows the Service Day's commencement (§2.4).
2. Cumulative volume discounts across invoices using retained history; reused IDs not double-counted. Granularity differs: H4 (§8.3–8.5) line-level — applies only when prior cumulative utilisation already exceeds the threshold, not on the crossing line; ordered by service date then line id; deeper tier once its threshold is exceeded. H2 (§8.3) unit-level ("each subsequent Unit") — a line can straddle the threshold; counted across all patients over the whole term. H1/H3/H5: confirm the model from each clause before implementing; log it.
3. Pricing detections: flag when recomputed total differs from billed on fully resolved lines; use the specific category (e.g., premium_omitted). No FP on clean dev or decoy proxies.
4. Daily-cap amounts: billed quantity over cap → correct to capped quantity; unobservable sub-cap quantity → flag, capped amount, confidence penalty. One documented rule.
5. Hand-computed unit tests: ≥2 per rule family from actual clauses, incl. a threshold-straddling line (H2) and a threshold-crossing line (H4).
Exit (dev): ≥40/42 (aim 42), 0 FP on clean dev, 0 decoy flags, amount exact-match ≥0.90 on dev TPs, H2–H5 flag rates.

GATE 6 (ambiguity threshold and confidence) — keep short
1. For invoices whose only findings are ambiguous lines, sweep the error-fraction threshold 1/6 → 1; pick the value minimising dev 5·FN+FP. Too few dev cases → default majority-of-readings, log it.
2. Confidence tiers fitted to dev accuracy (structural; MATCH fully priced; NO_MATCH; ambiguous; partial amount; clean). Cap H2–H5 confidence below fitted H1 values. Stop once monotone and ECE ≤0.08.
Exit: threshold and tiers documented; ECE ≤0.08; dev cost not worse than Gate 5.

GATE 7 (decoy and distribution audit)
1. Rerun decoy proxies: 0 flags.
2. For each of H2–H5, sample 15 flagged and 15 withheld invoices; inspect traces. Thin-evidence flag → tighten that check; withheld invoice with an obvious error → fix the abstention leak; after any fix rerun dev (0 FP, cost not worse).
3. Flag rates within 4–12% for all four hospitals, or deviation explained.
Exit: 0 decoy flags; audit findings and fixes listed; flag rates in band; regenerate submission.csv, report SHA-256 and rows/flags per hospital.

SAVING: push directly to main after each step; report the hash. Tags are blocked — I tag gate5/6/7 from your hashes.
RULES: dev partition only; never read the check partition; no Python installs (stop if setup >10 min); revert any change adding FP on clean dev or decoy proxies; lean context. No invoice IDs, record counts or input hashes in runtime logic — every fix must be a general rule for unseen invoices. Stop after Gate 7 — do not start the Final Gate.
