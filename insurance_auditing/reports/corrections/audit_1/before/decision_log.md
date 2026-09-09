# Insurance auditing - decision log
Implementation candidate | Source commit 6fee1da60b74512156637a22be15d996a36627e1

## Evidence and execution boundary
The Work-session assistant extracted and source-reviewed finite JSON rules and frozen service mappings. This was author review, not independent validation. Python replays saved records without an LLM/API. Accepted bundles bind source, schema, mapping and review identities. Unknown operators and incompatible packages fail before pricing.

## Service identity and incomplete opinions
Contract catalogs are not proof that an incomplete description identifies their only similar service. H1 development exposed one wrong specialty assignment (INV-H1-000236, 43,650 cents); all 39 analogous mapping keys were withdrawn. Essential qualifiers need independent description evidence; only generic noun elision retains a lower evidence grade. Billed rates/units never select service identity. If any necessary fact is unresolved, withhold the complete row; a known error alone does not establish the corrected total.

## Quantities, history and allocation
Use supplied billed quantities under the contracts' pricing rules; a wrong unit label does not authorize a guessed conversion. Composite hour/item quantities lack a second dimension and remain unsupported. Prior usage is strictly ordered by service date and line ID, over the supplied term; all relevant omitted/quarantined records remain possible context. Conflicting invoice ownership and duplicate service/day allocation have no invented split. A supported single capped line can be limited to the contractual maximum. Round integer cents half-up after each adjustment.

## Exclusions and amendments
H1/H2/H4 explicitly support bidirectional exclusions; H3/H5 direction is unresolved at nonzero distances. Use same-patient scope as the recorded contextual reading and withhold exactly-N-day boundary cases. H3 A1.1 applies seven repricings and two additions from service date 2025-01-01 despite the broad amendment header. A1.4.2 settlement protection uses the explicit interpretation that a valid invoice cannot settle before issue/service; no settlement field is fabricated.

## Hospital-specific missing facts
H4 section 1.4 defines instance as unit, but section 8 leaves patient aggregation unclear: bound same-patient through all-patient usage and emit only invariant outcomes. H5 line facility is absent; adopt invoice facility from the supplied relational shape and section 10.1, as an explicit assumption. Outcome-relevant opinions are capped at .65 confidence. H2 Articles II/XIII need actual submission, episode/leave and possible waiver facts; invoice date is not submission. All H2 full opinions are withheld. Its 07:00 Service Day is not established by calendar dates; day-dependent diagnostics remain bounded or uncertain.

## Confidence, evaluation and remaining work
H1 patient groups were fixed before label development; the reserved check is now exposed and later checks are regressions. H1 sparse-error and target confidence are policy judgments, not demonstrated target calibration. Missing necessary facts cannot be repaired by a low score. Final mappings/rules, error history and omissions are retained. See evaluation_report.md and docs/implementation_changes.md. Independent challenge, external publishing, access and email delivery are later stages.
