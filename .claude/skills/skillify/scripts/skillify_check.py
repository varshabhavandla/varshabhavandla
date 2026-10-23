#!/usr/bin/env python3
"""Gate for skills: python3 skillify_check.py SKILL_DIR | --all [SKILLS_ROOT]. Exit 0 = pass."""
import json, re, subprocess, sys
from pathlib import Path

def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm

def check_skill(d, run_tests=True):
    d = Path(d); errs = []
    sk = d / "SKILL.md"
    if not sk.exists():
        return [f"{d.name}: missing SKILL.md"]
    text = sk.read_text(encoding="utf-8")
    fm = frontmatter(text)
    if fm is None:
        return [f"{d.name}: no frontmatter"]
    if fm.get("name") != d.name:
        errs.append(f"name {fm.get('name')!r} != directory {d.name!r}")
    desc = fm.get("description", "")
    for key in ("USE WHEN", "NOT FOR"):
        if key not in desc:
            errs.append(f"description lacks '{key}'")
    t = re.search(r"^Tier:\s*([DJL])\b", text, re.M)
    if not t:
        errs.append("no 'Tier: D|J|L' line"); tier = None
    else:
        tier = t.group(1)
    cases = d / "evals" / "cases.json"
    if not cases.exists():
        errs.append("missing evals/cases.json")
    else:
        try:
            c = json.loads(cases.read_text())
            for k in ("should_trigger", "should_not_trigger"):
                if len(c.get(k, [])) < 3:
                    errs.append(f"evals/cases.json: need >=3 in {k}")
        except json.JSONDecodeError as e:
            errs.append(f"evals/cases.json invalid: {e}")
    scripts = [p for p in (d / "scripts").glob("*.py")] if (d / "scripts").exists() else []
    tests = list((d / "tests").glob("test_*.py")) if (d / "tests").exists() else []
    if tier == "D":
        if not scripts: errs.append("tier D needs scripts/*.py")
        if not tests: errs.append("tier D needs tests/test_*.py")
    if scripts and not tests:
        errs.append("scripts without tests")
    if tests and run_tests:
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(d / "tests")],
                           capture_output=True, text=True)
        if r.returncode != 0:
            errs.append("unit tests fail:\n" + r.stderr[-500:])
    reg = d.parent / "SKILLS.md"
    if not reg.exists() or not re.search(rf"\b{re.escape(d.name)}\b", reg.read_text(encoding="utf-8")):
        errs.append("not registered in SKILLS.md")
    return [f"{d.name}: {e}" for e in errs]

def main(argv):
    if not argv:
        print(__doc__); return 2
    if argv[0] == "--all":
        root = Path(argv[1] if len(argv) > 1 else ".claude/skills")
        dirs = sorted(p for p in root.iterdir() if p.is_dir())
    else:
        dirs = [Path(argv[0])]
    errs = [e for d in dirs for e in check_skill(d)]
    for e in errs: print("FAIL", e)
    print("PASS" if not errs else f"{len(errs)} problem(s)")
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
