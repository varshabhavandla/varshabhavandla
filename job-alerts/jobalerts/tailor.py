"""Draft a short note and resume tweaks with Claude, grounded only in resume.md."""
import logging
import os

from .sources import Job

log = logging.getLogger(__name__)
MODEL = "claude-sonnet-5-5"

PROMPT = """You help a job seeker apply quickly. Using ONLY the facts in RESUME, write for the JOB below:
1. FIT: 2 lines on why she matches, and any gaps to be honest about.
2. KEYWORDS: up to 8 job-description keywords to mirror in her resume (only ones she truly has).
3. BULLETS: up to 3 existing resume bullets to move to the top, reworded for this job.
4. NOTE: a 90-word recruiter message. Plain, specific, no flattery.
Never invent employers, tools, metrics or years. If something is not in RESUME, do not claim it.

RESUME:
{resume}

JOB: {title} at {company} ({location})
{description}
"""


def draft(job: Job, resume: str) -> str:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return "(Set ANTHROPIC_API_KEY to get a tailored draft.)"
    try:
        import anthropic

        msg = anthropic.Anthropic().messages.create(
            model=MODEL,
            max_tokens=900,
            messages=[{"role": "user", "content": PROMPT.format(
                resume=resume, title=job.title, company=job.company,
                location=job.location, description=job.description[:6000])}],
        )
        return "".join(b.text for b in msg.content if b.type == "text")
    except Exception as exc:
        log.warning("draft failed for %s: %s", job.uid, exc)
        return "(Draft unavailable.)"
