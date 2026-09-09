# Retained instruction and acquisition history

These are Work-session instructions applied by the authoring assistant, not invented transcripts of a separately called LLM endpoint. The user-instruction file v1 explicitly labels itself a summary. No hidden reasoning transcript or unobserved model version is claimed.

| File | Actual role |
|---|---|
| `implementation_user_v1.md` | Retained summary of the user's governing implementation instruction. |
| `implementation_user_v2.md` | Subsequent user override removing all effort restrictions. |
| `extract_v1.md` | Finite schema, exact numeric transcription, source evidence and missing-fact instructions applied during acquisition. |
| `review_v1.md` | Author source review, clause coverage and acceptance boundary. |
| `map_v1.md` | Initial service identity review, before the development failure. |
| `map_v2.md` | Revised open-catalog / essential-qualifier policy following H1 development error D007, then applied to the remaining hospitals. |
| `audit_correction_user_v1.md` | Retained summary of the later user-authorized correction and regression-verification stage following the supplied independent audit. |

`reports/h1_acquisition_manifest.json` and `reports/H2_acquisition_manifest.json` through `H5_acquisition_manifest.json` identify source and prompt hashes for historical acquisition. Each hospital has retained raw contract/mapping output, accepted JSON and a source-review record. H1 mapping v1 and schema1 packages are archived; the v2 change report lists the withdrawn groups. `reports/provenance_check.json` checks current review-to-raw bindings; historical acquisition hashes are not misrepresented as current after revision.

The assistant also wrote the interpreter, tests, reporting/replay scripts and documentation and executed implementation verification. Source-derived tests were reasoned from the contracts; they are separate from H1 label comparison. No external API, embeddings, alternate model pipeline or independent reviewer was invoked during implementation. Fresh acquisition is not part of deterministic replay.

After initial implementation, the user supplied an independently produced audit. It is retained unchanged in `governance/audits/independent_implementation_1/`; the author did not generate that audit or its verdict. Later correction work and tests are author verification, with independent closure re-audit still pending.
