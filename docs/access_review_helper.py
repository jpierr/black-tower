#!/usr/bin/env python3
import csv
import sys
from datetime import datetime, timedelta

PRIV_KEYWORDS = ("admin", "owner", "root", "superuser")


def parse_date(date_str: str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        return None


def is_privileged(role: str) -> bool:
    r = (role or "").lower()
    return any(k in r for k in PRIV_KEYWORDS)


def main():
    if len(sys.argv) < 2:
        print("Usage: python access_review_helper.py <input.csv>")
        sys.exit(1)

    path = sys.argv[1]
    rows = []
    seen_users = set()
    duplicate_users = set()

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user = (row.get("user") or "").strip()
            if user in seen_users:
                duplicate_users.add(user)
            seen_users.add(user)
            rows.append(row)

    today = datetime.today()
    stale_cutoff = today - timedelta(days=90)

    privileged = []
    stale = []
    disabled_privileged = []

    for row in rows:
        user = (row.get("user") or "").strip()
        role = (row.get("role") or "").strip()
        last_login_str = (row.get("last_login") or "").strip()
        status = (row.get("status") or "").strip().lower()

        priv = is_privileged(role)
        last_login_dt = parse_date(last_login_str)

        if priv:
            privileged.append(row)

        # stale = missing login OR older than 90 days (if parseable)
        if not last_login_dt or last_login_dt < stale_cutoff:
            stale.append(row)

        if status == "disabled" and priv:
            disabled_privileged.append(row)

    report_lines = []
    report_lines.append("Access Review Helper v0 — Report")
    report_lines.append("")
    report_lines.append("SUMMARY")
    report_lines.append(f"- Total users reviewed: {len(rows)}")
    report_lines.append(f"- Privileged users: {len(privileged)}")
    report_lines.append(f"- Stale access (missing or >90d): {len(stale)}")
    report_lines.append(f"- Disabled but privileged: {len(disabled_privileged)}")
    report_lines.append(f"- Duplicate users detected: {len(duplicate_users)}")
    report_lines.append("")

    def section(title, items):
        report_lines.append(title)
        for r in items:
            report_lines.append(
                f"- {r.get('user','')} | role={r.get('role','')} | last_login={r.get('last_login','')} | status={r.get('status','')}"
            )
        report_lines.append("")

    section("PRIVILEGED USERS", privileged)
    section("STALE ACCESS", stale)
    section("DISABLED BUT PRIVILEGED", disabled_privileged)

    if duplicate_users:
        report_lines.append("DUPLICATES")
        for u in sorted(duplicate_users):
            report_lines.append(f"- {u}")
        report_lines.append("")

    output = "\n".join(report_lines).strip() + "\n"
    print(output)

    # also write report file
    with open("access_review_report.txt", "w", encoding="utf-8") as out:
        out.write(output)


if __name__ == "__main__":
    main()
