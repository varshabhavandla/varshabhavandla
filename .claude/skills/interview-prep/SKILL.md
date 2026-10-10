---
name: interview-prep
description: Prepare for job interviews - build a STAR story bank from the user's real experience, drill behavioral, technical (platform/DevOps/cloud: Kubernetes, Terraform, CI/CD, GitOps, observability, security, cost) and system-design questions, run mock interviews with scoring, and debrief after rounds. USE WHEN the user has an interview coming, asks how to answer a question, wants a mock interview, or wants to debrief a round. NOT FOR resume writing, cover letters, or salary negotiation.
---

Tier: J (rubric below; evals in evals/cases.json)

# Interview prep

## Steps
1. **Context:** role, company, round type (recruiter screen, hiring-manager, technical, system design, panel), date, JD, interviewer names if known.
2. **Story bank (once):** extract 6-8 real stories from the user's experience, each as Situation / Task / Action / Result with a number: an outage or incident, a migration, a cost or performance win, a conflict or disagreement, a failure and what changed, a leadership/mentoring moment, an ambiguous-scope project, a security decision. Store in a private file, not a public repo. Tag each story with the competencies it covers.
3. **Map** questions to stories; never invent a story. Gaps -> tell the user what experience is missing and how to speak honestly about it.
4. **Technical drill (platform roles):** ask one question at a time, wait for the answer, then grade and give the model answer. Cover: Kubernetes scheduling/networking/failure modes, Terraform state/modules/drift, CI/CD and blue-green/rollback, GitOps with ArgoCD, observability (SLIs/SLOs, alert quality), IAM/zero trust/secrets, incident response, cost control. For system design: clarify requirements -> components -> failure modes -> scale -> trade-offs.
5. **Mock:** run a timed mock in the actual round format; score with the rubric.
6. **Debrief** after a real round: what was asked, where it wobbled, what to fix before the next round; log in `job-tracker` and draft a thank-you (within 24h).

## Scoring rubric (1-5 each)
Structure (answer first, then detail) - Specificity (real numbers, named tools) - Ownership ("I" vs "we" clarity) - Depth under follow-up - Honesty (says "I don't know, here's how I'd find out") - Concision (< 2 min per behavioral answer).

## Rules
Be candid about weak answers. Do not coach the user to misrepresent experience or to use AI assistance during a live interview where it is prohibited.
