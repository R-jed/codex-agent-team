<p align="center">
  <img src="assets/subagents-dispatch-logo.svg#gh-light-mode-only" alt="subagents-dispatch" width="112">
  <img src="assets/subagents-dispatch-logo-dark.svg#gh-dark-mode-only" alt="subagents-dispatch" width="112">
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

Rename a function? Main handles it. Need to read code, write changes, and run tests at the same time? It hands each piece to a specialist Agent, runs them in parallel, and merges the results.

## Quick start

You ask Codex to add pagination to an API and write tests.

Without subagents-dispatch, the main session does everything: reads code, changes implementation, writes tests. One step at a time.

With subagents-dispatch:

```
/dispatch Add pagination to /api/users, with tests
```

The main session splits it into three responsibilities — Reader inspects the current code, Worker changes the implementation, Worker writes tests — runs them in parallel, then combines the results. You can preview, steer, or take over at any point.

## Control active work

See the plan before it runs:

```
/dispatch preview Add pagination to /api/users, with tests
```

Preview gives you the likely responsibilities and dependencies. No Agents spawned, no code changed.

Check what's running:

```
/dispatch status
```

Guide a running responsibility:

```
/dispatch steer U2: check the existing pagination middleware first, don't rewrite from scratch
```

Take a responsibility back:

```
/dispatch takeover U2
```

Takeover settles the previous Agent first. For writing work, Main stays read-only until the previous writer is confirmed stopped or terminal. If the state can't be determined, it stays `UNKNOWN` — no guessing.

## Compact execution receipt

When a task actually spawns Agents, it ends with a one-line receipt:

```
Dispatch: Reader inspect -> Worker implement · no retry · Final Review not required
```

Blocked tasks report the reason just as compactly. The receipt covers verifiable facts only — no hidden reasoning, does not estimate token usage or currency cost. Tasks without child Agents skip the receipt.

## Evidence-bound handoffs

Between consecutive responsibilities, a Handoff Capsule passes already-verified facts and `DO NOT REDO` guidance, so the next Agent doesn't rediscover the same things.

Each child gets fresh context. No transcript forwarding — only Main-verified claims enter the capsule. If the files change, old capsule facts are invalidated.

## Install

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

Start a new Codex session after installing.

On the first task that needs an Agent, if the five managed Agent profiles aren't installed yet, the system explains what it needs, asks permission, and installs them. Some Codex versions may require one additional fresh Codex session before the profiles are visible.

Development:

```
/dispatch <task>
```

Diagnostics and maintenance:

```
/doctor <request>
```

Doctor is read-only by default. `/skills` opens the picker. Dispatch doesn't auto-activate on regular tasks.

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

## Safety

- Main owns the user's goal, permissions, team composition, and final response
- Child Agents can't create their own teams
- Within one subagents-dispatch orchestration, same Git checkout, one writer at a time; other Codex sessions, editors, hooks, and external processes are outside this guarantee
- Steering can't widen responsibility, permissions, or mutation authority
- Takeover must settle the previous owner first
- Handoff Capsules carry only Main-verified evidence
- An Agent saying "done" is a claim — artifacts and test results are the proof
- Model, token, or cost claims need actual runtime evidence

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
