# Implementation result

The selected **LLM contract-to-schema with deterministic pricing** solution is implemented, executed and verified for its documented supported scope. No independent auditing/challenging or publishing stage has been started.

The governing workbook is preserved unchanged in `governance/`. The explicit user override removed all effort constraints; omissions below result from source evidence or unsupported corrections, not elapsed effort.

## Actual implementation

- All five hospital contracts were inspected, including H3's three-document hierarchy and H2's full prose agreement. All 486 catalog services and 2,330 observed normalized description keys are represented. Raw acquisition, author review, accepted versions, prompts and corrections are retained.
- A finite schema and one fixed Python interpreter handle date/version precedence, units, exact staged cents, bundles, facility/tier multipliers, premiums, weekends, strict-prior discounts, supported caps and non-price checks. There is no model call in replay.
- Historical context retains omitted and quarantined records as known or possible contributions. Unresolved service identity, eligibility, allocation or necessary context prevents a complete opinion. Process failures are separate from invoice omissions.
- The submission exporter reconciles every emitted amount to all its source lines and the current confidence policy, independently parses the exact six-column CSV, and promotes a validated local manifest. Stale inputs, changed bytes and interrupted promotion are rejected.
- Code, tests, dependencies, schemas, mappings, prompts, decisions, evaluation, omissions and trace evidence live in this one repository-ready project.

## Executed results

| Hospital | Unique invoice IDs | Complete opinions | Flagged opinions | Withheld |
|---|---:|---:|---:|---:|
| H1 | 913 | 250 | 5 | 663 |
| H2 | 1125 | 0 | 0 | 1125 |
| H3 | 932 | 148 | 5 | 784 |
| H4 | 835 | 64 | 1 | 771 |
| H5 | 1050 | 128 | 0 | 922 |

The target `submission.csv` contains **340 rows**, including 6 predicted erroneous and 334 predicted correct invoices. There are no H1 rows. Target correctness is unmeasured because H2-H5 have no labels.

Full H1 has **250 exact flag-and-amount matches out of 250 emitted opinions**, but only **27.38% coverage** and **8.62% error recall** (5 of 58 labelled errors detected; 53 withheld). Development has 169/622 opinions; the check has 81/291. High accuracy on the emitted subset is not broad coverage or proven target accuracy. `reports/evaluation_report.md` supplies category metrics, denominators, confidence support and observed failure mechanisms.

H2 has no accepted complete payable scope: Articles II/XIII require actual submission, episode/leave and possible waiver facts absent from the CSVs. Invoice date is not silently treated as submission. All 76 rates and applicable rule families are available for diagnostic execution; all 1,125 H2 full opinions are withheld. H4 patient scope is bounded. H5 invoice-facility projection is a recorded assumption, with all 128 emitted H5 opinions capped at .65 confidence.

All **66,097 raw CSV occurrences** reconcile: 4,886 header records and 61,211 line records, including 35 quarantined malformed-date lines. There are 4,855 unique invoice IDs. Conflicting identities are not resolved by guessing allocations from IDs. `reports/workload.json` records overlapping omission causes and distinct review items.

## Verification actually completed

- **61 tests passed**, zero failures, errors or skips, both in the working project and in a clean clone. They include source/version/operator rejection, contract examples, amended rates, rounding and strict thresholds, cross-invoice rules, unchanged-total faults, failure handling and known-answer metrics.
- Every full hospital result matches after deterministic permutation of all loaded header, line and disposition records. The initial failing check found only source-header ordering in conflicting-ID traces; D015 preserves the failure and correction. No opinion fields changed.
- All six H1 opinion fields and every development/check/full metric match the frozen evaluated baseline. The check has already been exposed, so these are explicitly regression results, not a fresh holdout.
- An execution guard rejected label access during all pricing and export stages: zero label-file opens occurred. Socket creation/connections were blocked for the entire guarded replay: zero network attempts occurred. H1 evaluation reads labels only after predictions are finalized.
- A clean local clone removed every prior run and generated output, used a sanitized environment without inherited credentials or Work variables, and executed the README commands. Submission, metrics, workload report, evaluation report and full release manifest reproduced exactly.
- The decision log renders to **one page** and the accompanying write-up to **two pages**. All three final PDF pages were visually inspected after embedding fonts. Recovery checkpoints were actually extracted and checked by file hash.

Clean reproduction tested commit: `55f5b5f49af8bd0549b7fb11188570b18fbb5e03`. Subsequent changes are evidence/status records, not a claim that commit IDs are identical.

The guarded all-hospital replay took 29.50 seconds and measured 421.78 MiB peak process RSS. This is one observed workload, not a performance guarantee. The 6.6 MB source snapshot is small; retained historical traces account for most of the working project's disk usage. Core replay and tests require only Python 3.12.13. Optional PDF rendering dependencies are separately pinned.

## Status and evidence

**65 subtasks are Completed and verified.** This closes BT01-BT10 under the user override and documented scope dispositions. All 17 implementation quality gates are addressed. QG18 and the four BT11 subtasks remain **Not started** because they concern later repository publication, assessor access and actual delivery. QG19-QG22 were explicitly excluded as mandatory requirements by the governing reconciliation; no unimplemented production capability is claimed.

No implementation task remains in progress or awaits user action. H2 opinion coverage and other omissions remain source-evidence limitations. Source clarifications or additional facts would be required to expand that coverage; they are not prerequisites for reproducing the completed submission.

Detailed evidence:

| Record | Role |
|---|---|
| `reports/implementation_status.json` | All 69 original subtasks, governing completion conditions, actual evidence and precise qualifications |
| `reports/gate_status.json` | Big Task gates, QG01-QG22 dispositions and C01-C10 task links |
| `reports/provenance_check.json` | Current source/review/raw/package bindings and mapping counts |
| `reports/final_regression.json` | H1 baseline comparison, changed decision inputs and five full permutation checks |
| `reports/reproduction_check.json` | Actual clean clone, removed outputs, executed commands, hashes and 61-test result |
| `reports/guarded_reproduction.json` | Actual label/network guards, execution count and resource observations |
| `reports/release_manifest.json` | Nonrecursive current source/code/policy/evaluation/output identities |
| `reports/document_checks.json` | PDF hashes, page limits and final visual inspection |
| `docs/implementation_changes.md` | Expected behavior, observed contradictions, decisions, reasons and retained failures |
| `README.md` | Verified reproduction commands and replay/acquisition distinction |

The project is ready to hand over for the user's next independent auditing/challenging stage. No external repository has been published, no assessor access claimed and no email sent.
