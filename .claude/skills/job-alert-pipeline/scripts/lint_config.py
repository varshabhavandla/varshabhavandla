#!/usr/bin/env python3
"""Lint job-alerts config.yaml: python3 lint_config.py CONFIG. Exit 0 = ok."""
import re
import sys

import yaml

SLUG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
KNOWN = {"greenhouse", "lever", "ashby"}


def lint(cfg: dict) -> list[str]:
    errs = []
    if not isinstance(cfg, dict):
        return ["config is not a mapping"]
    for top in ("profile", "search", "sources"):
        if top not in cfg:
            errs.append(f"missing '{top}'")
    s = cfg.get("search", {}) or {}
    for key in ("title_include", "skills"):
        if not s.get(key):
            errs.append(f"search.{key} is empty or missing")
    if "min_score" in s and not 0 <= s["min_score"] <= 100:
        errs.append("search.min_score must be 0-100")
    for p in cfg.get("exclude_patterns", []) or []:
        try:
            re.compile(p)
        except re.error as e:
            errs.append(f"bad regex {p!r}: {e}")
    src = cfg.get("sources", {}) or {}
    if not any(src.values()):
        errs.append("sources has no company slugs")
    for kind, slugs in src.items():
        if kind not in KNOWN:
            errs.append(f"unknown source type {kind!r}")
        for slug in slugs or []:
            if not SLUG.match(str(slug)):
                errs.append(f"malformed slug {slug!r} under {kind}")
        if len(set(slugs or [])) != len(slugs or []):
            errs.append(f"duplicate slug under {kind}")
    return errs


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    errs = lint(yaml.safe_load(open(argv[0])))
    for e in errs:
        print("FAIL", e)
    print("PASS" if not errs else f"{len(errs)} problem(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
