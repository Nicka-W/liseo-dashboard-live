"""Reads the Liseo workbook's 'Production Data' sheet and writes dashboard_data.json."""
import glob, json, os, shutil, sys, tempfile
from datetime import datetime, timezone
import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dashboard_data.json")
PATTERN = "Liseo*Assemblies*Master*Sheet*.xls*"
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def find_workbook(arg=None):
    arg = arg or os.environ.get("LISEO_WORKBOOK")
    if arg and os.path.isfile(arg):
        return arg
    home = os.path.expanduser("~")
    roots = [ROOT, os.path.dirname(ROOT), home + r"\Desktop", home + r"\Documents", home + r"\Downloads"]
    roots += glob.glob(home + r"\OneDrive*")
    hits = []
    for r in roots:
        for depth in ("", "*", os.path.join("*", "*")):
            hits += [h for h in glob.glob(os.path.join(r, depth, PATTERN)) if not os.path.basename(h).startswith("~$")]
    if not hits:
        sys.exit("Workbook not found. Pass its path: python refresh_dashboard_data.py \"C:\\path\\Liseo Assemblies Master Sheet.xlsm\"")
    return max(hits, key=os.path.getmtime)

def build(path):
    tmp = os.path.join(tempfile.mkdtemp(), "snap.xlsm")
    shutil.copy2(path, tmp)  # copy first so an open/locked workbook still reads
    wb = openpyxl.load_workbook(tmp, read_only=True, data_only=True)
    rows = []
    for r in wb["Production Data"].iter_rows(min_row=2, values_only=True):
        tech, yr, mn, qty, pts, st = r[8], r[2], r[4], r[5], r[11], r[9]
        if not tech or not isinstance(yr, int) or not isinstance(mn, int):
            continue
        rows.append({"tech": str(tech).strip(), "yr": yr, "mo": MONTHS[mn-1], "moNum": mn,
                     "u": int(qty or 0), "p": float(pts or 0), "s": st or "Inactive"})
    wb.close()
    techs = {x["tech"]: x["s"] for x in rows}
    now = datetime.now(timezone.utc)
    mod = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc)
    return {"meta": {"workbookName": os.path.basename(path), "generatedAt": now.isoformat(),
                     "generatedAtLabel": now.strftime("%d %b %Y %H:%M UTC"),
                     "sourceModifiedAt": mod.isoformat(timespec="seconds"), "sourceSheet": "Production Data"},
            "stats": {"rows": len(rows), "totalUnits": sum(x["u"] for x in rows),
                      "totalPoints": sum(x["p"] for x in rows), "techCount": len(techs),
                      "activeTechCount": sum(1 for s in techs.values() if s == "Active")},
            "rows": rows}

def main(arg=None):
    new = build(find_workbook(arg))
    try:
        old = json.load(open(OUT, encoding="utf-8"))
        if old.get("rows") == new["rows"]:
            print("No data change."); return False
    except Exception:
        pass
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(new, f, indent=2)
    print("Wrote", OUT, new["stats"]); return True

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
