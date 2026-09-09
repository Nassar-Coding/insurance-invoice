# Insurance Auditing — Independent Implementation Audit

Audit date: 7 September 2026. Selected solution: **LLM contract-to-schema with deterministic pricing**.

**Verdict: PASS WITH CORRECTIONS — implementation is fundamentally sound but identified issues should be corrected before publishing.**

The reported test count, deterministic replay, submission counts and Hospital 1 flag-and-amount metrics were independently reproduced. The retained numeric contract representations also match the supplied contracts. This audit found two substantive issues: a **Major** defect in propagating uncertainty from quarantined invoice headers, and a **Moderate** defect in bundle-clause citations. The first was demonstrated with an isolated input fixture; it is not present in the supplied snapshot. The second affects actual retained traces. Neither finding establishes that a current submitted amount is wrong. Neither should be described as a completed quality gate without correction.

This is an audit of the submitted technical candidate. No implementation, accepted schema, original prediction file or governing workbook was changed. Execution and additional audit fixtures used separate copies. No alternative solution, architecture, publication or delivery work was undertaken.

## 1. Authority, inspected material and verification boundaries

The governing challenge is the [original repository README at the inspected commit](https://github.com/majedzahrani3/insurance_auditing/blob/6fee1da60b74512156637a22be15d996a36627e1/README.md). I rechecked the repository through the GitHub connection and compared all 20 selected source files against its Git blob identities. Those files include the README, template, H1 labels, all ten invoice/line CSVs and all seven Markdown contract documents. All matched.

The challenge allows omitted invoices and does not require complete coverage. A submitted row must provide an opinion on the invoice, with the template's exact six fields. H1 is development/measurement data; target accuracy cannot be measured without H2–H5 labels. The user's subsequent instruction removed the original effort constraint for implementation. That override is retained in `governance/overrides.md` and is applied in this audit; missing the original 6–8 hour envelope is not a finding.

| Evidence | Identity / inspection result |
|---|---|
| Original challenge snapshot | `6fee1da60b74512156637a22be15d996a36627e1` |
| Implemented Git HEAD in checkpoint | `d468718711de952be5300906ee09a85d3d35ec2c` |
| Author's reported clean-test commit | `55f5b5f49af8bd0549b7fb11188570b18fbb5e03`; comparison to HEAD changes nine evidence/status/work-log files, with no runtime, rules, mappings or tests changed |
| Uploaded checkpoint ZIP | SHA-256 `2a8c49d972b81ee76908a41b904d2701c19ab14ba74b8a7fa451e6b4f8f92fa1`; all 701 manifest-listed entries verified after extraction |
| Uploaded ready workbook | SHA-256 `59095b64481e5e1fea2f3af06f8e1bb12d902f972d36efe5397891ce6cc09a45`; identical to the retained governing workbook |
| Uploaded implementation report | SHA-256 `3febf8eb9b0084f13ae4532f42b97caaf9fbe6b2922f1d695e739c24f592b63d`; identical to `reports/implementation_report.md` |
| Uploaded submission | SHA-256 `2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c`; identical to the checkpoint and independently regenerated CSV |

I inspected the runtime modules, all nine test modules and their source-derived fixture file, current accepted contracts and mappings, acquisition/review/prompt history, evaluation policy and split, current output traces, report evidence, and all 69 implementation-status entries against their governing completion conditions. All 69 IDs and completion-condition texts agree with the workbook. Every cited subtask evidence path exists in the original checkpoint.

Verification terminology:

- **Verified:** the stated claim was independently substantiated, with the method identified below.
- **Verified with qualification:** evidence supports a narrower or conditional claim; the qualification is material to interpretation.
- **Unsupported:** available evidence cannot establish the claim. This does not mean it is false.
- **Contradicted:** inspection or execution produced contrary evidence.

Execution demonstrates behavior in the tested environment. Inspection demonstrates what retained code and records contain. Neither reconstructs every action or thought in the original Work session, nor supplies missing target labels.

## 2. Reproduction and independent numerical checks

Two independent local Git clones were created from the checkpoint. The clean clone had all historical runs and the documented generated submission/evaluation outputs removed before reproduction. It ran with Python **3.12.13**, a sanitized environment, `PYTHONPATH=src`, no inherited application credentials, and no user-site imports. Core requirements contain no third-party packages: no package installation is required for the documented replay or tests. Optional PDF rendering dependencies were not needed or reinstalled.

| Actual command / check | Outcome | Observed elapsed time |
|---|---|---:|
| `python tools/run_checks.py independent_working` | 61 tests; 0 failures, errors or skips; exit 0 | 15.79 s |
| Clean `PYTHONPATH=src python -m insurance_audit reproduce` | All five hospitals recomputed, submission exported, H1 evaluated, stable reports regenerated; exit 0 | 38.27 s |
| Clean `PYTHONPATH=src python -m insurance_audit verify-submission` | Passed; exit 0 | 2.28 s |
| Clean `python tools/run_checks.py independent_clean` | 61 tests; 0 failures, errors or skips; exit 0 | 13.97 s |
| `python tools/reproduce_with_evidence.py` in the working audit clone | Label access blocked during pricing/export; sockets blocked throughout replay; 0 attempted label opens in guarded stages and 0 network attempts | 39.96 s |
| `python tools/verify_current_evidence.py` in the working audit clone | All five full shuffled results equal; H1 six-field baseline and all three metric sets equal; source/raw bindings pass | Passed |

These times are observations on this environment, not throughput guarantees. The guarded replay measured **422.01 MiB** peak process RSS, consistent with the report's approximate 422 MiB observation. I did not independently recreate the historical measurement of exactly 29.50 seconds.

The following files were byte-identical after clean regeneration:

| Regenerated file | SHA-256 |
|---|---|
| `submission.csv` | `2a208c622dd60391b1aaa3d28ee2413103f02268707fb28079aac6c32ba5c99c` |
| `reports/metrics.json` | `d10353d837cb44a812ad407c89b74b1932f40d1b7f871053b84182290d02d808` |
| `reports/workload.json` | `0e0f912676daae5d0c95020891abd8da2cee988a304b6ab100fd7ae72fd50b6c` |
| `reports/evaluation_report.md` | `73a3a2584723b050abdbce7ee2155ba7ae2052001037930766b4fd24b87bcad7` |
| `reports/release_manifest.json` | `47d11c03384edff6f18455f46b0ee91bd7fb14ee045ad25b69afb1f621a7504f` |

The three detailed `reports/evaluation_<partition>.json` files differ **only at `/provenance/attempt`**. Attempt IDs intentionally vary; this is disclosed and is not a reproduction defect. Fresh LLM extraction and historical acquisition are separate from this replay and are not claimed to regenerate byte-identically.

Additional checks did not import the implemented evaluator or pricing functions: H1 flag/amount metrics were recalculated directly from CSV labels and output opinions; all submission fields were independently parsed and reconciled; source tables/prose were compared against all numeric rule records; and emitted arithmetic was checked using separate decimal half-up calculations. All **5,605 lines in 590 emitted H1/target opinions**, including **14,225 recorded rounded stages**, reconciled. Of those, **3,106 lines** support the 340 submitted target opinions. These arithmetic checks validate calculations under the selected rules; they do not prove every interpretation or unseen target label.

## 3. Findings requiring correction

### AUD-01 — Quarantining a header can turn disputed patient ownership into a definite exclusion

- **Area:** input quality, identity, cross-invoice context, fail-closed behavior, test coverage.
- **Severity:** **Major**.
- **Claim being checked:** historical context preserves omitted/quarantined records as known or possible contributions, and unresolved necessary context prevents a complete invoice opinion.
- **Evidence inspected:** `src/insurance_audit/context.py`, especially construction of `headers` at line 30, the line-only quarantine loop at line 38, and patient ownership at line 52; `io.py`; `audit.py`; `submission.py::validate_result`; H1 §10 exclusion table; `tests/test_inputs.py`, `tests/test_pricing.py`; an independently executed three-header/two-line fixture using the unchanged accepted H1 contract, mappings and confidence policy.
- **Audit result:** **Contradicted by execution for quarantined-header ownership.** The existing 61 tests still pass. The new fixture produces an unsupported opinion that also passes the implementation's result validator.

**Reproduction facts.** Invoice I1 belongs to patient P1. Its one line is H1-S004, Advanced Metabolic Anaesthesia Administration, quantity 1, billed at **9,200 cents** on 2024-01-02. Invoice ID I2 has conflicting headers for P1 and P2; its line is H1-S100, Standard Endocrine Endoscopic Procedure, on the same date. H1's recorded exclusion interpretation makes the first service nonbillable if the anchor belongs to the same patient within seven days. With the two valid I2 headers, anchor ownership is disputed.

| Fixture | Correct evidence state for I1 | Actual implementation result |
|---|---|---|
| Both conflicting I2 headers have valid invoice dates | Ownership remains disputed: either 0 or 9,200 cents may be supported depending on the anchor's patient | I1 withheld for `unresolved_exclusion`; I2 withheld for conflicting identity |
| Change only the P2 header's invoice date to impossible `2024-02-30` | Quarantine does not prove that its line belongs to P1; ownership remains disputed | I1 emitted with `flagged=1`, `expected_total_cents=0`, confidence **0.65**, no interpretation qualification, and `outcome_invariant_uncertainty=false`; I2 withheld |

**Reasoning.** `Context.headers` includes only successfully parsed headers. The quarantine recovery loop reconstructs line items, but not recoverable header ownership. Dropping the P2 header from this structure converts `{P1,P2}` into `{P1}` for the anchor. The engine then calls the exclusion certain. Quarantining the anchor's own invoice does not preserve its uncertainty for related invoices. A finite confidence score and successful arithmetic/serialization validation do not resolve that missing fact.

**Current impact and what remains uncertain.** The supplied snapshot has **zero quarantined invoice headers**; its 35 quarantines are malformed-date line items. This counterexample therefore does not establish a wrong current submission row. The defect matters to the already promised invalid-input and dependency behavior, not to an invented production requirement. The same ownership construction is shared across hospitals and patient-scoped context operations; this audit demonstrated the exclusion case, not every possible downstream effect.

**Correction acceptance condition.** Preserve relevant uncertainty from malformed/conflicting headers through dependent calculations. Both fixture variants must withhold the unsupported I1 opinion, while retaining I2's explicit disposition. Add a regression that reaches confidence assignment/result validation, then recheck affected context behavior and the supplied-data outputs. Reopen the implicated completion claims, particularly ST02.03–ST02.04, ST05.02/ST05.05 and QG02/QG03/QG07/QG09, until that evidence exists. No fix was made in this audit.

### AUD-02 — Bundle calculation traces cite standalone rates instead of the applied bundle clause

- **Area:** contract evidence, calculation traceability, defensible reporting.
- **Severity:** **Moderate**.
- **Claim being checked:** an invoice's trace identifies the controlling contract rule and evidence for each applied calculation.
- **Evidence inspected:** `src/insurance_audit/pricing.py:60`; accepted `contracts/hospital_*.json` bundle records; current H1/H3/H4/H5 line traces; controlling source bundle tables, including H4 §7, source line 216.
- **Audit result:** **Contradicted for the bundle-stage source field; numerical bundle pricing is supported.**

**Reasoning and observed example.** The bundle stage records `source: service['refs']`, rather than the selected bundle's `source`. On actual flagged invoice **INV-H4-000583**, line **H4-L00583-03** uses Elective Obstetric Transfusion Service at **1,250 cents**, but cites source line 71, whose standalone rate is **1,425 cents**. Partner **H4-L00583-04** uses **111,675 cents**, but cites its standalone **126,900-cent** row at line 98. The applied substituted rates are correctly specified by the [H4 bundle clause](https://github.com/majedzahrani3/insurance_auditing/blob/6fee1da60b74512156637a22be15d996a36627e1/contracts/hospital_4/conditional_reimbursement_agreement.md#L216).

This occurs on **352 emitted bundle-priced lines across 151 invoices**: H1 100 lines, H3 76, H4 84, H5 92. Within the submitted target scope, **252 lines across 103 invoices** have this gap. The correct bundle references remain in the accepted contract records, so the calculation can be reconstructed by an engineer. The trace's own source pointer nevertheless fails to support the substituted amount it accompanies.

**What remains uncertain.** No erroneous bundle amount was found. This is not evidence of lost contract files or irrecoverable lineage. It is a specific gap in the asserted clause-level trace evidence.

**Correction acceptance condition.** A bundle substitution's trace must identify its controlling bundle record/source and the context establishing applicability. Verify the actual example and the other emitted substitutions against those references. Include this in QG11/ST05.05/ST09.04 evidence, and refresh generated trace/report identities as appropriate. This is technical audit evidence, not presentation polish.

## 4. Verification findings and qualifications

### AUD-03 — Runnable project, frozen replay and clean reproduction

- **Area:** reproducibility and dependencies.
- **Severity:** **No issue** within the declared replay scope.
- **Claim being checked:** another person can clone, select the documented runtime, run the commands and regenerate the technical outputs without hidden Work state.
- **Evidence inspected:** README, `.python-version`, both requirements files, CLI/pipeline/batch modules, Git tree/history, required accepted bundles and review files; executions and hashes in section 2.
- **Audit result:** **Verified by execution.** The checkpoint supplies a usable local Git repository and all required replay inputs. The README commands work after deleting old runs and outputs. No external model or network connection was used in guarded replay.
- **Reasoning:** source inputs were actually audited again; the pipeline did not copy a committed CSV. Dependencies are standard-library-only for core execution/tests. Historical regression tools require historical runs, as documented; ordinary replay does not. Required `reports/H*_source_review.json` files are explicitly documented as decision inputs and are tracked, so their directory name is not a hidden dependency.
- **What remains uncertain:** public remote cloning and assessor access are later actions and were not tested. Optional PDF-rendering installation and other operating systems were not exercised. None is represented here as a failed core replay.

### AUD-04 — The 61-test claim is true, but its scope is narrower than system correctness

- **Area:** tests and regression protection.
- **Severity:** **No issue** for the count; qualifications include AUD-01/AUD-02.
- **Claim being checked:** 61 passing tests provide meaningful verification of the implemented supported scope.
- **Evidence inspected:** all nine test modules, `tests/fixtures/h1_contract_examples.json`, `tools/run_checks.py`, test logs, full-snapshot permutation and frozen-baseline evidence.
- **Audit result:** **Verified with qualification**, by execution and inspection. The 61 are top-level unittest methods, some containing several cases; they are not 61 independent contract audits.

| Test module | Methods | Meaningful coverage inspected |
|---|---:|---|
| `test_inputs.py` | 7 | CSV schema/value failures, raw accounting, source counts, split/label boundaries |
| `test_schema.py` | 11 | Finite records, compatibility/source changes, unknown operators, mapping keys and ambiguity |
| `test_pricing.py` | 16 | Exact rounding, thresholds, cap, bundle/exclusion context, duplicate allocation, malformed-date influence, history revision and complete-row withholding |
| `test_targets.py` | 10 | H3 rate/addition boundaries and inherited rules; H4 units/scope; H5 ordered multipliers, bundles and cumulative usage |
| `test_h2.py` | 8 | H2 diagnostic rules, unavailable service-day/eligibility facts, and avoiding imported prohibitions |
| `test_evaluation.py` | 3 | Known-answer denominators, abstentions and category-family behavior |
| `test_confidence.py` | 2 | Supported/sparse/novel/unresolved treatment and invalid scores |
| `test_submission.py` | 3 | Exact serialization, invalid/stale output and failed promotion behavior |
| `test_batch.py` | 1 | Repetition, failure status and tamper/current-result behavior |

- **Reasoning:** the suite includes substantive source-rule and uncertainty cases, not merely mechanical assertions. Serialization tests using mocks establish serialization behavior, not independent pricing correctness. The passing suite misses the concrete quarantined-header interaction in AUD-01 and does not assert the controlling bundle citations in AUD-02. Full shuffled results and the H1 baseline were additionally reproduced, but comparing an engine with itself cannot detect a stable semantic error.
- **What remains uncertain:** target accuracy, every possible rule interaction and the behavior on arbitrary future malformed inputs are not established. Those are not implied by the number 61.

### AUD-05 — Contract-to-schema acquisition and numeric transcription

- **Area:** LLM extraction reliability, source semantics and selected-solution fidelity.
- **Severity:** **No issue** for checked transcription; interpretation qualifications remain.
- **Claim being checked:** all catalog services and price mechanisms are retained as finite, reviewed, source-bound records used by a fixed interpreter.
- **Evidence inspected:** every supplied Markdown contract; all accepted service/rule records; acquisition scripts/raw outputs, source-review records, schema validation, versioned extraction/review prompts and changes D007–D014.
- **Audit result:** **Verified with qualification**, by exhaustive numeric/unit reconciliation and source/code inspection.

| Hospital | Services | Rate versions | Daily caps | Daily premiums | Weekend uplifts | Discount tiers | Bundle pairs | Exclusion rules |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| H1 | 108 | 108 | 7 | 9 | 7 | 11 | 3 | 6 |
| H2 | 76 | 76 | 8 | 9 | 8 | 12 | 3 | 6 |
| H3 | 120 | 127 | 12 | 14 | 12 | 19 | 5 | 10 |
| H4 | 98 | 98 | 18 | 18 | 0 | 4 | 7 | 15 |
| H5 | 84 | 84 | 9 | 10 | 9 | 15 | 3 | 7 |

All base/revised cents, unit representations, caps, threshold quantities, uplift/discount ratios, bundle amounts and exclusion service/window relationships matched. All **504 H5 facility/tier multiplier cells** also matched. H3's 120 services comprise 118 original services plus two additions; seven services have a second price version.

- **Reasoning:** the implementation correctly uses H3 A1.1's service-date effective boundary of **2025-01-01**, preserves inherited conditions, and treats additions as nonbillable before that date. H4's explicit instance=unit definition and absence of weekend uplifts are represented. H2's distinct service-day and invoice-effectiveness requirements are not silently replaced with H1 semantics. Compound hour/item dimensions remain unsupported instead of receiving invented conversions.
- **Acquisition qualification:** this is Work-model-assisted interpretation and author review, with deterministic transcription aids and retained finite outputs. It is not a separately invoked model API or an independent second reviewer. That is disclosed and preserves the selected solution. Structural validation and accepted hashes establish package identity, not semantic truth. The independent source comparison supplies additional evidence for transcription; it does not turn interpretation choices into observed facts.
- **What remains uncertain:** H3 settlement chronology, H3/H5 exclusion direction, exact window inclusivity and H5 facility projection remain recorded interpretations. H4 aggregation ambiguity is bounded. The source does not provide universal external clinical, episode or legal truth; no such truth was introduced in this audit.

### AUD-06 — Deterministic calculations and actual flagged target examples

- **Area:** pricing and cross-field consistency.
- **Severity:** **No issue** for the checked supplied-data calculations; see AUD-01 for the input-uncertainty defect.
- **Claim being checked:** the engine applies accepted rules with exact, ordered arithmetic and produces supported corrected totals.
- **Evidence inspected:** `pricing.py`, `checks.py`, version resolution, accepted source rules, all emitted line-stage arithmetic, all six flagged target invoice traces and their raw source rows.
- **Audit result:** **Verified with qualification.** All emitted line amounts and invoice sums reconcile under the recorded rule selections. Independent decimal calculations match every recorded rounded stage. Source-derived checks cover the materially different rule families.

| Flagged target invoice | Billed cents | Expected cents | Checked explanation |
|---|---:|---:|---|
| INV-H3-000029 | 801,990 | 794,425 | A wrong unit leaves one line's amount unchanged; another line uses 14,225 rather than 16,359 cents; an unearned discount is removed from a 20,700-cent service |
| INV-H3-000067 | 2,127,583 | 2,118,775 | Nine billed units capped at four at 3,450 cents; another service's premature discount is removed |
| INV-H3-000344 | 3,057,951 | 3,052,251 | Service on 2024-10-04 uses 2,575 cents, not the 3,050-cent rate effective in 2025; difference is 12 × 475 cents |
| INV-H3-000676 | 3,978,332 | 3,815,132 | Same-patient/day bundle replaces 6,925 and 442,975 cents with 5,675 and 363,250; quantities 3 and 2 account for the 163,200-cent reduction |
| INV-H3-000716 | 1,461,455 | 1,446,155 | Two units corrected from 38,250 to the 30,600-cent contracted rate |
| INV-H4-000583 | 947,375 | 819,575 | Bundle reductions of 525 and 15,225 cents plus a 112,050-cent standalone-rate correction |

- **Reasoning:** quantity multiplication follows staged rate adjustments; half-up uses exact integer ratios. Discounts depend on strictly prior usage and the deepest eligible tier, not stacked tiers. Unsupported duplicate allocation is withheld. A wrong unit can correctly produce a flag without changing cents. H5's sampled 268,575-cent rate multiplied by 0.92 gives 247,089 cents before later applicable stages, matching its trace.
- **What remains uncertain:** these are source-supported computational checks, not target-label validation or proof that the service actually delivered matched every description. The H5 checks are conditional on the disclosed invoice-facility projection. AUD-02 concerns citations, despite correct bundle values.

### AUD-07 — Service mapping is transparent and conservative, with explicit semantic limits

- **Area:** description mapping and extraction evidence.
- **Severity:** **No issue** in the checked mapping-policy consistency.
- **Claim being checked:** 2,330 observed normalized keys are represented; accepted identities have evidence; ambiguous/unseen identities do not get forced by billed rates or units.
- **Evidence inspected:** all current mapping records/raw aliases, `lexicon_v1.json`, normalizer/resolver, acquisition and mapping-review tools, prompts v1/v2, retained H1 mapping revision, all raw line descriptions.
- **Audit result:** **Verified with qualification**, by independent inventory/token-evidence checks and code inspection.

| Hospital | Normalized keys | Accepted | Unresolved | Accepted generic-noun elision keys |
|---|---:|---:|---:|---:|
| H1 | 470 | 407 | 63 | 14 |
| H2 | 441 | 304 | 137 | 23 |
| H3 | 507 | 422 | 85 | 11 |
| H4 | 488 | 380 | 108 | 15 |
| H5 | 424 | 348 | 76 | 11 |

- **Reasoning:** all observed keys, including descriptions on quarantined lines, are accounted for. Accepted keys have one supported hospital-catalog candidate under the recorded lexicon and satisfy the stated independent-token rule. I checked every accepted record against that rule, including all elision keys. Opaque terminal suffixes are removed without using them as service truth. Runtime lookup of a genuinely new normalized key remains unresolved; an unresolved candidate is not accepted just because it has one lexical possibility. Prices and billed units do not choose identity.
- **Development correction:** the generic `Fract Outpatient Radiotherapy` mapping wrongly supplied a missing Metabolic specialty in initial development. The retained revision withdraws all 39 analogous keys, preserving the error and reduced coverage. This is defensible general development, not an invoice-specific amount patch.
- **What remains uncertain:** lexicon meanings and permitted generic-noun omission are reviewed semantic judgments. Matching this policy is not external proof of actual delivered service or target mapping accuracy. Unknown cases can reduce coverage both directly and through related context; that behavior is disclosed.

### AUD-08 — Hospital 1 evaluation numbers are correct and heavily conditional on coverage

- **Area:** measurement, abstention and systematic failure analysis.
- **Severity:** **No issue** in the reproduced metrics and their stated denominators.
- **Claim being checked:** 250/250 emitted flag-and-exact-amount matches, 27.38% coverage and 8.62% error recall.
- **Evidence inspected:** original H1 labels, source invoice IDs, frozen split, regenerated opinions, independent CSV-based recomputation, evaluator/crosswalk, evaluation report and retained initial error evidence.
- **Audit result:** **Verified by independent recomputation**, with the interpretation below.

| Population | Invoice IDs | Emitted | Joint matches | Labelled errors | Detected errors | Error recall |
|---|---:|---:|---:|---:|---:|---:|
| Development | 622 | 169 | 169 | 42 | 4 | 9.52% |
| Check | 291 | 81 | 81 | 16 | 1 | 6.25% |
| Full H1 | 913 | 250 | 250 | 58 | 5 | 8.62% |

- **Reasoning:** full coverage is `250/913 = 27.3823%`; recall is `5/58 = 8.6207%`. The 250 emitted opinions consist of **245 labelled-correct invoices and five labelled errors**. Of 663 withheld invoices, **53 are labelled errors and 610 are labelled correct**. Error precision is 5/5 on emitted positive flags. Withheld errors are counted as misses; withheld correct invoices are not counted as correct negative predictions.
- **Metric limits:** the joint match event is flag plus exact expected cents. It does not establish exact free-text error-category correctness or calibrated confidence. Categories use a disclosed many-to-one family crosswalk; broad pricing flags do not identify every specific discount/premium cause. H1 is development data; the check has already been exposed and later checks are explicitly regressions. Patient groups share legitimate contract-wide utilization and are not independent external samples.
- **Failure analysis:** the report distinguishes its observed initial emitted mapping error from current omission mechanisms. It gives actual examples rather than inventing four final false-positive families. The final emitted subset has no observed flag/amount errors, but 91.38% of labelled errors are withheld. That limitation is prominently disclosed.
- **What remains uncertain:** performance on omitted invoices, new hospitals and new input distributions is not established by 250/250. No broader accuracy claim is warranted.

### AUD-09 — No execution-path label leakage found; development use is legitimate and disclosed

- **Area:** leakage, calibration and chronology.
- **Severity:** **No issue** in the inspected data flow.
- **Claim being checked:** H1 labels are used for development/evaluation, not copied into contract records, mappings or target prediction decisions.
- **Evidence inspected:** runtime and acquisition imports/reads, mapping selection inputs, `freeze_confidence.py`, split and frozen development evidence, historical baseline/mapping records, Git history, independently executed label/network guard.
- **Audit result:** **Verified with qualification.** Pricing/export completed with label opens prohibited. No runtime label lookup, per-invoice answer patch, target labels or label-based mapping selector was found. The retained policy evidence contains exactly 622 development IDs, all assigned to development, and matches the policy's recorded evidence hash.
- **Reasoning:** H1's general mapping correction and confidence policy are allowed development. The split is based on connected patient identities, keeping reused-ID patient groups together. Unlabelled global utilization shared across partitions is necessary retrospective context, not copied ground truth. The evaluator skips nonrequested partition labels before constructing scored label records; reading the shared CSV for identities/hashing does not itself fit the model on those outcomes.
- **What remains uncertain:** retained artifacts support the reported freeze-before-check chronology, but cannot independently prove that no person/model ever viewed other label values earlier in the original session. Earlier label structure/count and ambiguity-distribution inspection is disclosed. Consequently this audit does not certify an untouched external holdout or a complete historical access log.

### AUD-10 — H2 withholding is defensible, but the missing-fact statement needs precise interpretation

- **Area:** H2 contract interpretation, temporal eligibility and scope.
- **Severity:** **No issue** in withholding H2 complete opinions.
- **Claim being checked:** missing submission/episode/waiver evidence prevents supported complete H2 payable opinions.
- **Evidence inspected:** H2 Articles II, III, XIII and other governing prose/rate clauses; both H2 CSV schemas and all headers; accepted semantics, diagnostic traces and H2 tests.
- **Audit result:** **Verified with qualification.** There are 1,125 unique H2 IDs and zero opinions. The source does not supply an actual submission timestamp/date, leave intervals or written exception evidence. Article XIII.1–XIII.5 makes effectiveness depend on timely submission and permits written exceptions. Invoice date is not evidence of actual submission.
- **Reasoning:** the missing submission fact alone supports conservative withholding of a complete payable amount; a likely late invoice cannot simply be assigned zero when the contract permits exceptions. H2 also defines a 07:00–06:59 Service Day with an exception for service wholly within one calendar day. Calendar service dates alone do not prove the relevant duration/timing condition. H2 diagnostic code correctly avoids importing the other hospitals' explicit service-date-after-invoice and duplicate-service/day prohibitions.
- **Important qualification:** **all 1,132 H2 header records contain admission and discharge dates**. It would be incorrect to summarize the finding as “no episode dates exist.” What is absent is the additional evidence needed to establish the applicable episode/leave and actual submission/exception conditions. The current diagnostic traces retain discharge dates and provisional deadlines; the report's short “episode facts absent” wording must be read in that narrower sense.
- **What remains uncertain:** the withheld invoices' actual eligibility and payable totals remain unknown. Conservative withholding is supported; it is not proof all H2 invoices are erroneous, nor a claim that every H2 price calculation is impossible. Its 76 service records and diagnostics are implemented; full H2 opinion coverage is not.

### AUD-11 — Submission structure, target counts and current-output consistency

- **Area:** target execution and submission integrity.
- **Severity:** **No issue** in checked file integrity.
- **Claim being checked:** submission contains the reported target opinions, follows the template and agrees with source billed data/current outputs.
- **Evidence inspected:** attached and regenerated CSVs, original template, all source header IDs/totals, emitted raw-line membership and traces, exporter/validator and current release manifest.
- **Audit result:** **Verified by execution and independent parsing.**

| Hospital | Unique IDs | Opinions | Flagged | Withheld | Opinion coverage |
|---|---:|---:|---:|---:|---:|
| H2 | 1,125 | 0 | 0 | 1,125 | 0.00% |
| H3 | 932 | 148 | 5 | 784 | 15.88% |
| H4 | 835 | 64 | 1 | 771 | 7.66% |
| H5 | 1,050 | 128 | 0 | 922 | 12.19% |
| Targets combined | 3,942 | 340 | 6 | 3,602 | 8.63% |

- **Reasoning:** the file has exactly `invoice_id,flagged,error_category,expected_total_cents,billed_total_cents,confidence`, in order; 340 unique target IDs; no H1 IDs; 0/1 flags; integer money; finite in-range confidence; and category presence consistent with flags. Every field matches the corresponding current internal opinion. Billed totals match unique source headers, and every source line of each emitted invoice is represented. Unflagged rows also reconcile billed line arithmetic and totals. There are six predicted errors and 334 predicted-correct invoices.
- **Accounting:** the raw snapshot contains **4,886 headers + 61,211 lines = 66,097 occurrences**, and 4,855 unique invoice IDs across all five hospitals. These counts reconcile; duplicate raw identities are not multiplied through joins. All 35 quarantines are malformed-date line items.
- **What remains uncertain:** no H2–H5 labels exist, so neither zero observed CSV integrity errors nor the source checks establish target precision/recall. In particular, H5's 128 opinions depend on the explicit facility projection described below. Unlabelled target correctness remains unmeasured.

### AUD-12 — Confidence is an explicit policy, not validated target probability calibration

- **Area:** confidence, interpretation and uncertainty.
- **Severity:** **No issue** in disclosed policy assignment; AUD-01 exposes a separate unresolved-fact escape.
- **Claim being checked:** confidence reflects evidence and uncertainty, with no unsupported transfer of empirical H1 accuracy to targets.
- **Evidence inspected:** frozen policy/evidence, policy-generation and assignment code, confidence tests, all emitted scores/tiers, H5 D012 and governing ST08.03.
- **Audit result:** **Verified with qualification.** All emitted values follow the retained policy. H1 scores are 0.95/0.90 for supported correct-opinion tiers and 0.65 for sparse error tiers. Targets use 0.80/0.70 for explicit/elided identities, with interpretation or invariant-uncertainty caps of 0.65. All 128 H5 opinions have that interpretation qualification and score 0.65.
- **Reasoning:** the frozen development support is 122/122 explicit correct opinions, 43/43 elided correct opinions, 4/4 explicit errors and zero elided errors. The policy explicitly labels sparse and target scores as judgments. The displayed Wilson calculations do not establish independent calibration after development selection or with shared context. H3/H4's 0.80/0.70 values are reproducible judgments, not measured target success probabilities.
- **H5 qualification:** the contract speaks of a line facility, while the CSV supplies an invoice facility also required by §10.1. Projecting that header attribute onto its lines is a documented interpretation of the supplied relational representation. The plan explicitly anticipated a recorded facility interpretation. It is defensible as a qualified candidate assumption, but neither the source fields nor 0.65 confidence proves it true. These results should remain described as conditional on that assumption, not as observed line-facility facts or validated H5 accuracy.
- **What remains uncertain:** numerical target calibration and the actual H5 line-facility facts. A lower score cannot repair missing necessary evidence; that principle is correctly stated in the report but is violated by the distinct implementation defect in AUD-01.

## 5. Governing execution and real-world quality gates

The status ledger contains exactly **65 “Completed and verified” and four “Not started”** entries. The four unstarted entries are ST11.01–ST11.04, which concern later destination/publication/access/delivery work. H2's conditional subtasks can close through a truthful diagnostic-only/no-opinion disposition; they need not falsely claim H2 coverage. The time-control entries correctly record the user override instead of claiming original-budget compliance.

The count of completed labels is verified. **Unqualified completion of every underlying technical gate is not:** AUD-01 and AUD-02 require the affected completion/evidence claims to be reopened or qualified. This is a consequence of those two findings, not a third independent defect.

| Quality gate | Independent disposition and evidence |
|---|---|
| QG01 — Source freshness/package compatibility | Supported for this snapshot: all 20 source files match the repository; changed-source/unaccepted/incompatible packages are rejected; invoice revisions have new run identities. Does not discover contracts absent from the supplied snapshot. |
| QG02 — Input schema/value integrity | Source accounting and rejection/quarantine fixtures pass. **Correction needed:** quarantine's downstream uncertainty promise is incomplete for header ownership, AUD-01. |
| QG03 — Identity/joins/hospital isolation | Current scoped joins and conflicting-ID omissions are supported. **Correction needed:** recoverable conflicting ownership in a quarantined header can disappear, AUD-01. |
| QG04 — Service identity/normalization | All 2,330 keys reconciled and accepted token/grade policies checked; unseen and ambiguous identities remain unresolved. Semantic confidence remains qualified, AUD-07. |
| QG05 — Extraction semantics/clause coverage | Numeric records independently reconciled, source hierarchy reviewed and raw/review lineage retained. Recorded interpretations remain judgments; acceptance hashes alone are not proof. |
| QG06 — Temporal applicability/observable facts | H3 before/on/after boundaries, inherited terms and additions are supported. H2 service-day/submission uncertainty is explicit; H3 settlement chronology is a recorded assumption. |
| QG07 — Cross-invoice context/uncertainty | Omitted and malformed-date line context plus revision/permutation checks are meaningful. **Not fully closed:** the quarantined-header counterexample in AUD-01 defeats the broader gate. |
| QG08 — Exact money/correction consistency | All emitted arithmetic independently reconciles; staged half-up, caps and unchanged-total faults have source cases. Correct arithmetic remains conditional on correct context. |
| QG09 — Fail-closed opinions/batch release | Failure status, staged release and tamper checks work. **Not fully closed:** an unsupported complete opinion in AUD-01 passes result validation despite uncertain ownership. |
| QG10 — H1 evaluation/leakage/confidence | Metrics independently reproduced; policy support and runtime label isolation verified. Target calibration and an untouched external holdout are not established. |
| QG11 — Lineage/defensible reporting | Inputs, versions, rows and calculations are retained. **Correction needed:** applied bundle-stage source references are wrong/incomplete, AUD-02; “all gates complete” needs corresponding qualification. |
| QG12 — Clean deterministic reproduction | Independently executed after deleting old outputs/runs; stable files match; no Work/API dependency in replay. |
| QG13 — Change impact/regression | H1 baseline, all three metric sets and five shuffled full results reproduced. Existing regression does not detect AUD-01/AUD-02; their corrections need relevant additional regression evidence. |
| QG14 — Durable checkpoint/recovery | Current delivered ZIP extracted and all 701 manifest entries matched. Historical recovery records exist; the exact older recovery exercises were not independently reenacted. |
| QG15 — Workload/review burden/capacity | Omission reasons, affected IDs, distinct mapping keys and resource observations are retained. Current target coverage is 8.63%, leaving 3,602 omissions; this is visible and potentially substantial review work. No large-scale or manageable-review guarantee is established or required. |
| QG16 — Snapshot revisions | Input identities change; full relevant snapshots are recomputed; prior provenance is retained. The implemented prior-quantity revision case passes. No unseen-feed completeness claim is made. |
| QG17 — Source-to-execution boundary | Finite operators, source-as-data prompts and instruction/unknown-operation rejection are present. No arbitrary generated contract functions or runtime `eval` path was found. |
| QG18 — Access/publication/delivery | Correctly remains later/unstarted. No technical finding for its absence in this stage. |
| QG19 — Mandatory OCR/dual pipeline | Correctly excluded; supplied Markdown/CSV formats are sufficient and selected explicitly. |
| QG20 — Streaming/high availability | Correctly excluded; implementation declares batch scope. |
| QG21 — External clinical/code/legal truth | Correctly excluded as a mandatory external pipeline; missing necessary supplied facts are generally withheld or explicitly interpreted. |
| QG22 — Real-patient compliance certification | Correctly excluded for this synthetic exercise; no such certification is claimed. |

At Big Task level, BT02/BT05/BT09 completion is qualified by AUD-01, and BT05/BT09/BT10 evidence closure by AUD-02 and the resulting report/status updates. BT01/BT03/BT04/BT06/BT07/BT08 have supporting scoped evidence, subject to the interpretation and measurement limits above. BT11 remains intentionally unstarted. This audit has not promoted the pre-implementation workbook's readiness statements into proof of implementation completion.

Operating-quality limits are concrete: context scans and retained traces must be measured before much larger volumes, cached reviewed artifacts need source/version checks, and broad uncertainty creates a substantial review burden. The current batch and observability evidence expose these limitations. A streaming platform, OCR pipeline, production certification or external terminology system would not close the two observed defects and is not added as a requirement.

## 6. Reconciliation of important implementation-report claims

| Claim in the report | Classification | Independent result |
|---|---|---|
| Selected solution implemented with finite records and a fixed interpreter | **Verified** | Current execution follows that boundary; no alternative engine or runtime model call found. |
| 486 services and 2,330 normalized keys represented | **Verified** | Source and inventory comparisons agree, including H3 additions. |
| Contracts/rules correctly extracted for the documented scope | **Verified with qualification** | Numeric/unit/rule-table transcription agrees; source interpretation, author-review independence and target truth have the limits in AUD-05/AUD-12. |
| Relevant quarantined/omitted context always preserves necessary uncertainty | **Contradicted** | AUD-01: malformed header ownership can become false certainty. The current malformed-line cases do work. |
| Every emitted amount reconciles to source lines and policy | **Verified with qualification** | Current amounts, line membership and policy assignment reconcile. This validator is not an independent semantic proof and accepts AUD-01's unsupported opinion. |
| Clause-level traces support every applied rule | **Contradicted** | AUD-02; correct bundle clauses remain recoverable from accepted records. |
| 340 targets: H3 148, H4 64, H5 128, H2 0 | **Verified** | Independently recomputed and parsed. |
| Six target errors and 334 target correct opinions | **Verified with qualification** | Correct counts of predictions, not known target outcomes. The report makes that distinction. |
| H1 250/250, 27.38% coverage, 8.62% error recall | **Verified** | Recomputed directly from labels/opinions; interpretation is conditional on coverage. |
| H2 missing facts justify no full opinions | **Verified with qualification** | Actual submission/exception and detailed episode/service-day evidence are absent; admission/discharge dates are present. |
| All 128 H5 opinions use qualified facility projection at 0.65 | **Verified with qualification** | Actual assignment verified; the assumed line facility and calibration are not independently established. |
| 66,097 raw occurrences, 4,855 unique IDs, 35 malformed-date quarantines | **Verified** | Independent counts and output accounting agree. |
| 61 tests pass in working and clean environments | **Verified** | Reexecuted twice; no skips/failures/errors. |
| Five full shuffled results and H1 baseline metrics agree | **Verified** | Reexecuted the retained regression checks against the current candidate. |
| No label opens during pricing/export or network attempts in guarded replay | **Verified** | Independently executed the inspected guard. Does not prove the entire original session's access history. |
| Clean replay reproduces submission, metrics and stable reports | **Verified** | Byte-identical stable artifacts; detailed evaluation JSON differs only by attempt ID. |
| 65 subtasks are labelled completed | **Verified** | All 69 IDs/conditions and the 65/4 status count match the governing ledger. |
| All 65 tasks and all 17 implementation quality gates are completely verified | **Contradicted** | Affected gates must reflect AUD-01/AUD-02; most underlying evidence is real and reproduced. |
| One-page decision log and two-page write-up | **Verified** | Retained PDFs have one and two pages, respectively, with extractable text. Optional re-rendering and presentation polish were not audited. |
| All PDF pages were visually inspected during authoring | **Unsupported** | The author's record exists; this audit cannot independently prove that past visual inspection occurred. Not a technical correction finding. |
| Check was first viewed only after freeze; no earlier undisclosed label influence | **Verified with qualification** | Retained development evidence and baseline are consistent with the sequence; absence of every earlier session access is not independently provable. No illicit data flow was found. |
| Recovery checkpoints were extracted and hash-checked | **Verified with qualification** | This delivered checkpoint restored correctly; older claimed restore events are retained records, not independently reenacted here. |
| Exact historical runtime/RSS observations | **Verified with qualification** | Recorded values exist; current observed runtime differs, with similar memory. No guarantee is asserted. |
| No publishing/delivery or independent audit had occurred at checkpoint creation | **Verified with qualification** | Local status/scope are consistent. External account actions were not investigated; this report is the subsequent independent audit. |

The report should now acknowledge AUD-01's limitation to header uncertainty and AUD-02's bundle-citation gap, and qualify the affected completion claims. Its existing low-coverage, target-label, author-review, H5 projection, H2 missing-fact and fresh-extraction limitations are appropriate and should be retained.

## 7. Reproduce AUD-01 without modifying the implementation

Run the following from an extracted project root with the documented interpreter. It reads the existing accepted H1 artifacts and writes only temporary synthetic CSV fixtures. It does not change project code, source inputs, accepted mappings or submission. The fixture's descriptions are existing accepted explicit aliases, so an unseen-description fallback is not involved.

```python
import csv, json, sys, tempfile
from pathlib import Path

root = Path.cwd()
sys.path.insert(0, str(root / "src"))
from insurance_audit.io import INVOICE_COLUMNS, LINE_COLUMNS, load_hospital
from insurance_audit.audit import audit
from insurance_audit.confidence import assign_confidence
from insurance_audit.submission import validate_result

contract = json.loads((root / "contracts/hospital_1.json").read_text())
maps = json.loads((root / "mappings/hospital_1.json").read_text())
policy = json.loads((root / "evaluation/confidence_policy.json").read_text())
services = {s["id"]: s for s in contract["services"]}
aliases = {
    sid: next(r["raw_descriptions"][0] for r in maps["records"]
              if r["state"] == "accepted" and r["service_id"] == sid
              and r["grade"] == "explicit")
    for sid in ["H1-S004", "H1-S100"]
}

def header(ident, patient, invoice_date="2024-01-03"):
    return dict(invoice_id=ident, hospital_id="H1",
                contract_number=contract["contract_number"],
                invoice_date=invoice_date, patient_id=patient,
                facility_code="F-MAIN", plan_tier="BRONZE",
                admission_date="2024-01-01", discharge_date="2024-01-02",
                invoice_total_cents=9200 if ident == "I1" else 124450)

def line(ident, line_id, sid):
    svc = services[sid]
    rate = svc["versions"][0]["cents"]
    return dict(line_id=line_id, invoice_id=ident, line_no=1,
                service_date="2024-01-02", description=aliases[sid],
                quantity=1, unit_basis_as_billed=svc["unit"],
                unit_price_cents=rate, line_total_cents=rate)

with tempfile.TemporaryDirectory() as directory:
    for malformed in [False, True]:
        snapshot = Path(directory) / str(malformed)
        (snapshot / "invoices").mkdir(parents=True)
        headers = [header("I1", "P1"), header("I2", "P1"),
                   header("I2", "P2", "2024-02-30" if malformed
                          else "2024-01-03")]
        lines = [line("I1", "L1", "H1-S004"),
                 line("I2", "L2", "H1-S100")]
        for kind, columns, rows in [
            ("invoices", INVOICE_COLUMNS, headers),
            ("line_items", LINE_COLUMNS, lines),
        ]:
            path = snapshot / "invoices" / f"hospital_1_{kind}.csv"
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=columns)
                writer.writeheader()
                writer.writerows(rows)
        data = load_hospital(snapshot, "H1")
        result = audit(data, contract, maps)
        assign_confidence(result, policy)
        validation = validate_result(result, data, policy)
        opinion = next((o for o in result["opinions"]
                        if o["invoice_id"] == "I1"), None)
        print(json.dumps({"malformed_header": malformed,
                          "I1_opinion": opinion,
                          "validation": validation}, indent=2))
```

Observed: the valid-conflict case has no I1 opinion; the malformed-header case emits I1 at zero cents and 0.65 confidence, and validation succeeds. Expected after correction: both cases retain unresolved ownership and withhold I1. This fixture is audit evidence and was not added to the implementation's 61-test suite.

### Verified claims

- The source snapshot, attachment/checkpoint correspondence and current checkpoint recovery hashes agree.
- Both test executions pass all 61 tests; clean replay and verification work with documented Python and no third-party core dependencies.
- Submission, metrics, workload, evaluation Markdown and release manifest reproduce byte-for-byte.
- All 486 service definitions' numeric/unit records and applicable table/prose price facts reconcile, including H3 amendments/additions and H5 multipliers.
- All 2,330 mapping keys are accounted for; accepted records satisfy the disclosed token/evidence policy.
- Current emitted arithmetic, source-line membership, billed totals, submission schema/types and all target counts reconcile.
- H1's 250/250 conditional flag-and-amount result, 27.38% coverage and 8.62% error recall are correct.
- Guarded pricing/export uses no label input, guarded replay attempts no network access, and five full permutation/baseline comparisons pass.
- H2 withholding and the report's low-coverage/unknown-target-accuracy qualifications are supported. H5 projection is explicit and confidence-capped.

### Findings requiring correction

1. **AUD-01 — Major:** quarantined invoice-header ownership can silently create a definite exclusion and an unsupported complete opinion. Correct the uncertainty propagation and demonstrate the supplied counterexample remains withheld through result validation.
2. **AUD-02 — Moderate:** actual bundle stages cite standalone-rate evidence. Bind the applied bundle clause in the trace and verify the affected substitutions.

Reflect both findings in affected task/quality-gate/report completion statements. No separate defect is inferred merely from low coverage, H2 omission, the use of author review, target uncertainty, absent production infrastructure or later publishing tasks.

### Unverified claims

- Actual H2–H5 prediction accuracy and numerical target confidence calibration; the necessary labels do not exist in the supplied evidence.
- Actual line-level H5 facility facts and H2 submission/exception facts; the current data do not establish them.
- A complete, independently observed history of original Work-session label access, prompt application or visual inspection. Retained records support the disclosed process but cannot prove every historical action.
- Bit-identical fresh LLM acquisition, optional rendering installation on a new machine, other operating systems and large-volume operational performance. These are not claimed as core replay guarantees.
- Exact reenactment of older checkpoint restorations and historical resource timings. The delivered checkpoint and current timings were independently checked instead.

These limits are distinct from the two demonstrated defects. Their absence does not create a requirement to redesign the solution.

### Final audit verdict

**PASS WITH CORRECTIONS — implementation is fundamentally sound but identified issues should be corrected before publishing.**

The present technical candidate is reproducible, source-grounded and candid about its narrow measured coverage. No wrong current submitted amount was demonstrated. However, the broad fail-closed claim and complete clause-trace claim are not fully supported. Correct AUD-01 and AUD-02, verify their focused regressions and affected release evidence, and qualify completion claims before publishing. This verdict does not authorize fixes, external publication or delivery; none was performed during this audit.
