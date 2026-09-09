# Snapshot and revision contract

The pipeline audits exactly the supplied pinned CSV snapshot. It does not know whether records outside that package exist. A row omitted from submission still contributes known or possible context to related rows; quarantined dates or uncertain service identity are not zero utilisation.

Changing a prior invoice/line, its identity, quantity, date, mapping, or governing rule changes decision-input identity. Rerun the whole relevant hospital snapshot with `audit`, or all five with `reproduce`. Old successful attempts retain their own identity; `current_run`/`verify-submission` reject their use as current evidence after changed inputs. Contract-source or semantics changes additionally require a new source review and accepted bundle; changing only invoice bytes does not automatically require re-extracting an unchanged contract.

`test_later_revision_of_prior_claim_changes_subsequent_price` changes a prior H1 quantity from 60 to 61 and verifies that the next rate changes from 25,250 to 22,220 cents under the source's strict threshold. `test_malformed_date_preserves_possible_dependency` proves that an unresolved prior date can block an outcome rather than vanish. Repetition and full-snapshot permutation checks verify deterministic retrospective context.

This is batch revision handling, not a streaming freshness or completeness guarantee. No availability SLA or production feed is part of the exercise.

AUD-01 adds raw-header ownership regressions in `tests/test_audit_corrections.py`. Changing only a conflicting header's valid date to an impossible date must not make a dependent exclusion certain. Tests cover missing patient identity, only-quarantined headers, unrelated known patients, daily/bundle/duplicate context, H4 patient-scope bounds and invariant all-patient prior usage. A malformed header is not a deletion from the source snapshot. Current supplied-data and shuffled-snapshot comparisons are recorded in `reports/corrections/audit_1/correction_verification.json` and `reports/final_regression.json`.
