# Coverage and limitations

All five source contracts and every observed description key were examined. A complete opinion requires supported service identity, applicable contract rules, relevant context and a uniquely supported corrected total. A detected fault alone does not establish that total. Missing necessary facts cause omission; rows from omitted invoices still contribute known or possible context.

| Hospital | Unique IDs | Complete opinions | Withheld | Flagged |
|---|---:|---:|---:|---:|
| H1 | 913 | 663 | 250 | — (labelled, not submitted) |
| H2 | 1,125 | 674 | 451 | 76 |
| H3 | 932 | 722 | 210 | 69 |
| H4 | 835 | 467 | 368 | 61 |
| H5 | 1,050 | 674 | 376 | 75 |

All 4,855 unique invoice identities receive an internal disposition. Target coverage is **2,537/3,942**, with 281 flags. No target labels or accuracy estimates exist for the scored hospitals. H1 is the labelled development hospital; its check partition was exposed by the earlier implementation and provides regression evidence only.

H2 emitted no complete opinion at all until Gate 2, because a single unresolved fact — a submission date Article XIII conditions effectiveness on, which the data never records — suppressed every other check on the invoice. Article XIII is now logged as unresolved and blocks nothing: evidence that is itself the error is never withheld on account of an unrelated unresolved fact. Its 07:00 Service Day still cannot be observed, since the records carry no times; it is settled instead by how the parties billed (see the [decision log](../reports/decision_log.md)). Detailed episode and leave facts and possible written exceptions under Article II remain missing; admission and discharge dates are present.

Unresolved mappings, compound quantity dimensions, conflicting identities, context uncertainty and nonunique correction allocations remain explicit omissions. H3/H5 exclusion direction and boundaries, H3 settlement chronology, H4 patient scope and H5 invoice-facility projection retain the qualifications in the [decision log](../reports/decision_log.md).

The repository includes runnable code and pinned dependencies, `submission.csv`, Hospital 1 evaluation and failure analysis in [EVALUATION_REPORT.md](../EVALUATION_REPORT.md), every versioned technical prompt under [prompts/](../prompts/README.md), and the one-page [decision log](../reports/decision_log.md). [Reproduction instructions](../README.md) regenerate the predictions from saved reviewed artifacts.
