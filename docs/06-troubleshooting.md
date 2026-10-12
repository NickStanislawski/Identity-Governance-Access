# Troubleshooting

Symptom: Python command opens the store or cannot run. Cause: an unavailable Windows app alias. Resolution: use a working Python installation's absolute executable path. Observed during this build; resolved with the bundled runtime.

Symptom: test temporary directory permission failure. Cause: restricted system temp directory. Resolution: create the test temporary directory inside tests. Observed during the initial run; the final test uses this location.

Symptom: output directory already exists. Cause: evidence overwrite guard. Resolution: choose a new run ID; preserve original evidence. Symptom: unknown entitlement or duplicate ID. Cause: malformed CSV. Correct the source and rerun into a new directory. Symptom: incomplete campaign or unauthorized reviewer. Correct campaign coverage and owner mappings; do not bypass validation.

Recovery: the engine does not change CSV input or external accounts, so restore by running unchanged source into a fresh directory. If interrupted, keep the partial directory as failed evidence and choose another directory. Live integration recovery has not been implemented or tested.
