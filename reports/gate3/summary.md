# Gate 3 — mapping

## Exit criteria (development partition)

| Criterion | Target | Result |
|---|---|---|
| Cumulative detection | ≥ 33 of 42 | **PASS — 38 of 42** |
| False positives on the 580 clean development invoices | 0 | **PASS — 0** |
| Decoy-proxy flags | 0 | **PASS — 0 of 184** |
| Flag rates H2–H5, none below 3% | none < 3% | **PASS — 4.98 / 7.08 / 6.35 / 6.00 %** |
| Generalization recall drop | reported (plan target ≤ 10%) | **reported — 13.2%, above target** |

Development: **38 TP, 4 FN, 0 FP, cost 20**, from 26/16/0 and cost 80 at Gate 2.
Per-category: `unknown_service` 9/9, `wrong_unit_basis` 5/6, `cross_invoice_duplicate` 2/2.
Amount exact match 0.763 on true positives. Submission rows 512 → 1,872.

The four remaining development misses are `daily_cap_exceeded`,
`exclusion_window_violation` (Gate 4) and two pricing-only invoices (Gate 5).

## What changed

**Step 0 — Hospital 2 cross-invoice repeats.** Gate 2 withheld H2's seven matches
because H2's agreement carries no express prohibition while the other four do.
Silence is not permission: no H2 clause allows a repeat, and on the only labelled
hospital all four invoices this exact pattern matches are labelled errors. At
4/4 labelled precision the posterior is far above the 1/6 flag threshold. All
seven are reported and **no exemption was taken**.

**Steps 1–3 — the matcher.** A billed description is scored against contracted
service *names* only. No price, rate, quantity or total reaches the module: one
test walks its syntax tree, another triples every unit price and line total
across Hospital 1 and asserts not one mapping moves.

`NO_MATCH` is decided on how much of the **billed** wording a contracted name
explains, not on overall similarity. A legitimate abbreviation drops words from
the contracted name but never adds one. This separates "Consultation Adv", which
is Advanced Neurological Consultation abbreviated, from "Adv Renal
Consultation", which the contract has no service for — the two score identically
on similarity. The floor was swept on development: every value from 0.85 to 1.00
gives the same result, and 0.90 is taken from the middle of that interval.

**Step 4 — unit basis.** Checked on every identified line rather than only on
lines the pricing engine could reach. A tie or a weak reading identifies no
service and is not checked against one.

**Step 5 — reopened keys.** Each Hospital 1 key was reopened one at a time and
kept only if development gained no false positive and the decoy proxies gained no
flag, applied cumulatively so an interaction between two keys could not slip
through independent trials. 41 of 63 kept; 12 left withdrawn because the matcher
calls them NO_MATCH, 10 because it calls them TIE. The same validated rule was
then applied to H2 (106 keys), H3 (64), H4 (85) and H5 (56).

**Step 6 — every reading.** A line whose wording names more than one service is
audited under each candidate. Every reading faulty is a confident error on the
categories they share; no reading faulty is a clean line; anything else is
ambiguous and carries the error fraction for Gate 6. Where every reading finds
the same fault but they disagree on the corrected amount, the fault is reported
and the line keeps what was billed.

## Step 7 — generalization under description drift

`tools/generalize_recall.py` perturbs 30% of Hospital 1's line descriptions with
the Gate 0 harness's own drift (case, whitespace, abbreviation swaps, token
reordering, a one-character typo, service code kept on half) and leaves every
identifier, quantity, date and amount untouched, so the difference is
attributable to wording alone.

| | recall | new false positives |
|---|---|---|
| First measurement | 0.905 → 0.952 | **478** |
| After the three guards | 0.905 → 0.786 | **0** |

The first measurement was a real failure, not a harness artifact: a typo makes a
token unexplained, which is indistinguishable from a genuinely absent service, so
ordinary drift produced hundreds of false `unknown_service` flags. Three guards
fixed it, and each is justified on its own terms rather than by the harness:

1. **A word the contract never uses anywhere is drift, not a claim.** "Renal" is
   a specialty this contract sells in other combinations, so billing it in a
   combination the contract lacks is a claim about a service. A corrupted string
   the contract never uses is a mistyping. This also recovered the ninth
   `unknown_service` invoice, taking that category from 8/9 to 9/9.
2. **A reviewed wording is recognised however its words are ordered or
   abbreviated.** The reviewers accepted a description, not a spelling of it.
3. **A description one character from one the contract fully explains is read as
   a mistyping.** The harness's typo turned "Ent" (otolaryngologic) into "Ext"
   (extended) — one character, landing on another real contract abbreviation.

Cross-invoice duplicate matching now keys on the canonical wording for the same
reason, so reordering or abbreviating cannot hide a repeat.

**The remaining 13.2% drop is above the plan's 10% target.** Five invoices are
lost, and four of them (`unit_price_mismatch`, `bundle_not_applied`,
`wrong_unit_basis`, `premium_omitted`) are detections that inherently require
knowing which service was delivered; a typo in the description genuinely removes
that ability. Under 5·FN + FP the current position is much the better one: five
lost detections cost 25 against the 478 false positives the earlier behaviour
produced. The trade was taken deliberately and is recorded here rather than
tuned away.

## Withheld reasons, Hospital 1 development

| Reason | Count |
|---|---:|
| `ambiguous_service_mapping` | 147 |
| `multiple_supported_rate_outcomes` | 30 |
| `unresolved_service_mapping` | 9 |
| `duplicate_service_day_allocation` | 2 |
| `unresolved_exclusion` | 1 |

`unresolved_service_mapping` fell from 392 to 9: most of what was simply
unresolved is now either reported, priced under every reading, or named
`ambiguous_service_mapping` with a recorded error fraction.

139 tests pass. The check partition was not read.
