# AI assistance

AI assistance was used throughout: to interpret all five contracts, propose and
review service mappings, design the finite schema and interpreter, write code and
tests, investigate failures, evaluate results, and prepare documentation.
Deterministic table and description processing assisted acquisition. Contract and
mapping review during acquisition was part of implementation; it was not an
independent review.

## Which assistant did what

| Phase | Assistant | Work |
|---|---|---|
| Acquisition, Gates 0–1 | **Codex** | Contract extraction and review, service mapping and its v2 revision, the schema and interpreter, the original submission, then the portability/independence invariants and the measurement rebuild. |
| Gates 2–9 | **Claude Code** | The structural and term-window layer, the four-state matcher, contract-rule checks, the pricing engine, confidence tiers, the decoy and distribution audit, the held-out read and freeze, the population-consistency resolution, and this documentation refresh. |
| Throughout | **Research assistance** (conversational) | Diagnosing why the original submission scored as it did, reading the leaderboard and cost metric, and drafting the plan that the gates implement. It wrote no code and touched no artifact in this repository. |

## How the work was run

The original submission placed 29th at a cost of 1395. The organisers granted a
revisit window afterwards, and everything from Gate 2 onward was done inside it.
That work followed one loop, repeated per gate:

1. **Plan.** [docs/Revised_Plan_Rank29_to_Top3.md](Revised_Plan_Rank29_to_Top3.md)
   set out the gates, in order, each with an exit criterion stated as a number.
2. **Gated prompt.** One gate was issued at a time as a single instruction,
   carrying its own exit criteria and standing rules (development only; the check
   partition stays closed; revert anything that adds a false positive on clean
   development or on the frozen decoy proxies; no rule may key off an invoice
   identifier, a record count or an input fingerprint). From Gate 3 the
   instruction was held as a stop condition until every exit criterion had been
   shown. Every gate prompt is published verbatim in
   [prompts/](../prompts/README.md).
3. **Review.** Each gate ended with its numbers printed and a short summary under
   `reports/gate<N>/`, and was not left until they met the bar. The next gate did
   not start until the previous one passed.

Two of the plan's own assertions were contradicted by the source documents during
this work — Hospital 2's volume-discount basis and a group of invoices the plan
predicted would be flagged. In both cases the contract and the data were followed
rather than the plan, and the deviation was reported.

## Evidence and limits

Raw candidates, source references, review records, accepted schemas and mapping
revisions are retained. H1 development exposed a mapping error that led to the
general revision in D007. No target labels were available or acquired.

The H1 check partition was first opened by the earlier implementation, after
mapping revision 2 and the confidence freeze, so it is regression evidence rather
than an untouched holdout. Across the gated rebuild it was read once more, at the
Final Gate, and nothing was changed as a result.

The executable pipeline consumes the saved, reviewed JSON. It makes no
programmatic LLM or embedding calls and requires no API credentials. Fresh LLM
acquisition is separate from deterministic reproduction and is not guaranteed to
recreate identical schemas. An exact API model identifier and token usage were not
recorded.

Two independent technical audits were run against the original implementation,
and their findings were corrected and verified before the gated rebuild began.
What they found and what changed is recorded in
[implementation_changes.md](implementation_changes.md); their own report packages
and execution logs described an implementation that no longer exists, so they
were removed at the Gate 10 cleanup and remain recoverable at the `gate9` tag.
