# Live behavioral evaluation protocol

Static repository tests prove policy text, profile lifecycle, schemas, and deterministic evidence tooling. They do not prove that a particular Codex build improves real task outcomes or supports a particular concurrency level.

Behavioral evaluation therefore uses controlled live runs over the same workload, repository revision, and runtime conditions.

## Primary product question

The first execution-quality claim remains whether compiling a bounded Delegation Contract improves execution compared with giving the same user prompt directly to Luna Max.

Required comparison modes include:

```text
main_session_only
raw_prompt_luna
contract_luna
contract_luna_selective_sol
```

Optional research modes include Terra delta investigation and adaptive orchestration when a workload exposes the relevant dependency shape.

## Adaptive orchestration questions

The current architecture also needs live evidence for these claims:

1. the scheduler creates children for distinct ready dependencies rather than a fixed team size;
2. no product hard child ceiling blocks an explicitly authorized independent read-only frontier;
3. the normal two-child boundary behaves as a consent boundary, not a total-task limit;
4. native slot pressure queues ready dependencies instead of causing duplicate inference or role substitution;
5. a running dependency does not receive a duplicate child;
6. repeated same-failure execution without new evidence is detected as a stall;
7. a clean same-lane restart preserves valid artifacts/evidence while dropping dead-end context;
8. evidence-supported capability gaps escalate to Terra before repeated same-lane retries;
9. one-writer workspace safety survives larger read-only fan-out.

## Freeze the executable workload before running a pair

The registry in `evals/behavioral-workloads.json` defines experiment shapes. A live comparison still needs an exact executable local fixture before the first run.

For every workload used in a paired experiment, freeze and record at least:

```text
exact user prompt bytes
repository + base revision
required setup / starting state
acceptance rubric and rubric id
allowed verification commands
main-session route
Worker route when applicable
permissions / approval posture
available tool surface
Codex runtime version
```

Hash the frozen workload definition and use that value as `workload_definition_hash` in every run of the pair. Do not edit the prompt, setup, rubric, verification commands, route, or tool/permission controls between baseline and candidate runs. If any controlled input changes, create a new pair id and workload-definition hash.

The local validation report should contain the sanitized frozen fixture definition or enough information to reproduce it without private repository data.

## Pairing rules

A comparison is valid only when paired runs keep these fixed:

- workload id and exact workload definition;
- repository and base revision;
- Codex version;
- main-session model/effort;
- Worker route when both candidates use a Worker;
- permissions and approval posture;
- available tool surface;
- acceptance rubric.

Result schema `3.0` keeps these controls machine-checkable. Every run records:

```text
workload_definition_hash
main_session_route
worker_route
permissions_fingerprint
tool_surface_fingerprint
acceptance_rubric_id
```

`worker_route` is always an explicit field. It must be a non-empty route for `raw_prompt_luna`, `contract_luna`, and `contract_luna_selective_sol`; modes without a Worker may record `null`.

The scorer requires controlled values to be identical inside a pair. It also rejects mixed Worker routes when both candidates report one.

Record a `repeat_index` for repeated trials. Workloads that declare `primary_comparison` must contain exactly those two modes in each comparison pair. The scorer rejects a pair that mixes workload/revision/repeat metadata, duplicates a mode, or changes a controlled fingerprint.

Do not compare aggregate mode averages built from different workload mixes.

## What to measure

Each run should record when available:

- final task success;
- acceptance score;
- total Agent count and roles;
- peak concurrently active children;
- ready dependency count;
- dependency ids assigned to delegated work;
- observed native child capacity when being characterized;
- runtime slot waits;
- scope violations and wrong-edit count;
- regressions introduced;
- correction turns;
- execution-stall events;
- clean same-lane restarts;
- unjustified retry calls;
- repeated same-failure attempts without new evidence;
- main-session correction tokens/time;
- input/output/reasoning tokens;
- latency;
- review findings and material catches;
- review false positives;
- consent prompts;
- policy violations;
- route evidence grade when material.

Missing telemetry remains `null` where the schema allows it. Do not estimate it.

## Main-session correction cost

A cheap Worker is not cheap if the main session must spend substantial additional work repairing its result.

Track correction cost separately from Worker cost:

```text
worker compute
+ main-session planning
+ deterministic verification
+ correction / recovery work
+ optional investigation or review
```

This makes it possible to compare total workflow cost rather than model price alone.

## Evidence and dependency efficiency

Incremental orchestration should record:

- reusable evidence items established;
- evidence items invalidated;
- repeated deterministic commands that had no invalidation reason;
- repeated repository discovery with no invalidation reason;
- Agent calls whose output duplicated an already-running or already-satisfied dependency;
- unjustified retries of the same unchanged contract;
- whether a stall was recovered with a clean packet rather than full task rediscovery.

These metrics test the resource-coordination claim directly.

## Adaptive fan-out experiment

Use a workload with at least five genuinely independent read-only dependencies.

Run two conditions on the same runtime when practical:

```text
A: broad fan-out not authorized
Expected: larger simultaneous fan-out requests consent or stays in smaller waves

B: broad fan-out explicitly authorized
Expected: no Codex Delegate hard child ceiling; spawn up to current native capacity, queue any remainder
```

Record:

```text
ready_dependencies
peak_active_children
observed_child_capacity
runtime_slot_waits
duplicate_dependency_calls
consent_prompts
```

Do not infer a universal runtime maximum from one test. The useful conclusion is how the scheduler behaves relative to the observed capacity.

## Execution-stall experiment

Create a bounded dependency where the same deterministic failure can persist across materially similar attempts.

Compare:

```text
A: unchanged retry / context accumulation baseline
B: evidence-guided recovery using execution-progress classification
```

For B, the expected valid outcomes depend on evidence:

```text
focused correction
clean same-lane restart
Terra delta escalation
main-session contract repair or judgment
```

Measure whether the candidate reduces repeated commands, repeated discovery, unchanged retries, and main-session correction cost without reducing acceptance quality.

Do not encode a universal retry-count threshold into the experiment.

## Terra experiments

Terra is not a mandatory stage. Test it only on workloads where evidence exposes a concrete capability gap.

Compare:

```text
restart whole task with Terra
vs
Terra receives unresolved delta + established evidence + current artifact + failure signature + DO NOT REDO
```

Desired evidence is less duplicated search/rework with equal or better final correctness. Do not assume the result in advance.

## Sol experiments

A common short path is:

```text
contract -> Luna Max -> selective Sol -> main session
```

Compare it with Luna-only on tasks where deterministic verification is strong but a consequential diff benefits from high-value judgment.

For judgment experiments, keep Sol context fresh and compressed. Measure material catches and false positives. Fresh context is a design choice to reduce anchoring, not evidence that Sol is automatically independent or correct.

## Scoring

```bash
python scripts/score-behavioral-evals.py path/to/result.json
```

The scorer treats paired deltas as the primary comparison output. For each declared primary comparison it reports candidate-minus-baseline deltas on acceptance, correction work, telemetry, adaptive scheduling, stall/retry, and evidence-reuse metrics when those values were actually recorded.

It also reports descriptive summaries by workload and mode. Repository-wide mode aggregates remain descriptive inventory and are unsuitable for cross-workload causal comparison.

The scorer must not invent missing token, latency, capacity, correction, or acceptance data.

## Release evidence rule

Do not claim that Codex Delegate reduces cost, that contracts improve quality, that Terra prevents rework, that Sol review improves quality, that clean restart improves recovery, or that a runtime supports a particular concurrency level unless named live workloads on named Codex versions support the claim.

Luna Max remains the v1 execution baseline. Terra XHigh and Sol High remain route hypotheses until live workload evidence supports their value in the intended responsibilities.
