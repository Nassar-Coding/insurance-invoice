# AI assistance

Implementation is assisted by the model in this ChatGPT Work session. It reads source contracts, designs the finite schema/interpreter, proposes and reviews mappings, writes code/tests, executes commands and interprets test/evaluation results. This is visible session-assisted acquisition, not a separately called model API or an independent human review.

The project retains the governing user instruction summary, extraction/review/mapping instructions actually used, raw acquisition candidates and review changes. No hidden chain-of-thought or invented API transcript is claimed. Deterministic table/description processing is explicitly identified as an acquisition aid where used. Accepted artifacts are retained so a clone can reproduce execution without this session.

Current model endpoint/version is not independently verifiable from executable runtime. Do not infer a proprietary API model ID from the UI name ASTRA. Actual model assistance is disclosed without inventing an endpoint or token bill.

The complete scope of assistance includes all five contract interpretations, mapping proposals and source review, Python implementation, source-derived tests, execution/evaluation, failure investigation, regression and documentation. H1 development prompted the general mapping revision recorded as D007; check results were opened only after that revision and confidence freeze. Subsequent use of that check is explicitly regression after exposure. No target labels were available or acquired.

`prompts/README.md` relates retained instructions to acquisition manifests, raw outputs, revisions and accepted packages. Acquisition review statements mean the authoring assistant's source review, not a second independent model or human. The user subsequently supplied the first independent implementation audit (PASS WITH CORRECTIONS); its unchanged report is retained in `governance/audits/independent_implementation_1/`. This assistant inspected and corrected its two findings and performed author regression verification. It did not act as the independent closure re-auditor. The correction instruction summary is versioned in `prompts/audit_correction_user_v1.md`. Code/prompt/version history and actual execution artifacts provide reproducibility without reproducing proprietary Work-session behavior.


## Publication preparation assistance

The user supplied the completed independent closure re-audit. Its unchanged verdict and evidence are retained separately from author checks. The Work assistant prepared documentation and packaging, used two bounded read-only agents to review file dependencies and documentation completeness, and executed final reproduction. Those agents did not perform a new independent technical audit or modify the implementation. New publishing instructions are recorded under `docs/publishing_instructions_v1.md`, outside the release-bound prompt directory. No programmatic LLM/API call is added.
