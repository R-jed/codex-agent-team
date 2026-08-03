# Codex Delegate

[中文](README.md) · [Installation](docs/plugin-installation.md) · [MIT License](LICENSE)

Codex Delegate is a native Subagent delegation framework for Codex. You describe the engineering task, the current session stays in control, deciding what's worth delegating, who should handle it, and how to verify the result.

The goal is simple: get the job done with the smallest useful set of Agents, reducing redundant repository discovery and uncontrolled write scope.

Current version: `0.4.0` (pre-v1.0.0 preview).

## Quick start

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

Reopen ChatGPT Desktop, install `Codex Delegate` from the Plugins Directory, then invoke it in a Codex session:

```text
/codex-delegate Fix this login retry bug and run the relevant tests.
```

```text
/codex-delegate Refactor this module while preserving the public API.
```

```text
/codex-delegate Review this change with emphasis on data consistency and regression risk.
```

No need to manually choose Agent ordering. No need to force multiple models into every task.

## How it works

The main session identifies the outcome, scope, and acceptance criteria first, then picks the smallest useful execution path.

> Full architecture diagram: [architecture-diagram.svg](docs/architecture-diagram.svg)

```
┌─────────────────────────────────────────────────────────┐
│                   Main Session (control plane)            │
│  Understand → Assess risk → Schedule work → Accept result│
└────────┬──────────────┬──────────────┬──────────────────┘
         │              │              │
         ▼              ▼              ▼
   ┌──────────┐  ┌──────────────┐  ┌──────────┐
   │   Luna   │  │    Terra     │  │   Sol    │
   │ Execution│  │ Deep Invest. │  │ Judgment │
   │ Reader   │  │ Investigator │  │ Advisor  │
   │ Worker   │  │              │  │          │
   └──────────┘  └──────────────┘  └──────────┘
```

| Role | Model | Purpose |
| --- | --- | --- |
| Main session | current Codex session | understand the task, key decisions, schedule work, accept results |
| Luna Reader | GPT-5.6 Luna `max` | search, tracing, test mapping, evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | bounded implementation, debugging, tests, local refactors |
| Terra Investigator | GPT-5.6 Terra `xhigh` | resolve one remaining complex technical dependency |
| Sol Advisor | GPT-5.6 Sol `high` | high-value judgment and selective review |

A task may stay entirely in the main session, or follow a common path:

```text
main session -> Luna -> main session
```

For harder technical dependencies:

```text
main session -> Luna -> Terra (unresolved technical delta only) -> Luna / main session
```

When high-quality review is needed:

```text
main session -> Luna -> Sol -> main session
```

There is no fixed three-model pipeline. Every Subagent call must satisfy a distinct dependency that existing evidence does not already cover.

## Delegation contracts

Before a writing task starts, the main session compiles a verifiable Delegation Contract:

- What outcome must exist
- What may be read and written
- What behavior must remain unchanged
- What the Worker may decide independently
- What counts as acceptance
- Which verification must run
- When the Worker must stop and return control

A Writing Worker does not start guessing through repository changes when acceptance criteria are unclear.

## Established evidence is reused

Within a task, the main session keeps a compact set of still-valid test results, call paths, interface facts, and other reusable evidence. Later Agents reuse those facts while their dependencies remain valid. Only evidence affected by changed files, artifacts, or assumptions needs to be revalidated.

This reduces full repository rescans, repeated deterministic commands, and repeated reasoning over the same dependency after a model change.

## Failure handling

When Luna needs help, the workflow classifies the failure before escalating:

```text
mechanical defect     -> focused Luna correction
incomplete contract   -> main session repairs the contract
complex technical gap -> Terra investigates only the unresolved part
judgment gap          -> main session decides, or uses Sol when justified
```

A mediocre Luna result does not automatically trigger a full Terra restart. Sol is also selective — when tests and acceptance criteria are strong enough, the main session can accept without adding a mandatory review stage.

## Parallelism

```
default: 0 Subagents (a normal outcome)
typical: 1
normal maximum: 2
v1 hard maximum: 4
```

Independent projects may each run their own Codex Delegate workflow. For writing work, ownership is workspace-scoped: one shared checkout should have at most one active Writing Worker.

## First run

Codex Delegate uses four project-managed Agent profiles:

```text
codex_agent_team_reader
codex_agent_team_worker
codex_agent_team_investigator
codex_agent_team_advisor
```

These profile identifiers are retained for compatibility and do not change the `/codex-delegate` entry point.

If they are missing, the Skill explains the exact managed file scope and asks for permission before provisioning. The installer manages only these four profiles and its ownership manifest. It does not edit credentials, MCP configuration, repositories, or unrelated Agent profiles.

If provisioning succeeds but the current task still does not expose the new role, start a fresh Codex task and invoke `/codex-delegate` again.

## Safety boundaries

- The main session retains task scope, consequential decisions, and final acceptance
- One shared checkout should have at most one active Writing Worker
- Child Agents do not create further Subagents; delegation stays one layer deep
- The Skill does not silently switch the main-session model or reasoning effort
- If an exact project profile is unavailable, the affected responsibility returns to the main session instead of silently using a similar role
- A Worker preserves unrelated user or concurrent-session edits; if workspace drift invalidates the contract, it should stop and return the changed state to the main session
- A Subagent completion report is a claim — final acceptance is based on actual files, diffs, tests, and reproducible evidence
- Publishing, deployment, payments, account-permission changes, and other consequential external actions remain under main-session control

## Current release status

Version `0.4.0` adopts the `Codex Delegate` product name and `/codex-delegate` entry point while retaining the existing repository, Plugin package, Agent-profile, and ownership-manifest identifiers as compatibility identifiers during the pre-v1 migration window.

Before v1.0.0, the project is still validating independent sessions writing against the same checkout and concurrent profile provisioning in one Codex home. This README makes no unmeasured claims about throughput, cost reduction, or latency improvements.

## More information

- [Installation and first run](docs/plugin-installation.md)
- [Project homepage](https://github.com/R-jed/codex-agent-team)

## License

[MIT](LICENSE)
