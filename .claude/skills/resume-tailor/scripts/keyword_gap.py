#!/usr/bin/env python3
"""Compare a job description against a resume and list missing keywords.

Usage: keyword_gap.py JD.txt RESUME.txt
Keywords = known tech/skill phrases found in the JD + other words repeated 2+ times in the JD.
Output is a CHECKLIST of things to genuinely evidence - never add a skill you don't have.
"""
import re, sys
from collections import Counter

PHRASES = ["github actions", "gitlab ci", "azure devops", "ci/cd", "infrastructure as code", "zero trust", "service mesh",
           "site reliability", "incident response", "on-call", "blue-green", "helm", "argocd", "gitops", "terraform", "ansible",
           "kubernetes", "aks", "eks", "gke", "docker", "azure", "aws", "gcp", "prometheus", "grafana", "datadog", "opentelemetry",
           "python", "go", "bash", "powershell", "linux", "devsecops", "iam", "vault", "keyvault", "finops", "cost optimization",
           "observability", "sre", "platform engineering", "self-service", "developer experience", "mlops", "sql", "networking"]
STOP = set("""a an and are as at be by for from has have in is it its of on or our that the their this to we will with you your
who what when where which how not but if can may must should would about across into over per such than then them they these
those other more most any all each both also etc using use used work working team teams role experience years year strong
ability skills skill knowledge including include looking join help build building new e g i s""".split())

def tokens(text):
    return re.findall(r"[a-z][a-z0-9+#./-]*", text.lower())

def keywords(jd):
    low = " " + " ".join(tokens(jd)) + " "
    found = {p for p in PHRASES if re.search(rf"(?<![a-z0-9]){re.escape(p)}(?![a-z0-9])", low)}
    counts = Counter(t.strip(".-/") for t in tokens(jd) if t not in STOP and len(t) > 2)
    found |= {w for w, c in counts.items() if c >= 2 and w}
    return found

def gap(jd, resume):
    rlow = " " + " ".join(tokens(resume)) + " "
    kws = keywords(jd)
    have = {k for k in kws if re.search(rf"(?<![a-z0-9]){re.escape(k)}(?![a-z0-9])", rlow)}
    return {"have": sorted(have), "missing": sorted(kws - have),
            "coverage_pct": round(100 * len(have) / len(kws), 1) if kws else 100.0}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    r = gap(open(sys.argv[1], encoding="utf-8").read(), open(sys.argv[2], encoding="utf-8").read())
    print(f"coverage: {r['coverage_pct']}%\nmissing: {', '.join(r['missing']) or '-'}\nhave: {', '.join(r['have']) or '-'}")
