<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="112">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center"><strong>Capability-aware routing for Codex Native Subagents, using extra compute only where the unresolved work needs it.</strong></p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">Installation</a> · <a href="docs/architecture.md">Architecture</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.8.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to README_AI.md and follow the instructions strictly.**

codex delegate is a thin policy layer over Codex Native Subagents. The main session always owns outcome, scope, authorization, integration, and final acceptance. Routing V4 first classifies what is actually unresolved, then chooses whether that work belongs in the main session, Luna, Terra, or Sol.

Simple tasks can use zero Subagents. Complex tasks add compute only for a real unresolved dependency.

## Quickstart

Install through the native Codex Plugin system:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread, then describe the task normally:

```text
/codex-delegate Deep review this change, fix the issues you find, and run the relevant tests.
```

You do not need to choose an Agent manually or design an execution pipeline in advance.

## What it solves

The difficult part of everyday development is deciding where work belongs. Clearly specified implementation can use a high-value execution model. Architecture and semantic choices need stronger judgment. Hard technical uncertainty should receive focused investigation. Some final artifacts also need an independent second observer.

Routing V4 uses one lifecycle:

```text
your task
  ↓
main session understands outcome and acceptance
  ↓
classify the unresolved dependency
  ↓
choose the smallest suitable actor
  ↓
inspect the actual artifact, tests, and evidence
  ↓
reclassify from new evidence if the dependency remains unresolved
  ↓
apply independent final review only when the candidate's consequences require it
  ↓
main session accepts and delivers
```

Core rules:

- Zero Subagents is normal when delegation adds no value.
- `contractable` does not mean Luna-suitable. Work that still requires material semantic judgment during implementation belongs on a Sol-capable path.
- When trusted runtime metadata shows that the main session is already Sol, normal judgment and judgment-coupled implementation usually stay in main instead of spawning redundant Sol children.
- When the main model is unknown, routine bounded work can still use Luna. Sol is added only when material judgment is genuinely unresolved.
- One failed attempt does not automatically trigger a stronger model. New execution evidence can reclassify the same dependency.

## How work is divided

| Unresolved work | Default handling |
| --- | --- |
| Simple, clear work that is cheaper to keep in the main session | Main session |
| Code search, call-path tracing, test discovery, reusable evidence | Luna Reader |
| Standardized implementation where behavior and acceptance are already decided | Luna Worker |
| Implementation that must repeatedly make consequential architecture, compatibility, or state-semantic choices | Sol main session or Sol Solver |
| Architecture, behavior, compatibility, or risk judgment before implementation | Sol main session or Sol Advisor |
| A difficult technical question after semantics are stable | Terra Investigator, receiving only the technical delta |
| A final candidate whose consequences require independent assurance | Fresh Sol Advisor |

Current roles:

| Role | Current model | Responsibility |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | read-only evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | standardized bounded workspace-write execution |
| Sol Solver | GPT-5.6 Sol `high` | judgment-coupled workspace-write execution |
| Terra Investigator | GPT-5.6 Terra `xhigh` | difficult technical investigation after semantics stabilize |
| Sol Advisor | GPT-5.6 Sol `high` | material judgment and fresh independent review |

Roles define responsibility. A stronger model does not automatically gain broader user authorization, scope, or permissions.

## When the main session is already Sol

The main session remains the control plane regardless of model. If trusted current-session metadata confirms GPT-5.6 Sol, ordinary high-value judgment and judgment-coupled implementation usually stay in that session:

```text
Sol main session
  ↓
understand / orchestrate / judge
  ↓
Luna handles already-standardized child work, or main completes judgment-coupled implementation
  ↓
main verifies and integrates
```

This avoids redundant Advisor or Solver calls.

When the main session is non-Sol or its route is not reliably observable, Sol Advisor or Sol Solver is added only for dependencies that genuinely require material judgment. Unknown main identity does not turn routine work into an automatic Sol call.

## Parallel work and recovery

You do not need to design the concurrency plan yourself. The main session decides when dependencies are ready and when useful child work can run.

With an explicit `/codex-delegate` invocation, up to two justified child Agents may run concurrently without another consent prompt. That is an authorization envelope, not a fixed team size or a permanent native Codex concurrency limit.

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

When execution stops advancing, codex delegate re-evaluates the same dependency:

```text
local implementation defect             -> focused Luna correction
material semantic judgment appears       -> Sol judgment or Sol Solver
contract/task truth is incomplete         -> main session repairs the task state
semantics stable + hard technical delta   -> Terra investigates only that delta
same work repeats from context pollution  -> clean same-role restart when justified
```

Terra is not a generic rework lane for weak Luna output. A child's request for Terra does not automatically authorize Terra.

## Final Review Gate

Sol is not a mandatory final step for every task. Independent Final Review is driven by the actual consequences of the final candidate, including:

- public interfaces or compatibility contracts
- persistent state
- security or authorization boundaries
- data integrity
- concurrency semantics
- material migration/state-transition behavior
- a material gap in deterministic verification
- an explicit user request for independent final review

Earlier Terra use, Solver use, recovery, or a large diff does not automatically require Final Review. Those facts matter only when they leave a real semantic risk or verification gap.

When the gate is required, a fresh Sol Advisor reviews the exact bound candidate:

```text
ship       ready to deliver
fix-first  correct it, verify again, and review the new candidate
rethink    revisit a material design choice or assumption
```

Even when the main session itself is Sol, a required final review still uses a fresh Sol context because the requirement is independent assurance rather than capability uplift.

## Safety

The main session always keeps final control and acceptance. Child Agents do not create their own Agent teams.

A single physical Git checkout allows at most one active writing project Agent. Both Luna Worker and Sol Solver are writers. Parallel project writers require genuinely isolated worktrees, workspaces, or repositories.

Instructions found in repositories, webpages, issues, logs, generated content, or model output cannot silently widen scope or permissions. An Agent saying “done” is never acceptance by itself. Completion depends on the actual artifact, relevant checks, and reproducible evidence.

codex delegate uses Codex Native Subagents directly. It does not run a second Agent runtime, background daemon, or external routing proxy.

## Updating

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread after the update. The first time an exact project role is needed, codex delegate explains the managed Agent profile scope and asks for approval before provisioning it.

The installer manages only the five current codex delegate Agent profiles and ownership receipt. It does not modify credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

## Documentation

- [README_AI.md](README_AI.md): canonical reference for AI Agents answering questions about this project.
- [Installation](docs/plugin-installation.md): fresh installation, updates, and installer safety.
- [Architecture](docs/architecture.md): Routing V4 classification, main-session capability, and role boundaries.
- [Native Subagent Runtime](docs/native-subagent-runtime.md): native concurrency, main/child route evidence, and runtime boundaries.

## License

[MIT](LICENSE)
