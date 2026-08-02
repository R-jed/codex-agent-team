# Codex Agent Team

[中文](README.md) · [Install](docs/plugin-installation.md) · [Architecture](docs/architecture.md) · [Evals](docs/behavioral-evals.md) · [Local validation handoff](HEADOFF.md)

Codex can already spawn Subagents. The harder engineering problem is scheduling them well: which work is worth delegating, how precisely it should be specified, which results can be reused, when a stronger model adds new value, and who accepts the final result.

Codex Agent Team puts those decisions into one workflow. The current Codex session remains the **main session** and owns intent, boundaries, scheduling, reusable evidence, and final acceptance. Luna, Terra, and Sol are compute resources selected for unresolved dependencies, not stages in a fixed pipeline.

## Quick start

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

Reopen ChatGPT Desktop and install `Codex Agent Team` from the Plugins Directory.

Invoke it explicitly when needed:

```text
/codex-agent-team
```

## Current status

The repository has completed the static closure pass for the current architecture cycle. Deterministic tests cover Plugin packaging, the managed Agent profile lifecycle, Delegation Contract rules, orchestration policy, Runtime Truth, and paired behavioral-eval tooling.

The current remote branch audit found 11 branches. The 10 non-main branches are historical heads of already merged PRs. None contains work that should be merged again. They only need remote-ref cleanup, with the exact command in [`HEADOFF.md`](HEADOFF.md).

The next phase is fixed: **local real-runtime validation**. Static CI cannot establish live Codex role discovery, model routing, sandbox behavior, parent-thread metadata, Agent lifecycle behavior, evidence-reuse compliance, cost, or task quality. A local takeover should execute `HEADOFF.md` before redesigning the orchestration model.

## How work is divided

| Tier | Current route | Primary use |
| --- | --- | --- |
| Main session | current Codex session | understand the task, set boundaries, make key decisions, schedule work, accept results |
| Luna Reader | GPT-5.6 Luna `max` | search, tracing, test mapping, evidence collection |
| Luna Worker | GPT-5.6 Luna `max` | bounded implementation, debugging, tests, local refactors |
| Terra Investigator | GPT-5.6 Terra `xhigh` | one unresolved complex technical dependency |
| Sol Advisor | GPT-5.6 Sol `high` | high-value judgment and selective review |

These are not pipeline stages. Valid paths include:

```text
main session
main session -> Luna -> main session
main session -> Luna -> Sol -> main session
main session -> Luna -> Terra (unresolved delta only) -> Luna / main session
```

`Luna -> Terra -> Sol` is never a sequence every task must complete.

## Compile a delegation contract before execution

A writing Worker should not receive a raw ambiguous user request when the main session can define a bounded execution contract first.

The contract states:

```text
OUTCOME          what must exist when the work is done
SCOPE            what may be read and written
INVARIANTS       behavior and interfaces that must remain true
DECISION RIGHTS  choices the Worker may make on its own
ACCEPTANCE       observable completion criteria
VERIFICATION     commands and evidence that prove the result
STOP / ESCALATE  conditions that return control to the main session
```

If acceptance or decision rights remain materially unclear, the workflow does not create a writing Worker.

The division of labor is deliberate: the main session owns `WHAT / WHY / SCOPE / RISK / ACCEPTANCE`; Luna solves `HOW TO EXECUTE` inside that contract.

## Reuse work that has already been established

The main session maintains a compact Shared Evidence State. It records reusable test results, file relationships, call paths, interface facts, and other evidence together with the files or artifacts they depend on.

Later Agents reuse evidence while those dependencies remain valid. A changed input invalidates only evidence that depends on it. Repository scans and deterministic commands are not repeated merely because another model joined the task.

Model judgments are kept separate from established facts. A hypothesis stays challengeable even if multiple Agents repeat it.

## Classify a weak Luna result before escalation

```text
mechanical defect -> focused Luna correction
contract gap -> main session repairs the contract
capability gap -> Terra receives only the unresolved technical delta
judgment gap -> main session decides, or uses Sol when that adds real value
```

Terra is a read-only complex-investigation tier by default. It receives established evidence, the current artifact, the unresolved question, and explicit `DO NOT REDO` items. A mediocre Luna result does not automatically trigger a whole-repository scan or full reimplementation by Terra.

Once Terra resolves the technical dependency, bounded implementation normally returns to Luna or the main session.

## Luna + Sol is a normal short path

Some tasks have clear implementation standards but still benefit from higher-value judgment over the finished artifact:

```text
main session
-> Luna Max implementation
-> Sol review of the actual diff and evidence
-> main-session acceptance
```

Terra does not appear merely to complete a three-tier structure.

When deterministic tests and acceptance oracles are already strong enough, the path may stop at:

```text
main session -> Luna -> main session
```

Or use zero Subagents.

## Parallelism is for independent dependencies

Useful parallelism means concurrent work produces different inputs required by the task. Examples include two independent read-only investigations, or the main session preparing acceptance and risk checks while Luna performs bounded implementation.

Running Luna, Terra, and Sol over the same question simply to keep compute busy is duplicated inference. Every Agent call must add value that existing valid work cannot already provide.

## What you see

When delegation materially changes execution, the Skill emits a compact receipt:

```text
Agent Team
Luna Worker: implemented the bounded retry fix
Sol Advisor: reviewed the final diff because payment-state semantics were high consequence
Reused evidence: E03 reproduction, E07 caller trace, E11 baseline tests
Verification: 38 tests passed
```

When the main session handles the task directly:

```text
Agent Team: Main session only
Why: the change was already isolated and delegation added no useful dependency
Verification: 12 tests passed
```

## Boundaries

- Zero Subagents is normal. The default is 1, the normal maximum is 2, and the hard maximum is 4.
- There is at most one active Writing Worker per shared workspace.
- Child Agents do not create further Subagents; delegation stays one layer deep.
- The Skill never silently switches the main-session model or reasoning effort.
- A missing exact project profile returns the responsibility to the main session; there is no cross-role substitution.
- Runtime route proof requires both the expected route and observed route to contain role, model, and effort completely; missing exact-route fields fail closed.
- A Subagent completion report is a claim. Final acceptance uses actual files, diffs, commands, tests, and reproducible evidence.

The project uses Codex native `spawn_agent`. It does not implement a second Agent runtime, persistent task DAG, or background scheduler.

<details>
<summary>Which Agent profiles are checked on first use?</summary>

```text
codex_agent_team_reader
codex_agent_team_worker
codex_agent_team_investigator
codex_agent_team_advisor
```

If a required profile is missing, the Skill discloses the complete managed file scope before asking permission. The installer manages only these four current profiles and its ownership manifest. Older model-named profiles are removed only when their current bytes are proven by the active previous project ownership manifest. User-modified, unproven, or intentionally recreated legacy files do not inherit deletion authority from stale ownership data.

</details>

## What to validate next

[`HEADOFF.md`](HEADOFF.md) is the authoritative local Codex takeover contract, organized around four test domains:

- Plugin installation, profile consent, live route / sandbox / ancestry, and Runtime Truth;
- Contractability, Shared Evidence, Luna failure classification, Terra delta, and selective Sol;
- paired raw-prompt versus compiled-contract evaluation, useful parallelism, and Agent lifecycle stress;
- installer fault injection, historical branch cleanup, and the final release gate.

Luna Max is the current execution baseline. Terra XHigh and Sol High remain route hypotheses requiring representative live workload evidence. Do not publish cost, latency, or quality-improvement claims before that evidence exists.

## Documentation

- [Local runtime validation handoff](HEADOFF.md)
- [Plugin installation and first run](docs/plugin-installation.md)
- [Architecture](docs/architecture.md)
- [Native Subagent Runtime](docs/native-subagent-runtime.md)
- [Model routing and evidence](docs/model-route-assurance.md)
- [Delegation Contract](plugins/codex-agent-team/skills/codex-agent-team/references/delegation-contract.md)
- [Runtime Evidence](plugins/codex-agent-team/skills/codex-agent-team/references/runtime-assurance.md)
- [Behavioral Evals](docs/behavioral-evals.md)
- [OpenAI References](docs/openai-references.md)

## License

[MIT](LICENSE)
