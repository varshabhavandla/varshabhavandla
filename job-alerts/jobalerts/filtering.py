"""Decide whether a job is relevant, and score it against resume skills."""
import re
from datetime import datetime, timedelta, timezone

from .sources import Job


def blocked_reason(job: Job, patterns: list[str]) -> str | None:
    text = f"{job.title} {job.description}".lower()
    for p in patterns:
        if re.search(p, text, re.I):
            return p
    return None


def score(job: Job, skills: dict[str, int]) -> tuple[int, list[str]]:
    text = f"{job.title} {job.description}".lower()
    hits = {s: w for s, w in skills.items() if s.lower() in text}
    total = sum(skills.values()) or 1
    return round(100 * sum(hits.values()) / total * 2.5), sorted(hits)  # x2.5: no JD lists every skill


def evaluate(job: Job, cfg: dict, now: datetime | None = None):
    """Return (keep, score, matched_skills, reason)."""
    s = cfg["search"]
    now = now or datetime.now(timezone.utc)
    title = job.title.lower()
    if not any(k in title for k in s["title_include"]):
        return False, 0, [], "title"
    if any(k in title for k in s.get("title_exclude", [])):
        return False, 0, [], "title_exclude"
    locs = [l.lower() for l in s.get("locations", [])]
    if locs and not any(l in job.location.lower() for l in locs):
        return False, 0, [], "location"
    if job.posted and now - job.posted > timedelta(hours=s.get("max_age_hours", 48)):
        return False, 0, [], "stale"
    bad = blocked_reason(job, cfg.get("exclude_patterns", []))
    if bad:
        return False, 0, [], f"blocked:{bad}"
    sc, hits = score(job, s["skills"])
    sc = min(sc, 100)
    if sc < s.get("min_score", 0):
        return False, sc, hits, "low_score"
    return True, sc, hits, ""
