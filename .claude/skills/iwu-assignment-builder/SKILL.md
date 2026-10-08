---
name: iwu-assignment-builder
description: Set up and work through Indiana Wesleyan University (IWU) graduate assignments (UNV-501 GPT/CPT discussions, MGMT-501 workshops, externship papers) - scaffold GPT-N/Workshop-K/x.y folders, unzip uploaded assignment .html.zip files, extract prompt + word limits + rubric, coach a draft grounded in the student's real portfolio/work experience, check word count, and build the APA-style .docx. USE WHEN the user mentions workshop, discussion 1.1, externship paper, CLO table, UNV-501, MGMT-501, IWU, or uploads "*.html.zip" assignment files. NOT FOR general writing, non-IWU coursework, or resume/job-search work.
---

# IWU assignment builder

## Integrity rule (read first)
Many IWU discussion prompts say the reflection "MUST be your personal interpretation and without the use of AI".
- **Discussion posts / reflections with that rule -> COACH mode only:** outline, questions to answer, structure and rubric check, word-count check, feedback on the student's own draft. Do NOT write submit-ready prose.
- **Papers with no such rule (e.g. externship paper 3.1) -> DRAFT mode** is fine, but it must use only facts from the student's portfolio/syllabus, and the student reviews it.
- If unsure which applies, quote the prompt's rule back and ask.

## Steps
1. **Scaffold + unzip (deterministic):** `python3 scripts/scaffold_workshop.py . <course#> <workshops> --unzip <zips...>`. Zip names must contain an item number like `1.2`. Then commit.
2. **Extract the prompt (judgment):** read the HTML; record the task, word limit, rubric, due date, required sections. Run limit text through `scripts/check_draft.py --prompt` later.
3. **Course outcomes:** use only text the student pasted from the syllabus. Brightspace needs the student's login - ask for a paste up front, never use catalog text as if it were the CLO list.
4. **Ground in real facts:** pull role, stack, projects from the portfolio repos / README. Missing fact (e.g. instructor name) -> leave a visible placeholder and list it as open; never invent.
5. **Draft or coach** per the integrity rule.
6. **Check:** `python3 scripts/check_draft.py draft.txt --prompt prompt.txt` (exit 1 = outside the limit). Fix and re-run.
7. **Build docx (papers):** copy `templates/externship_paper.js`, fill CONFIG, `npm i docx`, run. Times New Roman 12, double-spaced, title page.
8. **Deliver:** commit scratch/drafts only when the student asks; report open placeholders.

## Tests
`python3 -m unittest discover -s tests` (from this directory) must pass before editing scripts.
