---
name: job-alert-pipeline
description: Operate and extend the job-alerts service in job-alerts/ (polls Greenhouse/Lever/Ashby boards, filters by resume skills, skips US-citizen/clearance roles, drafts a note with Claude, emails new matches). Covers adding companies, tuning filters, SMTP/Actions secrets, debugging silent or noisy alerts, and linting config.yaml. USE WHEN the user says job alerts, "alert me when jobs are posted", add a company to the watch list, no emails arriving, too many alerts, citizenship filter, or edits job-alerts/config.yaml. NOT FOR auto-submitting applications or scraping LinkedIn (violates its terms; refuse and point to LinkedIn job alerts), resume tailoring, or tracking applications (use job-tracker).
---

# Job alert pipeline

Tier: D (config lint script + tests; choosing companies and filters is judgment)

Code lives in `job-alerts/` (`config.yaml`, `resume.md`, `jobalerts/`, workflow `.github/workflows/job-alerts.yml`). It alerts and drafts only; the user applies.

## Rules
- Never add auto-apply or LinkedIn scraping. Route LinkedIn coverage through its own "as soon as posted" alerts.
- Drafts may use only facts in `job-alerts/resume.md`. Never invent employers, tools or metrics.
- Citizenship/clearance exclusions stay on. Sponsorship exclusions are the user's call (off by default).
- Secrets (`SMTP_USER`, `SMTP_PASSWORD`, `ANTHROPIC_API_KEY`) live in Actions secrets, never in files.

## Steps
1. **Change config** (`job-alerts/config.yaml`): companies under `sources`, titles/locations/skills under `search`, regexes under `exclude_patterns`.
2. **Lint (deterministic):** `python3 scripts/lint_config.py job-alerts/config.yaml` (exit 1 on bad regex, missing keys, malformed slugs, empty lists).
3. **Verify new slugs live:** a wrong slug 404s and is skipped with a warning. Run `cd job-alerts && python3 -m jobalerts.main --dry-run -v --state /tmp/s.json` and grep the log for `failed:`; remove dead slugs.
4. **Test:** `cd job-alerts && python3 -m unittest discover -s tests`.
5. **Deploy facts:** scheduled workflows run only from the default branch; GitHub may delay a "*/5" cron by minutes; first run seeds existing postings silently (delete the state cache to re-seed).

## Debugging
- No emails: check Actions logs for `alerts=0`; confirm secrets exist; first run is silent by design; `max_age_hours` or `min_score` may be dropping everything (`-v` logs the skip reason).
- Too many: raise `min_score`, tighten `title_include`/`locations`, add `title_exclude`.
- Missed role: it's on a board not in `sources` or is a non-ATS site; add the slug or rely on LinkedIn alerts.
