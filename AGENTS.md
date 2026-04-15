# Agent Registry

Every agent is an identity-bearing entity (see [agentpassport](https://github.com/cognis-digital/agentpassport)) with an owner, scopes, and an audit trail.

| Agent | Layer | Scopes | Human owner |
|---|---|---|---|
| `commander` | Coordination | route, delegate | Chief of Agents |
| `researcher` | Cognitive | web.search, read | BLACKBOOK pod |
| `coder` | Cognitive | repo.read, repo.write (PR-gated) | PROMETHEUS pod |
| `reviewer` | Control | repo.read, comment | IRONCLAD pod |
| `verifier` | Control | run.tests | IRONCLAD pod |
| `outreach` | Cognitive | crm.read, email.draft | FOUNDRY pod |

Rules: least-privilege scopes, scope-narrowing on delegation, every action logged, humans approve anything
regulated/ambiguous/high-risk.
