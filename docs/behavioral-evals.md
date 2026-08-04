# Live behavioral evaluation protocol

Static tests prove repository contracts, packaging, profile lifecycle, schemas, and deterministic tooling. They do not prove task quality, model value, native capacity, or Final Review Gate yield on a real Codex runtime.

Behavioral evaluation therefore uses controlled live runs over frozen workloads.

## Primary product questions

The live suite answers four distinct questions:

1. Does compiling a bounded Delegation Contract improve execution versus giving the same prompt directly to Luna?
2. Does adaptive dependency scheduling reduce duplicate work without reducing correctness?
3. Does Terra delta escalation reduce rework when a real capability gap exists?
4. Does optional or mandatory Fresh Sol review catch material issues at acceptable false-positive/cost levels?

These questions must not be collapsed into one global “better mode” score.

## Comparison modes

Schema `3.0` currently recognizes:

```text
main_session_only
raw_prompt_luna
contract_luna
contract_luna_selective_sol
contract_luna_final_review_gate
contract_delta_terra
adaptive_orchestration
external_baseline
```

`contract_luna_selective_sol` measures optional review. `contract_luna_final_review_gate` measures the mandatory risk-triggered acceptance path. Keep those populations separate.

## Freeze the executable workload

Before the first run in a pair, freeze and record:

```text
exact user prompt bytes
repository + base revision
required setup / starting state
acceptance rubric + rubric id
allowed verification commands
main-session route
Worker route when applicable
permissions / approval posture
available tool surface
Codex runtime version
```

Hash that frozen definition into `workload_definition_hash`. If a controlled input changes, create a new pair id and hash.

The registry in `evals/behavioral-workloads.json` defines experiment shapes. It does not claim benchmark results.

## Pairing rules

Paired runs must keep these controls identical:

```text
workload_id / frozen workload definition
repo_revision
repeat_index
workload_definition_hash
main_session_route
worker_route when applicable
permissions_fingerprint
tool_surface_fingerprint
acceptance_rubric_id
runtime conditions
```

The scorer rejects mixed controls, duplicate modes, mixed Worker routes, and pairs that do not match the workload's declared `primary_comparison`.

Do not compare repository-wide mode averages across different workload mixes. Global mode aggregates are descriptive only.

## Core metrics

Record when available:

### Outcome

```text
success
acceptance_score
scope_violations
wrong_edits
regressions
```

### Resource use

```text
agent_count
peak_active_children
ready_dependencies
runtime_slot_waits
input_tokens
output_tokens
reasoning_tokens
latency_ms
consent_prompts
```

### Recovery / correction

```text
correction_turns
execution_stall_events
clean_same_lane_restarts
unjustified_retry_calls
same_failure_without_new_evidence
main_session_correction_tokens
main_session_correction_ms
```

### Evidence efficiency

```text
evidence_established
evidence_invalidated
unjustified_repeated_commands
unjustified_repeated_discovery
duplicate_dependency_calls
```

### Review

```text
review_findings
review_caught_material_issue
review_false_positives
final_review_requirement
final_review_trigger_reasons
final_review_attempts
final_review_verdict
final_review_gate_satisfied
review_artifact_verify_failures
post_review_mutations
```

Missing telemetry remains `null` where permitted. Never estimate unavailable token, latency, runtime, or route data.

## Contract experiment

Primary comparison:

```text
raw_prompt_luna
vs
contract_luna
```

Use the same Luna route and frozen task. Measure correctness, scope discipline, correction work, evidence reuse, tokens/latency when exposed, and repeated commands/discovery.

The hypothesis is that a bounded contract improves execution quality or correction cost. Do not assume the result.

## Adaptive scheduling experiment

Use at least five genuinely independent read-only dependencies.

```text
A: broad fan-out not authorized
-> normal consent boundary applies

B: broad fan-out explicitly authorized
-> no Codex Delegate hard child ceiling; native capacity determines the wave and excess work queues
```

Record ready dependencies, peak children, observed child capacity, slot waits, duplicate dependency calls, and consent prompts.

One runtime observation does not establish a universal Codex capacity limit.

## Intervention / clean-restart experiment

Create a bounded responsibility where the same deterministic failure can persist across materially similar attempts.

Compare an unchanged retry/context-accumulation baseline with evidence-guided recovery.

Valid evidence-guided outcomes include:

```text
focused correction
clean same-lane restart
Terra delta escalation
main-session contract repair or judgment
```

Measure repeated commands/discovery, unchanged retries, acceptance quality, and main-session correction cost. Do not encode a universal retry-count threshold.

## Terra delta experiment

Use Terra only when the workload exposes a concrete technical capability gap.

Compare:

```text
whole-task restart with stronger investigation
vs
Terra receives unresolved delta + valid evidence + current artifact + failure signature + DO NOT REDO
```

Measure duplicate work, correction cost, latency/tokens when available, and final correctness.

## Optional Sol experiment

Use `contract_luna_selective_sol` for consequential diffs where deterministic verification is already strong but independent judgment may add value.

Compare with Luna-only/contract execution on the same frozen workload. Measure material catches, false positives, correction work, latency/tokens, and acceptance.

Fresh context is a design choice to reduce anchoring. It is not evidence that Sol is automatically correct or independent.

## Mandatory Final Review Gate experiment

Use `contract_luna_final_review_gate` only when a semantic trigger makes independent review part of completion.

Record the full lifecycle:

```text
main-session verification
-> final_review_requirement = required
-> Candidate Ready
-> review_artifact_id
-> fresh Advisor review
-> ship | fix-first | rethink
```

Also test:

```text
INSUFFICIENT_EVIDENCE
-> gate remains unresolved

fix-first
-> correction + re-verification + new artifact id + new fresh review

rethink
-> invalidate affected architecture/contract assumptions

post-review deliverable mutation
-> artifact verification fails and old ship no longer satisfies the gate

implicit invocation + declined required Sol call
-> Candidate Ready remains, gate_satisfied = false
```

Measure review attempts, material catches, false positives, artifact verification failures, post-review mutations, and gate satisfaction.

A useful review-yield metric is:

```text
material review catches / final review attempts
```

Interpret it only with workload mix and false positives. A high yield from intentionally adversarial workloads is not a production-rate claim.

## Main-session correction cost

Model price alone is not workflow cost. Track:

```text
Worker compute
+ main-session planning
+ deterministic verification
+ correction/recovery work
+ optional investigation/review
```

This is why `main_session_correction_tokens` and `main_session_correction_ms` remain first-class metrics.

## Scoring

```bash
python scripts/score-behavioral-evals.py path/to/result.json
```

The scorer validates schema and controlled pairing first. Paired candidate-minus-baseline deltas are the primary comparison output. Workload/mode summaries are descriptive inventory.

The scorer must never manufacture missing telemetry.

## Release evidence rule

Do not claim that Codex Delegate reduces cost, improves correctness, prevents rework, increases safe concurrency, or makes review more valuable unless named live workloads on named runtime versions support that claim.

Luna Max remains the v1 execution baseline. Terra XHigh and Sol High remain role-route hypotheses whose value must be demonstrated on representative workloads.
