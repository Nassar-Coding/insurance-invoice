# Insurance auditing — publishing preparation report

**PUBLISHING PREPARATION COMPLETE — READY FOR GITHUB / FINAL DELIVERY**

The independently audited implementation is preserved. The final local clean
reproduction passed all 75 tests and reproduced the exact 340-row submission.
This report records preparation and author verification; it is not a new
independent technical audit. No repository was pushed, no account permission
changed and no email sent.

## Publishing baseline verified

| Baseline artifact | SHA-256 |
|---|---|
| Corrected implementation checkpoint ZIP | `c3b49e516b335d9a2cd424279df3b983e66d6f23946a87fda6bbace61ade891e` |
| Attached corrected implementation report | `950da8b3322ae0cd1b9ea2b6038341d12336fed981d9b0f93402dae4213b9b20` |
| Attached audited submission | `2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c` |
| Attached independent closure report | `c159bdde3d9fa8d184c0f52dd84d8ded091584531a285cf838e1f59fee68e979` |

The attached companion ZIP contains the independent closure report and execution
evidence rather than the implementation project. The matching checkpoint was
recovered and its checksum compared with the closure report. All 874 checkpoint
manifest entries were verified; the standalone report and CSV match the checkpoint.
All 17 file entries in the auditor's companion manifest match. The audited local
implementation commit is `ebc3f05fd42bd84584cc5455dc7c0b74a2c8bc8c`;
the pinned challenge source is `6fee1da60b74512156637a22be15d996a36627e1`.

The unchanged independent verdict is **PASS — BOTH FINDINGS CLOSED, NO MATERIAL
REGRESSIONS**. AUD-01 preserves quarantined-header ownership uncertainty; AUD-02
records controlling bundle clauses and applicability evidence. Those fixes,
their failing examples, 14 added tests and original 61 tests remain unchanged.
No pricing, contract interpretation, accepted schema, mapping, confidence,
uncertainty, category, abstention or prediction logic was modified during preparation.

## What was prepared

- One source project with code/tests, unchanged source data, accepted/raw/revised
  contract and mapping records, policy/split evidence, source reviews and dependencies.
- Final README with executed installation, reproduction, validation and test
  commands; actual coverage, uncertainty, structure and history restoration guidance.
- Versioned prompts and prompt iterations unchanged. Publication instructions
  are recorded separately so the original release-bound prompt directory is untouched.
- Decision/history documents with explicit closure and preparation additions;
  negative results, withdrawn mappings, uncertain interpretations and omissions retained.
- Current one-page decision-log PDF and two-page write-up PDF, rendered with the
  pinned optional packages and visually checked on all three pages. Only stage
  wording changed; substantive decisions and metrics are preserved.
- Corrected implementation report with a dated addendum above unchanged original
  text. Exact original report/README/page-limited documents remain available.
- Independent audits and their execution evidence, author correction evidence,
  governing workbook/gates and the user override.
- Git-ready metadata, a full file-disposition register, verified compact original
  history, final execution evidence and package-level file checksums.

Every original executable file under `src/`, `tests/` and `tools/` remains
byte-identical. New `publishing/` utilities only verify packaging/reproduction
or render Markdown documents; prediction code does not import them. All **145
protected files** and **40 release-bound entries** were checked. The regenerated
release manifest is exactly unchanged:
`b6a52c763c3964fc105241f9993d352c4d0b5bb102897d1f5882eb399c4868c0`.

The generated evaluation report, prompt index and release-manifest scope retain
their original “closure pending” text because their exact bytes belong to the
audited release. Current status is clearly supplied by the README, this report
and the unchanged closure audit. Historical test/gate records retain dated
claims and hashes; `reports/README.md` distinguishes them from the final checks.

## Final executed reproduction

The clean-clone harness tested local preparation commit
`2cb44034ee47d7070ea9032aed552f2e6b681474`. It created a fresh virtual environment,
installed the empty core requirement file without an index and passed `pip check`.
Only pip 25.0.1 was present. It removed saved reports/results, historical runs,
reference/correction caches, audit attachments and Git history from the child
clone; kept the required reviewed input files; and supplied a sanitized environment.

| Verification | Result |
|---|---|
| Full original suite | **75 passed**, zero failures/errors/skips |
| All-hospital `reproduce` | Passed |
| `verify-submission` | Passed |
| Development/check/full H1 evaluation commands | Passed |
| Five complete hospital result files | Byte-identical to audited results |
| Five input-quality files | Byte-identical to audited results |
| Metrics, workload and evaluation report | Byte-identical |
| Full release manifest | Byte-identical |
| Detailed evaluation output | Equal except fresh attempt provenance |
| Submission schema/IDs/cents/confidence/order | Validated; 340 unique target IDs |
| Submission contents and bytes | Identical to attached reference |

All commands, return codes, logs, comparison hashes and new attempt statuses
are retained in `evidence/publishing/final_reproduction/`. No previous pass was
substituted for an executed check. `159.85` seconds
was observed for the pipeline on this run; maximum child-process RSS across
verification was `463.35 MiB`. This run generated
`266,033,447` bytes of attempt/release files. Timing and
attempt IDs differ from the earlier audit, as expected; these observations are
not deployment guarantees. The final metadata commit adds only evidence and
documentation to the tested state; the package manifest identifies the prepared
commit and all distributed bytes.

The root `submission.csv` was replaced with the newly generated identical bytes.
Its SHA-256 remains `2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c`.

## Preserved numerical results and limitations

| Hospital | Unique IDs | Complete opinions | Predicted errors | Withheld |
|---|---:|---:|---:|---:|
| H1 | 913 | 250 | 5 | 663 |
| H2 | 1125 | 0 | 0 | 1125 |
| H3 | 932 | 148 | 5 | 784 |
| H4 | 835 | 64 | 1 | 771 |
| H5 | 1050 | 128 | 0 | 922 |

H1 development: 169/622 opinions, 169 joint successes, 4/42 error recall.
Exposed check: 81/291 opinions, 81 joint successes, 1/16 error recall.
Full H1: 250/913 opinions, 250 joint successes, **27.38% coverage**,
**5/58 = 8.62% population error recall**, F1 **0.158730**. All 53 remaining
labelled errors are withheld. The check is regression evidence after exposure,
not a fresh holdout. H2–H5 accuracy is unknown.

| Hospital | Unchanged confidence value: opinion count |
|---|---|
| H1 | 0.65: 5, 0.9: 77, 0.95: 168 |
| H2 | No opinions |
| H3 | 0.7: 27, 0.8: 121 |
| H4 | 0.7: 14, 0.8: 50 |
| H5 | 0.65: 128 |

Whole-result byte comparison covers every confidence value, abstention identity
and reason, error category, arithmetic stage and source/context trace. There are
no changed technical results. H2's missing actual-submission/episode/exception
facts, H3/H5 directional/boundary qualifications, H4 scope bounds, H5 facility
projection, unsupported quantity dimensions and uncertain service identities
remain real limitations. Preparation does not manufacture better coverage.

## Intentionally excluded or archived

| Material | Disposition and reason |
|---|---|
| Nine incomplete atomic-write temporary files | Excluded: no successful attempt output map or runtime/test/gate consumes them |
| Loose historical/current attempt payloads and pointers | Archived in original Git history; normal reproduction generates fresh attempts. Exact original paths and failed runs remain recoverable |
| Obsolete storage observations and old page-preview PNGs | Archived in original history; replaced by current preparation checks for current status |
| Modified checkpoint recovery note | Preserved separately as historical evidence, not current validation |
| Workstation Git configuration/hooks, virtual environments, caches and new scratch outputs | Excluded from source ZIP; not dependencies or challenge deliverables |
| Duplicate outer checkpoint/attachment ZIPs | Not nested wholesale in the submission project; required project/evidence contents and original identities are retained |

No required source, review input, prompt, decision, failure example, schema,
mapping, policy, evaluation or audit evidence was discarded. All 360 non-Git
checkpoint files have an explicit disposition in
`evidence/publishing/file_disposition.json`. New files are identified by the
package manifest. The original seven-commit history bundle is 20,231,420 bytes;
its restoration and supplemental checkpoint bytes were verified.

A history-recovery check found one old H2 file whose Git copy is truncated:
`runs/attempts/0f10a3b2ecb245b7bda5230c379067bb/H2.json`.
The checkpoint copy is valid JSON and matches its attempt's declared hash;
it is preserved exactly in `evidence/history/checkpoint_differences.zip`, while
the original Git bytes remain in the bundle. The initial recovery assumption
was investigated and corrected, including an initial reversed interpretation
of which copy failed parsing. This does not involve the current audited H2 run
`4d449a6fc6fc49399da2cd567bdb1b51`, whose reproduced bytes match. No old file
was silently repaired. All 351 tracked checkpoint files are recoverable exactly
using the verified bundle plus explicit supplements.

## Dependencies and portability

Core execution/tests require CPython 3.12.13 standard library only. No model/API,
GPU, embeddings, database or Work-session behavior is required for replay.
Frozen generated schemas and mappings are explicit repository inputs; fresh
LLM extraction is a different process and is not claimed deterministic.

Optional PDF rendering used the exact unchanged pins: reportlab 4.4.9,
pillow 12.3.0, charset-normalizer 3.4.4 and pypdf 6.10.0. Those installed versions
and successful rendering/page/text checks were verified. A fresh online install
of optional PDF packages was not required or tested; core installation was
verified in the fresh environment. Linux commands were executed; the README's
PowerShell spelling and other platforms/Python versions remain untested.

The file inventory and high-specificity credential scan found no included
private-key/token signatures. Original synthetic data, relevant challenge
recipient and truthful AI/author attribution remain. This is a bounded content
check, not a universal secret or production-compliance certification.

## Remaining actions requiring the user or later authorization

1. Choose/authorize the solution repository destination and visibility, and
   provide a usable authorized GitHub connection or perform the upload yourself.
   No destination, remote credentials or write permission has been assumed.
2. Authorize the actual push/publication, then verify the remote file content
   against the prepared package. Local preparation is complete; remote publication is not.
3. Verify public readability or grant and confirm actual private access for
   `majedzahrani3`. A sent but unaccepted invitation is still pending access.
4. Check the original invitation's recipient/deadline/timezone or retain a
   defensible conservative send-time basis. The quoted recipient is
   `majedzahrani1@gmail.com`, Thursday 17 September, 11:59 PM; no timezone was supplied.
5. Send the final predictions, published repository link and two-page write-up,
   or explicitly authorize a supported sending action, then retain sent evidence.

These are later delivery actions, not local implementation/preparation blockers.
The historical ledger remains 65 verified implementation subtasks with four
external BT11 tasks uncompleted; QG18's actual access/delivery evidence is pending.
No unresolved issue blocks local preparation. The historic H2 Git discrepancy
is fully disclosed and preserved and does not change the audited submission.
