#!/usr/bin/env python3
"""CSV job-application tracker.

Path: $JOB_TRACKER, else ~/.job-search/tracker.csv. Keep it OUT of public repos (it has personal data).
  tracker.py add "Company" "Role" [--url U] [--status applied] [--date YYYY-MM-DD]
  tracker.py update ID --status interview --next "Prep call" --next-date 2026-10-20 --notes "..."
  tracker.py list [--status S]     tracker.py due [--today YYYY-MM-DD]     tracker.py stats
"""
import argparse, csv, os, sys
from datetime import date
from pathlib import Path

FIELDS = ["id", "company", "role", "url", "status", "date_applied", "next_action", "next_action_date", "notes"]
STATUSES = ["wishlist", "applied", "screen", "interview", "offer", "accepted", "rejected", "withdrawn"]
OPEN = {"wishlist", "applied", "screen", "interview", "offer"}

def default_path():
    return Path(os.environ.get("JOB_TRACKER") or Path.home() / ".job-search" / "tracker.csv")

def load(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save(path, rows):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)

def add(rows, company, role, url="", status="applied", applied=None):
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}")
    nid = str(max([int(r["id"]) for r in rows] + [0]) + 1)
    row = {k: "" for k in FIELDS}
    row.update(id=nid, company=company, role=role, url=url, status=status,
               date_applied=applied or (date.today().isoformat() if status != "wishlist" else ""))
    rows.append(row)
    return row

def update(rows, rid, **kw):
    for r in rows:
        if r["id"] == str(rid):
            if kw.get("status") is not None and kw["status"] not in STATUSES:
                raise ValueError(f"status must be one of {STATUSES}")
            r.update({k: v for k, v in kw.items() if v is not None and k in FIELDS})
            return r
    raise KeyError(f"no row with id {rid}")

def due(rows, today=None):
    t = (today or date.today()).isoformat()
    return sorted((r for r in rows if r["status"] in OPEN and r["next_action_date"] and r["next_action_date"] <= t),
                  key=lambda r: r["next_action_date"])

def stats(rows):
    counts = {s: sum(r["status"] == s for r in rows) for s in STATUSES}
    applied = sum(1 for r in rows if r["status"] != "wishlist")
    advanced = sum(counts[s] for s in ("screen", "interview", "offer", "accepted"))
    return {"counts": counts, "applied_total": applied,
            "response_rate": round(100 * (advanced + counts["rejected"]) / applied, 1) if applied else 0.0,
            "interview_rate": round(100 * advanced / applied, 1) if applied else 0.0}

def main(argv):
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("company"); a.add_argument("role")
    a.add_argument("--url", default=""); a.add_argument("--status", default="applied"); a.add_argument("--date")
    u = sub.add_parser("update"); u.add_argument("id"); u.add_argument("--status")
    u.add_argument("--next", dest="next_action"); u.add_argument("--next-date", dest="next_action_date"); u.add_argument("--notes")
    l = sub.add_parser("list"); l.add_argument("--status")
    d = sub.add_parser("due"); d.add_argument("--today", type=date.fromisoformat)
    sub.add_parser("stats")
    n = ap.parse_args(argv); p = default_path(); rows = load(p)
    if n.cmd == "add":
        print(add(rows, n.company, n.role, n.url, n.status, n.date)); save(p, rows)
    elif n.cmd == "update":
        print(update(rows, n.id, status=n.status, next_action=n.next_action,
                     next_action_date=n.next_action_date, notes=n.notes)); save(p, rows)
    elif n.cmd == "list":
        for r in rows:
            if not n.status or r["status"] == n.status:
                print(f"{r['id']:>3} {r['status']:<10} {r['company']} - {r['role']}")
    elif n.cmd == "due":
        for r in due(rows, n.today): print(f"{r['next_action_date']} #{r['id']} {r['company']}: {r['next_action']}")
    else:
        print(stats(rows))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
