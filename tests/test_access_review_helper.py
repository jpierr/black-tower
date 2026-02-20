import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
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
