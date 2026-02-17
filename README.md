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
