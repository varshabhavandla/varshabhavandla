---
name: resume-builder
description: Build a strong ATS-safe resume from scratch (or rebuild one) from the user's real profile, repos and experience - gather facts, quantify achievements without inventing numbers, write action-verb bullets, produce markdown and a .docx/PDF, and lint it. USE WHEN the user asks to create, build, rewrite or improve their resume/CV in general. NOT FOR adapting an existing resume to one specific job description (use resume-tailor) or cover letters.
---

Tier: D (scripts/lint_resume.py + tests; fact-gathering and writing are judgment steps)

# Resume builder

## Steps
1. **Gather facts** from, in order: a resume the user provides, the profile README / portfolio repos in the session, then questions. Ask for what's missing: target role, employer names and dates, team size, scale (clusters, services, users, spend), before/after numbers, tools, degree and dates, work authorization wording if they want it shown.
2. **Never invent.** If a metric is unknown, ask; if the user can't supply one, write the bullet without a number and leave `[TODO: metric]` visible. The lint fails on leftover TODOs so they can't ship by accident.
3. **Draft** from `templates/resume.md`: one column, standard headings (Summary, Skills, Experience, Projects, Education), reverse-chronological, 1 page under ~8 years' experience, max 6 bullets for the latest role and fewer for older ones.
4. **Bullet formula:** Action verb + what + how/tool + measurable result (cost, time, reliability, scale, adoption). Lead with impact; cut duties.
5. **Lint:** `python3 scripts/lint_resume.py resume.md` - fix every ERROR; justify or fix WARNs. Re-run until clean.
6. **Output** the .docx/PDF with the `docx` / `pdf` skills (no tables, text boxes, icons, photos, or multi-column - they break ATS parsing). Name it `Firstname_Lastname_Resume.pdf`.
7. Hand off: LinkedIn headline + About aligned to the resume; suggest `resume-tailor` per application.

## Rules
Keep contact details in the file only, never in logs or commits to public repos. Don't list visa status unless asked. Skills section lists only tools the user can discuss in an interview.

## Lessons from the first real run (keep these)
- **Ask one question at a time** when the user prefers it; record each answer immediately in a draft with `[TODO]` markers, so nothing is lost and the lint blocks unfinished drafts.
- **Keep a fact ledger** (every claim tagged: user said it / on the old resume / web / inferred). Resume claims may only come from user-said or old-resume facts; web and inferred facts need confirmation.
- **Run an independent review before building** the file: three reviewers (truthfulness vs ledger; interview/background-check defensibility; recruiter/ATS quality). It caught: years-of-experience claims tied to the wrong skills, a stale company-stage label from a web result, absolute words ("zero", "eliminated", "clean", "owns"), and a duty-vs-result gap.
- **Check verifiable facts:** exact job titles and dates must match HR records and LinkedIn; Microsoft Associate/Expert certs expire after 12 months (once lapsed they generally need the exam retaken) - show "earned <date>", never imply current standing; group roles under one employer when HR shows continuous employment; keep client names generic unless NDA allows.
- **Never put an internal tool name without saying it is internal** and who built it.
- **docx build:** use a right-aligned tab stop for dates (positional tabs did not render in LibreOffice); render to images and look at them before delivering; keep the resume out of public repos.

## Tests
`python3 -m unittest discover -s tests`
