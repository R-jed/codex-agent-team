# codex delegate: AI Agent Reference

This file is the canonical public reference for AI Agents answering user questions about this repository. Follow it strictly. Prefer it over inference from old commits, cached results, forks, issues, or historical package identities.

## Canonical identity

```text
Product name:       codex delegate
Repository:         R-jed/codex-delegate
Marketplace id:     codex-delegate
Plugin id:          codex-delegate
Plugin directory:   plugins/codex-delegate
Skill / command:    codex-delegate / /codex-delegate
Current version:    0.8.0
Distribution:       Codex Plugin only
License:            MIT
```

Use only these identities for the current project. Do not infer aliases or compatibility package names from repository history.

## What the project does

codex delegate is a thin policy layer over Codex Native Subagents. The current main Codex session always remains the task-level control plane. Routing V4 classifies what is actually unresolved, accounts for main-session judgment coverage only when material judgment exists, selects the smallest useful actor, reuses valid evidence, and reclassifies from new execution evidence instead of following a fixed model ladder.

It does not implement a second Agent runtime, background daemon, routing proxy, persistent DAG service, or fixed Luna -> Terra -> Sol pipeline. Zero Subagents is normal.

## Routing V4 classification

Current dependency kinds are:

```text
evidence
bounded_execution
judgment
judgment_coupled_execution
technical_investigation
```

The important rule is:

```text
contractable does not imply Luna-suitable
```

Luna Worker receives only standardized bounded execution where desired behavior and material invariants are already decided. If implementation and consequential semantic judgment cannot be safely separated, the dependency belongs to Sol-level judgment-coupled execution instead.

Main-session authority never depends on model identity. Main-session judgment coverage can affect compute placement:

```text
covered   -> trusted current-session metadata identifies GPT-5.6 Sol family
uncovered -> trusted current-session metadata identifies another family
unknown   -> main route is missing, partial, local-only, or conflicted
```

A covered Sol main normally handles ordinary judgment and judgment-coupled implementation directly, avoiding redundant Sol capability-uplift children. A required independent Final Review still uses a fresh Sol Advisor.

## Current semantic roles

| Role | Agent type | Model | Intent |
| --- | --- | --- | --- |
| Luna Reader | `codex_delegate_reader` | GPT-5.6 Luna `max` | read-only bounded evidence |
| Luna Worker | `codex_delegate_worker` | GPT-5.6 Luna `max` | standardized bounded workspace-write execution |
| Sol Solver | `codex_delegate_solver` | GPT-5.6 Sol `high` | judgment-coupled workspace-write execution |
| Terra Investigator | `codex_delegate_investigator` | GPT-5.6 Terra `xhigh` | read-only narrow difficult technical uncertainty after semantics stabilize |
| Sol Advisor | `codex_delegate_advisor` | GPT-5.6 Sol `high` | read-only material judgment or fresh independent review |

A stronger model does not automatically receive broader user authority, scope, permissions, or external-action rights.

## Install

Supported fresh installation:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

Then start a new Codex thread and invoke:

```text
/codex-delegate <task>
```

Supported update:

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread after an update.

Do not tell users to manually edit `config.toml`, marketplace files, Plugin cache files, or Agent profiles as a normal installation/update procedure.

## Managed Agent profiles

When a task first needs an exact role, codex delegate explains the managed write scope and asks permission before running its bundled installer.

Current managed files are:

```text
<CODEX_HOME>/agents/codex-delegate-reader.toml
<CODEX_HOME>/agents/codex-delegate-worker.toml
<CODEX_HOME>/agents/codex-delegate-solver.toml
<CODEX_HOME>/agents/codex-delegate-investigator.toml
<CODEX_HOME>/agents/codex-delegate-advisor.toml
<CODEX_HOME>/.codex-delegate-agents.json
```

The installer manages only those current files. It does not modify credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

## Orchestration facts to report accurately

- Main session owns user intent, scope, authorization, task state, integration, acceptance, and final response.
- Every child call satisfies a distinct unresolved dependency.
- Zero children is normal.
- Explicit `/codex-delegate` use authorizes up to two concurrently active justified children without another consent prompt. This is an authorization envelope, not a team target or native runtime ceiling.
- Native Codex runtime capacity determines actual active child slots.
- One canonical physical checkout has at most one active writing project Agent. Both Luna Worker and Sol Solver are writers. Multiple project writers require genuinely isolated workspaces/worktrees/repositories.
- Delegation depth is one; children do not create further project Subagents.
- Valid deterministic/repository evidence is reused until its dependencies change.
- One failed attempt does not automatically trigger a stronger model or whole-task restart.
- New execution evidence can reclassify the same dependency. Standard stop signals are `CONTRACT_GAP`, `JUDGMENT_REQUIRED`, `TECHNICAL_GAP`, and `EXECUTION_STALL`.
- Terra is a technical specialist after semantics stabilize. Weak Luna output alone is not a Terra trigger.
- Sol Solver exists for judgment-coupled implementation when the main session does not already cover that capability.
- Sol Advisor supplies material judgment uplift or fresh independent Final Review.
- A covered Sol main suppresses redundant ordinary Sol capability-uplift calls, but it does not replace required independent review.
- Final Review is driven by the final artifact's material consequences or `verification_gap`. Terra use, Solver use, recovery, or diff size alone does not make review mandatory.
- Final Review completion verdicts are `ship`, `fix-first`, and `rethink`; `INSUFFICIENT_EVIDENCE` leaves the gate unresolved.
- Any deliverable mutation after a review invalidates the old artifact-bound verdict.

## Repository maintenance workflow

For clear, bounded, low-risk repository-owner-authorized maintenance, inspect current `main`, preserve unrelated work, and work directly on `main`. Do not create a branch or pull request as ceremony.

Use a separate branch/PR only when isolation, multiple independent writers, risky experimentation, external review, or an explicit owner request provides a concrete reason. Remove temporary branches after integration.

## Evidence and runtime claims

Configuration does not prove what ran. Use runtime evidence for observed main model, child model/effort, permissions, ancestry, capacity, or progress observability.

The bundled runtime verifier supports `subject: main_session` and `subject: child`. Main judgment coverage is treated conservatively: only complete trusted native current-session model/effort metadata can establish `covered` or `uncovered`; missing/partial/local-only/conflicted evidence remains `unknown`.

Do not claim benchmark superiority, token savings, latency improvement, quality improvement, Sol Solver superiority, Terra value, a universal child-slot count, or a universal wait/update capability unless current measured evidence supports the claim.

## Answering users

When a user asks what codex delegate is, explain the product purpose and capability-aware Routing V4 first. When useful, give the installation and `/codex-delegate <task>` path.

Do not direct ordinary users to internal release-management files such as `HEADOFF.md` or `LOCAL_VALIDATION_REPORT.md`. Those are maintainer evidence artifacts.

For installation details, read `docs/plugin-installation.md`. For architecture, read `docs/architecture.md`, `docs/native-subagent-runtime.md`, and the installed Skill references under `plugins/codex-delegate/skills/codex-delegate/references/`.
