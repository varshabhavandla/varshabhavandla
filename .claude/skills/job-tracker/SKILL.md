---
name: job-tracker
description: Track job applications in a CSV pipeline - add, update status (wishlist/applied/screen/interview/offer/accepted/rejected/withdrawn), set next actions, list what follow-ups are due, and report response and interview rates. USE WHEN the user logs an application, asks what is due this week, who to follow up with, or how the search is going. NOT FOR planning the search (use job-search-roadmap) or writing the follow-up message itself (use networking-outreach).
---

Tier: D (scripts/tracker.py + tests)

# Job tracker

## Where data lives
`$JOB_TRACKER` or `~/.job-search/tracker.csv`. It contains personal data: **never commit it to a public repo** (the profile repo `varshabhavandla/varshabhavandla` is public). In a cloud session the container is wiped, so point `JOB_TRACKER` at a file in a PRIVATE repo, or export the CSV to the user at the end.

## Commands
`python3 scripts/tracker.py add "Company" "Role" --url URL [--status applied]`
`... update ID --status interview --next "Prep system design" --next-date 2026-10-20 --notes "..."`
`... list [--status S]`, `... due [--today D]`, `... stats`

## Steps
1. Log or update on request; confirm the row back in one line.
2. Every status change should set a next action and date (default: follow up 7 days after applying, 2 days after an interview).
3. On "how is it going": run `stats`, then interpret - low response rate -> resume/targeting problem (`resume-tailor`); screens but no interviews -> `interview-prep`; interviews but no offers -> debrief each loss.

## Rules
Statuses are a fixed set (the script rejects others). Never delete rows; mark withdrawn/rejected.

## Tests
`python3 -m unittest discover -s tests`
