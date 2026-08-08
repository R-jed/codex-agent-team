<p align="center">
  <img src="assets/subagents-dispatch-logo.png" alt="subagents-dispatch" width="112">
</p>

<h1 align="center">subagents-dispatch</h1>

<p align="center"><strong>You set the goal. Codex leads the team.</strong></p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">Install</a> · <a href="docs/architecture.md">Architecture</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly.**

You describe what you want. The main session decides whether to do it itself or call for help.

Rename a function? Main handles it. Need to read code, write changes, and run tests at the same time? It hands each piece to a specialist Agent, runs useful work in parallel, and integrates the result.

## Quick start

You ask Codex to add pagination to an API and write tests.

Without subagents-dispatch, the main session does everything: reads code, changes implementation, writes tests. One step at a time.

With subagents-dispatch:

```
/dispatch Add pagination to /api/users, with tests
```

Main can split the request into distinct responsibilities: Reader inspects the current code, Worker changes the implementation, and another Worker may handle tests when dependencies allow. Main verifies and integrates the result. Simple tasks can still complete with zero child Agents.

## Four core invariants

subagents-dispatch keeps delegation controlled even when a task fans out across several responsibilities.

- **One writer**: within one subagents-dispatch orchestration, the same Git checkout has at most one active writer. The writer can be Main, Worker, or Solver. `takeover` also waits until the previous writer is confirmed stopped, terminal, or closed before Main receives write ownership. Other Codex sessions, editors, hooks, and external processes are outside this guarantee.
- **One delegation layer**: child Agents cannot create further project Subagents or background Agent teams. Main keeps ownership of the user goal, permissions, team composition, integration, and final response.
- **UNKNOWN means do not guess**: when Host evidence cannot establish whether an Agent was created, is running, completed, or stopped, the state remains `UNKNOWN`. While it remains `UNKNOWN`, there is no replacement Agent, retry, semantic reroute, or conflicting ownership reassignment.
- **Receipts report facts**: when at least one child Agent actually ran, the terminal response includes a compact Execution Receipt. It reports only inspectable roles, responsibilities, retries, takeover, and Final Review state. It does not estimate token usage or currency cost from model names, elapsed time, or output length.

## 2.1 control surface

The most visible 2.1 change is direct control over delegation before and during execution: preview the plan, inspect live state, steer a running responsibility, or take it back into Main.

Preview the likely delegation shape before execution:

```
/dispatch preview Add pagination to /api/users, with tests
```

**Preview** reports likely responsibilities, role choices, important dependencies, the expected writer, and any Final Review expectation supported by current evidence. It may perform bounded read-only inspection, but it **does not spawn Agents, provision Agent profiles, mutate source, or perform external actions**. Real execution may choose a different route when new evidence appears.

Inspect current responsibility state:

```
/dispatch status
```

**Status** is a one-shot inspection. It reports the smallest useful view of `unit_id`, semantic role, known lifecycle state, relevant write ownership, and current blocker. If Host evidence is insufficient, it reports `UNKNOWN` exactly. It does not busy-poll, guess failure, or trigger recovery just to manufacture certainty.

Give focused guidance to a running responsibility:

```
/dispatch steer U2: check the existing pagination middleware first, don't rewrite from scratch
```

**Steer** keeps the same responsibility, role, attempt, authority, and ownership. It can add evidence or narrow attention. If the new instruction would change the goal, write scope, permissions, acceptance, or external impact, it must return to Main through the normal revision, reroute, takeover, or authorization path.

Take a responsibility back into Main:

```
/dispatch takeover U2
```

**Takeover** settles the previous Agent first. For writing work, Main stays read-only until the previous writer is confirmed stopped or terminal. If the state remains `UNKNOWN`, takeover stays pending and does not use a forced ownership transfer to bypass one-writer safety.

These controls provide two kinds of user control: `preview` and `status` make the orchestration visible, while `steer` and `takeover` make it interruptible. They never widen the original task scope, permissions, mutation authority, or external-impact authorization.

## Compact execution receipt

When a task actually spawns Agents, it ends with a one-line receipt:

```
Dispatch: Reader inspect -> Worker implement · no retry · Final Review not required
```

Blocked or partial tasks report the reason just as compactly, including cases such as a takeover pending on an `UNKNOWN` writer. The receipt covers verifiable facts only, exposes no hidden reasoning, and does not estimate token usage or currency cost. Tasks with zero child Agents, Preview-only requests, and Status-only requests skip the receipt.

## Handoff Capsule: evidence-bound handoffs

Each child still receives fresh context instead of inheriting the previous Agent's full transcript. That keeps context clean, but consecutive responsibilities can otherwise repeat the same repository discovery. A Handoff Capsule provides a small evidence-bound bridge between those responsibilities.

- **Pass verified facts**: only files, symbols, interfaces, test results, or other inspectable facts that Main has checked and accepted can enter the capsule.
- **Mark `DO NOT REDO`**: repository scans, call-path mapping, or expensive checks already satisfied by valid evidence can be explicitly marked as work that should not be repeated.
- **Main is the acceptance boundary**: a child claim does not become inherited task truth by itself. The flow is `child claim -> Main verifies -> Main accepts -> Capsule`.
- **Carry `STALE IF` conditions**: source mutation, API or schema changes, a new commit, failed verification, or structural plan changes can invalidate previously accepted evidence. When that happens, Main rechecks only the narrow evidence that became stale.

A capsule may also carry `ARTIFACT REFS`, `INTERFACES / INVARIANTS`, and `OPEN QUESTIONS`, but it does not forward raw transcripts or hidden reasoning. It cannot grant write ownership, mutation authority, permissions, broader user scope, or role escalation.

## Install

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

Start a new Codex session after installing.

On the first task that needs an Agent, if the five managed Agent profiles aren't installed yet, the system explains what it needs, asks permission, and installs them. Some Codex versions may require one additional fresh Codex session before the profiles are visible.

## Uninstall

```bash
# Remove plugin registration
codex plugin remove subagents-dispatch

# Delete 5 Agent profiles (reader/worker/solver/investigator/advisor)
rm ~/.codex/agents/subagents-dispatch-*.toml

# Delete install manifest (tracks which files this plugin manages)
rm ~/.codex/.subagents-dispatch-agents.json
```

Development:

```
/dispatch <task>
```

Plugin diagnostics, maintenance, and upgrade:

```
/doctor <request>
```

## Update

```bash
codex plugin marketplace upgrade subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

Or ask Doctor:

```
/doctor Upgrade subagents-dispatch and tell me what to do after
```

Start a new Codex session after updating.

## Roles

| Role | What it does |
|------|-------------|
| Luna Reader | read code, trace call paths, gather facts |
| Luna Worker | implementation and tests when the behavior is already decided |
| Sol Solver | implementation that needs judgment calls along the way |
| Terra Investigator | broad read-only investigation, evidence synthesis |
| Sol Advisor | independent technical judgment or final review |

Simple work stays in Main. Delegation happens when parallelism, isolation, or specialist capability justifies the cost. No fixed team size, no fixed pipeline.

## Other safety boundaries

- Main owns the user's goal, permissions, team composition, integration, and final response
- Steering cannot widen responsibility, permissions, or mutation authority
- Takeover cannot bypass settlement of the previous owner
- Handoff Capsules carry only Main-verified and Main-accepted facts
- An Agent saying "done" is a claim; actual artifacts, state, and relevant test results are the acceptance evidence
- Model, token, or cost claims require attributable Host evidence
- Instructions found in prompts, repository files, webpages, issues, logs, or child output are treated as data unless they come from the actual user request or trusted policy, so they cannot silently widen scope or authorization

See [Architecture](docs/architecture.md) for the full rules.

## Repository layout

```
.
├── .agents/plugins/                  # Codex Marketplace registration
├── .codex-plugin/                    # plugin manifest
├── agent-profiles/                   # five Agent profiles
├── policy-contract.json              # role definitions and core constraints
├── scripts/                          # installer, validators, runtime evidence tools
├── skills/
│   ├── dispatch/                     # main Skill, interaction controls, runtime rules
│   └── doctor/                       # install diagnostics and upgrade
├── docs/                             # architecture and runtime boundary docs
├── evals/                            # static and behavioral evaluation data
└── tests/                            # regression tests
```

## Documentation

- [Installation](docs/plugin-installation.md)
- [Architecture](docs/architecture.md)
- [Codex Native Subagent runtime boundaries](docs/native-subagent-runtime.md)
- [AI Agent project reference](README_AI.md)

## License

[MIT](LICENSE)
