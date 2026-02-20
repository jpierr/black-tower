#!/usr/bin/env python3
import csv
import sys
import argparse
from datetime import datetime, timedelta
import os
import json

VERSION = "0.1.0"

# Exit codes:
# 0 = clean run
# 1 = input/validation error
# 2 = disabled privileged accounts detected
# 3 = strict mode failure (any findings detected)



PRIV_KEYWORDS = ("admin", "owner", "root", "superuser")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Access Review Helper - Audit privileged and stale access"
    )

    # Accept either positional input_file OR --input for convenience.
    # If both are provided, --input wins.
    parser.add_argument(
        "input_file",
        nargs="?",
        default=None,
        help="Path to CSV access list (positional)",
    )
    parser.add_argument(
        "--input",
        dest="input_file_flag",
        default=None,
        help="Path to CSV access list (same as positional)",
    )

    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Stale threshold in days (default: 90)",
    )

    parser.add_argument(
        "--output",
        default="docs/access_review_report.txt",
        help="Output report file path",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (text or json). Default: text",
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any findings are detected",
    )

    args = parser.parse_args()

    # Resolve final input path
    final_input = args.input_file_flag or args.input_file
    if not final_input:
        parser.error("missing input file. Provide a CSV path or use --input <path>.")

    # Normalize to a single attribute so the rest of the script stays simple
    args.input_file = final_input
    return args


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
    args = parse_args()
    path = args.input_file
    output_path = args.output

    # Basic file validation
    if not os.path.exists(path):
        print(f"Error: File '{path}' not found.")
        sys.exit(1)

    rows = []
    seen_users = set()
    duplicate_users = set()

    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            required = {"user", "role", "last_login", "status"}
            headers = set(h.strip() for h in (reader.fieldnames or []))

            if not headers:
                print("Error: CSV appears empty or missing header row.")
                sys.exit(1)

            missing = required - headers
            if missing:
                print(f"Error: CSV missing required columns: {', '.join(sorted(missing))}")
                sys.exit(1)

            for row in reader:
                user = (row.get("user") or "").strip()
                if user in seen_users:
                    duplicate_users.add(user)
                seen_users.add(user)
                rows.append(row)
            if not rows:
                print("Error: CSV has no data rows.")
                sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    today = datetime.today()
    stale_cutoff = today - timedelta(days=args.days)

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
    report_lines.append(f"- Stale access (missing or >{args.days}d): {len(stale)}")
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

    if args.format == "json":
        json_output = {
            "summary": {
                "total_users": len(rows),
                "privileged": len(privileged),
                "stale": len(stale),
                "disabled_privileged": len(disabled_privileged),
                "duplicates": len(duplicate_users),
            },
            "privileged_users": privileged,
            "stale_users": stale,
            "disabled_privileged_users": disabled_privileged,
            "duplicates": sorted(list(duplicate_users)),
        }
        print(json.dumps(json_output, indent=2))
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(json_output, out, indent=2)
    else:
        output = "\n".join(report_lines).strip() + "\n"
        print(output)
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(output)

    # Exit behavior
    # 2 = disabled users retain privileged access
    # 3 = strict mode failure (any findings detected)
    exit_code = 0

    if len(disabled_privileged) > 0:
        exit_code = 2

    if args.strict:
        if privileged or stale or disabled_privileged or duplicate_users:
            exit_code = 3

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
