import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Ensure repo root is on sys.path so `access_review_helper.py` can be imported
# regardless of where pytest is invoked from.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from access_review_helper import analyze_access

SCRIPT = REPO_ROOT / "access_review_helper.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures"


def run_cli(args):
    cmd = [sys.executable, str(SCRIPT)] + args
    return subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)


def test_strict_clean_exits_0(tmp_path):
    clean_csv = FIXTURES / "clean.csv"
    out_file = tmp_path / "out.txt"
    r = run_cli([str(clean_csv), "--strict", "--output", str(out_file)])
    assert r.returncode == 0, r.stdout + r.stderr


def test_strict_sample_exits_3(tmp_path):
    sample_csv = REPO_ROOT / "docs" / "sample_access_list.csv"
    out_file = tmp_path / "out.txt"
    r = run_cli([str(sample_csv), "--strict", "--output", str(out_file)])
    assert r.returncode == 3, r.stdout + r.stderr


def test_bad_path_exits_1():
    r = run_cli(["no_such_file.csv"])
    assert r.returncode == 1
    assert "not found" in (r.stdout + r.stderr).lower()


def test_analyze_access_basic_counts():
    rows = [
        {"user": "a@example.com", "role": "Admin", "last_login": "2099-01-01", "status": "active"},
        {"user": "b@example.com", "role": "User", "last_login": "", "status": "active"},
    ]

    result = analyze_access(rows, 90)

    # Core behavior: 1 privileged (Admin), 1 stale (missing last_login)
    assert len(result.get("privileged_users", [])) == 1
    assert len(result.get("stale_users", [])) == 1


def test_analyze_access_deterministic_today_stale_cutoff():
    # Freeze time so stale logic is deterministic.
    fixed_today = datetime(2026, 2, 1)

    # With days=90, cutoff is 2025-11-03.
    rows = [
        {"user": "fresh@example.com", "role": "User", "last_login": "2025-12-15", "status": "active"},
        {"user": "stale@example.com", "role": "User", "last_login": "2025-10-01", "status": "active"},
        {"user": "missing@example.com", "role": "User", "last_login": "", "status": "active"},
    ]

    result = analyze_access(rows, days=90, today=fixed_today)

    # stale: last_login missing OR older than cutoff
    assert len(result.get("stale_users", [])) == 2


def test_stale_cutoff_boundary_equal_not_stale():
    # Rule: stale if last_login is missing OR last_login < cutoff (strictly older).
    # If last_login == cutoff, it should NOT be considered stale.
    fixed_today = datetime(2026, 2, 1)

    # With days=90, cutoff is 2025-11-03.
    rows = [
        {"user": "equal@example.com", "role": "User", "last_login": "2025-11-03", "status": "active"},
        {"user": "older@example.com", "role": "User", "last_login": "2025-11-02", "status": "active"},
    ]

    result = analyze_access(rows, days=90, today=fixed_today)
    stale_users = {r.get("user") for r in result.get("stale_users", [])}

    assert "equal@example.com" not in stale_users
    assert "older@example.com" in stale_users
