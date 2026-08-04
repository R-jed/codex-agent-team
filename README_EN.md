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
  <img src="https://img.shields.io/badge/status-pre--v1-orange.svg" alt="Status">
</p>

Codex Delegate is **a delegation policy layer over Codex Native Subagents**. The main session keeps ownership of the outcome, architecture, consequential decisions, and final acceptance. Only responsibilities that are worth isolating and can be bounded cleanly are delegated.

Current version: `0.6.0`, pre-v1.

## 1. What it solves

Codex already has native Subagents and parallel execution. The harder engineering problem is how the main session uses those capabilities:

- which work is worth delegating;
- which dependencies can run concurrently and which must stay serial;
- how to avoid duplicate discovery and duplicate implementation;
- whether a failure calls for continued work, a repaired contract, a clean context, or stronger technical investigation;
- when an independent Sol review is worth the additional compute;
- how actual diffs, tests, and runtime evidence determine completion.

Codex Delegate keeps those decisions in the current main session. There is **No fixed Agent count** and no mandatory `Luna -> Terra -> Sol` pipeline.

```text
user outcome
  ↓
main session identifies unresolved dependencies
  ↓
compute the current ready frontier
  ↓
delegate only responsibilities with concrete value and enforceable acceptance
  ↓
run safe independent work concurrently
  ↓
when any child completes, merge that evidence and recompute the frontier
  ↓
recover, investigate, or independently review only when justified
  ↓
main session accepts the actual deliverable
```

A clear local change may use zero Subagents. A difficult task does not automatically invoke every model.

## 2. Installation

Codex Delegate is distributed only through the native Codex Plugin system.

Fresh install:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin add codex-agent-team@codex-agent-team
```

Start a **new Codex thread** after installation, then use:

```text
/codex-delegate Fix this bug and run the relevant tests.
```

Existing installation:

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

Start a new Codex thread after upgrade/reinstall as well.

### First use of model-specific custom Agents

The Plugin distributes the Skill and project bundle. The four custom Agent profiles use Codex's separate Agent configuration surface under:

```text
$CODEX_HOME/agents
```

normally `~/.codex/agents`.

Codex Delegate does not silently write those profiles during Plugin installation. When a task first justifies a model-specific role and the exact profile is unavailable, the Skill explains the managed scope and asks for approval.

The installer manages only the four Codex Delegate profiles and its ownership manifest. It does not edit credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles. The Plugin manifest does not invent an `agents` component.

See [Plugin Installation](docs/plugin-installation.md) for migration, ownership, upgrade, and failure behavior.

## 3. Roles and responsibility

| Role | Current model | Primary responsibility |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | search, call-path tracing, test mapping, evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | bounded implementation, debugging, tests, local refactors |
| Terra Investigator | GPT-5.6 Terra `xhigh` | one genuine unresolved complex technical delta |
| Sol Advisor | GPT-5.6 Sol `high` | high-value judgment, selective review, risk-triggered independent final review |

Roles express responsibility. Models are compute resources. A stronger model does not automatically gain broader product, architecture, permission, or scope authority.

The main session first turns the task into unresolved dependencies. A writing responsibility is delegated only when scope, interfaces, invariants, decision rights, acceptance, and verification are clear enough to enforce.

## 4. Concurrency and actual performance

Users should not have to manually tell Codex "spawn two Agents here" or identify every parallel branch themselves. In normal use, describe the **outcome, constraints that must remain true, and observable success criteria**. Codex Delegate is responsible for identifying which dependencies are ready and whether concurrency creates real value.

Scheduling is completion-driven around the ready frontier:

```text
start the current safe, useful ready work
        ↓
any child completes
        ↓
inspect it, merge evidence, close the completed child
        ↓
recompute the ready frontier
        ↓
a slot is free and a new dependency is ready
        ↓
refill immediately instead of waiting for the whole previous wave
```

A barrier wait is appropriate only when a real join dependency requires all active results, or when the current Codex runtime exposes only a coarser waiting surface.

So performance is not determined mainly by prompt wording. Prompt clarity helps the main session understand acceptance and dependency boundaries, but wall-clock performance also depends on:

- whether the task actually contains independent dependencies;
- whether the main session uses completion-driven scheduling instead of avoidable batch barriers;
- the child capacity and completion-notification surface exposed by the current native Codex runtime;
- write conflicts and genuinely serial critical-path work;
- real model and verification latency;
- duplicate discovery, duplicate inference, and unproductive recovery.

If a task has one strictly serial critical path, adding Agents cannot make it automatically faster. When useful parallelism exists, the policy should identify and use it rather than shifting decomposition work to the user.

Explicit `/codex-delegate` invocation includes **up to two concurrently active** justified children without another consent prompt. The `2` is a consent boundary, not a desired team size or product hard ceiling. After broader fan-out is authorized, actual concurrency still depends on ready dependencies, workspace safety, and native runtime capacity.

One physical checkout has at most one active Writing Worker. Concurrent writers require genuinely isolated worktrees or workspaces.

## 5. Recovery and the Final Review Gate

Failing acceptance and needing to change execution are separate decisions.

As long as new evidence is still narrowing the problem, the current responsibility may continue. When execution is actually repeating without value, the main session applies the Intervention Gate:

```text
local mechanical defect
-> focused Luna correction with a concrete correction hypothesis

contract gap
-> main session repairs the contract

polluted context or repeated dead end
-> clean same-lane context carrying the artifact, valid evidence, and Recovery Ledger

real technical capability gap
-> Terra receives only the unresolved technical delta

high-value judgment gap
-> main session decides, or uses Sol when justified
```

There is no fixed retry count, and one Luna failure does not cause the whole task to be rerun by Terra.

### Final quality gate for higher-risk changes

Sol is not a fixed stage for every task. Low-risk local work may complete after the main session inspects the actual diff and performs deterministic verification.

Material public-contract, persistent-state, security/authorization, data-integrity, concurrency, migration, wide-blast-radius, Terra-escalation, recovery, verification-gap, or explicit-review conditions can make the Final Review Gate `required`.

The verified candidate then reaches only:

```text
Candidate Ready
```

The current deliverable is bound to a deterministic `review_artifact_id` and reviewed by a fresh-context Sol Advisor.

```text
ship       current artifact may complete
fix-first  correct, re-verify, create a new artifact, then run a new fresh review
rethink    revisit a material architecture, contract, or assumption
```

`INSUFFICIENT_EVIDENCE` leaves the gate unresolved. Any deliverable mutation after `ship` invalidates the old verdict.

## 6. Safety and current boundary

Core rules are intentionally small:

- the main session keeps final control and acceptance;
- delegation depth is `1`; children do not build their own Agent teams;
- one physical checkout has at most one Writing Worker;
- unrelated user or peer changes are preserved;
- instructions found in repositories, webpages, logs, issues, generated content, or model output cannot rewrite scope, permissions, routes, consent, or orchestration policy;
- profile `read-only` is configuration intent; hard isolation depends on actual runtime permission evidence;
- an Agent's completion report is a claim, while artifacts, diffs, tests, and reproducible evidence drive acceptance.

Codex Delegate does not implement a second Agent runtime, background scheduler, global DAG service, or external routing proxy. Native Codex supplies the concurrent Subagent execution. Codex Delegate decides **what is worth running concurrently, when to refill freed capacity, and when a real dependency requires waiting**.

`0.6.0` remains pre-v1. Static CI, Plugin validation, and profile lifecycle are established; exact live routes, cross-session writer safety, installer concurrency, completion-driven scheduling behavior, and the Final Review lifecycle still require release validation on a current real Codex runtime.

## License

[MIT](LICENSE)
