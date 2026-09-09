# Implementation evidence and departures from provisional expectations

The following technical revisions preserve the original expectations, observed evidence and resulting decisions.

| ID | Initial expectation | Observed source/execution evidence | Resolution and reason |
|---|---|---|---|
| D007 | A unique catalog candidate with elided qualifiers could be accepted. | H1 development INV-H1-000236: generic outpatient radiotherapy was incorrectly assigned the Metabolic rate; expected amount differed by 43,650 cents. README does not promise a closed catalog. | Require independently supported essential concepts; withdraw all 39 analogous H1 keys. Preserve v1 and v2, original error, and the reduced coverage. No invoice-specific amount patch. |
| D008 | Initial normalizer handled observed H1/H3 suffixes. | Source descriptions also contain terminal /SA-, /CW-, /PH- identifiers. | Normalizer v2 handles exactly five observed suffix families; original text retained; no semantic qualifier stripped. H1 prediction values must remain unchanged. |
| D009 | Shared invoice checks might fit each source. | H2 does not contain the H1/H3/H4/H5 service-date-after-invoice and same-service/day duplicate prohibitions. | Schema/semantics v2 makes these requirements explicit. H2 does not inherit absent rules. All prior accepted packages are migrated with archived original bytes and regression checks. |
| D010 | H3 exclusion operator and amendment could reuse the shared engine. | H3 §9 lacks explicit temporal direction; A1.1 explicitly uses service date despite the document header. A1.4.2 protects invoices settled before effectiveness. | Reprice seven services and add two from 2025-01-01. Directional ambiguity propagates for nonzero distances; same-day anchors are definite under both readings. Assume settlement cannot precede invoice/service for otherwise valid invoices; no settlement fact is invented. |
| D011 | H4 instance and cumulative thresholds were candidates for shared usage logic. | §1.4 explicitly defines instance=unit; §8 does not explicitly state patient aggregation scope. | Unit equivalence accepted. Bound patient-specific through all-patient prior usage and emit only rate-invariant outcomes. Compound quantity dimension remains unknown. |
| D012 | H5 needs facility and tier multiplication. | §1.2/Table2 say line facility; supplied CSV only has invoice facility, also required by §10.1. | Adopt invoice facility as the line attribute in the supplied relational representation. This is an explicit interpretation, not an observed line field; outcome-relevant rows are qualified and capped at .65 confidence. Invariant facilities do not incur that cap. All table cells retained. |
| D013 | A supportable H2 complete-invoice subset might exist after source review. | H2 XIII.1–5 makes invoice effectiveness conditional on submission within 60 days of discharge, with written exceptions. Actual submission, episode/leave and waiver facts are absent. II.2 defines a 07:00 Service Day plus a wholly-single-calendar-day qualification; neither timestamps nor durations are supplied. | All 76 rates and every price rule are represented and tested for diagnostic replay, but all H2 submission opinions are withheld. Invoice date is not silently renamed submission date. Day-dependent rules use conservative quantity/presence envelopes or abstain. This is a source-evidence limit, not a compute or implementation blocker. H2 has no accepted final submission scope. |

The H1 check partition was first examined only after mapping revision 2 and
confidence freeze. Further common-code checks are regression evaluations after
check exposure, never a new held-out estimate. Target data have no labels.

## Final implementation details (D014)

The implemented CLI uses plural `--hospitals` and immutable attempt IDs; [cli_contract.md](cli_contract.md) documents the actual commands and paths.

H1 source-review counts in the historical `mapping_qualifications` sentence describe v1; the same review explicitly records v2 withdrawal. `reports/current_candidate_closure.json` and `reports/provenance_check.json` bind final accepted counts/bytes. Initial viability and acquisition records are retained as history, not silently substituted as current results.

Source/normalization validation now rejects empty rule references and a stored mapping key inconsistent with its retained raw aliases. All five accepted bundles still validate. The previously implemented H5 .65 qualification cap is now an explicit confidence-policy field, not a code fallback; H1 confidence scores are unchanged. Final regression compares all six H1 opinion fields and every metric with the frozen baseline, and rechecks each target's source examples and full shuffled snapshot.

The final target execution includes H2 for diagnostic and omission evidence. It is inactive for submission: eligibility uncertainty is enforced before an opinion can be emitted, and no H2 row is released. Diagnostic processing does not establish a supported payable opinion.

## D015 - Full-snapshot permutation exposed trace ordering

Full results must be repeatable under input permutation. The first full H1 permutation comparison failed: all six opinion fields were identical, but `source_headers` within conflicting-ID abstention traces followed the order of input records. `reports/regression_initial_failure.json` retains the exact differing paths and source rows. Canonical source filename/row ordering now stabilizes that trace list. The underlying dispositions, mappings, cents and confidence are unchanged. A two-header reversal test covers the defect; full-hospital permutation and H1 baseline regression are rerun on the corrected code.

## D016 - AUD-01: quarantined header ownership must survive

**Expected:** malformed relevant records remain uncertain dependencies. **Observed:** the independent audit's unchanged three-header/two-line fixture was executed before correction. Making only I2's P2 invoice date impossible changed I1 from an unresolved exclusion to an emitted zero-cent opinion with confidence .65. The result validator accepted it. `reports/corrections/audit_1/before/auditor_aud01_reproduction.txt` and the original runtime hashes retain this failure. The snapshot has no quarantined headers, so this does not establish a wrong existing submission row.

**Decision: Accept.** Keep recoverable ownership evidence from all valid/quarantined headers separately from typed auditable headers. Finite conflicting patients remain possible; missing patient identity is unbounded. Preserve source-row provenance. Emit explicit omissions for recoverable IDs with no valid header, and reject complete opinions when a quarantined header cannot be linked to any invoice. Same-patient evidence and all-patient utilization are not arbitrarily weakened by unrelated invalid fields. No date, allocation, rate, patient or confidence evidence is invented. Fourteen new test methods jointly cover both findings, including the exact counterexample through confidence assignment and result validation. See the after/ fixture outputs and correction_verification.json for executed closure evidence and downstream comparison.

## D017 - AUD-02: controlling bundle clauses belong in calculation traces

**Expected:** the trace supports the rule actually applied. **Observed:** all 352 emitted bundle-priced lines (151 invoices; targets 252 lines/103 invoices) referenced standalone service rows instead of controlling bundle clauses. H4 invoice INV-H4-000583 uses 1,250 and 111,675 cents from section 7 line 216, while old traces cited standalone 1,425 and 126,900-cent rows. The accepted bundle record and numerical calculations were correct.

**Decision: Accept.** Each bundle stage now records the dated base version, bundle-record index/source, service and partner, substituted cents, presence state and exact context entry establishing applicability. Selected source references cite controlling clauses; absent partners retain the dated standalone source; uncertain alternatives retain both. Pricing arithmetic, extracted contracts, mappings and confidence policy are unchanged. Verify every emitted base/bundle stage against accepted records and recomputed raw context, including all 352 substitutions and the H4 example. Controlled citation/context/cents corruption must fail that verification. Before/after traces and full-result comparisons are retained under reports/corrections/audit_1.

## D018 - Correction verification and H2 evidence clarification

Both reproduced defects were corrected and verified with 75 tests, complete reruns, before/after comparisons, source/context checks and clean reproduction. Independent verification confirmed both findings closed without material regression. The original reports and execution records remain available under `governance/audits/` and `reports/corrections/audit_1/`.

All 1,132 H2 headers contain admission/discharge dates. Missing facts are actual submission dates, detailed episode/leave evidence and possible written exceptions. This clarification does not change the H2 omission policy.

## Historical result recovery

One older diagnostic H2 output differs between the original Git history and the recovered archive: the Git copy is truncated; the archive copy parses and matches that attempt's recorded checksum. An initial interpretation reversed these locations and was corrected after separate parse/hash checks. Both versions remain identified in [the history index](../evidence/history/README.md). Neither is a current result; no historical output was repaired or used to replace current evidence.
