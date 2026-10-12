# Data contract
All bundled records are synthetic. Source CSV files contain identities, entitlements, and access assignments. IDs must be unique per entity; entitlement references must resolve. Orphan identity references are deliberately allowed for detection. Booleans are true/false; last_login_days is an integer. Owners M0–M4 are simulated reviewers, not authenticated human accounts.
Live exports belong in ignored data/live/. Minimize fields and remove personal data before use. The CSV collector reads the same schema; it does not connect to Active Directory or SaaS services.
