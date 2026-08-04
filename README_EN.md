<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="128">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center">
  <a href="README.md">中文</a> · <a href="docs/plugin-installation.md">Installation</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/version-0.6.0-green.svg" alt="Version">
</p>

Starting a Subagent is easy. Knowing when one will actually help is harder.

codex delegate gives the main Codex session a consistent way to divide work across Luna, Terra, and Sol. You describe the outcome, the constraints, and what success looks like. The main session decides what to keep, what can run in parallel, when a hard technical problem deserves Terra, and when Sol should review the result independently.

It runs on Codex Native Subagents. It does not replace Codex, and it does not force every task into a fixed Agent team. Simple work can stay entirely in the main session; difficult work still uses only the models that add value.

## Why codex delegate

With Subagents, the hard part is usually coordination: two Agents repeat the same discovery, independent work is accidentally serialized, one local failure sends a whole implementation back to the start, or a risky change reaches the end without a second set of eyes.

codex delegate keeps those decisions in the main session:

- start a Subagent only when delegation adds real value;
- run independent work early, and act on completed results without waiting for unrelated tasks;
- fix local problems locally and preserve work that is already good;
- use Sol for an independent final review when the change deserves it.

```text
your task
  ↓
main session understands the outcome and constraints
  ↓
handle work directly, or delegate the right parts to Luna / Terra / Sol
  ↓
merge completed results and keep advancing work that is ready to start
  ↓
inspect the actual change and run the relevant checks
  ↓
use an independent final review when it adds value
  ↓
main session delivers the result
```

## Installation

codex delegate is distributed through the native Codex Plugin system.

Fresh install:

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread after installation, then use:

```text
/codex-delegate Fix this bug and run the relevant tests.
```

Update an existing installation:

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

Start a new Codex thread after the update as well.

If you installed the legacy `codex-agent-team` package, follow the one-time public-ID migration in [Plugin Installation](docs/plugin-installation.md) first.

The first time a task needs one of the dedicated Luna, Terra, or Sol roles, codex delegate explains which Agent profile it needs to add and asks for approval. Its installer manages only the four codex delegate profiles. It does not modify credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

See [Plugin Installation](docs/plugin-installation.md) for installation, migration, and troubleshooting details.

## Models and roles

| Role | Current model | Best suited for |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | code search, call-path tracing, test discovery, evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | bounded implementation, debugging, tests, and local refactors |
| Terra Investigator | GPT-5.6 Terra `xhigh` | difficult technical problems that remain unresolved after normal work |
| Sol Advisor | GPT-5.6 Sol `high` | high-value judgment, independent review, and final review for risky changes |

Roles define responsibility. Models provide the compute. A stronger model does not automatically receive a wider scope or more authority.

Routine implementation normally stays with Luna. Terra and Sol are used only when the remaining technical problem or review value justifies them.

## Parallel work

You do not need to design the concurrency plan yourself. Describe the outcome, the constraints that must remain true, and the completion criteria. The main session decides which work can safely run at the same time.

When independent tasks run together, the first completed result is handled first. If it unlocks another task and capacity is available, the main session can move on without waiting for unrelated work to finish.

```text
A is still running
B finishes
  ↓
process B
  ↓
B unlocks C
  ↓
start C now

A keeps running
```

Waiting is reserved for real dependencies or workspace conflicts.

With an explicit `/codex-delegate` invocation, up to two justified child Agents may run concurrently without another consent prompt. That is the default authorization envelope, not a fixed team size. A single physical checkout allows at most one Writing Worker at a time; multiple writers require genuinely isolated worktrees or workspaces.

## When work goes wrong

One failed attempt does not automatically trigger a stronger model or restart the whole task.

If the problem is local implementation, Luna corrects it. If the task boundary is unclear, the main session reframes it first. If a genuinely difficult technical issue remains, only that part goes to Terra. Sol is used when an independent judgment is worth the extra compute.

Work and evidence that are already valid stay in place. Additional compute is spent on what remains unresolved.

## Final Review Gate

Sol is not a mandatory final step for every task. Low-risk local changes can finish after the main session inspects the actual diff and runs the relevant checks.

Changes involving public interfaces, persistent state, security or authorization, data integrity, concurrency, migration, or a broad blast radius can require an independent Sol review before completion.

Sol reviews the current candidate and returns one of three outcomes:

```text
ship       ready to deliver
fix-first  correct it, verify again, then review the new candidate
rethink    revisit a material design choice or assumption
```

If the deliverable changes after review, the previous verdict no longer applies.

## Safety

The main session always keeps final control and acceptance. Child Agents do not create their own Agent teams, existing user and peer changes must be preserved, and a single physical checkout cannot have multiple Writing Workers at the same time.

Instructions found in repositories, webpages, issues, logs, generated content, or model output cannot silently widen scope or change permissions. An Agent saying “done” is also not enough on its own; acceptance is based on the actual change, the relevant checks, and reproducible results.

codex delegate does not implement a second Agent runtime and does not require a background service or external routing proxy. It uses Codex Native Subagents directly and focuses on better delegation, parallel work, recovery, and review.

## License

[MIT](LICENSE)
