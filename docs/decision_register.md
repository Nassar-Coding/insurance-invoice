# Decision register

Entries are appended. A changed interpretation records expected/observed/evidence/decision/why and affected artifacts, rather than silently replacing history.

## D001 — Time entry

- Plan expected: measured prior effort or explicit conservative allowance, before coding.
- Observed: no reliable effort log; file timestamps include inactive time and cannot establish effort.
- Decision: reserve 300 prior minutes, maximum 180 additional minutes, 75-minute finishing reserve; disable optional hospital expansion initially.
- Evidence: `docs/budget.json`, `docs/work_log.md`.
- Qualification: this is an explicit assumption, not verified total-effort compliance. Revise immediately if actual prior effort is established.

## D002 — Governing source and stage

- Plan expected: pinned source and closed review, constrained records/fixed interpreter.
- Observed: source commit `6fee1da60b74512156637a22be15d996a36627e1`; all five reconciled sheets match the prior artifact exactly; new Final Closure Check closes C01–C10 and retains a nonblocking E03 verification qualification.
- Decision: retain that snapshot/architecture and implement. Defer independent challenge and publishing as explicitly requested.
- Evidence: `docs/source_manifest.json`, `governance/Insurance_Auditing_Implementation_Ready.xlsx`.

## D003 — Acquisition and replay

- Decision: Work-session model interpretation with retained candidate/reviewed records; standard-library-only Python replay. No programmatic model/API execution is implied.
- Evidence: `docs/architecture.md`, `prompts/`, `.python-version`, `requirements.txt`.

## D004 — Actual invalid dates and input test correction

- Expected: the first implementation test incorrectly assumed all 11,415 raw H1 lines would become accepted typed lines. The governing plan itself already required quarantine.
- Observed: 11,409 accepted H1 lines + six malformed dates, including `2025-06-31` and `not-a-date`; 35 date-malformed lines across all hospitals. No rows were lost. Reused IDs have different patients/totals rather than identical headers.
- Evidence: `reports/tests_inputs_initial_failure.json`, `reports/input_quality.json`.
- Decision: fix the test to reconcile accepted + quarantined counts; preserve raw invalid dates and their possible contextual influence. Omit conflicting-ID invoice opinions because one output total cannot be established. Do not guess patient ownership from line-ID formatting or silently normalize impossible dates.
- Plan change: none; this applies C03 and the existing identity/uncertainty gates.

## D005 — User override OVR-001

- Plan expected: time-controlled scope, optional hospital activation and stop conditions.
- New governing instruction: the user explicitly removed every time constraint and requested full implementation/verification of all applicable work.
- Decision: deactivate those controls, examine all remaining hospitals, and continue until implementation gates are addressed. Preserve all uncertainty/source/reproduction requirements. Independent challenging and publishing remain separate stages.
- Evidence: `governance/overrides.md`, `prompts/implementation_user_v2.md`.
- Effect: prior time-based scope decisions are superseded; no completed evidence is erased and no claim of original-budget compliance is made.

## D006 — H1 source interpretation and mapping acceptance

- Evidence: complete H1 §§1–11, all 108 rate rows and the separately printed adjustment tables; 488 raw description proposals reviewed as 108 service groups plus 24 unresolved descriptions. Candidate/review artifact hashes are retained.
- Decision: accept exact rate/unit and rule transcription. Interpret exclusion windows for the same patient, consistent with surrounding patient-specific delivery restrictions; §10.1 explicitly makes H1 windows bidirectional. Withhold equality at exactly N days because “within” is not explicit about the boundary. This is a recorded interpretation, not a quoted patient-scope sentence absent from §10.
- Duplicate service/patient/day billing or conflicting invoice ownership has no generally unique corrected invoice allocation; withhold affected opinions. Do not choose which invoice to pay or drop from a line-ID pattern. A single unambiguous capped line may be priced at the maximum billable quantity; no proportional split allocation is invented.
- Billed quantity is the multiplication input under §3.3; a wrong unit label is a separate error, not permission to invent a conversion. Invalid or disallowed dates are retained as uncertainty in corrected facts and dependent context.
- Exact billed quantities remain in contract-wide utilisation as §2.4/§7 define billed units. Unknown identities/dates carry possible contributions rather than zero history. Only outcome-relevant uncertainty blocks an opinion.
- Descriptions with elided qualifiers are accepted only when the reviewed supplied catalog has one semantic candidate, with an elided evidence grade. Eleven incompatible descriptions and thirteen two-candidate descriptions remain unresolved; `Std Endo Endoscopic Procedure` is not forced using its billed amount.
- No label values were used. Accepted data remains finite and replay uses no model. Source review does not certify universal completeness.

## D007 — Open-catalog mapping, after development error analysis
The initial rule accepted a unique catalog match despite missing essential name concepts. H1 development invoice INV-H1-000236 exposed a 43,650-cent over-correction from mapping generic outpatient radiotherapy to the Metabolic service. The contract does not supply the missing specialty. Mapping revision 2 withdraws all 39 H1 keys with analogous missing essential concepts, not just this invoice/alias. Fourteen keys retain only a generic final noun elision and remain a separate evidence tier. No billed rate/unit selects identity. Original mappings, raw records, review and first metrics are retained. See reports/H1_mapping_change_v2.json. All future hospitals use the same policy.


## P001 — Independent closure intake and publishing preparation (2026-09-08)

- Expected: preserve the exact corrected implementation accepted by independent closure; organize final documentation without changing technical results.
- Observed: the checkpoint SHA-256 is `c3b49e516b335d9a2cd424279df3b983e66d6f23946a87fda6bbace61ade891e`; attached report and submission equal the checkpoint. The independent closure report returns PASS with both findings closed and no material regressions. Its companion archive contains auditor evidence, not the implementation; the matching checkpoint was recovered and verified separately.
- Decision: freeze all original source, tests, author tools, contract/mapping artifacts, prompts, policy and runtime pins. Update only current documentation/stage presentation, repository metadata and packaging. Retain the original seven Git commits compactly; omit non-authoritative temporary write remnants and move historical run bulk out of the main checkout.
- Evidence: `evidence/publishing/baseline.json`, `file_disposition.json`, `history_verification.json`, `final_reproduction/`, and the unchanged independent closure report.
- Qualification: dated generated reports/prompts preserve their original stage wording because those bytes belong to the audited release identity. Current status is supplied separately. BT11 repository publication, access and sending are not claimed complete.


## P002 — Historical recovery discrepancy (2026-09-08)

- Expected: the Git bundle alone would reproduce all tracked checkpoint bytes apart from the documented recovery note.
- Observed: recovery found one additional difference in the old diagnostic H2 attempt `0f10a3b2ecb245b7bda5230c379067bb`; the checkpoint version parses and matches its status hash, while the committed Git copy is truncated and fails JSON parsing. An initial interpretation reversed these two locations; separate parse/hash checks corrected that mistake before packaging. The current audited H2 attempt is a different, unchanged record. The initial all-file recovery assertion failed and was investigated.
- Decision: preserve the exact checkpoint bytes in `evidence/history/checkpoint_differences.zip`, preserve original Git history separately, and record the discrepancy. Do not repair historical outputs or treat them as current evidence. No source, prediction logic, accepted artifact, policy or current audited result changes.
- Evidence: `evidence/publishing/history_verification.json` and the per-file disposition register.
