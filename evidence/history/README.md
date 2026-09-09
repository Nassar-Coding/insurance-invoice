# Original implementation history

`audited_implementation.bundle` preserves all seven original commits and their
tracked files, including initial mistakes, failed tests/attempts, schema and
mapping revisions, audit corrections and the final independently audited traces.
The corrected checkpoint is commit
`ebc3f05fd42bd84584cc5455dc7c0b74a2c8bc8c` on branch `implementation`.
This archive is historical evidence, not a prediction input.

From the submission repository root, recover it into a **new, separate** directory:

```bash
git bundle verify evidence/history/audited_implementation.bundle
git clone evidence/history/audited_implementation.bundle ../insurance-audit-history
git -C ../insurance-audit-history log --oneline
```

That historical checkout contains full original paths and can run its historical
author checks. Its README and status records are historical and retain the original wording. Do not copy old current-run pointers over newly generated pointers
in the submission checkout. No history restoration is required by the normal
README reproduction commands.

Important retained attempts:

| Attempt | Historical role |
|---|---|
| `c18fd65cf16d44a9b4fa86b34d2dcc4a` | Failed early H1 execution |
| `d0804aaa2af64ce2a8991289a9af941b` | Initial H1 development, including the mapping mistake |
| `b62dc53945c74386b17c3279636d94c6` | Frozen H1 evidence used by historical current-evidence checks |
| `21de44a39e574fcab93b00230f9ffdc5` | H1 before audit corrections |
| `521a93eae8af41ad94469b9968c36633` | Targets before audit corrections |
| `a1ee1b9f209f4f41913349e165fe8a26` | Independently audited corrected H1 |
| `4d449a6fc6fc49399da2cd567bdb1b51` | Independently audited corrected targets |

The bundle preserves all original tracked attempts, not only this list. Full
paths and SHA-256 values are indexed in `../publishing/file_disposition.json`.
`../publishing/history_verification.json` records actual recovery and hash checks.
The checkpoint's modified `reports/recovery_latest.json` is saved separately as
`checkpoint_recovery_latest.json`; it is an older storage note, not an execution result. Nine incomplete temporary writes were never authoritative
attempt outputs and are excluded. The original comparison manifest is preserved at `../audited_baseline/reproduction_baseline.json`.


Historical recovery also found that checkpoint file
`runs/attempts/0f10a3b2ecb245b7bda5230c379067bb/H2.json` differs from the truncated Git copy. The checkpoint version parses and matches
its recorded status hash. Its exact bytes are preserved in
`evidence/history/checkpoint_differences.zip` (paths are relative to repository
root); the separate Git bundle retains the original truncated committed version. Neither
is the current audited H2 result, which belongs to target attempt
`4d449a6fc6fc49399da2cd567bdb1b51`. No historical byte was silently repaired.
`evidence/publishing/history_verification.json` gives both hashes, parse results
and the original attempt's declared output hash.

For the exact checkpoint's complete old H2 file, after the separate history
clone above, apply only this explicit checkpoint supplement from the submission
root:

```bash
python -m zipfile -e evidence/history/checkpoint_differences.zip ../insurance-audit-history
```

This visibly changes the historical checkout relative to its Git commit and
restores the checksum named by that old attempt's status. The original Git bytes
remain in the bundle. No new current-run pointer is overwritten.
