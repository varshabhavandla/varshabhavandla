---
name: infra-readiness-review
description: Run a senior-level infrastructure go/no-go review and troubleshoot production scenarios - SLOs, Kubernetes, CI/CD and rollback, IaC, supply-chain security, observability, DR/backup, incidents, cost, governance - and answer DevOps/SRE scenario interview questions in stabilize-diagnose-fix-prevent-communicate order. USE WHEN the user asks "is my infra ready", production readiness, launch checklist, go/no-go, DR or Sev-1 questions, "what would you check before prod", CrashLoopBackOff/high CPU/failed deploy triage, or senior DevOps interview scenario answers. NOT FOR resume writing, general interview logistics (use interview-prep), or implementing infrastructure code.
---

# Infrastructure readiness review

Tier: J (judgment only; rubric below, cases in evals/cases.json)

Checklist, troubleshooting playbook and interview mapping are in `references/checklist.md`. Load it, then:

1. **Scope:** ask for stack (cloud, Kubernetes or not, datastore, traffic) only if it changes the checklist; otherwise state assumptions.
2. **Review:** walk the ten sections; for each item mark Verified (name the evidence: test, dashboard, drill), Accepted risk (owner + date), or Gap.
3. **Gate:** the six final checks (load test vs SLO, rollback exercised, restore verified, alerts fire + runbooks known, security/access review, cost forecast) must each be Verified or an explicit accepted risk.
4. **Report:** gaps ranked by blast radius x likelihood, each with a concrete next action. Do not claim anything is verified that you did not see evidence for.
5. **Interview mode:** answer scenarios as stabilize -> diagnose -> fix -> prevent -> communicate, using the user's real experience (`resume.md` facts only; never invent metrics).

## Rubric (self-check before replying)
- Every claim of "ready" cites evidence or is flagged as assumed.
- Mitigation precedes root cause in incident answers.
- Automation vs human-approval boundary stated for destructive/irreversible actions.
- Cost advice states its reliability impact.
