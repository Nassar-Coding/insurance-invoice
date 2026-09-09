# AI assistance

AI assistance was used to interpret all five contracts, propose and review service mappings, design the finite schema and interpreter, write code and tests, investigate failures, evaluate results, and prepare documentation. Deterministic table and description processing assisted acquisition. Contract and mapping review during acquisition was part of implementation; it was not an independent review.

The technical prompts and their versions are indexed in [prompts/README.md](../prompts/README.md). Raw candidates, source references, review records, accepted schemas and mapping revisions are retained. H1 development exposed a mapping error that led to the general revision in D007. The check partition was opened after mapping revision and confidence freeze; subsequent evaluation of it is regression evidence. No target labels were available or acquired.

The executable pipeline consumes the saved, reviewed JSON. It makes no programmatic LLM or embedding calls and requires no API credentials. Fresh LLM acquisition is separate from deterministic reproduction and is not guaranteed to recreate identical schemas. An exact API model identifier and token usage were not recorded.

Independent technical audit reports and their execution evidence are preserved unchanged under [governance/audits/](../governance/audits/README.md). Their findings and the resulting corrections are summarized in [implementation_report.md](../reports/implementation_report.md).
