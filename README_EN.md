# Codex Delegate

> A delegation policy layer over Codex Native Subagents. Turn engineering tasks into the smallest useful set of verifiable delegations.

[中文](README.md) · [Installation](docs/plugin-installation.md) · [MIT License](LICENSE)

Codex Delegate turns an engineering task into the smallest useful set of verifiable delegations, and calls Codex Native Subagents only when delegation adds concrete value.

The current main session always owns user intent, scope, consequential decisions, scheduling, acceptance, and the final response. Codex Delegate decides which bounded responsibilities are worth giving to Luna, Terra, or Sol, and when the main session should simply complete the work itself.

Current version: `0.4.0`, pre-v1.

## Quick start

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

Reopen the ChatGPT desktop app, install `Codex Delegate` from the Plugins Directory, then give it a task directly:

```text
/codex-delegate Fix this login retry bug and run the relevant tests.
/codex-delegate Refactor this module while preserving the public API.
/codex-delegate Review this change with emphasis on data consistency and regression risk.
```

You do not need to choose a model or plan the model sequence first.

## How it works

Codex Delegate first asks whether delegation is useful at all. If the task is already clear and local, the main session can finish it directly. Using `0` Subagents is a normal outcome.

When delegation is justified, an execution responsibility is first compiled into a verifiable Delegation Contract covering outcome, scope, invariants, decision rights, acceptance criteria, verification, and stop conditions. Agents are then created only for distinct dependencies that still need to be satisfied.

There is no fixed three-model pipeline. Luna, Terra, and Sol are all optional execution or judgment lanes.

| Role | Model | Primary responsibility |
| --- | --- | --- |
| Main session | current Codex session | understand intent, decide, schedule, accept |
| Luna Reader | GPT-5.6 Luna `max` | search, tracing, test mapping, evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | implementation, debugging, tests, local refactors |
| Terra Investigator | GPT-5.6 Terra `xhigh` | resolve a remaining complex technical dependency |
| Sol Advisor | GPT-5.6 Sol `high` | high-value judgment and selective review |

If Luna misses acceptance, the workflow classifies the failure before escalating. Mechanical defects normally stay with Luna for a focused correction. Contract gaps return to the main session. Terra receives only genuine unresolved technical deltas. Sol is used when a bounded decision or artifact merits higher-value judgment.

## Established evidence is reused

Within the current task, the main session carries forward still-valid test results, interface facts, and other evidence. Later Agents receive relevant established evidence directly, and only evidence affected by changed files, runtime state, or contradictory facts is revalidated.

This reduces repeated discovery, repeated tests, and whole-task restarts. It does not imply a persistent global evidence store shared across independent sessions.

## Parallelism and multiple sessions

The v1 resource envelope is scoped per main session:

```text
0 Subagents: normal outcome
default: 1
normal maximum: 2
hard maximum: 4
```

These limits are per main session, not a machine-wide or account-wide Agent cap. Independent projects may run their own Codex Delegate workflows concurrently.

Writing ownership is scoped to the canonical workspace. The product rule is at most one active Writing Worker for one physical checkout. Separate, genuinely isolated workspaces or worktrees may each have a writer.

Version `0.4.0` is still completing live validation of same-checkout writer exclusion across independent main sessions. Before v1.0.0, if you run multiple independent Codex sessions, avoid having two sessions write the same physical checkout at the same time.

## First run

Codex Delegate uses four project-managed role profiles: Reader, Worker, Investigator, and Advisor. Exact internal profile identifiers and migration rules are documented in the [installation guide](docs/plugin-installation.md).

When a required profile is missing, the Skill explains the Codex-home paths it may manage and asks for permission first. Under its ownership rules, the installer may create or update the four current project profiles, maintain its ownership manifest, and remove a legacy project profile only when exact historical ownership is proven.

It does not edit credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

If installation succeeds but the current task still does not expose the new role, start a fresh Codex task and invoke `/codex-delegate` again.

## Safety boundaries

- The main session retains user intent, task scope, consequential decisions, and final acceptance
- One canonical checkout has a product rule of at most one active Writing Worker
- Child Agents do not create further Subagents; delegation remains one layer deep
- The Skill does not silently switch the main-session model or reasoning effort
- If an exact project profile is unavailable, the affected responsibility returns to the main session instead of silently using a similar role
- A Worker must preserve unrelated user or concurrent-session edits; if workspace drift invalidates the contract, it stops and returns control to the main session
- A Subagent completion report is an execution claim; final acceptance is based on actual files, diffs, tests, and reproducible evidence
- Publishing, deployment, payments, account-permission changes, and other consequential external actions remain under main-session control

## Current release and compatibility

Version `0.4.0` uses the `Codex Delegate` product name and `/codex-delegate` as the canonical user entry point.

To reduce pre-v1 upgrade risk, the GitHub repository slug, Plugin package id, and internal managed-profile namespace temporarily retain `codex-agent-team` compatibility identifiers. Users do not need to rename these resources manually.

Before v1.0.0, three user-relevant areas remain under live validation: cross-session same-checkout writer exclusion, concurrent installer behavior in one Codex home, and the real Plugin upgrade path from `0.3.x` to `0.4.x`. This README does not claim runtime guarantees beyond evidence that has actually been established.

## More information

- [Installation and first run](docs/plugin-installation.md)
- [Project homepage](https://github.com/R-jed/codex-agent-team)

## License

[MIT](LICENSE)
