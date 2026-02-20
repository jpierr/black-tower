# Black Tower (v0)

![tests](https://github.com/jpierr/black-tower/actions/workflows/tests.yml/badge.svg)

Operator-grade proof projects focused on automation, reliability, and security-minded workflows.

---

## Requirements
- Python 3.9+

## Input format
### CSV
Required columns:
- `user`
- `role`
- `last_login` (YYYY-MM-DD or blank)
- `status` (e.g., `active`, `disabled`)

### JSON
A JSON file containing a list of objects with the same required keys as CSV.
(Extra keys are allowed.)

---

## Mission
Black Tower simulates real-world IT and security workflows to demonstrate:
- Systems thinking
- Practical automation
- Security awareness
- Documentation discipline
- Production-style execution

---

## Deliverable #1 — Access Review Helper

A lightweight CLI tool that simulates an internal access review process.

### Real-World Context
Commonly required for:
- SOC 2 audits
- ISO 27001 compliance
- Privileged access reviews
- Internal governance controls

### Detection Capabilities
- Privileged role detection (Admin / Owner / Root)
- Stale access (configurable threshold via `--days`, default 90)
- Disabled but still privileged accounts
- Duplicate user records

---

## Behavior Contracts

- **Stale definition:** `last_login` is stale if it is missing/blank **OR** `last_login < (today - days)`.
- **Boundary rule:** If `last_login == (today - days)`, it is **not** stale.

---

## Quickstart

From the project root directory:

```bash
# install as a local CLI (editable)
python3 -m pip install -e .

# run via installed command
black-tower docs/sample_access_list.csv
```

Or run the script directly:
```bash
# default text output
black-tower docs/sample_access_list.csv

# configurable stale threshold
black-tower docs/sample_access_list.csv --days 45

# JSON output to terminal
black-tower docs/sample_access_list.csv --format json

# JSON output to file
black-tower docs/sample_access_list.csv --format json --output docs/report.json

# strict mode (fail if ANY findings are detected)
black-tower docs/sample_access_list.csv --strict
echo $?
```

### Output
- Prints a structured report to the terminal
- Writes `docs/access_review_report.txt` (default)

### Exit Codes

- `0` → No critical findings
- `1` → Input / validation error
- `2` → Disabled but privileged accounts detected
- `3` → `--strict` enabled and any findings detected (privileged/stale/disabled/duplicates)

Exit codes allow integration with automation pipelines and CI workflows.

---

## Tests + CI

Run the test suite locally:

```bash
pytest -q
```

Note: core logic is exposed via `analyze_access(rows, days=90, today=None)` and tests inject a fixed `today` for deterministic stale-access behavior.

CI:
- GitHub Actions runs `pytest` on every push and pull request.
---

## Project Structure

```
black-tower/
├── access_review_helper.py
├── docs/
│   ├── sample_access_list.csv
│   ├── sample_report.txt
│   ├── access_review_report.txt
│   └── spec.md
├── tests/
│   ├── fixtures/
│   │   └── clean.csv
│   └── test_access_review_helper.py
├── .github/
│   └── workflows/
│       └── tests.yml
└── README.md
```

---

## Current Sprint
- CLI argument improvements
- JSON input support
- Enhanced reporting format
- Basic error handling

---

## Roadmap
- Access Review Helper (v1 CLI upgrade)
- Audit Evidence Collector
- Incident Postmortem Generator

---

Built as operator-grade proof of execution.