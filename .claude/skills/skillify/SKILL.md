---
name: skillify
description: Skillify-as-a-verb - distill a working session (or a pointed-at chat history) into a permanent, TESTED, registered skill in .claude/skills/. Steps - look-back extraction, scaffold, split deterministic vs judgment steps, unit tests, trigger evals, run the gate (scripts/skillify_check.py), cross-review, register in SKILLS.md. USE WHEN the user says "skillify it", "skillify this", "package this as a skill", "make this a skill", "turn this into a skill", or at the end of an ad-hoc workflow that worked and should become permanent. NOT FOR one-off tasks with no reusable procedure, or pure discovery of "what do I repeat" (just analyze transcripts and report).
---

# /skillify

Tier: D (gate script + tests; extraction and review are judgment steps)

A feature that doesn't pass the gate is not a skill. Do the steps in order.

1. **Look-back extraction** - from the session or the pointed-at history, list: the trigger phrases the user actually used, the inputs, the steps that repeated, the corrections the user made, and the output format. Quote real phrases; don't invent.
2. **Scaffold** - `.claude/skills/<name>/SKILL.md` (frontmatter: `name` = directory name; `description` with `USE WHEN` and `NOT FOR`), plus `scripts/`, `tests/`, `evals/`.
3. **Split latent vs deterministic** - mechanical steps (file layout, parsing, counting, validation) become scripts; reading, judging and writing stay in SKILL.md prose.
4. **Declare a tier** in SKILL.md as a line `Tier: D|J|L`:
   - **D** deterministic: has scripts, and tests that pass.
   - **J** judgment only: no pure function; needs `evals/cases.json` with held-out cases and a stated rubric in SKILL.md.
   - **L** lens: routing/perspective skill; needs `evals/cases.json` of when it should and should not fire.
5. **Unit tests** for every script (`tests/test_*.py`, stdlib unittest). For tier D, break a script on purpose once and confirm a test fails (mutation check), then restore it.
6. **Trigger evals** - `evals/cases.json`: `{"should_trigger": [...], "should_not_trigger": [...]}`, at least 3 each, written as real user phrasings (include near-misses for the NOT FOR cases).
7. **Gate** - `python3 .claude/skills/skillify/scripts/skillify_check.py .claude/skills/<name>` must exit 0. Add `--all` to audit every skill.
8. **Cross-review** - have a fresh subagent (or the user) read only the SKILL.md and say what it would do for each eval case; fix mismatches.
9. **Register** - add a row to `.claude/skills/SKILLS.md` (name, tier, one-line purpose, date). The gate fails if it's missing.
10. **Commit** the skill, tests, evals and registry together.

## Safety
Never copy secrets, tokens or personal data from transcripts into a skill. Student/personal facts belong in a separate reference skill, not in procedure skills.
