# Technical prompts and versions

These files retain the instructions the work was done under. They are historical
prompt records, not runtime inputs to a model call: deterministic replay uses the
accepted JSON artifacts and does not repeat acquisition. Nothing in this folder is
read by `src/insurance_audit`, and no invoice identifier appearing in a prompt
reaches any runtime rule.

## Acquisition

| Prompt | Role and version history |
|---|---|
| [extract_v1.md](extract_v1.md) | Extract finite contract facts, controlling definitions and source references; retain raw candidates and explicit uncertainty. |
| [review_v1.md](review_v1.md) | Check candidate values and predicates against source clauses. Acquisition review is distinct from independent implementation testing. |
| [map_v1.md](map_v1.md) | Review descriptions and candidate meanings without using billed amounts or labels as identity evidence. |
| [map_v2.md](map_v2.md) | Revision after H1 development exposed unsupported essential-qualifier elision; withdraw all analogous keys and apply the stricter standard to targets. |

The four original acquisition prompts are unchanged, including their historical
introductory wording. Acquisition manifests in `reports/` record prompt/source
hashes. Raw contract and mapping candidates, source reviews, accepted bundles and
earlier schema/mapping versions preserve the relationship from instruction to
accepted artifact. The H1 revision is documented in
`reports/acquisition/H1_mapping_change_v2.json` and D007 in `docs/decision_register.md`.

## The gate sequence

Gates 2 onward were driven by [docs/Revised_Plan_Rank29_to_Top3.md](../docs/Revised_Plan_Rank29_to_Top3.md),
written after the first submission placed 29th at a cost of 1395. Each gate was
issued as a single instruction with explicit exit criteria and could not be left
until those criteria were shown; the next gate was not started until the previous
one passed. Gates 3 onward were delivered through a `/goal` mechanism that held
the instruction as a stop condition. Every file below is verbatim as received
except where its own header says otherwise.

| Prompt | What it asked for | What changed as a result |
|---|---|---|
| [gate0_implementation_v1.md](gate0_implementation_v1.md) | Portability, prediction-input independence, label-free generalization; no new detection logic. | Invariants and the trace tool; detection untouched. |
| [gate1_measurement_rebuild.md](gate1_measurement_rebuild.md) | Restore the scorer, reason histograms and the miss cross-tab after an unpublished checkpoint was lost. | Measurement only. Baseline registered at development cost **190**. |
| [gate2_structural_and_decision_layer.md](gate2_structural_and_decision_layer.md) | Stop withholding an invoice on evidence that *is* the error; decouple structural and term-window checks from mapping; line-level decision layer; decoy proxies. | The largest single drop: **190 → 80**. H2 went from 6 flags to hundreds; the frozen decoy-proxy set entered the loop and has read 0 flags since. |
| [gate3_gate4_mapping_and_contract_rules.md](gate3_gate4_mapping_and_contract_rules.md) | A four-state matcher (match / no-match / weak / tie), `unknown_service` on a confident no-match, no price features in mapping, unit-basis check, reviewed cap and exclusion clauses with citations. | **80 → 20 → 10.** A first attempt cost 478 false positives under description drift and was rebuilt around coverage of *billed* tokens with three generalization guards. |
| [gate5_gate6_gate7_pricing_confidence_audit.md](gate5_gate6_gate7_pricing_confidence_audit.md) | Pricing order and rounding, cumulative discounts, daily-cap amount rule, hand-computed clause tests; then a confidence-tier sweep; then a decoy and distribution audit. | Cost held at 10 while amount exact-match rose to 0.925 and ECE fell to ≤ 0.04. Confidence became a tier on the whole emitted row. |
| [final_gate_heldout_read_and_freeze.md](final_gate_heldout_read_and_freeze.md) | Read the check partition **once**, add an independent submission validator, re-measure generalization, reproduce from a fresh clone, then freeze. | Exposed a latent crash in `validate_result` that would have failed the Generalization run — the same failure mode that cost the original submission. Submission bytes unchanged. |
| [gate8_population_consistency.md](gate8_population_consistency.md) | Settle a rate ambiguity by how the parties performed the contract: test each admissible reading against the hospital's own billed lines and adopt only on a decisive margin. | **10 → 0** on development (42/0/0). H2's calendar Service Day adopted at 98.23% against 42.70%; H4 and H5 stayed ambiguous. Flags across H2–H5 rose 249 → 281. |
| [gate9_deliverables_refresh.md](gate9_deliverables_refresh.md) | Rewrite the decision log to one page, publish these prompts, refresh the graded documents. | Documentation only. No code and no prediction changed; `submission.csv` is byte-identical. |

## Reproduction

No external LLM API or embedding model is needed for reproduction. Fresh LLM
extraction is not guaranteed to regenerate identical records. See
[AI assistance](../docs/ai_usage.md) for the scope of assistance,
[technical changes](../docs/implementation_changes.md) for observed failures and
corrections, and [the decision log](../reports/decision_log.md) for every contract
ambiguity and what was decided.
