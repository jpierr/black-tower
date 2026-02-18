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
- Stale access (>90 days or missing login)
- Disabled but still privileged accounts
- Duplicate user records

---

## Quickstart

From the project root directory:

```bash
python3 access_review_helper.py docs/sample_access_list.csv
```

### Output
- Prints a structured report to the terminal
- Writes `docs/access_review_report.txt`

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