# Decision register

This register records source interpretations and technical revisions. Decision identifiers are retained for cross-references; earlier interpretations below must be read with their explicit subsequent revisions. Further decisions D008–D018 are in [implementation_changes.md](implementation_changes.md).

## D002 — Source snapshot

- Decision: use the supplied CSV and Markdown snapshot at commit `6fee1da60b74512156637a22be15d996a36627e1`, with a finite schema and fixed interpreter.
- Evidence: `docs/source_manifest.json` records the source paths and checksums.

## D003 — Acquisition and replay

- Decision: LLM-assisted interpretation with retained candidate/reviewed records; standard-library-only Python replay. No programmatic model/API execution is implied.
- Evidence: `docs/architecture.md`, `prompts/`, `.python-version`, `requirements.txt`.

## D004 — Actual invalid dates and input test correction

- Expected: the first implementation test incorrectly assumed all 11,415 raw H1 lines would become accepted typed lines.
- Observed: 11,409 accepted H1 lines + six malformed dates, including `2025-06-31` and `not-a-date`; 35 date-malformed lines across all hospitals. No rows were lost. Reused IDs have different patients/totals rather than identical headers.
- Evidence: `reports/tests_inputs_initial_failure.json`, `reports/input_quality.json`.
- Decision: fix the test to reconcile accepted + quarantined counts; preserve raw invalid dates and their possible contextual influence. Omit conflicting-ID invoice opinions because one output total cannot be established. Do not guess patient ownership from line-ID formatting or silently normalize impossible dates.
- Required invariant: accepted and quarantined records together account for every raw occurrence.

## D006 — H1 source interpretation and mapping acceptance

- Evidence: complete H1 §§1–11, all 108 rate rows and the separately printed adjustment tables; 488 raw description proposals reviewed as 108 service groups plus 24 unresolved descriptions. Candidate/review artifact hashes are retained.
- Decision: accept exact rate/unit and rule transcription. Interpret exclusion windows for the same patient, consistent with surrounding patient-specific delivery restrictions; §10.1 explicitly makes H1 windows bidirectional. Withhold equality at exactly N days because “within” is not explicit about the boundary. This is a recorded interpretation, not a quoted patient-scope sentence absent from §10.
- Duplicate service/patient/day billing or conflicting invoice ownership has no generally unique corrected invoice allocation; withhold affected opinions. Do not choose which invoice to pay or drop from a line-ID pattern. A single unambiguous capped line may be priced at the maximum billable quantity; no proportional split allocation is invented.
- Billed quantity is the multiplication input under §3.3; a wrong unit label is a separate error, not permission to invent a conversion. Invalid or disallowed dates are retained as uncertainty in corrected facts and dependent context.
- Exact billed quantities remain in contract-wide utilisation as §2.4/§7 define billed units. Unknown identities/dates carry possible contributions rather than zero history. Only outcome-relevant uncertainty blocks an opinion.
- Initial interpretation, superseded by D007: descriptions with elided qualifiers were accepted when the reviewed supplied catalog had one semantic candidate, with an elided evidence grade. Eleven incompatible descriptions and thirteen two-candidate descriptions remain unresolved; `Std Endo Endoscopic Procedure` is not forced using its billed amount.
- No label values were used. Accepted data remains finite and replay uses no model. Source review does not certify universal completeness.

## D007 — Open-catalog mapping, after development error analysis
The initial rule accepted a unique catalog match despite missing essential name concepts. H1 development invoice INV-H1-000236 exposed a 43,650-cent over-correction from mapping generic outpatient radiotherapy to the Metabolic service. The contract does not supply the missing specialty. Mapping revision 2 withdraws all 39 H1 keys with analogous missing essential concepts, not just this invoice/alias. Fourteen keys retain only a generic final noun elision and remain a separate evidence tier. No billed rate/unit selects identity. Original mappings, raw records, review and first metrics are retained. See reports/H1_mapping_change_v2.json. All future hospitals use the same policy.
