# Utilities

Current execution uses `python -m insurance_audit reproduce`, `verify-submission` and `tools/run_checks.py local`. The additional clean-clone checker is `publishing/check_reproduction.py`; current PDF rendering uses `publishing/render_delivery_documents.py`.

`reproduce_with_evidence.py` verifies that prediction/export cannot read labels and that replay makes no network calls. `inspect_bundle_traces.py` checks bundle source and partner evidence.

The acquisition, mapping revision, review recording, acceptance and confidence-freeze scripts preserve how the saved artifacts were produced. They are historical acquisition utilities, not steps in ordinary replay. Their descriptive strings reflect the original acquisition records. Running them may replace reviewed artifacts and would require a new technical review; do not run them just to reproduce the submission.

`verify_current_evidence.py`, `verify_audit_corrections.py` and `check_clean_reproduction.py` retain historical regression checks whose original attempt paths are in the [history archive](../evidence/history/README.md). Use a separate restored historical checkout for those comparisons. The current 75-test suite and clean-clone checker require no history restoration.
