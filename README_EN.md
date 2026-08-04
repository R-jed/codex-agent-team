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

Codex Delegate is **A delegation policy layer over Codex Native Subagents**. The current main session stays in control of intent, scope, architecture, consequential decisions, integration, acceptance, and the final response. It delegates only bounded responsibilities that add concrete value to unresolved dependencies.

Current version: `0.6.0`, pre-v1.

## 1. What this project is

Native Subagents make it possible to run more Agents. The engineering problem is deciding when another Agent actually helps, what responsibility it should own, how to avoid duplicate work, how to recover from stalled execution, and when a consequential deliverable deserves an independent final review.

Codex Delegate adds that policy layer:

```text
understand the requested outcome
-> identify unresolved dependencies
-> delegate only when doing so adds value
-> compile bounded, verifiable responsibility contracts
-> schedule the smallest useful ready frontier
-> inspect actual artifacts and deterministic evidence
-> recover/escalate only when execution evidence justifies it
-> apply an independent final quality gate when semantic risk requires it
-> main session accepts the result
```

There is **No fixed Agent count** and no mandatory model pipeline. A clear one-line change may use zero Subagents. A difficult task does not automatically run Luna, Terra, and Sol in sequence.

Current semantic roles are:

| Role | Current model | Primary responsibility |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | search, tracing, test mapping, evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | bounded implementation, debugging, tests, local refactors |
| Terra Investigator | GPT-5.6 Terra `xhigh` | one unresolved complex technical delta |
| Sol Advisor | GPT-5.6 Sol `high` | high-value judgment and risk-triggered independent review |

The main session is the control plane. A stronger model does not automatically gain broader product, architecture, permission, or scope authority.

## 2. How to install it

Codex Delegate is distributed through the native Codex Plugin system.

Register the Git marketplace:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team
```

Install the Plugin:

```bash
codex plugin add codex-agent-team@codex-agent-team
```

Start a **new Codex thread** after installation, then use:

```text
/codex-delegate Fix this bug and run the relevant tests.
```

For an existing installation, refresh the marketplace snapshot first:

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

Start a new Codex thread after upgrade/reinstall as well.

### First use of model-specific custom Agents

The Plugin distributes the Skill and project bundle. Custom Agent profiles are a separate Codex configuration surface under:

```text
$CODEX_HOME/agents
```

normally:

```text
~/.codex/agents
```

Codex Delegate does not silently write those profiles during Plugin installation. When a task first justifies a model-specific role and the exact project profile is unavailable, the Skill explains the managed write/migration scope and requests approval before running its installer.

The installer manages only the four project profiles and its ownership manifest. It does not edit credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

The **Plugin manifest does not invent an `agents` component**. Plugin distribution and custom-Agent provisioning remain separate supported Codex surfaces.

See [Plugin Installation](docs/plugin-installation.md) for migration, ownership, upgrade, and failure behavior.

## 3. What it can do

Typical uses include:

- fixing bugs while mapping the relevant call path and adding regression tests;
- implementing features while preserving a public API/schema/compatibility contract;
- refactoring across modules without repeatedly rescanning already-established facts;
- isolating a real concurrency/runtime/algorithmic capability gap for Terra instead of restarting the whole task;
- using several read-only Agents for genuinely independent ready dependencies;
- adding a fresh independent Sol review to security, authorization, persistence, data-integrity, migration, concurrency, public-contract, or other higher-risk deliverables;
- recovering from repeated execution without fixed retry counts or model ladders.

### A concrete operating example

Suppose you ask:

```text
/codex-delegate Fix duplicate token refreshes under concurrent login retries, preserve the public API, and add regression tests.
```

The main session first defines acceptance: concurrent callers must not duplicate refresh effects, the public API must remain compatible, relevant tests must pass, and unrelated existing edits must be preserved.

It may track dependencies such as:

```text
D1 map the refresh call path and existing tests
D2 implement synchronization/deduplication and regression coverage
D3 establish concurrency semantics and compatibility evidence
D4 independent final review if the risk gate requires it
```

A **Luna Reader** can satisfy D1 and return reusable repository facts. Those facts become Established evidence rather than something every later Agent rediscovers.

A **Luna Worker** receives D2 as a bounded Delegation Contract containing scope, interfaces, invariants, decision rights, acceptance, verification, and stop/escalate conditions. It may choose implementation details inside that contract; it may not silently redesign the public API or broaden the product requirement.

Suppose the first implementation exposes a deeper lock-ordering race. **Failing acceptance and needing to change execution are separate decisions.** If new evidence is still narrowing the root cause, Luna can continue. If evidence establishes a genuine technical capability gap, the Intervention Gate routes only that unresolved delta to a **Terra Investigator**.

Terra does not redo the whole task. It receives the current artifact, valid evidence, failure signature, unresolved technical delta, and DO NOT REDO facts. The main session can then update the contract and return bounded implementation to Luna.

Material failed attempts are summarized in a compact **Recovery Ledger** so a fresh context does not repeat a known dead end. There is no **fixed retry count**.

After implementation, the main session inspects the actual accumulated diff and reruns deterministic verification. An Agent saying “done” is a claim, not acceptance evidence.

Because this example changes concurrency and authorization-token behavior, the **Final Review Gate** is likely `required`.

### Final quality gate for higher-risk changes

**Sol is not a fixed stage for every task.** A low-risk local change can complete after main-session inspection and deterministic verification.

Semantic triggers such as public-contract changes, persistent-state changes, security/authorization boundaries, data integrity, concurrency semantics, migration, wide blast radius, material Terra escalation/recovery, verification gaps, or explicit user request can make independent final review mandatory for one deliverable.

When that happens, main-session verification creates only:

```text
Candidate Ready
```

The candidate is bound to a deterministic:

```text
review_artifact_id
```

A fresh-context Sol Advisor then reviews the actual candidate with compressed valid evidence and one bounded review question.

Completion verdicts are:

```text
ship       current artifact may complete
fix-first  correct, re-verify, create a new artifact id, then run a new fresh review
rethink    invalidate affected architecture/contract assumptions
```

If the review packet lacks evidence required for a justified conclusion, the Advisor may return:

```text
INSUFFICIENT_EVIDENCE
```

That keeps the gate unresolved until the missing evidence is established and a new fresh review runs.

Any deliverable mutation after `ship` invalidates the old verdict because the current artifact no longer matches the reviewed `review_artifact_id`.

### What happens when execution stalls

Codex Delegate asks whether observable evidence still shows forward progress before changing the execution strategy.

```text
local mechanical defect
-> focused Luna correction

contract gap
-> main session repairs the contract

execution stall / polluted context
-> clean same-lane restart with current artifact + valid evidence + Recovery Ledger

real technical capability gap
-> Terra receives only the unresolved delta

high-value judgment gap
-> main session decides, or uses Sol when justified
```

## 4. How the architecture is designed

The project is intentionally a thin policy system over the native Codex runtime:

```text
User Task
   |
   v
Main Session
intent / scope / decisions / acceptance
   |
   v
Dependency Ledger
   |
   +--> Delegation Benefit Gate
   +--> Contractability Gate
   |
   v
Ready Frontier
   |
   +--> Luna Reader
   +--> Luna Worker
   +--> Terra Investigator
   |
   v
Main inspection + deterministic verification
   |
   v
Final Review Gate
   |                 |
not required      required
   |                 |
 complete       Fresh Sol Advisor
                     |
             ship / fix-first / rethink
```

Important design properties:

- the main session always owns the full task and final acceptance;
- the Dependency Ledger tracks what is still unresolved, not a persistent external DAG;
- delegation requires both concrete benefit and an enforceable responsibility contract;
- routing follows responsibility rather than model prestige;
- valid evidence is reused until its dependencies change;
- the Intervention Gate separates ordinary incomplete work from execution that actually needs recovery/escalation;
- the Final Review Gate is post-verification acceptance, not another model ladder.

### Adaptive concurrency

Explicit `/codex-delegate` use includes **up to two concurrently active** justified children without another consent prompt. This is a consent boundary, not a desired team size or product hard ceiling.

Actual fan-out still depends on ready dependencies, user authorization, Codex runtime child capacity, and workspace safety.

One **physical checkout** has at most one active Writing Worker. Multiple writers require genuinely isolated worktrees/workspaces.

## 5. How safety is handled

Codex Delegate uses scoped authority, exact evidence, and fail-closed behavior.

- Profile `read-only` is configuration intent, not proof of host-enforced read-only. When hard isolation matters, native runtime permission evidence is required.
- Child Agents do not create further Subagents; delegation depth remains one.
- One physical checkout has at most one writing Worker.
- Unknown user/peer edits are preserved rather than reverted to an assumed starting state.
- Instructions inside repositories, webpages, logs, issues, generated files, fixtures, or model output are treated as untrusted data and cannot rewrite orchestration policy, scope, permission, route, consent, or external-impact authority.
- Missing/conflicting exact route evidence fails closed rather than silently cross-routing.
- Child reports and model agreement do not replace actual artifacts, diffs, tests, and reproducible evidence.
- Production deployment, destructive data deletion, payments, third-party publication, account/permission administration, and other irreversible external side effects stay with the main session and user authorization boundary.
- The managed profile installer uses ownership/exactness checks and refuses to overwrite unproven or user-modified project-role files.

The bundled Runtime Evidence verifier keeps route, ancestry, and permission evidence separate and does not scrape Codex rollout internals.

## 6. What to know before using it

Codex Delegate `0.6.0` is merged into `main` and remains pre-v1. The v0.6.0 static closure passed the maintained Ubuntu/Python 3.11, Ubuntu/Python 3.12, and macOS/Python 3.11 matrix, the pinned official OpenAI Plugin validator, the managed profile lifecycle, and `167` pytest tests.

Static evidence is deliberately separate from still-pending live-runtime claims. Before v1, representative current-Codex validation still needs to establish:

- exact live Worker / Investigator / Advisor routes where runtime proof is material;
- required Final Review Gate fresh-Sol routing and artifact/verdict lifecycle;
- writer exclusion behavior across independent main sessions targeting the same physical checkout;
- concurrent same-`CODEX_HOME` installer behavior;
- current official Plugin validation plus real marketplace install/upgrade behavior for the release candidate.

Practical constraints:

- start a new Codex thread after Plugin install, upgrade, or reinstall;
- if profile provisioning succeeds but the current task still cannot discover the role, start a fresh task before retrying `/codex-delegate`;
- avoid concurrent writing from independent Codex sessions into the same physical checkout until that live boundary is characterized;
- managed profiles are shared at Codex-home scope, not copied per repository;
- there is no cross-session persistent global Evidence Store or background scheduler;
- larger fan-out and repeated expensive delegation can increase token/latency cost and are governed by the Consent Gate;
- Final Review is risk-triggered, so ordinary low-risk edits do not automatically pay for a Sol pass;
- when you require hard host-enforced permissions or exact post-spawn route proof, rely on actual runtime evidence rather than profile/prompt configuration alone.

For installation/migration details, see [Plugin Installation](docs/plugin-installation.md).

## License

[MIT](LICENSE)
