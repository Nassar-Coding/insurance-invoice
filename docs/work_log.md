# Work log

**Current policy: OVR-001 supersedes all time limits below.** There is no active time limit, finishing reserve, time-based scope restriction or elapsed-time stop rule. Earlier entries are preserved as history. See `governance/overrides.md`.

2026-09-06: implementation authorized; governing closure PASS.

Prior effort is not measured. The explicit prior allowance is **300 minutes**; maximum additional effort is **180 minutes** against the 480-minute cap. This is a planning assumption, not an assertion that previous work took 300 minutes. Use 21:49 UTC as a conservatively early start for this turn and stop by 00:49 UTC on 7 September. Protect 75 minutes for final evidence/reproduction/delivery work. Optional hospital onboarding is disabled for this checkpoint. Source/workbook inspection began before any auditor coding.

First checkpoint objective: verified canonical inputs, source/mapping coverage, deterministic H1 execution and development evidence if viable. No independent challenge or publishing is performed.

Runtime measurements and subsequent decisions are appended as work proceeds.

## H1 interpreter execution
30 source/logic checks and then 31 combined tests passed. Initial CLI integration failed because the three-value bundle return was unpacked into two variables; the failed attempt status is retained. Fixed the caller and executed all 913 unique H1 identities: 579 opinions and 334 abstentions; 11,415 raw line occurrences retained in context, six quarantined dates. A controlled staged failure did not change the success pointer. No H1 check labels inspected.

## First frozen H1 evaluation
Mapping v2 + frozen confidence: development 169/622 opinions, 169 exact flag-and-cent successes; check 81/291 opinions, 81 successes; full H1 250/913, five true flags, zero false flags, 53 labelled errors withheld. Full population error recall is 5/58 (8.62%), not 100%. Initial mapping failure and lost-coverage consequences retained. Check now exposed; future shared-code changes are regression checks and cannot be represented as a fresh holdout.

## Completed implementation verification - 2026-09-07
All five source packages executed. Final submission: 340 rows (H3 148, H4 64, H5 128; H2 none). H2 full payable scope withheld for absent submission/episode/waiver facts; diagnostics retained. Final 61 tests pass in the working project and clean clone. Full five-hospital permutations agree after D015 trace-order correction; H1 six fields/metrics match the frozen baseline. Label/network guards pass. PDF page/visual checks pass. Clean clone commit 55f5b5f49af8bd0549b7fb11188570b18fbb5e03 recomputed matching CSV, metrics, workload, report and manifest. BT01-BT10 implementation tasks closed; independent challenge and BT11 publishing/delivery unperformed. No elapsed-effort scope condition is active. See reports/implementation_report.md and the status/evidence ledgers.


## Independent audit corrections and regression closure

The user supplied the first independent implementation audit (PASS WITH CORRECTIONS). Both findings were reproduced on the original code before modification. AUD-01 now retains quarantined-header patient evidence in cross-invoice context, including missing/ambiguous ownership and explicit malformed-header dispositions. AUD-02 now records controlling bundle sources and partner applicability. Original failing probe output, source examples, old/new inventories and old reports remain under reports/corrections/audit_1; the original audit is unchanged in governance/audits.

The original 61 tests plus 14 regressions pass (75 total). Corrected guarded replay produced new H1/target attempts a1ee1b9f209f4f41913349e165fe8a26 and 4d449a6fc6fc49399da2cd567bdb1b51. All opinion fields, confidence values, omission reason categories and calculation amounts are unchanged on the supplied snapshot. All 352 emitted bundle substitutions and 5,605 base/bundle stages pass source/context checks. The 340-row CSV, metrics and workload are byte-identical. Trace metadata changes are quantified separately.

Clean clone e5efadf4af7fe58ca1b75d904aac9c426093109d removed all run/output caches, recomputed the submission/evaluation and passed 75 tests. It reproduced the full hospital trace/input-quality hashes, stable reports and release manifest. Both author corrections and all applicable implementation gates are closed with current evidence. The existing document drafts were factually refreshed and retain their one-/two-page limits. Independent closure re-audit, publication/access and delivery remain pending. No target accuracy, new holdout or formal proof of arbitrary malformed-input behavior is claimed.


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
