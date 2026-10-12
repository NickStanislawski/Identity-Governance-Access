# Environment setup

Prerequisites: Python 3.10 or later and a writable local directory. No packages are required. Extract the project folder before running; do not run directly inside a ZIP. Commands below are relative to the extracted repository root.

```powershell
python --version
python -m unittest discover -s tests -v
python scripts/governance.py --source data/source --out data/evidence/my-run-001
```

Use a new output directory for each run. The script refuses to overwrite existing evidence. To use an installed Python executable with spaces, invoke it with PowerShell's call operator and a quoted absolute path. The bundled Codex Python runtime was used for the recorded validation; tests/results.txt records the execution output. No SaaS setup is represented as completed.
