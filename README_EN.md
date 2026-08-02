# Codex Agent Team

<p align="center">
  <img src="assets/readme/hero.svg" alt="Codex Agent Team: the main session owns the task, Subagents own bounded work" width="100%">
</p>

<p align="center">
  <a href="README.md">中文</a> ·
  <a href="docs/plugin-installation.md">Install</a> ·
  <a href="docs/architecture.md">Architecture</a> ·
  <a href="docs/behavioral-evals.md">Evals</a>
</p>

Codex can already spawn Subagents. The missing piece is operating policy: when to delegate, which specialist to call, who may write to the workspace, when independent review is warranted, and who accepts the result.

Codex Agent Team makes those decisions explicit. The current main session always owns scope, risk, and acceptance. Luna, Terra, and Sol take bounded responsibilities only when their trigger is met.

## Install

Add this repository marketplace to Codex:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

Reopen the ChatGPT desktop app and install `Codex Agent Team` from its marketplace in the Plugins Directory. You can then invoke it explicitly:

```text
/codex-agent-team
```

You can also describe the development task normally. The Skill first decides whether delegation is useful at all.

## One task, one concrete route

<p align="center">
  <img src="assets/readme/example.svg" alt="A payment-callback concurrency issue routed through Codex Agent Team" width="100%">
</p>

Take a concurrency bug in a payment callback. The main session first sets scope and acceptance checks. Heavy tracing or bounded implementation can move to Luna. If the change crosses a security boundary, Terra can review it independently. The result still comes back to the main session for diff, test, and evidence checks.

If the task is already small and isolated, the main session simply completes it. Sol is reserved for rare unresolved high-consequence judgment and requires explicit user consent.

## Operating model

<p align="center">
  <img src="assets/readme/operating-model.svg" alt="Codex Agent Team operating model: one main session with Luna, Terra, and Sol as specialist Subagents" width="100%">
</p>

This is the core of the workflow: the main session owns the full task; each Subagent receives only a bounded responsibility. If a trigger is absent, that specialist is not created.

| Role | Default route | Main responsibility |
| --- | --- | --- |
| Main session | current Codex session | understand intent, set scope, own risk, accept work, deliver the final answer |
| Luna | GPT-5.6 Luna `max` | search, code tracing, bounded implementation, debugging, tests |
| Terra | GPT-5.6 Terra `xhigh` | detached review of risky changes, conflicting evidence, and key assumptions |
| Sol | GPT-5.6 Sol `high` | rare unresolved high-consequence judgment after user consent |

Luna has explorer and worker profiles. Terra is a reviewer, not an implementation fallback. Sol does not sit at the end of every task.

## What you see

When a Subagent is actually created, or when an orchestration check materially changes execution, the Skill adds a compact receipt:

```text
Agent Team
Luna Worker: implemented bounded auth refresh change
Terra Reviewer: triggered by security boundary; verdict clear
Verification: 38 tests passed
```

When the main session handles the task directly:

```text
Agent Team: Main session only
Why: change already isolated; delegation had no concrete benefit
Verification: 12 tests passed
```

The receipt reports observed facts only. Agents that were considered but never created are omitted, and runtime evidence is never claimed when it was not observed.

## Safety boundaries

- Zero Subagents is normal, the default is 1, and the normal maximum is 2.
- There is at most one active writing Worker per shared workspace.
- Workers do not create another Subagent team; delegation stays one layer deep.
- The Skill never silently switches the main session model or reasoning effort.
- If an exact route, permission boundary, or scope cannot be established, responsibility returns to the main session.
- A Subagent completion report is a claim. The main session still accepts the work from actual files, diffs, commands, tests, and reproducible evidence.

The project uses Codex native `spawn_agent`. There is no second Agent runtime, persistent task DAG, or background scheduler in this repository.

<details>
<summary>Why does first use check four Agent profiles?</summary>

Model-specific routes are pinned through four managed custom Agent profiles:

```text
luna_explorer
luna_worker
terra_reviewer
sol_judge
```

If a profile is missing, the Skill first shows the write scope and asks for permission. After approval, it installs and verifies only those four profiles plus their ownership manifest. It does not modify `config.toml`, MCP configuration, credentials, or unrelated Agent profiles.

The Skill then rechecks which roles are visible on the current `spawn_agent` surface. A fresh Codex task is needed only when role discovery has not refreshed yet.

</details>

## Documentation

Use the README for the normal workflow. Use these docs for implementation details:

- [Plugin installation and first run](docs/plugin-installation.md)
- [Architecture](docs/architecture.md)
- [Native Subagent Runtime](docs/native-subagent-runtime.md)
- [Model routing and evidence](docs/model-route-assurance.md)
- [Runtime Evidence](plugins/codex-agent-team/skills/codex-agent-team/references/runtime-assurance.md)
- [Compatibility](docs/compatibility.md)
- [Behavioral Evals](docs/behavioral-evals.md)
- [OpenAI References](docs/openai-references.md)
- Policy: [Routing](plugins/codex-agent-team/skills/codex-agent-team/references/routing-policy.md) · [Safety](plugins/codex-agent-team/skills/codex-agent-team/references/safety-policy.md) · [Consent](plugins/codex-agent-team/skills/codex-agent-team/references/consent-policy.md)

## Current validation scope

CI covers Plugin packaging, the custom-Agent installer lifecycle, routing policy, runtime evidence, and the deterministic verifier on Ubuntu Python 3.11 / 3.12 and macOS Python 3.11. Real Codex behavior still requires live behavioral evaluation and runtime evidence; repository tests are not presented as runtime results.

## License

[MIT](LICENSE)
