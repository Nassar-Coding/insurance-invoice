# Gate 1 measurement rebuild instructions

The user requested a lean recovery after the unpublished checkpoint was lost: restore the scorer with development 4/38/0 cost190 and full 5/53/0 cost265; add --trace, H1-development/H2–H5 reason histograms and the 38-miss family cross-tab; register the baseline with the recorded description-perturbation result 4→1 and zero new FP. Do not rerun generalization or clean-checkout verification. Preserve submission bytes. Publish after each numbered step, skip tags, then stop before Gate 2.

Assistant contribution: standard-library observation/scoring tools, synthetic tests, reports and documentation. Existing deterministic audit code, extracted rules, reviewed mappings and confidence policy are unchanged. No new model/API inference was introduced. Generalization values are explicitly carried-forward prior observations; no reconstructed log is represented as fresh evidence.
