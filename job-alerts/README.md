# job-alerts

Polls company job boards (Greenhouse, Lever, Ashby public APIs) every ~5 minutes, filters for roles matching the resume,
skips roles requiring US citizenship / security clearance, drafts a tailored note with Claude, and **emails you the link**.
You click and apply yourself — it does not submit applications or touch LinkedIn (which prohibits automation).

## Setup
1. Edit `config.yaml`: companies under `sources`, titles/locations/skills under `search`. Slugs come from board URLs
   (`boards.greenhouse.io/<slug>`, `jobs.lever.co/<slug>`, `jobs.ashbyhq.com/<slug>`).
2. Keep `resume.md` accurate — it's the only source Claude may use when drafting.
3. Repo secrets (Settings → Secrets → Actions): `SMTP_USER` (your Gmail), `SMTP_PASSWORD` (a Gmail
   [app password](https://myaccount.google.com/apppasswords)), `ANTHROPIC_API_KEY` (optional; without it you get alerts without drafts).
4. The workflow `.github/workflows/job-alerts.yml` runs every 5 minutes. The first run seeds existing postings silently.
   Scheduled workflows only run from the default branch, so merge this there to activate it.

## LinkedIn
Turn on LinkedIn job alerts ("as soon as posted") for your saved searches; they land in the same inbox. This covers
roles at companies not listed in `sources`.

## Local use
    pip install -r requirements.txt
    python -m jobalerts.main --dry-run -v     # prints alerts; seeds state on first run
    python -m unittest discover -s tests

## Notes
- Visa sponsorship filters are commented out in `config.yaml`; enable them if you want to skip "no sponsorship" roles.
- Always review the draft; it is generated from `resume.md` but may be imperfect.
