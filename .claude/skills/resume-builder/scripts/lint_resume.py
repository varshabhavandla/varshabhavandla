#!/usr/bin/env python3
"""Lint a plain-text/markdown resume for common ATS and quality problems.

Usage: lint_resume.py RESUME.md [--max-bullets-per-role 6]
Exit 0 = no errors (warnings allowed), 1 = errors. Checks:
 ERROR  missing standard sections (Experience, Education, Skills), no email, [TODO] placeholders left
 WARN   bullet not starting with an action verb, weak phrases ("responsible for"), first-person pronouns,
        bullet with no number/metric, bullet over 220 chars, too many bullets in one role, table/pipe layout
"""
import re, sys

VERBS = set("""achieved architected automated built championed cut configured consolidated created decreased delivered deployed designed
developed drove eliminated enabled engineered established executed expanded implemented improved increased integrated introduced launched
led managed migrated mentored modernized monitored negotiated operated optimized orchestrated owned partnered provisioned reduced
refactored released remediated replaced resolved restructured scaled secured shipped simplified standardized streamlined supported
transformed upgraded validated wrote analyzed authored collaborated coordinated debugged diagnosed documented evaluated hardened
instrumented maintained onboarded piloted rolled saved tested trained tuned unified used leveraged""".split())
IRREGULAR = set("""built led ran drove wrote cut set took taught grew made kept sold won spent oversaw troubleshot rebuilt
lead build run drive write take teach grow make keep sell oversee troubleshoot rebuild""".split())
BULLET = r"^\s*[-*\u2022\u25cf\u25aa\u25e6]\s+"
WEAK = ["responsible for", "duties included", "worked on", "helped with", "assisted with", "participated in", "various", "etc"]
SECTIONS = {"experience": r"experience|employment", "education": r"education", "skills": r"skills|technical"}

def is_action_verb(word):
    """Known verb, past tense (-ed), irregular, or present tense of a known verb (current-role bullets)."""
    return (word in VERBS or word in IRREGULAR or (len(word) > 4 and word.endswith("ed"))
            or word + "ed" in VERBS or word + "d" in VERBS)

def bullets(text):
    return [re.sub(BULLET, "", l).strip() for l in text.splitlines() if re.match(BULLET, l)]

def lint(text, max_bullets=6):
    errors, warns = [], []
    low = text.lower()
    headings = [l.strip("# ").lower() for l in text.splitlines() if l.startswith("#") or (l.isupper() and 3 < len(l) < 40)]
    for name, pat in SECTIONS.items():
        if not any(re.search(pat, h) for h in headings):
            errors.append(f"missing section: {name}")
    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text):
        errors.append("no email address")
    if "[todo" in low:
        errors.append("unfilled [TODO] placeholder")
    if re.search(r"^\s*\|.*\|\s*$", text, re.M):
        warns.append("table/pipe layout detected - ATS parsers often scramble it")
    for b in bullets(text):
        first = re.match(r"[A-Za-z]+", b)
        word = first.group(0).lower() if first else ""
        if not is_action_verb(word):
            warns.append(f"bullet doesn't start with an action verb: '{b[:50]}'")
        for w in WEAK:
            if w in b.lower(): warns.append(f"weak phrase '{w}': '{b[:50]}'")
        if re.search(r"\b(i|my|me)\b", b, re.I):
            warns.append(f"first-person pronoun: '{b[:50]}'")
        if not re.search(r"\d", b):
            warns.append(f"no number/metric: '{b[:50]}'")
        if len(b) > 220:
            warns.append(f"bullet over 220 chars ({len(b)}): '{b[:40]}'")
    run = 0
    for line in text.splitlines() + [""]:
        if re.match(BULLET, line): run += 1
        else:
            if run > max_bullets: warns.append(f"{run} consecutive bullets (max {max_bullets}) - cut the weakest")
            run = 0
    return errors, warns

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    mb = int(sys.argv[sys.argv.index("--max-bullets-per-role") + 1]) if "--max-bullets-per-role" in sys.argv else 6
    e, w = lint(open(sys.argv[1], encoding="utf-8").read(), mb)
    for x in e: print("ERROR", x)
    for x in w: print("WARN ", x)
    print(f"{len(e)} error(s), {len(w)} warning(s)")
    sys.exit(1 if e else 0)
