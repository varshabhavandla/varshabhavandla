---
name: job-search-roadmap
description: Build a personalized week-by-week job-search and upskilling roadmap (default 12 weeks) from the user's target role, weekly hours, location/visa status and deadline - positioning, applying, networking, a skill-proof project, interview prep, close. USE WHEN the user asks where to start a job search, wants a plan/roadmap/schedule to get a new job fast, or says they are leaving a comfort zone/startup. NOT FOR tracking individual applications (use job-tracker), editing a resume, or writing a single message.
---

Tier: D (scripts/make_roadmap.py + tests; intake and tailoring are judgment steps)

# Job-search roadmap

## Intake (ask all in one message; skip what the user already said)
Target role(s) and seniority; location/remote; weekly hours available; hard deadline or runway; visa status (F-1/CPT/OPT -> also use `visa-aware-search`); current employer constraints (confidentiality of search); one-line strengths.

## Steps
1. Run `python3 scripts/make_roadmap.py --hours <h> --weeks <n> --start <YYYY-MM-DD> --role "<role>"`. Hours per week always sum exactly; phases are Foundation, Launch, Momentum, Interview push, Close.
2. Turn each phase into concrete deliverables for THIS user (e.g. Foundation: `resume-builder`, LinkedIn headline, 30-company target list; Launch: first 10 tailored applications via `resume-tailor`, outreach via `networking-outreach`; Momentum: ship one portfolio project that matches target JDs; Interview push: `interview-prep`; Close: `offer-negotiation`).
3. Set up tracking with `job-tracker` and put a weekly review on the calendar.
4. Present: the table, the 3 things to do in the next 48 hours, and what you assumed.

## Rules
- "Immediately" means a 48-hour first-action list, not a bigger plan.
- No guarantees about timelines or outcomes; say search length varies with market and role.
- Don't tell the user to hide the search from or badmouth their employer.

## Tests
`python3 -m unittest discover -s tests`
