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
  <img src="https://img.shields.io/badge/version-0.6.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/status-pre--v1-orange.svg" alt="Status">
</p>

Codex Delegate turns an engineering task into the smallest useful set of verifiable delegations. It creates Codex Native Subagents only when delegation adds concrete value to an unresolved dependency.

The current main session always owns user intent, scope, consequential decisions, scheduling, acceptance, and the final response. Luna, Terra, and Sol are selectable execution or judgment resources. There is no fixed model pipeline and no fixed Agent count.

Current version: `0.6.0`, pre-v1. v0.6.0 is now merged into `main`; the risk-triggered Final Review Gate, deterministic artifact binding, consent/recovery integration, and behavioral metrics are part of the current mainline.

## Project status

The final v0.6.0 merge candidate passed Ubuntu / Python 3.11, Ubuntu / Python 3.12, macOS / Python 3.11, the pinned official OpenAI Plugin validator, and `167` pytest tests.

The pre-v1 phase is still completing live validation on current Codex runtimes for exact Worker / Investigator / Advisor routing, the required Final Review Gate fresh-Sol and artifact lifecycle, same-checkout writer exclusion across independent main sessions, and the current Plugin validator plus real marketplace install/upgrade and installer-concurrency paths before release.

Repository-CI evidence and still-pending runtime claims therefore remain explicitly separated; an unfinished live gate is not presented as behavior already proven across Codex runtime versions.

## Quick start

Fresh install:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin add codex-agent-team@codex-agent-team
```

If this Git marketplace is already configured, refresh its snapshot before reinstalling the Plugin:

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

Start a new Codex thread after installation, upgrade, or reinstall, then give it a task directly:

```text
/codex-delegate Fix this login retry bug and run the relevant tests.
/codex-delegate Refactor this module while preserving the public API.
/codex-delegate Review this change with emphasis on data consistency and regression risk.
```

You do not need to choose a model, Agent count, or model sequence first. See the [installation guide](docs/plugin-installation.md) for migration and failure-handling details.

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
| Sol Advisor | GPT-5.6 Sol `high` | high-value judgment and risk-triggered independent review |

Task size does not automatically select a stronger model. A large but clear dependency can stay with Luna, while a small change may justify Sol when it crosses an important architecture, security, migration, or public-contract boundary.

## Final quality gate for higher-risk changes

Sol is not a fixed stage for every task. Ordinary low-risk work can still finish after the main session inspects the actual diff and completes the required deterministic verification.

When the final deliverable materially crosses a public contract, persistent-state, security or authorization, data-integrity, concurrency, migration, or wide-blast-radius boundary, or when execution materially depended on Terra escalation, significant recovery, or a verification gap, Codex Delegate promotes the Final Review Gate to `required`.

At that point main-session acceptance produces only `Candidate Ready`. Completion additionally requires a fresh-context Sol Advisor to independently review the final actual artifact. The verdict is bound to a deterministic `review_artifact_id`, so any deliverable mutation after review invalidates the old verdict.

Completion verdicts are:

```text
ship       -> the current artifact may complete
fix-first  -> correct the finding, verify again, then run a new fresh review
rethink    -> revisit the architecture, contract, or material assumption
```

If the Advisor lacks evidence required for a justified conclusion, it returns `INSUFFICIENT_EVIDENCE`. The gate remains unsatisfied until the named evidence dependency is established and a new fresh review runs; that state is never silently converted into `ship` or `fix-first`.

The Final Review Gate is triggered by semantic risk, not a fixed line count, file count, retry count, numeric risk score, or mandatory Luna -> Terra -> Sol pipeline.

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

Failing acceptance and needing to change execution are separate decisions.

If a test still fails while new deterministic evidence narrows the root cause or unresolved delta, the main session can continue the current responsibility instead of restarting context or escalating models early.

Only when evidence supports intervention does Codex Delegate classify the recovery path:

- a concrete local mechanical defect can return to Luna for a focused correction;
- an incomplete contract returns to the main session for repair;
- repeated unproductive context can trigger a clean same-lane restart using the current artifact, valid evidence, and compact recovery history;
- an evidence-supported complex technical capability gap sends only the unresolved delta to Terra;
- a consequential judgment stays with the main session or uses Sol when appropriate.

The main session keeps a bounded Recovery Ledger so fresh context does not accidentally revisit an established dead end. An Agent's suggested next action remains a recommendation; the effective action still passes main-session consent, safety, route, and runtime policy.

There is no fixed retry count, fixed stall count, or automatic model upgrade after a failure.

## Parallelism and multiple sessions

Independent projects may run their own Codex Delegate workflows concurrently.

Writing ownership is scoped to the canonical workspace. One physical checkout has at most one active Writing Worker. Separate, genuinely isolated workspaces or worktrees may each have a writer.

Version `0.6.0` is still completing live validation of same-checkout writer exclusion across independent main sessions and the Final Review Gate runtime path. Before v1.0.0, if you run multiple independent Codex sessions, avoid having two sessions write the same physical checkout at the same time.

## First run

Codex Delegate distributes its Skill through the native Plugin system. Its four project-managed custom Agent profiles use Codex's supported personal custom-Agent location under `$CODEX_HOME/agents`, normally `~/.codex/agents`.

When a required profile is missing or an exactly project-managed earlier generation needs upgrading, the Skill explains the Codex-home paths it may manage and asks for permission first. The installer creates, updates, or migrates only project-owned profiles and its ownership manifest when ownership rules permit.

The Plugin manifest does not invent an `agents` component. Custom Agent provisioning is an explicit post-install step; exact internal profile identifiers and migration rules are documented in the [installation guide](docs/plugin-installation.md).

It does not edit credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

Use a new Codex thread after Plugin installation or reinstall. If profile provisioning succeeds but the current task still does not expose the new role, start another fresh task and invoke `/codex-delegate` again.

## Safety boundaries

- The main session retains user intent, task scope, consequential decisions, and final acceptance
- One canonical checkout has at most one active Writing Worker
- Child Agents do not create further Subagents; delegation remains one layer deep
- The Skill does not silently switch the main-session model or reasoning effort
- If an exact project profile is unavailable, the affected responsibility returns to the main session instead of silently using a similar role
- A Worker must preserve unrelated user or concurrent-session edits; if workspace drift invalidates the contract, it stops and returns control to the main session
- A Subagent completion report or recovery recommendation is an execution claim; final acceptance and effective recovery actions rely on actual artifacts, reproducible evidence, and main-session policy
- When the Final Review Gate is required, the quality gate cannot be reported as passed without a fresh Sol `ship` bound to the unchanged current artifact
- Publishing, deployment, payments, account-permission changes, and other consequential external actions remain under main-session control

## License

[MIT](LICENSE)
