# Readiness checklist (senior)

Mark each item Verified (evidence) / Accepted risk (owner, date) / Gap.

## 1 Reliability and SLOs
SLIs/SLOs/error budgets per service with a policy; no SPOF (multi-AZ, health-checked LB); load tested incl. 2x headroom; timeouts, retries with backoff+jitter, circuit breakers, rate limits; graceful shutdown (preStop, draining, terminationGracePeriodSeconds).

## 2 Kubernetes / platform
HA or managed control plane, documented upgrade/version-skew path; requests+limits, PDBs, topology spread; correct liveness/readiness/startup probes; HPA/VPA + cluster autoscaler tested; quotas and LimitRanges; ingress, DNS, certs automated with expiry alerts; zero-downtime node patching.

## 3 CI/CD and delivery
Reproducible pipelines, pinned versions, immutable artifacts; rolling/blue-green/canary with automated health gates and auto-rollback; rollback tested incl. DB migrations (expand/contract); GitOps source of truth with drift detection; env parity, feature flags; prod approvals and audit trail.

## 4 Infrastructure as Code
Everything in code; remote encrypted locked state split by blast radius; plans reviewed in PRs, policy-as-code; rebuild-from-scratch tested; drift detected; versioned modules, ownership/cost tags.

## 5 Security and supply chain
Least-privilege IAM, no long-lived keys (workload identity/OIDC), MFA; secrets in a manager with rotation; segmented network, egress control, mTLS if needed; images scanned, signed, SBOM + provenance verified by admission control; hardened CI runners and tokens, protected branches; pod security standards; audit logging on; patch SLA; compliance mapped to controls.

## 6 Observability
Logs+metrics+traces correlated; golden-signal dashboards; SLO burn-rate alerts with runbook and owner; on-call and escalation; observability stack monitored independently; retention/cardinality/cost controlled.

## 7 Data, backup, DR
RPO/RTO per system; automated encrypted immutable cross-region/account backups with scheduled restore tests; DR pattern (backup/restore, pilot light, warm standby, active-active) matches business need; failover drill incl. DNS, replication and failback; HA for stateful services; retention policies.

## 8 Incident management
Severity levels, incident commander, comms channel, status page; runbooks for top failure modes; blameless postmortems with tracked actions; game days/chaos (pod, node, AZ, dependency loss).

## 9 Cost (FinOps)
Tagging and allocation; budgets and anomaly alerts; right-sizing and reserved/savings/spot mix; idle cleanup, transfer and storage tiering; savings checked against reliability.

## 10 Operations and governance
Service ownership/tier/docs; current diagrams, dependency maps, ADRs; quotas and limits checked (cloud limits, IP exhaustion, API rate limits); change management and freeze; explicit automate vs human-approval boundary (approve: prod data deletion, IAM changes, DR failover); third-party SLAs and fallbacks.

## Final gate
1 load test vs SLO, 2 rollback exercised, 3 backup restore verified, 4 alerts fired in test and runbooks known, 5 security scan and access review clean or risk accepted in writing, 6 cost forecast approved.

# Production troubleshooting playbook
| Scenario | First steps |
|---|---|
| Service down | Recent change (deploy/config/cert/dependency); health endpoints, LB, DNS; mitigate (rollback/failover/scale) before root cause |
| High CPU/memory | Spike vs trend; top / kubectl top; throttling vs limits; OOMKilled; leaks/GC; traffic and bad queries; then fix limits, scale or code |
| Logs | Start at alert time; correlate by trace/request id; first error not loudest; `kubectl logs --previous` |
| Dependency issue | Downstream status, DNS, network policy, credentials; timeouts/retries; circuit breakers |
| Permission denied | Identify actor and exact action/resource; IAM/RBAC/file perms/security context; grant least privilege |
| Failed deployment | Roll back first; then probes, image tags, config, migrations; add the missing pipeline gate |
| Alert storm | Triage by user impact; group/silence; move to SLO-based alerts; delete alerts nobody acts on |
| Fix, test, repeat | Postmortem; add test/alert/runbook; automate the manual fix |

Interview answer order: stabilize, diagnose, fix, prevent, communicate.

# Senior question to section map
Kubernetes platform 2; speed/reliability/security 1,3,5; Sev-1 8; SLIs/SLOs 1; supply chain 5; multi-region DR 7; cloud cost 9; observability 6; automation vs approval 10.
