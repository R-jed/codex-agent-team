# Codex Delegate

[中文](README.md) · [Installation](docs/plugin-installation.md) · [MIT License](LICENSE)

Codex Delegate is a native Subagent delegation workflow for Codex. You describe the engineering task, the current Codex session remains the **main session**, and the workflow decides which responsibilities are worth delegating, which role should handle them, which evidence can be reused, and how the final result should be accepted.

The goal is simple: delegate to the smallest useful set of Agents while reducing repeated repository discovery, redundant multi-model inference, and uncontrolled write scope.

Current version: `0.4.0`, pre-v1.0.0 preview.

## Install

Add the repository to the Codex Plugin marketplace:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

Reopen ChatGPT Desktop and install `Codex Delegate` from the Plugins Directory.

Invoke it in a Codex session with:

```text
/codex-delegate
```

The GitHub repository and Plugin package currently retain the `codex-agent-team` compatibility identifier, so the marketplace source URL has not changed yet.

## How to use it

Give it a normal engineering task, for example:

```text
/codex-delegate Fix this login retry bug and run the relevant tests.
```

```text
/codex-delegate Refactor this module while preserving the public API.
```

```text
/codex-delegate Review this change with emphasis on data consistency and regression risk.
```

You do not need to choose the Luna, Terra, and Sol order manually, and you do not need to force multiple Agents into every task.

## How delegation works

The main session first identifies the outcome, scope, risk, and acceptance criteria, then chooses the smallest useful execution path.

| Role | Current route | Purpose |
| --- | --- | --- |
| Main session | current Codex session | understand the task, make key decisions, schedule work, accept results |
| Luna Reader | GPT-5.6 Luna `max` | search, tracing, test mapping, evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | bounded implementation, debugging, tests, and local refactors |
| Terra Investigator | GPT-5.6 Terra `xhigh` | resolve one remaining complex technical dependency |
| Sol Advisor | GPT-5.6 Sol `high` | high-value judgment and selective review |

A task may stay entirely in the main session:

```text
main session
```

A common implementation path is:

```text
main session -> Luna -> main session
```

A harder technical dependency may use:

```text
main session -> Luna -> Terra (unresolved technical delta only) -> Luna / main session
```

A consequential finished artifact may use:

```text
main session -> Luna -> Sol -> main session
```

There is no fixed three-model pipeline. Every Subagent call must satisfy a distinct dependency that the current valid evidence does not already cover.

## Writing work gets bounded before execution

When a task requires file changes, the main session first turns the responsibility into an enforceable Delegation Contract covering:

```text
what outcome must exist
what may be read and written
what behavior must remain unchanged
what the Worker may decide independently
what counts as acceptance
which verification must run
when the Worker must stop and return control
```

If critical decision rights or acceptance criteria are still unclear, a Writing Worker should not start guessing through repository changes.

## Established evidence is reused

Within a task, the main session keeps a compact set of still-valid test results, call paths, interface facts, and other reusable evidence.

Later Agents reuse those facts while their dependencies remain valid. Only evidence affected by changed files, artifacts, or assumptions needs to be revalidated.

This reduces full repository rescans, repeated deterministic commands, and repeated reasoning over the same dependency after a model change.

## When Luna needs help

The workflow classifies the failure before escalating:

```text
mechanical defect     -> focused Luna correction
incomplete contract   -> main session repairs the contract
complex technical gap -> Terra investigates only the unresolved part
judgment gap          -> main session decides, or uses Sol when justified
```

A mediocre Luna result does not automatically trigger a full Terra restart.

Sol is also selective. When tests and the acceptance oracle are already strong enough, the main session can accept the result without adding a mandatory review stage.

## Parallelism and multiple sessions

The default resource envelope is:

```text
0 Subagents is a normal outcome
default: 1
normal maximum: 2
v1 hard maximum: 4
```

Independent projects may each run their own Codex Delegate workflow. The project does not impose a machine-wide or account-wide Agent total.

For writing work, ownership is workspace-scoped: one canonical physical checkout should have at most one active Writing Worker. Truly isolated worktrees or independent projects may have independent Writers.

Version `0.4.0` is still in pre-v1 runtime validation. Until v1.0.0 ships, avoid starting simultaneous writing tasks from two independent Codex sessions against the same physical checkout.

## First run

Codex Delegate currently uses four project-managed custom Agent profiles:

```text
codex_agent_team_reader
codex_agent_team_worker
codex_agent_team_investigator
codex_agent_team_advisor
```

These profile identifiers are retained for compatibility and do not change the `/codex-delegate` entry point.

If they are missing, the Skill explains the exact managed file scope and asks for permission before provisioning them. The installer manages only these four profiles and its ownership manifest. That authorization does not extend to credentials, MCP configuration, repository files, or unrelated Agent profiles.

If provisioning succeeds but the current task still does not discover the new roles, start a fresh Codex task and invoke `/codex-delegate` again.

## Safety boundaries

- The main session retains task scope, consequential decisions, and final acceptance.
- One shared physical checkout should have at most one active Writing Worker.
- Child Agents do not create further Subagents; delegation stays one layer deep.
- The Skill does not silently switch the main-session model or reasoning effort.
- If an exact project profile is unavailable or conflicting, the affected responsibility returns to the main session instead of silently using a similar role.
- A Worker preserves unrelated user or concurrent-session edits. If workspace drift makes the contract stale, it should stop and return the changed state to the main session.
- A Subagent completion report is a claim. Final acceptance is based on actual files, diffs, tests, commands, and reproducible evidence.
- Publishing, deployment, payments, account-permission changes, and other consequential external actions remain under main-session control and the user's current authorization.

## Current release status

Version `0.4.0` adopts the `Codex Delegate` product name and `/codex-delegate` entry point while retaining the existing repository, Plugin package, Agent-profile, and ownership-manifest identifiers for migration compatibility.

Before v1.0.0, the project is still validating a small number of real-runtime boundaries, including independent sessions writing against the same checkout and concurrent profile provisioning in one Codex home. This README therefore makes no unmeasured claims about throughput, cost reduction, latency improvements, or cross-session exclusion guarantees.

Running different Plugin generations that expect different managed profile generations in one Codex home is outside the v1 support contract. An exact-route mismatch should stop the affected delegation rather than trigger cross-role substitution.

## More information

- [Installation and first run](docs/plugin-installation.md)
- [Project homepage](https://github.com/R-jed/codex-agent-team)

## License

[MIT](LICENSE)
