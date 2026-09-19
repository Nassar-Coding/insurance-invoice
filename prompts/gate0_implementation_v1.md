# Gate 0 implementation instruction

Implement only Gate 0 of `docs/Revised_Plan_Rank29_to_Top3.md` in the insurance-invoice repository. The revised plan governs gate ordering and exits; contracts and challenge data govern factual behavior. The corrections memo is background, and the external leaderboard identifies the current candidate as rank 29.

Make replay survive different Python 3.12 patch versions and unseen invoice inputs. Remove exact-patch and historical fingerprint execution locks; keep hashes as provenance. Remove invoice-ID lists from prediction dependencies. Optional H1 evaluation must skip missing inputs and must not fail successful prediction. Never inspect check labels or evaluate check/full before the Final Gate.

Build a label-free generalization harness for all five hospitals: re-ID invoices, sample 70% of patients with whole histories, shuffle rows, and perturb 30% of descriptions with the specified case, whitespace, abbreviation, separator and non-code typo changes. Balance service-code retention/removal. Run the unchanged pipeline and validate outputs.

Verify clean clones under two distinct Python 3.12 patch versions and compare exact submission bytes. Retain finite-schema, monetary, source-row and completeness validation. Do not implement new structural detections, matching, pricing or confidence policies at this gate. Continue debugging until Gate 0 passes or an external blocker remains. Record every exit, development cost, clean false positives, decoy-proxy availability, target flag rates and discrepancies in `evaluation/gate_reports.md`. Commit and tag Gate 0, then stop.

This prompt records the actual user scope applied during Gate 0. AI assistance produced implementation and regression checks; prediction replay makes no model call.
