# Identity Governance, Access Certification & Audit Automation

## 1. Project Overview

A complete runnable synthetic identity governance and audit automation lab. V1 and V2 local workflows are implemented and tested. External integrations and public publication remain pending.

## 2. Objectives

Inventory at least 50 identities across five departments and applications, define 25 entitlements, certify 50+ assignments, detect SoD and risky access, track remediation, and preserve audit evidence.

## 3. Architecture

CSV source → normalized snapshot → risks and owner routing → simulated certification → after snapshot → drift and audit report. See [architecture](docs/01-architecture.md).

## 4. Technologies Used

Python standard library; CSV/JSON/Markdown; SHA-256 manifests. Python 3.10+ required. No licensed platform is needed.

## 5. Key Features

Implemented: collection, six risk types, priority scoring, owner routing, approve/revoke/exception decisions, expiry metadata, synthetic revocation, drift detection, privileged review export, audit reporting. Decisions and reviewers are simulated.

## 6. Implementation Summary

Run `python scripts/governance.py --source data/source --out data/evidence/my-run-001` from the repository root. See [implementation](docs/03-implementation.md).

## 7. Security Considerations

Synthetic data only. No credentials or external changes. Owner validation is a lab control, not authentication. Private material is excluded through .gitignore. See [controls](docs/04-security-controls.md).

## 8. Testing and Validation

14 automated tests executed successfully. See [test log](tests/results.txt), [methodology](docs/05-testing-and-validation.md), and [measured summary](data/evidence/validation-001/summary.json).

## 9. Results

60 identities; 5 departments; 5 applications; 25 entitlements; 64 assignments reviewed; 58 approvals; 5 revocations; 1 exception; 7 findings. All 5 revoked assignments are absent from the persisted after snapshot.

## 10. Challenges and Lessons Learned

Resolved unavailable Python alias and restricted temporary directory. Preserve evidence and validate campaign coverage before remediation. See [troubleshooting](docs/06-troubleshooting.md).

## 11. Project Limitations

No authenticated human approvals, live AD/SaaS integration, automatic exception expiry, production audit immutability, or external access remediation. Assignment IDs must remain stable for drift. No GitHub publication is claimed.

## 12. Future Improvements

Planned: Project 1 adapter, authenticated review UI, external write connectors with rollback, scheduling, expiry enforcement, robust schema validation, and signed audit persistence.

## 13. Documentation and Evidence

Public chapters:
- [Architecture](docs/01-architecture.md)
- [Environment setup](docs/02-environment-setup.md)
- [Implementation](docs/03-implementation.md)
- [Security controls](docs/04-security-controls.md)
- [Testing and validation](docs/05-testing-and-validation.md)
- [Troubleshooting](docs/06-troubleshooting.md)
- [Results and lessons](docs/07-results-and-lessons.md)

[Source](scripts/governance.py) · [Tests](tests/test_governance.py) · [Audit report](data/evidence/validation-001/report.md) · [Data contract](data/README.md).
