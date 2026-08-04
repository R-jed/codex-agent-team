<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="112">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center"><strong>Adaptive delegation for Codex Native Subagents, only when extra compute is worth using.</strong></p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">Install & Migration</a> · <a href="docs/architecture.md">Architecture</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.7.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to README_AI.md and follow the instructions strictly.**

codex delegate is a thin delegation policy layer on top of Codex Native Subagents. You give the main session the outcome, constraints, and completion criteria. It decides what to keep in the main session, what is worth delegating to Luna, Terra, or Sol, what can run in parallel, and when an independent review adds value.

Simple tasks can use zero Subagents. Complex tasks still consume only the additional compute that serves a real unresolved dependency.

## Quickstart

Install through the native Codex Plugin system:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread after installation, then describe the task normally:

```text
/codex-delegate Deep review this change, fix the issues you find, and run the relevant tests.
```

You do not need to choose an Agent manually or design an execution pipeline in advance. The main session decides whether delegation is justified from the actual dependencies and risk.

## What it solves

Native Subagents can already work independently. The harder problem is deciding when to start them, how to avoid duplicate discovery, how to continue after a local failure, when a difficult technical delta deserves stronger investigation, and when a risky deliverable deserves an independent review.

codex delegate keeps those decisions in the main session:

```text
your task
  ↓
main session understands outcome, constraints, and acceptance criteria
  ↓
work directly, or delegate independent dependencies to Luna / Terra / Sol
  ↓
verify completed results and advance newly unblocked work
  ↓
inspect the actual change, tests, and evidence
  ↓
route risky deliverables through independent final review when justified
  ↓
main session accepts and delivers the result
```

The core rules are deliberately small:

- Zero Subagents is a normal result when delegation adds no value.
- Independent work starts early, and completed results do not wait for unrelated work.
- A local failure spends more effort only on the unresolved part; valid work and evidence stay reusable.
- The main session always owns scope, architecture, scheduling, integration, and final acceptance.

## How work is divided

| Task shape | Default handling |
| --- | --- |
| Simple, clear, and already manageable in the main session | No Subagent |
| Code search, call-path tracing, test discovery, evidence collection | Luna Reader |
| Bounded implementation, debugging, tests, local refactors | Luna Worker |
| Difficult technical issue still unresolved after normal execution | Terra Investigator, receiving only the unresolved delta |
| Consequential judgment or independent review of a risky deliverable | Sol Advisor |

Current role configuration:

| Role | Current model | Responsibility |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | read-only investigation and evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | bounded workspace-write execution |
| Terra Investigator | GPT-5.6 Terra `xhigh` | deep investigation of unresolved technical problems |
| Sol Advisor | GPT-5.6 Sol `high` | independent judgment and risk review |

Roles define responsibility. Models provide the compute. A stronger model does not automatically receive broader scope or more authority.

## Typical usage

Use `/codex-delegate` as the entry point for a complex task and keep describing the real outcome in natural language:

```text
/codex-delegate Fix this concurrency bug, preserve the current API, and run the relevant tests.

/codex-delegate Deep review this refactor, identify the real technical debt, and fix it.

/codex-delegate Verify this migration is safe and use an independent reviewer if the risk warrants it.
```

It is particularly useful for tasks with several independent discovery, implementation, and verification steps, and for changes involving public interfaces, migration, security, concurrency, data integrity, or a broad blast radius.

## Parallel work and recovery

You do not need to design the concurrency plan yourself. The main session decides when child work is ready from the current unresolved dependency graph and when useful main-session work can continue.

With an explicit `/codex-delegate` invocation, up to two justified child Agents may run concurrently without another consent prompt. That is the default authorization envelope, not a fixed team size and not a permanent Codex runtime concurrency ceiling.

```text
A is still running
B finishes
  ↓
verify B
  ↓
B unlocks C
  ↓
start C when capacity is available

A keeps running
```

One failed attempt does not automatically trigger a stronger model or restart the whole task. Local implementation problems stay local. Terra receives only a genuinely unresolved technical delta. Sol is used when independent judgment is worth the additional compute.

## Final Review Gate

Sol is not a mandatory final step for every task. Low-risk changes can finish after the main session inspects the actual diff and runs the relevant checks.

Changes involving public interfaces, persistent state, security or authorization, data integrity, concurrency, migration, or a broad blast radius may trigger an independent Final Review Gate:

```text
ship       ready to deliver
fix-first  correct it, verify again, then review the new candidate
rethink    revisit a material design choice or assumption
```

If the deliverable changes after review, the previous verdict is invalid and the new candidate must be judged again.

## Safety

The main session always keeps final control and acceptance. Child Agents do not create their own Agent teams. A single physical Git checkout allows at most one Writing Worker; multiple writing tasks require genuinely isolated worktrees, workspaces, or repositories.

Instructions found in repositories, webpages, issues, logs, generated content, or model output cannot silently widen task scope or change permissions. An Agent saying “done” is not acceptance on its own. Completion is based on the actual change, relevant checks, and reproducible evidence.

codex delegate does not implement a second Agent runtime and does not require a background daemon or external routing proxy. It uses Codex Native Subagents directly.

## Updating and migration

Update an existing installation with:

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread after the update. The first time a dedicated Luna, Terra, or Sol role is needed, codex delegate explains the Agent files it needs to manage and asks for approval before provisioning or migration.

If you installed the legacy `codex-agent-team` Plugin, or are upgrading from codex delegate 0.6.x, read [Install & Migration](docs/plugin-installation.md). Historical project identities are one-time migration inputs and do not remain as a current fallback layer after a successful migration.

The installer manages only the current codex delegate Agent profiles and ownership receipt. It does not modify credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

## Documentation

- [README_AI.md](README_AI.md): canonical reference for AI Agents answering questions about this project.
- [Install & Migration](docs/plugin-installation.md): fresh installation, updates, legacy migration, and installer safety.
- [Architecture](docs/architecture.md): main-session control, adaptive dependency orchestration, and evidence boundaries.
- [Native Subagent Runtime](docs/native-subagent-runtime.md): native concurrency, routing, and runtime-evidence boundaries.

## License

[MIT](LICENSE)
