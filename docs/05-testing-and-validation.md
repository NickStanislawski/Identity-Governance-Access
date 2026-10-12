# Testing and validation

Run `python -m unittest discover -s tests -v`. Fourteen tests cover dataset targets, all six risk categories, stale threshold, clean baseline, duplicate IDs, unknown entitlements, decision coverage, removal verification, unauthorized reviewer, required exception expiry, incomplete campaigns, three drift types, overwrite protection and artifact hashes, and CSV round-trip collection.

Expected: 14 tests pass; the collector reproduces the fixture; each revoked assignment is absent; unchanged clean records have no findings. Observed: see tests/results.txt. The executed CSV-based campaign is in data/evidence/validation-001/. Summary counts were measured during execution. This is automated simulation evidence, not a human certification or SaaS integration test.

Independent verification: compare revoke IDs in decisions.json with assignment IDs in after.json; verify the manifest with hashlib; compare before and after snapshots with drift.json. Inspect reports alongside the raw JSON. Test isolation uses a temporary directory inside tests, removed after execution.
