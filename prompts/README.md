# Technical prompts and versions

These files retain the instructions used for contract acquisition, source review and service mapping. They are historical prompt records, not runtime inputs to a model call. Deterministic replay uses the accepted JSON artifacts and does not repeat acquisition.

| Prompt | Role and version history |
|---|---|
| [extract_v1.md](extract_v1.md) | Extract finite contract facts, controlling definitions and source references; retain raw candidates and explicit uncertainty. |
| [review_v1.md](review_v1.md) | Check candidate values and predicates against source clauses. Acquisition review is distinct from independent implementation testing. |
| [map_v1.md](map_v1.md) | Review descriptions and candidate meanings without using billed amounts or labels as identity evidence. |
| [map_v2.md](map_v2.md) | Revision after H1 development exposed unsupported essential-qualifier elision; withdraw all analogous keys and apply the stricter standard to targets. |

The four original prompt files are unchanged, including their historical introductory wording. Acquisition manifests in `reports/` record prompt/source hashes. Raw contract and mapping candidates, source reviews, accepted bundles and earlier schema/mapping versions preserve the relationship from instruction to accepted artifact. The H1 revision is documented in `reports/H1_mapping_change_v2.json` and D007 in `docs/decision_register.md`.

No external LLM API or embedding model is needed for reproduction. Fresh LLM extraction is not guaranteed to regenerate identical records. See [AI assistance](../docs/ai_usage.md) for the scope of assistance and [technical changes](../docs/implementation_changes.md) for observed failures and corrections.
