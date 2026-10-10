#!/usr/bin/env python3
"""Compare job offers by annualized total compensation.

Usage: compare_offers.py offers.json   (list of objects)
Fields: name, base, bonus_pct=0, equity_total=0, vest_years=4, signing=0, match_pct=0 (401k match % of base), other=0 (yearly)
Year-1 includes signing; steady-state excludes it. Equity counted at grant value - discount it for private companies.
"""
import json, sys

def total(o):
    for k in ("name", "base"):
        if k not in o: raise ValueError(f"offer missing '{k}'")
    base = float(o["base"]); vest = float(o.get("vest_years", 4))
    if base <= 0 or vest <= 0: raise ValueError("base and vest_years must be > 0")
    steady = (base + base * float(o.get("bonus_pct", 0)) / 100 + float(o.get("equity_total", 0)) / vest
              + base * float(o.get("match_pct", 0)) / 100 + float(o.get("other", 0)))
    return {"name": o["name"], "year1": round(steady + float(o.get("signing", 0)), 2), "steady": round(steady, 2)}

def compare(offers):
    return sorted((total(o) for o in offers), key=lambda r: r["steady"], reverse=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(2)
    for r in compare(json.load(open(sys.argv[1]))):
        print(f"{r['name']:<20} year1 ${r['year1']:>12,.0f}   steady ${r['steady']:>12,.0f}")
