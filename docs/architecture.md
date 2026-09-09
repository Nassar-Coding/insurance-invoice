# Implementation boundary

Selected solution: **LLM contract-to-schema with deterministic pricing**.

The Work-session model interprets supplied Markdown and description inventories into finite declarative records. It retains visible instructions, raw candidate data, source references, review changes and accepted artifacts. Table transcription can use deterministic parsing as an acquisition aid; semantics and mappings still require explicit source review. No claim is made that structural validation proves semantic completeness or that the schema covers every possible contract.

The runnable Python 3.12.13 project consumes frozen reviewed records and mappings. It loads CSV evidence without silently repairing billing faults, resolves contract versions, builds all relevant retrospective context, executes a fixed finite set of pricing/check operations with exact arithmetic, and emits supported complete opinions or explicit abstentions. No arbitrary generated contract code or expression evaluation is allowed. Confidence attaches to the complete opinion, not the alias score.

Only H1 labels are available. Audit execution cannot load labels; a separate evaluation command uses fixed patient/identity groups. Legitimate unlabelled history remains available across groups, so group separation does not imply fully independent contract/history observations.

Reproduction uses committed input snapshots, reviewed JSON, mappings, policy and code. It does not require Work, a live model call, API credentials, embeddings, GPU, database, Colab or a cloud service. Changes in decision inputs invalidate affected evidence. A pinned historical contract is not stale simply because the current date is later; input revisions identify a new audit run and recompute history.

This is a synthetic-data batch prototype. Independent audit, corrections and independent closure re-audit have completed. Current preparation preserves the audited implementation; actual publication and delivery remain user-controlled later actions. See publishing_preparation.md.
