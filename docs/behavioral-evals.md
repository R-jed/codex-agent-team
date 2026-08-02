# Live behavioral evaluation protocol

Static repository tests prove policy text, profile lifecycle, schemas, and deterministic evidence tooling. They do not prove that a particular Codex build improves real task outcomes.

Behavioral evaluation therefore uses paired live runs over the same workload and repository revision.

## Primary question

The first product claim to test is whether compiling a bounded Delegation Contract improves execution compared with giving the same raw user prompt directly to Luna Max.

Required comparison modes:

```text
main_session_only
raw_prompt_luna
contract_luna
contract_luna_selective_sol
```

Optional research modes may include Terra delta investigation when a workload exposes a genuine capability gap.

## Pairing rules

A comparison is valid only when paired runs keep these fixed:

- workload id;
- repository and base revision;
- user prompt;
- Codex version;
- main-session model/effort when applicable;
- permissions and available tools;
- acceptance rubric.

Record a `repeat_index` for repeated trials. Do not compare aggregate mode averages built from different workload mixes.

## What to measure

Each run should record:

- final task success;
- acceptance score when a rubric is available;
- actual Agent count and roles;
- scope violations and wrong-edit count;
- regressions introduced;
- correction turns after the first delegated result;
- main-session correction tokens/time when exposed;
- input/output/reasoning tokens when exposed;
- latency when exposed;
- review findings;
- review material catches;
- review false positives;
- consent prompts;
- policy violations;
- route evidence grade when material.

Missing telemetry remains `null`. Do not estimate it.

## Main-session correction cost

A cheap Worker is not cheap if the main session must spend substantial additional work repairing its result.

Track correction cost separately from Worker cost:

```text
worker compute
+ main-session planning
+ deterministic verification
+ correction work
+ optional review
```

This makes it possible to compare total workflow cost rather than model price alone.

## Evidence-reuse metrics

Incremental orchestration should also record:

- reusable evidence items established;
- evidence items invalidated;
- repeated deterministic commands that had no invalidation reason;
- repeated repository discovery with no invalidation reason;
- Agent calls whose output duplicated an already-satisfied dependency.

These metrics test the resource-coordination claim directly.

## Terra experiments

Terra is not a mandatory stage. Test it only on workloads where Luna or the main session exposes a concrete capability gap.

Compare:

```text
restart whole task with Terra
vs
Terra receives unresolved delta + established evidence
```

The desired behavior is less duplicated search, lower latency/token cost, and equal or better final correctness.

## Sol experiments

A common short path is:

```text
contract -> Luna Max -> selective Sol -> main session
```

Compare it with Luna-only on tasks where deterministic verification is strong but a consequential diff benefits from high-value judgment.

Measure true material catches and false positives. Sol is not assumed to improve every task.

## Scoring

```bash
python scripts/score-behavioral-evals.py path/to/result.json
```

The scorer validates paired-run metadata and summarizes metrics by workload and mode. It must not invent missing token, latency, or correction data.

## Release evidence rule

Do not claim that Agent Team reduces cost, that Terra prevents rework, that Sol review improves quality, or that a route/effort is optimal unless named live workloads on named Codex versions support the claim.

Luna Max is the current execution baseline by design. Terra XHigh and Sol High remain hypotheses until paired workload evidence justifies them.
