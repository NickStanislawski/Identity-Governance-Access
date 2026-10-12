# Implementation

Canonical source: scripts/governance.py. fixture() generates the deterministic synthetic model. collect() reads three CSVs and normalizes booleans and login age. validate() rejects duplicate entity IDs and unknown entitlements, while orphan identities intentionally remain detectable.

detect() emits one finding per risk per assignment. campaign() routes to entitlement owners and simulates certification decisions: revoke orphan, inactive, SoD, or excessive access; exception for stale-only access; otherwise approve. Exceptions carry an expiry. remediate() requires full campaign coverage, valid decision values, matching owners, rationale, timestamps, and exception expiry before producing an after snapshot. It never modifies a real source.

drift() compares stable assignment IDs for grants, removals, and changed identity/entitlement pairs. Changed access is recorded without claiming every change is an elevation. Privileged assignments get a dedicated review export. run() writes immutable-by-convention run directories, a summary, Markdown report, and SHA-256 manifest. Hashes detect accidental changes but are not signed or tamper-proof audit storage.

CSV collection, rule detection, scoring, routing, reporting, and simulated remediation are executable. Human decision entry, authentication, scheduling, and external write connectors are extensions.
