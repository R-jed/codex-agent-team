<p align="center">
  <img src="assets/subagents-dispatch-logo.png" alt="subagents-dispatch" width="112">
</p>

<h1 align="center">subagents-dispatch</h1>

<p align="center"><em>One command. Parallel agents. Controlled results.</em></p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">Install</a> · <a href="docs/architecture.md">Architecture</a> · <a href="LICENSE">MIT</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

---

> **If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly.**

## Quick start

You ask Codex to add pagination to an API and write tests.

Without subagents-dispatch, the main session does everything: reads code, changes implementation, writes tests. One step at a time.

With subagents-dispatch:

```
/dispatch Add pagination to /api/users, with tests
```

Main can run two read-only Reader responsibilities in parallel: one inspects the existing implementation and one maps the relevant tests. After that evidence is accepted, one Worker owns the implementation and test changes, then Main verifies the result.

## Control surface

Preview the delegation plan:

```
/dispatch preview Add pagination to /api/users, with tests
```

Check status during execution:

```
/dispatch status
```

Guide a running Agent:

```
/dispatch steer U2: check existing pagination middleware first
```

Take back control:

```
/dispatch takeover U2
```

## Compact execution receipt

When a task spawns Agents, it ends with a one-line receipt:

```
Dispatch: Reader inspect -> Worker implement · no retry · Final Review not required
```

The receipt covers verifiable facts only, exposes no hidden reasoning.

## Handoff Capsule: evidence-bound handoffs

Each child receives fresh context. A Handoff Capsule provides a small evidence-bound bridge between responsibilities.

- **Pass verified facts**: only facts that Main has checked and accepted can enter the capsule
- **Mark `DO NOT REDO`**: work already satisfied by valid evidence can be marked as do not repeat
- **Main is the acceptance boundary**: a child claim does not become inherited task truth by itself
- **Carry `STALE IF` conditions**: source changes can invalidate previously accepted evidence

## Four core invariants

These hold no matter how many responsibilities a task splits into:

- **One writer** — within one subagents-dispatch orchestration, the same Git checkout has at most one active writer. The writer can be Main, Worker, or Solver. Main stays read-only until the previous writer is confirmed stopped or terminal. Other Codex sessions, editors, hooks, and external processes are outside this guarantee.
- **One delegation layer** — child Agents cannot create further Subagents. Main keeps ownership of the user goal, permissions, team composition, and final response.
- **UNKNOWN means do not guess** — when state cannot be established, there is no replacement Agent, retry, or semantic reroute.
- **Receipts report facts** — does not estimate token usage or currency cost from model names, elapsed time, or output length.

## Roles

| Role | What it does |
|------|-------------|
| Luna Reader | read code, trace call paths, gather facts |
| Luna Worker | implementation and tests when the behavior is already decided |
| Sol Solver | implementation that needs judgment calls along the way |
| Terra Investigator | broad read-only investigation, evidence synthesis |
| Sol Advisor | independent technical judgment or final review |

Simple work stays in Main. Delegation happens when parallelism, isolation, or specialist capability justifies the cost. No fixed team size, no fixed pipeline.

## Install

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

Start a new Codex session after installing. On the first task that needs an Agent, if the five managed Agent profiles aren't installed yet, the system explains what it needs, asks permission, and installs them. Some Codex versions may require one additional fresh Codex session before the profiles are visible.

## Uninstall

```bash
# Remove plugin registration
codex plugin remove subagents-dispatch@subagents-dispatch
```

If you previously ran tasks that needed Agents, also delete these files:

```bash
# Delete 5 Agent profiles
rm ~/.codex/agents/subagents-dispatch-reader.toml
rm ~/.codex/agents/subagents-dispatch-worker.toml
rm ~/.codex/agents/subagents-dispatch-solver.toml
rm ~/.codex/agents/subagents-dispatch-investigator.toml
rm ~/.codex/agents/subagents-dispatch-advisor.toml

# Delete install manifest
rm ~/.codex/.subagents-dispatch-agents.json
```

## Update

```bash
codex plugin marketplace upgrade subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

Or ask Doctor:

```
/doctor Upgrade subagents-dispatch
```

Start a new Codex session after updating.

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
