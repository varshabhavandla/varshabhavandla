"""Fetch postings from public ATS job-board APIs and normalise them."""
import html
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone

import requests

log = logging.getLogger(__name__)
TIMEOUT = 20
HEADERS = {"User-Agent": "job-alerts/1.0 (personal job search)"}


@dataclass
class Job:
    uid: str
    company: str
    title: str
    location: str
    url: str
    description: str
    posted: datetime | None


def _strip(text: str) -> str:
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _get(url: str, **params):
    r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def greenhouse(token: str) -> list[Job]:
    data = _get(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs", content="true")
    return [
        Job(
            uid=f"gh:{token}:{j['id']}",
            company=token,
            title=j.get("title", ""),
            location=(j.get("location") or {}).get("name", ""),
            url=j.get("absolute_url", ""),
            description=_strip(j.get("content", "")),
            posted=_iso(j.get("first_published") or j.get("updated_at")),
        )
        for j in data.get("jobs", [])
    ]


def lever(token: str) -> list[Job]:
    data = _get(f"https://api.lever.co/v0/postings/{token}", mode="json")
    jobs = []
    for j in data:
        created = j.get("createdAt")
        posted = datetime.fromtimestamp(created / 1000, tz=timezone.utc) if created else None
        jobs.append(Job(
            uid=f"lv:{token}:{j['id']}",
            company=token,
            title=j.get("text", ""),
            location=(j.get("categories") or {}).get("location", "") or "",
            url=j.get("hostedUrl", ""),
            description=_strip(j.get("descriptionPlain") or j.get("description", "")),
            posted=posted,
        ))
    return jobs


def ashby(token: str) -> list[Job]:
    data = _get(f"https://api.ashbyhq.com/posting-api/job-board/{token}", includeCompensation="false")
    return [
        Job(
            uid=f"ab:{token}:{j['id']}",
            company=token,
            title=j.get("title", ""),
            location=j.get("location", "") + (" (Remote)" if j.get("isRemote") else ""),
            url=j.get("jobUrl", ""),
            description=_strip(j.get("descriptionHtml") or j.get("descriptionPlain", "")),
            posted=_iso(j.get("publishedAt")),
        )
        for j in data.get("jobs", [])
    ]


FETCHERS = {"greenhouse": greenhouse, "lever": lever, "ashby": ashby}


def fetch_all(sources: dict) -> list[Job]:
    jobs: list[Job] = []
    for kind, tokens in sources.items():
        fetch = FETCHERS.get(kind)
        if not fetch:
            log.warning("unknown source type %s", kind)
            continue
        for token in tokens or []:
            try:
                jobs.extend(fetch(token))
            except Exception as exc:  # one bad slug must not stop the run
                log.warning("%s/%s failed: %s", kind, token, exc)
    return jobs
