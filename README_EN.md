# Codex Agent Team

[中文](README.md) · [Install](docs/plugin-installation.md) · [Architecture](docs/architecture.md) · [Evals](docs/behavioral-evals.md)

Codex already knows how to spawn Subagents. The harder part in day-to-day development is deciding when delegation helps, which specialist should take the work, who may write to the workspace, when a second opinion is worth the cost, and who ultimately owns the result.

Codex Agent Team is a workflow policy built on Codex native `spawn_agent`. The current Codex session remains the **main session** and keeps ownership of scope, risk, and final acceptance. Luna, Terra, and Sol take bounded responsibilities only when their trigger is met.

## Quick start

Add the project marketplace to Codex:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

Reopen the ChatGPT desktop app and install `Codex Agent Team` from the Plugins Directory.

Invoke it explicitly when needed:

```text
/codex-agent-team
```

You can also describe the development task normally. The Skill first decides whether delegation would help before creating a Subagent.

## How work is assigned

| Role | When it appears | Default route | Responsibility |
| --- | --- | --- | --- |
| Main session | always | current Codex session | understand intent, set scope, own risk, accept work, deliver the final answer |
| Luna | heavy search, code tracing, or bounded implementation | GPT-5.6 Luna `max` | explore, implement, debug, test |
| Terra | a risky change benefits from an independent view | GPT-5.6 Terra `xhigh` | detached review of changes, conflicting evidence, and key assumptions |
| Sol | a high-consequence disagreement remains unresolved and the user consents | GPT-5.6 Sol `high` | one senior judgment |

Luna has `luna_explorer` and `luna_worker` profiles. Terra uses `terra_reviewer` and stays in the reviewer role. Sol uses `sol_judge` and is not a mandatory final step.

There is no fixed pipeline. Small tasks can stay in the main session from start to finish. Terra and Sol appear only when their conditions are actually met.

## A concrete task

Suppose you ask Codex to do this:

```text
Check the payment callback for a concurrency bug, fix it, and run the tests.
If the change crosses a security boundary, add an independent review.
```

The main session first establishes scope, risk, and acceptance checks.

1. If the issue is already well isolated, the main session can edit, test, and finish the task directly.
2. If the work needs substantial search or code tracing, the main session can delegate that bounded responsibility to Luna.
3. If the change crosses a security boundary, Terra can review the actual change independently.
4. Regardless of how many Subagents were used, the result returns to the main session for diff, test, and evidence checks.

Sol would normally stay out of this task. It is reserved for unresolved high-consequence judgment, and the main session asks for user consent before using it.

## Zero Subagents is a normal result

When the task is small, the context is already clear, and the edit location is known, delegation often adds more coordination and verification cost than value. A one-line configuration change, a local bug fix, or a focused test may be completed entirely in the main session.

Task length, file count, or a cheaper model are not enough on their own to justify delegation. The default goal is the smallest team that can complete the work well.

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

## Boundaries

- Zero Subagents is normal. The default is 1, the normal maximum is 2, and the hard maximum is 4.
- There is at most one active Writing Worker per shared workspace.
- Workers do not create another Subagent team; delegation stays one layer deep.
- The Skill never silently switches the main-session model or reasoning effort.
- If Luna is unavailable, Terra does not become an implementation Worker. If Terra is unavailable, review returns to the main session.
- If an exact route, permission boundary, or task scope cannot be established, responsibility returns to the main session.
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

The README covers the normal workflow. Implementation details live here:

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

CI covers Plugin packaging, the custom-Agent installer lifecycle, routing policy, runtime evidence, and the deterministic verifier on Ubuntu Python 3.11 / 3.12 and macOS Python 3.11.

These tests show that the repository rules and tooling satisfy their current contracts. Real Codex behavior still requires live behavioral evaluation and runtime evidence; static repository tests are not presented as task-performance results.

## License

[MIT](LICENSE)
