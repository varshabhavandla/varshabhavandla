"""Poll job boards, filter, draft, and email new matches."""
import argparse
import json
import logging
import os
from pathlib import Path

import yaml

from . import filtering, notify, sources, tailor

log = logging.getLogger("jobalerts")


def load_state(path: Path) -> set[str]:
    try:
        return set(json.loads(path.read_text()))
    except (FileNotFoundError, ValueError):
        return set()


def save_state(path: Path, seen: set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted(seen)))


def format_email(job, sc, hits, draft_text) -> tuple[str, str]:
    subject = f"[{sc}] {job.title} @ {job.company} — {job.location or 'n/a'}"
    posted = job.posted.strftime("%Y-%m-%d %H:%M UTC") if job.posted else "unknown"
    body = (f"{job.title}\n{job.company} | {job.location}\nPosted: {posted}\n"
            f"Match score: {sc}/100 | Skills: {', '.join(hits)}\n\nAPPLY: {job.url}\n\n"
            f"--- Draft (review before using) ---\n{draft_text}\n")
    return subject, body


def run(cfg_path: str, state_path: str, dry_run: bool) -> int:
    base = Path(cfg_path).parent
    cfg = yaml.safe_load(Path(cfg_path).read_text())
    resume = (base / cfg["profile"]["resume_file"]).read_text()
    state = Path(state_path)
    first_run = not state.exists()
    seen = load_state(state)

    jobs = sources.fetch_all(cfg["sources"])
    log.info("fetched %d postings", len(jobs))
    new = [j for j in jobs if j.uid not in seen]
    sent = 0
    for job in new:
        seen.add(job.uid)
        if first_run:  # seed silently; don't email the entire backlog
            continue
        keep, sc, hits, reason = filtering.evaluate(job, cfg)
        if not keep:
            log.debug("skip %s: %s", job.uid, reason)
            continue
        subject, body = format_email(job, sc, hits, tailor.draft(job, resume))
        if dry_run:
            print(subject, "\n", body, "\n", "=" * 60)
        else:
            notify.send(cfg["profile"]["email_to"], subject, body)
        sent += 1
    if first_run:
        log.info("first run: seeded %d postings, no emails sent", len(new))
    if not dry_run or first_run:
        save_state(state, seen)
    log.info("new=%d alerts=%d", len(new), sent)
    return sent


def cli() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--state", default=os.environ.get("STATE_FILE", ".state/seen.json"))
    ap.add_argument("--dry-run", action="store_true", help="print alerts instead of emailing")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    run(a.config, a.state, a.dry_run)


if __name__ == "__main__":
    cli()
