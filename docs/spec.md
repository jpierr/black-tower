# Access Review Helper v0 — Spec

## Goal
Given a list of user access/roles, flag common issues and produce a simple report.

## Input (v0)
CSV (or JSON) with fields like:
- user
- role
- last_login
- status (active/disabled)
- department (optional)

Example CSV header:
user,role,last_login,status,department

## Rules (v0)
Flag:
- Admin/privileged roles (role contains: admin, owner, root, superuser)
- Stale access (last_login > 90 days or blank)
- Disabled accounts with privileged roles
- Duplicate users / duplicate role entries

## Output (v0)
A text report + summary counts.

## Report sections
1) Summary counts
2) Privileged users list
3) Stale access list
4) Disabled-but-privileged list
5) Duplicates list

## Success criteria
- Anyone can understand input/output in 60 seconds.
- Report format is stable (even if logic evolves).
