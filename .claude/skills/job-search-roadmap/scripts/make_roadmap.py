#!/usr/bin/env python3
"""Generate a weekly job-search roadmap.

Usage: make_roadmap.py --hours 15 [--weeks 12] [--start 2026-10-12] [--role "Platform Engineer"]
Prints markdown. Weekly hours are split across buckets by phase; each split sums exactly to --hours.
"""
import argparse, math
from datetime import date, timedelta

BUCKETS = ["foundation", "apply", "network", "skill", "interview"]
# (phase name, theme, weight per bucket)
PHASES = [
    ("Foundation", "Position yourself: target roles, resume, LinkedIn, target-company list", [50, 10, 15, 20, 5]),
    ("Launch", "Start applying and networking; first skill-proof project", [10, 35, 25, 20, 10]),
    ("Momentum", "High-volume targeted applications, referrals, ship the project", [5, 35, 25, 20, 15]),
    ("Interview push", "Mock interviews, story bank, technical drills", [0, 25, 15, 15, 45]),
    ("Close", "Follow up, final rounds, offers and negotiation", [0, 20, 15, 5, 60]),
]
CUTS = [0.17, 0.33, 0.67, 0.83]  # fraction of the timeline where phases end

def phase_index(week, weeks):
    frac = (week - 1) / weeks
    return sum(frac >= c for c in CUTS)

def split_hours(total, weights):
    """Largest-remainder split in half-hour units so the parts sum exactly to total."""
    units = round(total * 2)
    wsum = sum(weights)
    raw = [units * w / wsum for w in weights]
    base = [math.floor(r) for r in raw]
    order = sorted(range(len(raw)), key=lambda i: raw[i] - base[i], reverse=True)
    for i in order[: units - sum(base)]:
        base[i] += 1
    return [b / 2 for b in base]

def plan(hours, weeks=12, start=None, role="target role"):
    if hours <= 0 or weeks < 4 or weeks > 16:
        raise ValueError("hours must be > 0 and weeks between 4 and 16")
    start = start or date.today()
    rows = []
    for w in range(1, weeks + 1):
        name, theme, weights = PHASES[phase_index(w, weeks)]
        h = dict(zip(BUCKETS, split_hours(hours, weights)))
        rows.append({
            "week": w, "start": start + timedelta(weeks=w - 1), "phase": name, "theme": theme,
            "hours": h,
            "targets": {"tailored_applications": math.floor(h["apply"] * 1.5),
                        "networking_touches": math.floor(h["network"] * 3),
                        "mock_interviews": 1 if h["interview"] >= 3 else 0},
            "role": role,
        })
    return rows

def render(rows):
    out = [f"# Job-search roadmap - {rows[0]['role']}", "",
           "| Wk | Starts | Phase | Foundation | Apply | Network | Skill | Interview | Apps | Touches | Mocks |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        h, t = r["hours"], r["targets"]
        out.append(f"| {r['week']} | {r['start']} | {r['phase']} | {h['foundation']} | {h['apply']} | {h['network']} | "
                   f"{h['skill']} | {h['interview']} | {t['tailored_applications']} | {t['networking_touches']} | {t['mock_interviews']} |")
    out += ["", "## Phases"] + [f"- **{n}**: {t}" for n, t, _ in PHASES]
    return "\n".join(out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, required=True)
    ap.add_argument("--weeks", type=int, default=12)
    ap.add_argument("--start", type=date.fromisoformat, default=None)
    ap.add_argument("--role", default="target role")
    a = ap.parse_args()
    print(render(plan(a.hours, a.weeks, a.start, a.role)))
