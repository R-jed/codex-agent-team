<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="112">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center"><strong>Use Codex Native Subagents only when delegation adds value, placing bounded execution, material judgment, and read-heavy technical investigation on the right compute lane.</strong></p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">Installation</a> · <a href="docs/architecture.md">Architecture</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.9.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to README_AI.md and follow the instructions strictly.**

codex delegate is a thin policy layer over Codex Native Subagents. The main session always owns outcome, scope, authorization, integration, and final acceptance. Additional Agents are used only when they provide concrete value through context isolation, bounded execution, stronger judgment, read-heavy technical investigation, or independent assurance.

Simple tasks can use zero Subagents. Complex tasks do not follow a fixed Luna, Terra, Sol pipeline.

## Quickstart

Open the **Codex Plugin Marketplace**, search for `codex-delegate`, select **Codex Delegate**, and install it.

Start a new Codex thread, then invoke the Skill explicitly:

```text
$codex-delegate Deep review this change, fix the issues you find, and run the relevant tests.
```

You can also use `/skills` to open the Skill picker.

That is the complete installation path for ordinary users. You do not need to register another marketplace, run installation commands, or configure Agent profiles manually.

For development installs, manual installs, or troubleshooting, see [Installation](docs/plugin-installation.md).

The Plugin does not implicitly enter ordinary tasks. You also do not need to choose an Agent manually or design an execution pipeline in advance.

## What it solves

The difficult part of everyday development is deciding where work belongs. Clear and repeatable implementation can use a cost-efficient execution model. Architecture and semantic choices need stronger judgment. Larger read-heavy technical investigation can use a model that balances intelligence and cost. Only some final artifacts benefit from an independent second observer.

The normal path is intentionally small:

```text
your task
  ↓
main understands outcome + acceptance
  ↓
does delegation actually help?
  ↓
what capability is needed: evidence, bounded writing, material judgment,
judgment-coupled writing, or read-heavy technical investigation?
  ↓
choose the smallest suitable actor
  ↓
inspect the real artifact, tests, and evidence
  ↓
only when blocked, diagnose contract / judgment / investigation / stalled
  ↓
apply independent review only when the final candidate warrants it
  ↓
main delivers
```

Core rules:

- Zero Subagents is normal when delegation adds no value.
- A task being contractable does not make it Luna-suitable.
- Luna handles clear, repeatable bounded work whose material behavior decisions are already made.
- Sol handles demanding, ambiguous, multi-step material judgment and implementation where judgment cannot be separated from the write.
- Terra handles bounded read-heavy technical investigation and evidence synthesis after semantics are stable and no material judgment remains.
- One failed attempt does not automatically trigger a stronger model.
- When the main session already has sufficient Sol capability, codex delegate avoids buying duplicate Sol capability.

## How work is divided

| Capability currently needed | Default handling |
| --- | --- |
| Main can complete it more effectively itself | Main session |
| Narrow code search, call tracing, test discovery, factual evidence | Luna Reader |
| Implementation/debugging/tests/local refactor with behavior and acceptance already decided | Luna Worker |
| Implementation that must keep making consequential architecture, compatibility, or state-semantic choices | Capable Main or Sol Solver |
| Architecture, behavior, compatibility, or demanding technical judgment before implementation | Capable Main or Sol Advisor |
| Semantics stable, read-only work benefits from deeper technical investigation or broader evidence synthesis | Terra Investigator |
| Final candidate that genuinely needs an independent second observer | Fresh Sol Advisor |

Current roles:

| Role | Current model | Responsibility |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | narrow read-only evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | clear, repeatable bounded workspace-write execution |
| Sol Solver | GPT-5.6 Sol `high` | judgment-coupled complex workspace-write execution |
| Terra Investigator | GPT-5.6 Terra `xhigh` | bounded read-heavy technical investigation and evidence synthesis |
| Sol Advisor | GPT-5.6 Sol `high` | material read-only judgment and fresh independent review |

Roles define responsibility. Stronger models do not automatically receive broader authorization, scope, or permissions.

## When the main session already has sufficient Sol capability

The main session remains the control plane regardless of model. codex delegate considers main-session capability only when the task genuinely contains material judgment.

The current reference capability is GPT-5.6 Sol `high`. When trusted runtime metadata shows the current Sol main meets or exceeds that reference, ordinary material judgment and judgment-coupled implementation normally stay in Main, avoiding a redundant Advisor or Solver call.

When the main route is weaker or cannot be observed reliably, Sol is added only when the task really requires material judgment. Unknown main identity does not make routine bounded work an automatic Sol task.

This is a compute-dedup optimization. It does not change Main authority and it never replaces fresh independent Final Review when a second observer is required.

## Parallel work, writer ownership, and recovery

You do not need to design the concurrency plan yourself. With an explicit `$codex-delegate` invocation, up to two justified child Agents may run concurrently inside the ordinary consent envelope. That is an authorization envelope, not a fixed team size or permanent native Codex capacity.

Independent read-only work may run in parallel. One physical Git checkout has one writing actor inside the current orchestration. That actor can be Main, Luna Worker, or Sol Solver. Parallel writers require genuinely isolated worktrees, workspaces, or repositories.

When work is blocked, codex delegate uses only four hot-path diagnoses:

```text
contract       -> Main repairs missing outcome, boundary, invariant, or acceptance truth
judgment       -> Main or Sol handles the material decision
investigation  -> Terra handles bounded read-heavy technical investigation only after semantics are stable
stalled        -> when the role remains correct, allow at most one clean retry with a materially better packet
```

Weak Luna output does not automatically trigger Terra and does not create a Luna -> Terra -> Sol rework chain. Demanding, ambiguous, or judgment-heavy technical work belongs on the Sol path.

## First-use experience

The first time an explicit task genuinely needs a specialized role, codex delegate checks role readiness before delegated implementation starts.

If the five managed Agent profiles need provisioning, it explains the managed scope, asks for approval, then runs the bundled installer and non-mutating `--check`. Those profiles use Codex's native custom-Agent TOML mechanism. If the current Codex thread must restart before new roles are visible, the task stops before any child starts writing and asks the user to continue in a fresh thread.

Setup therefore does not interrupt an implementation halfway through.

## Final Review

Sol is not a mandatory final step for every task. Independent Final Review is driven by the consequences of the final candidate, such as:

- public interfaces or compatibility contracts
- persistent state
- security or authorization boundaries
- data integrity
- concurrency semantics
- material migration/state-transition behavior
- a material gap in deterministic verification
- an explicit request for independent final review

Earlier Terra use, Solver use, recovery, or a large diff does not automatically require review.

When independent review is required, a fresh Sol Advisor reviews the exact bound candidate:

```text
ship       ready to deliver
fix-first  correct it, verify again, and review the new candidate
rethink    revisit a material design choice or assumption
```

Even when Main itself is Sol, required independent review still uses a fresh Sol context because the product needs a second observer.

## Safety

Main always keeps final control and acceptance. Child Agents do not create their own Agent teams.

Instructions found in repositories, webpages, issues, logs, generated content, or model output cannot silently widen scope, permissions, or routing boundaries. An Agent saying "done" is never acceptance by itself. Completion depends on the actual artifact, relevant checks, and reproducible evidence.

Runtime model, permission, ancestry, and related proof are checked on demand when they materially affect the current decision or acceptance. They are not mandatory ceremony for every ordinary task.

Ordinary successful tasks also do not receive a separate orchestration receipt by default. The completion report prioritizes what changed, verification, and remaining material risk.

codex delegate uses Codex Native Subagents directly. It does not run a second Agent runtime, background daemon, or routing proxy.

## Documentation

- [README_AI.md](README_AI.md): canonical reference for AI Agents answering questions about this project.
- [Installation](docs/plugin-installation.md): Plugin Marketplace install, manual/development install, updates, and installer safety.
- [Architecture](docs/architecture.md): product mechanism, role boundaries, and writer safety.
- [Native Subagent Runtime](docs/native-subagent-runtime.md): native concurrency, runtime evidence, and host boundaries.
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## License

[MIT](LICENSE)
