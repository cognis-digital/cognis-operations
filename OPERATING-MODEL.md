# The Cognis Agentic Operating Model (AOM)

Four interdependent layers (after Berkeley CMR / McKinsey's agentic-org work), instantiated on the Cognis stack.

| Layer | Purpose | Cognis implementation |
|---|---|---|
| **Cognitive** | reasoning, tools, skills | [uncensored-fleet](https://github.com/cognis-digital/uncensored-fleet) models + the 195-tool suite + [skills](https://github.com/cognis-digital/skills) |
| **Coordination** | orchestration, routing, memory | agent harness · [modelroute](https://github.com/cognis-digital/modelroute) · [engram](https://github.com/cognis-digital/engram) memory |
| **Control** | guardrails, approvals, audit | [toolguard](https://github.com/cognis-digital/toolguard) · [guardpost](https://github.com/cognis-digital/guardpost) · [agentpassport](https://github.com/cognis-digital/agentpassport) |
| **Governance** | policy, risk, accountability | [compliance-atlas](https://github.com/cognis-digital/compliance-atlas) · human review · [agentlog](https://github.com/cognis-digital/agentlog) |

**Principle:** agents own structured, repeatable execution; humans hold strategic direction and any
regulated / ambiguous / high-risk decision (human-in-the-loop). One pod of 2-5 humans can supervise an
"agent factory" of 50-100 specialized agents running an end-to-end outcome.
