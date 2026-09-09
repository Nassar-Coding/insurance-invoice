# Executed command interface

Use Python 3.12.13 with `PYTHONPATH=src` from the project root. The global `--project PATH` precedes the command. The initial interface sketch used different flags; this document records the actual tested interface, not aliases that were never implemented.

| Command | Actual behavior |
|---|---|
| `python -m insurance_audit inventory --hospitals H1 H2 H3 H4 H5` | Strict selected CSV ingestion and description/identity inventories; does not refit the H1 split. |
| `python -m insurance_audit audit --hospitals H1` | Accepted-bundle checks; identified attempt with opinions, omissions, traces and source counts; no label access. |
| `python -m insurance_audit audit --hospitals H2 H3 H4 H5` | Current final target batch; H2 remains diagnostic-only and contributes no complete submission rows. |
| `python -m insurance_audit evaluate --partition development` | Current H1 run only; fixed split. Also accepts `check` (exposed regression) and `full` (development-inclusive). |
| `python -m insurance_audit export` | Validates current target traces/fields, independently parses the staged CSV, then promotes a local pointer and root `submission.csv`. |
| `python -m insurance_audit verify-submission` | Rejects stale/changed source results, template, manifest or CSV bytes; confirms the current local artifact. |
| `python -m insurance_audit reproduce` | Recomputes all hospitals, final CSV, H1 metrics and report from frozen inputs; no extraction/refitting/network. |
| `python tools/run_checks.py NAME` | Standard-library tests with actual count, failures, captured output and tested-file hashes. |

A failed process is different from an invoice abstention. Failed audit attempts have `status=failed`, a reason and nonzero exit, and cannot replace a successful pointer. Export promotion uses a staged file plus a manifest-bound pointer. A crash between the final copy and pointer update is detected by checksum verification. A raw CSV viewed without its current manifest is not a claim that the latest attempted run succeeded.
