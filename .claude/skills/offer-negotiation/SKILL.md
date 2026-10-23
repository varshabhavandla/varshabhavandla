---
name: offer-negotiation
description: Evaluate and negotiate job offers - compare total compensation across offers (base, bonus, equity, signing, retirement match), research market ranges, decide what to ask for, and draft the negotiation email/script, including deadline and competing-offer handling. USE WHEN the user has an offer or is asked about salary expectations, or wants to compare offers. NOT FOR resume/cover letters/interview practice.
---

Tier: D (scripts/compare_offers.py + tests; strategy and scripting are judgment steps)

# Offer negotiation

## Steps
1. Collect each offer's numbers into `offers.json` (fields in the script's docstring) and run `python3 scripts/compare_offers.py offers.json` for year-1 and steady-state totals. Equity at grant value overstates private-company stock; ask the user how to discount it. Note benefits not in the numbers (health premium, PTO, remote, learning budget, visa sponsorship).
2. Anchor to market: ask for sources the user trusts (levels.fyi, Glassdoor, Blind, recruiter conversations) - if you can't verify current ranges, say so instead of guessing figures.
3. Choose 2-3 asks in priority order (base, signing, equity, level/title, start date, remote, sponsorship terms). Ask for more than the target; be ready to explain why with specific value delivered.
4. Draft the email: gratitude, enthusiasm, one specific ask with rationale, collaborative close; or a phone script with responses to "what's your expected salary" (turn it around to the range for the role, or give a researched range) and to "can you sign today".
5. Competing offers: mention only real ones; never fabricate. Ask for a reasonable extension rather than issuing ultimatums.
6. After agreement: get it in writing before resigning; log in `job-tracker`.

## Rules
Visa-dependent users: sponsorship, E-Verify (needed for STEM OPT) and start date are negotiable terms - see `visa-aware-search`. Not legal or tax advice. Never advise misrepresenting current pay or offers.

## Tests
`python3 -m unittest discover -s tests`
