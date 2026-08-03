<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="Codex Delegate" src="docs/logo-dark.svg" width="128">
  </picture>
</p>

<h1 align="center">Codex Delegate</h1>

<p align="center">
  A delegation policy layer over Codex Native Subagents.<br>
  <a href="README.md">中文</a> · <a href="docs/plugin-installation.md">Installation</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/version-0.5.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/status-pre--v1-orange.svg" alt="Status">
</p>

Codex Delegate turns an engineering task into the smallest useful set of verifiable delegations. It creates Codex Native Subagents only when delegation adds concrete value to an unresolved dependency.

The current main session always owns user intent, scope, consequential decisions, scheduling, acceptance, and the final response. Luna, Terra, and Sol are selectable execution or judgment resources. There is no fixed model pipeline and no fixed Agent count.

Current version: `0.5.0`, pre-v1.

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

You do not need to choose a model, Agent count, or model sequence first.

## How it works

Codex Delegate first identifies which dependencies are still unresolved and which of them are worth delegating.

If the work is already clear and local, the main session can finish it directly. Using `0` Subagents is a normal outcome.

When delegation is useful, the responsibility is compiled into a verifiable Delegation Contract covering dependency, outcome, scope, interfaces, invariants, decision rights, acceptance, verification, and stop conditions. Only responsibilities that are ready and add distinct value are scheduled.

| Role | Model | Primary responsibility |
| --- | --- | --- |
| Main session | current Codex session | understand intent and dependencies, decide, schedule, accept |
| Luna Reader | GPT-5.6 Luna `max` | search, tracing, test mapping, evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | implementation, debugging, tests, local refactors |
| Terra Investigator | GPT-5.6 Terra `xhigh` | resolve a remaining complex technical dependency |
| Sol Advisor | GPT-5.6 Sol `high` | high-value judgment and selective review |

Task size does not automatically select a stronger model. A large but clear dependency can stay with Luna, while a small change may justify Sol when it crosses an important architecture, security, migration, or public-contract boundary.

## No fixed Agent count

Codex Delegate decides whether to parallelize from the currently ready independent dependencies. It does not preconfigure a `1 / 2 / 4` team shape.

When `/codex-delegate` is explicitly invoked, up to two concurrently active justified child Agents fit inside the normal no-extra-consent resource envelope. If more Agents should run at the same time and broad parallel work was not already authorized, Codex Delegate explains why and asks first.

After consent, actual concurrency is determined by:

```text
ready independent dependencies
workspace safety
currently available Codex runtime child slots
```

If the runtime does not currently expose enough slots, remaining dependencies wait or run in later waves. Codex Delegate does not duplicate a question to keep slots busy and does not silently change roles because capacity is tight.

## Established evidence is reused

Within the current task, the main session carries forward still-valid test results, interface facts, and other evidence. Later Agents receive relevant established evidence directly, and only evidence affected by changed files, runtime state, or contradictory facts is revalidated.

This reduces repeated discovery, repeated tests, and whole-task restarts. Independent sessions do not currently share a persistent global evidence store.

## What happens when execution stalls

An Agent saying that it made progress does not automatically justify another attempt. The main session checks actual artifacts, deterministic verification, failure signatures, and new evidence.

When acceptance is not reached, Codex Delegate chooses recovery from the evidence:

- a concrete local mechanical defect can return to Luna for a focused correction;
- an incomplete contract returns to the main session for repair;
- repeated unproductive context can trigger a clean same-lane restart using the current artifact and valid evidence;
- an evidence-supported complex technical capability gap sends only the unresolved delta to Terra;
- a consequential judgment stays with the main session or uses Sol when appropriate.

There is no fixed retry count and no automatic model upgrade after a failure.

## Parallelism and multiple sessions

Independent projects may run their own Codex Delegate workflows concurrently.

Writing ownership is scoped to the canonical workspace. One physical checkout has at most one active Writing Worker. Separate, genuinely isolated workspaces or worktrees may each have a writer.

Version `0.5.0` is still completing live validation of same-checkout writer exclusion across independent main sessions. Before v1.0.0, if you run multiple independent Codex sessions, avoid having two sessions write the same physical checkout at the same time.

## First run

Codex Delegate uses four project-managed role profiles: Reader, Worker, Investigator, and Advisor. Exact internal profile identifiers and migration rules are documented in the [installation guide](docs/plugin-installation.md).

When a required profile is missing or an exactly project-managed earlier generation needs upgrading, the Skill explains the Codex-home paths it may manage and asks for permission first. The installer creates, updates, or migrates only project-owned profiles and its ownership manifest when ownership rules permit.

It does not edit credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

If installation succeeds but the current task still does not expose the new role, start a fresh Codex task and invoke `/codex-delegate` again.

## Safety boundaries

- The main session retains user intent, task scope, consequential decisions, and final acceptance
- One canonical checkout has at most one active Writing Worker
- Child Agents do not create further Subagents; delegation remains one layer deep
- The Skill does not silently switch the main-session model or reasoning effort
- If an exact project profile is unavailable, the affected responsibility returns to the main session instead of silently using a similar role
- A Worker must preserve unrelated user or concurrent-session edits; if workspace drift invalidates the contract, it stops and returns control to the main session
- A Subagent completion report is an execution claim; final acceptance is based on actual files, diffs, tests, and reproducible evidence
- Publishing, deployment, payments, account-permission changes, and other consequential external actions remain under main-session control

## Current release and compatibility

Version `0.5.0` keeps the `Codex Delegate` product name and `/codex-delegate` canonical entry point while moving scheduling to dependency- and execution-evidence-driven orchestration.

To reduce pre-v1 upgrade risk, the GitHub repository slug, Plugin package id, and internal managed-profile namespace temporarily retain `codex-agent-team` compatibility identifiers. Users do not need to rename these resources manually.

Before v1.0.0, live validation still covers real Plugin upgrades, cross-session same-checkout writer exclusion, concurrent installer behavior in one Codex home, and native fan-out capacity/slot recovery. This README describes the current product contract without presenting uncompleted runtime tests as established guarantees.

## License

[MIT](LICENSE)
