# Black Tower (v0)

Status: Deliverable #1 spec + sample output shipped (docs)

Operator-grade proof projects: automation + reliability + security-minded workflows.

## What this demonstrates
- systems thinking
- automation mindset
- documentation and repeatability
- operator workflows (access reviews, evidence collection, incident templates)

## Current sprint
- Ship 1 demo-ready tool this week
- Document it so anyone can run it

## Quickstart (v0)
## Why this matters (real-world use)

This tool simulates an internal access review process commonly required for:
- SOC 2 audits
- ISO 27001 controls
- Quarterly privileged access reviews
- Internal security governance

It demonstrates:
- Privilege detection
- Stale access identification
- Duplicate account detection
- Disabled account risk

Designed as a lightweight operator utility.
```bash
python access_review_helper.py docs/sample_access_list.csv
```
Output:
- prints a report to the terminal
- writes `access_review_report.txt`

## Roadmap (v0)
- Access Review Helper
- Audit Evidence Collector
- Incident Postmortem Generator

## Deliverable #1: Access Review Helper v0 
**Input:** access list (CSV/JSON)  
**Output:** report that flags privileged roles, stale access, disabled-but-privileged, and duplicates.

Docs:
- Spec: docs/spec.md
- Sample output: docs/sample_report.txt

# Black Tower (v0)

Status: Deliverable #1 shipped — Access Review Helper (demo-ready)

Operator-grade proof projects focused on automation, reliability, and security-minded workflows.

---

## Mission
Black Tower is a portfolio of operator-focused tools that simulate real-world IT and security workflows.

The goal is to demonstrate:
- Systems thinking
- Practical automation
- Security awareness
- Clear documentation and repeatability
- Production-style workflow discipline

---

## Deliverable #1 — Access Review Helper

A lightweight CLI tool that simulates an internal access review process.

### Real-World Use Case
This type of review is commonly required for:
- SOC 2 audits
- ISO 27001 compliance
- Quarterly privileged access reviews
- Internal governance and risk management

### What It Detects
- Privileged roles (Admin, Owner, Root)
- Stale access (>90 days or missing login)
- Disabled but still privileged accounts
- Duplicate user records

---

## Quickstart

From the project root directory:

```bash
python3 docs/access_review_helper.py docs/sample_access_list.csv
```

### Output
- Prints a structured report to the terminal
- Writes `docs/access_review_report.txt`

---

## Project Structure

```
black-tower/
├── docs/
│   ├── access_review_helper.py
│   ├── sample_access_list.csv
│   ├── sample_report.txt
│   ├── access_review_report.txt
│   └── spec.md
└── README.md
```

---

## Current Sprint
- Improve CLI usability (argument handling / flags)
- Add JSON input support
- Improve reporting format
- Add basic error handling

---

## Roadmap
- Access Review Helper (v1 CLI upgrade)
- Audit Evidence Collector
- Incident Postmortem Generator

---

Built as operator-grade proof of execution.