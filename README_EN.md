# Codex Agent Team

<p align="center">
  <img src="assets/readme/hero.svg" alt="Codex Agent Team: use a specialist Subagent only when it adds real value" width="100%">
</p>

<p align="center">
  <a href="README.md">中文</a> ·
  <a href="docs/plugin-installation.md">Install</a> ·
  <a href="docs/architecture.md">Architecture</a> ·
  <a href="docs/model-route-assurance.md">Routing & Evidence</a>
</p>

**Let Codex form a team only when the task earns it.**

You keep working in one main session. Small, already-isolated tasks stay there. When a task benefits from heavy exploration, bounded implementation, or independent review, the right part can move to Luna, Terra, or Sol. You do not have to design an agent graph before you start coding.

> “Main session” means the Codex session you are already using. The architecture docs call it the `Root Controller`; this README uses the more approachable “main session” throughout.

## Start in 30 seconds

Codex Plugin is the only supported distribution path. Register this repository marketplace first:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

Reopen the ChatGPT desktop app, choose the `Codex Agent Team` marketplace in the Plugins Directory, and install the plugin. After that, there is one command to remember:

```text
/codex-agent-team
```

You can also describe the development task normally. The Skill decides whether creating a Subagent has a concrete benefit.

```text
Fix this authentication issue, run the relevant tests, then decide whether an independent review is actually useful.
```

<details>
<summary>What happens on first use?</summary>

The first time a model-specific Subagent is needed, the plugin checks these 4 managed custom Agent profiles:

```text
luna_explorer
luna_worker
terra_reviewer
sol_judge
```

If they are missing, the Skill explains the exact write scope and asks for permission. After approval, it installs and verifies only those 4 profiles plus their ownership manifest. It does not edit `config.toml`, MCP configuration, credentials, or unrelated Agent profiles.

After installation, the Skill rechecks the current native `spawn_agent` role surface. If the current task can already discover the new roles, work continues immediately. A fresh Codex task is requested only when role discovery has not refreshed yet.

</details>

## How it decides whether to form a team

<p align="center">
  <img src="assets/readme/workflow.svg" alt="Codex Agent Team delegation flow" width="100%">
</p>

| Task shape | Default handling |
| --- | --- |
| Small and already isolated | Main session handles it directly |
| Heavy search, noisy context, or clearly bounded implementation | Luna explores, implements, debugs, and tests |
| Risky change where a detached view materially improves confidence | Terra performs an independent review |
| High-consequence disagreement remains unresolved | Ask for consent, then use one Sol judgment |

Zero Subagents is a normal result. Codex Agent Team aims for the smallest useful team, rather than adding agents for its own sake.

## Who does what

<p align="center">
  <img src="assets/readme/roles.svg" alt="Codex Agent Team roles: main session, Luna, Terra, and Sol" width="100%">
</p>

| Role | Default route | Responsibility |
| --- | --- | --- |
| Main session | current Codex session | understand intent, plan, own scope and risk, accept work, deliver the final answer |
| Luna executor | GPT-5.6 Luna `max` | search, tracing, bounded implementation, debugging, tests |
| Terra reviewer | GPT-5.6 Terra `xhigh` | detached review of risky changes, conflicting evidence, and key assumptions |
| Sol judge | GPT-5.6 Sol `high` | rare high-consequence adjudication after explicit user consent |

Luna is the normal execution route. Terra appears only when independent judgment has real acceptance value. Sol is reserved for unresolved high-consequence decisions.

## What you see

When `/codex-agent-team` is invoked explicitly, a child is actually created, or an orchestration gate materially changes execution, the Skill emits a compact receipt. It reports what happened without turning normal coding into ceremony.

```text
Agent Team
Luna Worker: implemented bounded auth refresh change
Terra Reviewer: triggered by security boundary; verdict clear
Verification: 38 tests passed
```

When the main session is the better choice:

```text
Agent Team: Main session only
Why: change already isolated; delegation had no concrete benefit
Verification: 12 tests passed
```

## What the workflow protects

- **Minimum Team**: zero Subagents is normal, the default is 1, and the normal maximum is 2.
- **The main session keeps final control**: the Skill never silently switches the main session model or reasoning effort. If route, permission, or scope cannot be established safely, the responsibility stays in the main session.
- **One writer, one delegation layer**: one active writing Worker per shared workspace. Workers do not create another Subagent team.
- **Evidence first**: Worker reports are claims. The main session accepts work from actual files, diffs, commands, tests, and reproducible evidence.

Codex Agent Team uses Codex’s native `spawn_agent` primitive. It does not create a second Agent runtime, a persistent task DAG, or a background scheduler, and it does not force every task through detached review.

## Deeper documentation

This README keeps the daily workflow approachable. Implementation details and evidence semantics live here:

- [Plugin Installation](docs/plugin-installation.md)
- [Architecture](docs/architecture.md)
- [Native Subagent Runtime](docs/native-subagent-runtime.md)
- [Model Route Assurance](docs/model-route-assurance.md)
- [Runtime Evidence](plugins/codex-agent-team/skills/codex-agent-team/references/runtime-assurance.md)
- [Compatibility](docs/compatibility.md)
- [Behavioral Evals](docs/behavioral-evals.md)
- [OpenAI References](docs/openai-references.md)
- Policy: [Routing](plugins/codex-agent-team/skills/codex-agent-team/references/routing-policy.md) · [Safety](plugins/codex-agent-team/skills/codex-agent-team/references/safety-policy.md) · [Consent](plugins/codex-agent-team/skills/codex-agent-team/references/consent-policy.md)

## Validation status

CI covers Plugin packaging, the custom-Agent installer lifecycle, routing policy, runtime evidence, and the deterministic verifier across Ubuntu Python 3.11 / 3.12 and macOS Python 3.11. Static tests establish repository contracts; real Codex behavior still depends on live behavioral evaluation and runtime evidence.

## License

[MIT](LICENSE)
