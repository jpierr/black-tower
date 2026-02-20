# Black Tower (v0)

Operator-grade proof projects focused on automation, reliability, and security-minded workflows.

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

## Quickstart

From the project root directory:

```bash
# default text output
python3 access_review_helper.py docs/sample_access_list.csv

# configurable stale threshold
python3 access_review_helper.py docs/sample_access_list.csv --days 45

# JSON output to terminal
python3 access_review_helper.py docs/sample_access_list.csv --format json

# JSON output to file
python3 access_review_helper.py docs/sample_access_list.csv --format json --output docs/report.json
```

### Output
- Prints a structured report to the terminal
- Writes `docs/access_review_report.txt`

### Exit Codes

- `0` → No critical findings
- `1` → Input / validation error
- `2` → Disabled but privileged accounts detected

Exit codes allow integration with automation pipelines and CI workflows.

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