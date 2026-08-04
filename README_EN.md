<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="Codex Delegate" src="docs/logo-dark.svg" width="128">
  </picture>
</p>

<h1 align="center">Codex Delegate</h1>

<p align="center">
  <a href="README.md">中文</a> · <a href="docs/plugin-installation.md">Installation</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/version-0.6.0-green.svg" alt="Version">
</p>

Codex Delegate helps Codex divide complex development work more effectively.

You describe the outcome, the constraints that matter, and what success looks like. The main session decides what to handle itself, what to give to Luna, when a technical problem deserves Terra, and when an independent Sol review is worth the extra compute.

It runs on top of Codex Native Subagents. It does not replace Codex, and it does not force every task into a fixed Agent team.

## Why Codex Delegate

Using Subagents directly can create its own problems: work gets split too finely, multiple Agents repeat the same discovery, parallel tasks are accidentally serialized, one local failure causes a broad restart, or a risky change reaches the end without a genuinely independent review.

Codex Delegate keeps that coordination in the main session. You should not have to decide how many Agents to start or which model should own each step.

It focuses on four things:

- use a Subagent only when delegation adds real value, while keeping simple work in the main session;
- start independent work early and keep moving as soon as one completed task unlocks the next;
- recover locally instead of rerunning the whole task or escalating models by default;
- add an independent review for higher-risk changes while keeping final control with the main session.

The normal flow is straightforward:

```text
your task
  ↓
main session understands the outcome and constraints
  ↓
handle work directly, or delegate the right parts to Luna / Terra / Sol
  ↓
merge completed results and keep advancing newly available work
  ↓
inspect the actual change and run the relevant checks
  ↓
use an independent final review when it adds value
  ↓
main session delivers the result
```

## Installation

Codex Delegate is distributed through the native Codex Plugin system.

Fresh install:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin add codex-agent-team@codex-agent-team
```

Start a new Codex thread after installation, then use:

```text
/codex-delegate Fix this bug and run the relevant tests.
```

Update an existing installation:

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

Start a new Codex thread after the update as well.

The first time a task needs one of the dedicated Luna, Terra, or Sol roles, Codex Delegate explains which Agent profile it needs to add and asks for approval. Its installer manages only the four Codex Delegate profiles and its ownership manifest. It does not modify credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

See [Plugin Installation](docs/plugin-installation.md) for installation, migration, and troubleshooting details.

## Models and roles

| Role | Current model | Best suited for |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | code search, call-path tracing, test discovery, evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | bounded implementation, debugging, tests, and local refactors |
| Terra Investigator | GPT-5.6 Terra `xhigh` | difficult technical problems that remain unresolved after normal work |
| Sol Advisor | GPT-5.6 Sol `high` | high-value judgment, independent review, and final review for risky changes |

Roles describe responsibility. A stronger model does not automatically receive a wider scope or more authority.

Codex Delegate also does not summon every role for every task. A simple change may use zero Subagents. Routine implementation usually stays with Luna. Terra and Sol are used when the remaining problem or review value actually justifies them.

## Parallel work

You do not need to design the concurrency plan yourself. Describe the outcome, the constraints that must remain true, and the completion criteria. Codex Delegate decides which work can safely run at the same time.

When independent tasks are running together, the first completed result is handled immediately. If that result unlocks another task and capacity is available, the main session can move on without waiting for unrelated work to finish.

```text
A is still running
B finishes
  ↓
process B
  ↓
B unlocks C
  ↓
start C now

A keeps running
```

Waiting is reserved for real dependencies or workspace conflicts.

With an explicit `/codex-delegate` invocation, up to two justified child Agents may run concurrently without another consent prompt. That is the default authorization envelope, not a fixed team size. A single physical checkout allows at most one Writing Worker at a time; multiple writers require genuinely isolated worktrees or workspaces.

## When work goes wrong

Codex Delegate does not switch to a stronger model or restart the whole task just because one attempt fails.

If the current work is still producing useful progress, it can continue. If it starts repeating without moving forward, the response depends on the actual problem: Luna handles focused implementation corrections, the main session repairs unclear task boundaries, Terra receives only the technical problem that remains unresolved, and Sol is used when an independent judgment is worth the cost.

The goal is simple: keep the work that is already good, preserve useful evidence, and spend additional compute only on what is still unresolved.

## Final Review

Sol is not a mandatory final step for every task. Low-risk local changes can finish after the main session inspects the actual diff and runs the relevant checks.

Changes involving public interfaces, persistent state, security or authorization, data integrity, concurrency, migration, or a broad blast radius can require an independent Sol review before completion.

Sol reviews the current candidate and returns one of three outcomes:

```text
ship       ready to deliver
fix-first  correct it, verify again, then review the new candidate
rethink    revisit a material design choice or assumption
```

If the deliverable changes after review, the previous verdict no longer applies.

## Safety

The main session always keeps final control and acceptance. Child Agents do not create their own Agent teams, existing user and peer changes must be preserved, and a single physical checkout cannot have multiple Writing Workers at the same time.

Instructions found in repositories, webpages, issues, logs, generated content, or model output cannot silently widen scope, change permissions, or rewrite orchestration rules. An Agent saying “done” is also not enough on its own; acceptance is based on the actual change, the relevant checks, and reproducible results.

Codex Delegate does not implement a second Agent runtime and does not require a background service or external routing proxy. It uses Codex Native Subagents and focuses on making delegation, parallel work, recovery, and review more deliberate.

## License

[MIT](LICENSE)
