<div align="center">

# cognis-operations

### How an **agentic company** actually runs — Cognis Digital's operating model, org chart, agent registry, and governance.

[![License: COCL 1.0](https://img.shields.io/badge/License-COCL%201.0-2b6cb0.svg)](LICENSE) ![Agentic](https://img.shields.io/badge/operating%20model-agentic-6b46c1) [![Suite](https://img.shields.io/badge/Cognis-Neural%20Suite-6b46c1.svg)](https://github.com/cognis-digital/cognis-neural-suite)

`#agentic-ai` `#operating-model` `#ai-native` `#org-design` `#governance`

</div>

A real, opinionated blueprint for running a company where **small human teams supervise factories of AI
agents**. This is how Cognis Digital operates — and a template you can fork.

- 🧠 [`OPERATING-MODEL.md`](OPERATING-MODEL.md) — the 4-layer agentic operating model
- 🗺️ [`ORG.md`](ORG.md) — the new org chart (humans + agent factories + AI-native roles)
- 🤖 [`AGENTS.md`](AGENTS.md) — the agent registry (roles, scopes, owners)
- 🛡️ [`GOVERNANCE.md`](GOVERNANCE.md) — human-in-the-loop, guardrails, audit & accountability
- 📚 [`SOURCES.md`](SOURCES.md) — McKinsey, Berkeley CMR, MIT Tech Review, Okta, NIST

## The operating model at a glance

```mermaid
flowchart TB
  G[Governance Layer<br/>policy · risk · accountability] --> C[Control Layer<br/>guardrails · approvals · audit]
  C --> O[Coordination Layer<br/>orchestration · routing · memory]
  O --> K[Cognitive Layer<br/>models · tools · skills]
  subgraph Humans
    CEO[Founder / Chief of Agents] --- POD[Outcome pods<br/>2-5 humans]
  end
  POD -->|supervise| O
  K --> FLEET[(uncensored-fleet + 195 tools)]
```

<a name="verification"></a>
## Verification



Every push is verified end-to-end. Latest audit (2026-06-13):

```text
tests        : 0 passed, 0 failed, 0 errored
compile      : all modules parse
cli          : n/a
package      : n/a
```

<details><summary>CLI surface (<code>--help</code>)</summary>

```text
(see --help)
```
</details>

Full machine-readable results: [`AUDIT.md`](AUDIT.md) · regenerate with `python -m cognis-operations --help` + `pytest -q`.

<div align="right"><a href="#top">↑ back to top</a></div>


## License
COCL v1.0 — see [LICENSE](LICENSE).
