# Final clean-clone reproduction result

**PASS — audited technical behavior reproduced.** Verified on 2026-09-08 with
CPython 3.12.13 in a fresh Linux virtual environment.

| Check | Executed result |
|---|---|
| Fresh local Git clone | Commit `2cb44034ee47d7070ea9032aed552f2e6b681474` |
| Dependency installation | `pip install --no-index -r requirements.txt` passed; runtime requirements intentionally empty |
| Dependency validation | `pip check` passed; only pip 25.0.1 installed |
| All five hospitals | Recomputed from source CSVs and frozen schemas/mappings |
| Full original suite | 75 passed; 0 failures, 0 errors, 0 skipped |
| H1 development/check/full commands | All passed; results match the audited evaluation |
| Whole-result comparison | All five hospital JSON and five input-quality JSON files exactly match audited hashes |
| Stable reports | Metrics, workload and evaluation Markdown match byte-for-byte |
| Release manifest | Identical to the independently audited release |
| Submission | 340 unique target rows, six predicted errors and 334 predicted correct; exact columns, contents, order and bytes match the attached reference |
| Detailed evaluation metadata | Equal after excluding only fresh `/provenance/attempt` values |
| Protected technical files | All 145 original files and all 40 release-bound entries unchanged |

The clone had no saved submission, historical runs, correction caches, audit
attachments, reference-output evidence or Git object history available to the
pipeline. Only required source/candidate review reports remained. The parent
verification harness retained comparison hashes/reference bytes outside the
clone. A sanitized environment and a new virtual environment removed reliance
on Work-session credentials, model keys or globally installed Python packages.

Submission SHA-256:

```text
2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c
```

Release-manifest SHA-256:

```text
b6a52c763c3964fc105241f9993d352c4d0b5bb102897d1f5882eb399c4868c0
```

H1: 250/913 opinions, 250/250 flag-and-exact-amount matches on emitted opinions,
27.38% coverage, and 5/58 = 8.62% population error recall; 53 labelled errors
withheld. Target opinions: H2 0, H3 148, H4 64, H5 128. Confidence values,
omission reasons, error categories, arithmetic and provenance content did not
change. Target accuracy remains unknown; the check partition is already exposed.

Observed pipeline execution: 159.85 seconds.
Maximum child-process RSS across the full verification sequence: 463.35 MiB
(Linux measurement, not a pipeline-only or deployment capacity guarantee).
Generated attempt/release files occupied 266,033,447 bytes.
Fresh attempt IDs and runtime are expected differences from the audited run.

The executed commands, return codes, logs, hashes, full metrics and new attempt
status records are in `evidence/publishing/final_reproduction/` inside the project.
The final evidence commit adds documentation/receipts only; the package manifest
records its commit and file hashes. The audited source, tests, schemas, mappings,
confidence policy and prompts are unchanged. No remote clone, GitHub publication,
assessor-account access or email delivery is claimed.
