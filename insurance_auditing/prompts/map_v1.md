# Service mapping instruction v1

Use hospital-specific contract names and observed free-text descriptions. Preserve raw text and meaningful qualifiers. Propose transparent word/abbreviation correspondences from the supplied data. Normalization/candidate generation may assist review, but a similarity score or opaque billing suffix is not truth.

Review the complete candidate set for each accepted normalized description. An omitted modifier, ambiguous abbreviation or collision must not be forced to one service using a billed price or unit that may itself be wrong. Keep all plausible services for unresolved descriptions so relevant daily/history/bundle/exclusion uncertainty can propagate. Retain reviewed mappings as fixed JSON for replay; no runtime LLM/embedding call. Do not use H1 expected totals or labels to assign aliases.
