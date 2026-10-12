# Security controls

Policy: Ledger requester and approver access for the same identity conflicts. Both conflicting assignments receive findings and are revoked by the demo policy; production should retain the explicitly approved role after a human review. Administrative access outside IT is excessive under this lab's policy. Stale means last login age >=90 days; inactive and unknown identities are separate findings.

Scores: SoD 95, orphan 90, excessive 85, inactive 80, privileged 70, stale 50. Scores are transparent fixed priorities, not a predictive risk model. Owner routing follows entitlement ownership. Expiry is required for exceptions but automatic expiry enforcement is not implemented.

Synthetic data avoids exposing people or credentials. review/ and live exports are excluded from Git. Reviewer names are validated against owner mappings but are not authenticated; never use this mechanism as production authorization. The source CSVs remain untouched. Remediation is verified from the persisted after export. Production needs authenticated approvals, least-privilege connectors, signed/append-only audit storage, retries, rollback, and human authorization for revocation.
