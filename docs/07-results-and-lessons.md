# Results and lessons

60 identities; 5 departments; 5 applications; 25 entitlements; 64 assignments reviewed; 58 approvals; 5 revocations; 1 exception; 7 findings. All 5 revoked assignments are absent from the persisted after snapshot.

The custom lab demonstrates the V1 certification lifecycle and V2 CSV collection, detection, drift, scoring, reporting, and privileged review. Minimum quantitative dataset targets passed. Evidence is linked in the README. Synthetic revocations were executed; real permissions were not changed. Tests prove local behavior only.

Lessons: separate requirements from measured counts; detect orphan references instead of rejecting them prematurely; use fresh run directories; validate owner mappings before remediation; isolate temporary test files in writable paths.

Remaining: actual Project 1 exports, human approval UI/authentication, commercial IGA platform setup, live connector reads/writes, exception expiry enforcement, automated schedules, signed audit storage, expanded input schema validation, and public GitHub publication/history review. Overall enterprise deployment and publication are not marked complete.
