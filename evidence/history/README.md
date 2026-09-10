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
Current recovery and hash checks are recorded in
[integrity_verification.json](integrity_verification.json).
`../publishing/history_verification.json` is an earlier receipt; its H2 truncation
claim and corresponding recovered-file hash are corrected below.
The checkpoint's modified `reports/recovery_latest.json` is saved separately as
`checkpoint_recovery_latest.json`; it is an older storage note, not an execution result. Nine incomplete temporary writes were never authoritative
attempt outputs and are excluded. The original comparison manifest is preserved at `../audited_baseline/reproduction_baseline.json`.


## Verified archive contents

A fresh recovery on 2026-09-10 found that
`runs/attempts/0f10a3b2ecb245b7bda5230c379067bb/H2.json` is complete in the Git
bundle: 59,848,332 bytes, valid JSON, and SHA-256
`d27b0462e8f1ec4562f12e2b14cc5c144d90e1db23cc70447a6e109f5d053a41`.
It matches its recorded attempt-status hash and is byte-for-byte identical to
the member in `checkpoint_differences.zip`. The earlier truncation claim in
`../publishing/history_verification.json` and the corresponding explanation in
`../publishing/file_disposition.json` were inaccurate. Those historical receipts
remain unchanged so the correction is explicit; use the current verification
record for archive integrity. The cause of the earlier discrepancy is not
established by the retained evidence.

The bundle and ZIP both retain their previously recorded checksums. No archive,
historical result or current prediction was repaired or replaced. The ZIP is a
redundant preserved checkpoint copy; extracting it is unnecessary for history
recovery and does not change that H2 file. This old attempt is separate from
the independently audited target attempt
`4d449a6fc6fc49399da2cd567bdb1b51`.

All 351 files at the historical checkpoint were recovered and hashed; all 219
JSON files parsed. The one actual separately retained checkpoint difference is
the older storage note `checkpoint_recovery_latest.json`, whose bytes differ
from the bundle's `reports/recovery_latest.json`. Both versions remain available;
neither is required for prediction replay. No current-run pointer needs to be
overwritten.
