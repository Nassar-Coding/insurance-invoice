# Coverage and limitations

All five source contracts and every observed description key were examined. A complete opinion requires supported service identity, applicable contract rules, relevant context and a uniquely supported corrected total. A detected fault alone does not establish that total. Missing necessary facts cause omission; rows from omitted invoices still contribute known or possible context.

| Hospital | Unique IDs | Complete opinions | Withheld |
|---|---:|---:|---:|
| H1 | 913 | 250 | 663 |
| H2 | 1,125 | 0 | 1,125 |
| H3 | 932 | 148 | 784 |
| H4 | 835 | 64 | 771 |
| H5 | 1,050 | 128 | 922 |

All 4,855 unique invoice identities receive an internal disposition. Target coverage is 340/3,942. No target labels or accuracy estimates exist. H1 is the labelled development hospital; its exposed check partition provides regression evidence only.

H2's 76-service package supports diagnostic execution. Actual submission dates, detailed episode/leave facts and possible written exceptions are missing under Articles II/XIII, and timestamps cannot establish its 07:00 Service Day. Admission/discharge dates are present. No complete H2 payable opinion is emitted.

Unresolved mappings, compound quantity dimensions, conflicting identities, context uncertainty and nonunique correction allocations remain explicit omissions. H3/H5 exclusion direction and boundaries, H3 settlement chronology, H4 patient scope and H5 invoice-facility projection retain the qualifications in the [decision log](../reports/decision_log.md).

The repository includes runnable code and pinned dependencies, `submission.csv`, H1 evaluation and failure analysis, versioned technical prompts, a one-page decision log and a two-page write-up. [Reproduction instructions](../README.md) regenerate the predictions from saved reviewed artifacts.
