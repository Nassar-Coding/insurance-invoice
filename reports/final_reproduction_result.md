# Reproduction verification

**PASS.** Verified on 2026-09-09 with CPython 3.12.13. Both working-directory execution and a fresh local Git clone passed all 75 tests and regenerated the reference 340-row submission.

| Check | Result |
|---|---|
| Tested source/document commit | `ec26e2560cb75850e56e49f2bb4fb4ffa904836d` |
| Dependency installation | Fresh virtual environment; `pip install --no-index -r requirements.txt` and `pip check` passed |
| Full test suite | 75 passed; zero failures, errors or skips; test files and assertions unchanged |
| Replay | All five hospitals recomputed from source inputs and reviewed artifacts |
| H1 evaluation | Development, check and full commands passed; all metric values and per-invoice details unchanged |
| Hospital results | Five result files and five input-quality files byte-identical to the original references |
| Submission | Exact template columns, 340 unique IDs, six flags, same contents, ordering and SHA-256 |
| File and manifest checks | All 137 retained protected files and 37 current source/test/documentation entries matched |
| Generated documentation | Evaluation report and manifest match the current templates |
| PDF documents | Decision log one page; write-up two pages; all three pages visually inspected |

The test clone contained no saved submission, historical results, correction caches, reference evidence or Git objects during pipeline execution. Only required source/candidate review reports remained. The parent checker held the comparison hashes and reference CSV outside the clone. The runtime requirements are empty; no third-party package supplied prediction or test behavior.

All five hospital result files and all five input-quality files match the original reference hashes exactly. Metrics and workload also match byte-for-byte. This comparison includes opinions, amounts, confidence values, omissions, source references and calculation traces. H1 retains 250/913 opinions, 250/250 correct flag-and-exact-amount matches on emitted opinions, and 5/58 population error recall. Target opinions remain H2 0, H3 148, H4 64 and H5 128.

The evaluation report's final paragraph and the manifest's descriptive scope were cleaned. Since the report generator is included in source identity, its prose-only edit changes run identifiers; the prompt index and removal of internal orchestration prompts also change documentation fingerprints. Detailed H1 evaluations are equal after excluding only attempt and run identifiers. No numerical or complete hospital-result reference hash was replaced.

Submission SHA-256:

```text
2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c
```

The pipeline took 50.96 seconds in the clean clone. The full check took 82.02 seconds and its maximum child-process RSS was 480,244 KiB on Linux. Generated run files occupied 266,033,447 bytes. These are observed measurements, not deployment capacity guarantees.

[Technical preservation checks](../evidence/publishing/cleanup_verification/technical_preservation.json) compare the revised documentation state with the original numerical and trace references. [Clean-clone results and logs](../evidence/publishing/cleanup_verification/clean_reproduction/result.json) record commands, return codes, hashes, complete metrics and the tested commit. Subsequent evidence files and the example-pointer metadata update do not change any file guarded by those 137/37 checks, comparison algorithm, required expected result hash or executable behavior.
