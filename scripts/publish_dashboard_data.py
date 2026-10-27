"""Refresh dashboard_data.json and push it to GitHub if it changed."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refresh_dashboard_data as rd

NOWIN = 0x08000000 if os.name == "nt" else 0  # no flashing console windows

def git(*a, check=True):
    return subprocess.run(["git", *a], cwd=rd.ROOT, capture_output=True, text=True,
                          creationflags=NOWIN, check=check).stdout.rstrip()

def main():
    rd.main()
    dirty = [l[3:].strip() for l in git("status", "--porcelain").splitlines()]
    if not dirty:
        return
    if dirty != ["dashboard_data.json"]:
        sys.exit("Other uncommitted files present, not publishing: " + ", ".join(dirty))
    git("add", "dashboard_data.json")
    git("commit", "-m", "Update dashboard data")
    git("pull", "--rebase", "--autostash", check=False)
    git("push")
    print("Published.")

if __name__ == "__main__":
    main()
