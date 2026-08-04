# Live Behavioral Evaluation Protocol

Static tests prove repository contracts, packaging, profile lifecycle, schemas, and deterministic tooling. They do not prove model quality, cost, native runtime behavior, or the value of a routing choice.

Routing V4 therefore uses paired live workloads to test the architecture's hypotheses rather than assuming Luna, Terra, or Sol superiority.

## Primary product questions

The live suite asks:

1. Does restricting Luna to genuinely bounded execution reduce correction work versus giving Luna the raw task?
2. For judgment-coupled implementation on a non-Sol main, does Sol Solver outperform an Advisor -> Luna handoff in total quality/correction cost?
3. When the main session is already Sol, does keeping normal judgment-coupled work in main avoid redundant Sol calls without reducing outcome quality?
4. When the main route is unknown, does Routing V4 avoid buying Sol for routine bounded work while still protecting material judgment?
5. Does evidence-driven reclassification prevent weak Luna execution from becoming blind Luna retry or false Terra escalation?
6. Does Terra delta investigation add value only for real difficult technical uncertainty after semantics stabilize?
7. Does consequence-driven Final Review catch material issues while avoiding decorative review caused only by process history?

These questions remain separate. Do not collapse them into one global mode score.

## Comparison modes

Schema `4.0` recognizes:

```text
main_session_only
raw_prompt_luna
bounded_luna
advisor_then_luna
sol_solver
terra_delta
adaptive_routing_v4
adaptive_routing_v4_final_review
external_baseline
```

The mode is the experimental strategy. `execution_route` records the actual primary execution route and may differ across paired strategies by design.

## Freeze controlled inputs

Before the first run in a pair, freeze:

```text
exact user prompt bytes
repository + base revision
setup / starting state
acceptance rubric + id
allowed verification commands
main-session route
main_judgment_coverage
permissions / approval posture
tool surface
Codex runtime version
```

Hash the frozen definition into `workload_definition_hash`. If a controlled input changes, create a new pair id/hash.

Paired runs must keep these controls identical:

```text
workload_definition_hash
main_session_route
main_judgment_coverage
permissions_fingerprint
tool_surface_fingerprint
acceptance_rubric_id
repo_revision / repeat_index
```

Do not require the same `execution_route` across a pair. The whole purpose of several Routing V4 experiments is to compare different execution placements under the same task and main-session conditions.

## Core metrics

Record only telemetry actually available.

### Outcome

```text
success
acceptance_score
scope_violations
wrong_edits
regressions
material_judgment_violations
```

### Routing / correction

```text
agent_count
peak_active_children
reclassification_events
correction_turns
execution_stall_events
clean_same_lane_restarts
unjustified_retry_calls
same_failure_without_new_evidence
judgment_uplift_calls
solver_calls
advisor_calls
terra_calls
redundant_sol_calls
```

### Resource use

```text
input_tokens
output_tokens
reasoning_tokens
latency_ms
main_session_correction_tokens
main_session_correction_ms
consent_prompts
```

### Evidence efficiency

```text
evidence_established
evidence_invalidated
unjustified_repeated_commands
unjustified_repeated_discovery
duplicate_dependency_calls
```

### Independent review

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

Missing telemetry stays `null` where allowed. Never estimate unavailable tokens, route facts, latency, or runtime observability.

## Experiment A: bounded Luna

Primary comparison:

```text
raw_prompt_luna
vs
bounded_luna
```

Use the same Luna route and frozen task. The candidate must be a true `bounded_execution` dependency whose material behavior decisions are already resolved.

Measure correctness, scope discipline, judgment violations, correction work, repeated discovery, and total resource use.

## Experiment B: judgment-coupled implementation on non-Sol main

Primary comparison:

```text
advisor_then_luna
vs
sol_solver
```

Use a workload where implementation repeatedly exposes consequential semantic choices that cannot be safely decided once up front.

The test asks whether a write-capable Sol dependency avoids repeated handoff/review loops. Do not assume Solver wins; measure outcome quality, correction turns, tokens, latency, and judgment violations.

## Experiment C: Sol main capability reuse

On the same judgment-coupled workload with trusted Sol main-session coverage compare:

```text
main_session_only
vs
sol_solver
```

The hypothesis is that an extra Sol child is redundant when it exists only for capability uplift. Record `redundant_sol_calls` and total compute alongside acceptance quality.

This experiment does not apply to independent Final Review, which intentionally requires a second fresh context.

## Experiment D: unknown main route

For routine bounded work with `main_judgment_coverage = unknown`, compare bounded Luna against an unnecessary Sol Solver strategy.

The purpose is to verify that unknown main identity does not automatically become “always buy Sol.”

Separately exercise a material judgment workload under unknown coverage to ensure Routing V4 still requests Sol capability when the dependency genuinely requires it.

## Experiment E: reclassification

Create a task that begins as valid bounded execution and later exposes material semantic uncertainty.

Compare continuing the original Luna responsibility with `adaptive_routing_v4`, which must preserve current evidence and reclassify the same dependency rather than restart the whole task.

Measure wrong edits, correction turns, repeated work, and whether the unresolved delta narrows.

## Experiment F: Terra technical delta

Only use a workload where desired semantics are already fixed and evidence isolates a difficult technical question.

Compare a broad stronger restart baseline with:

```text
Terra receives only the technical delta
+ current artifact
+ valid evidence
+ factual failure signature
+ DO NOT REDO facts
```

Measure duplicate work, correction cost, and final correctness.

Also test a false technical-gap case where semantics are unresolved; Routing V4 must return to judgment rather than send the ambiguity to Terra.

## Experiment G: consequence-driven Final Review

Use two populations.

### Required review

Exercise semantic triggers such as public contract, security, authorization, concurrency, persistent state, data integrity, material migration, explicit user request, or verification gap.

Record the full artifact-bound lifecycle:

```text
Candidate Ready
-> review_artifact_id
-> fresh Sol Advisor
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

### Process-history negative control

Use a candidate where Terra/Solver/recovery happened but no semantic trigger or material verification gap remains.

Compare:

```text
adaptive_routing_v4
vs
adaptive_routing_v4_final_review
```

This measures the cost and false-positive risk of decorative review. Process history must not be treated as a trigger by itself.

## Main-session correction cost

Workflow cost is:

```text
execution compute
+ main-session planning/integration
+ deterministic verification
+ correction/reclassification work
+ specialist investigation
+ independent review when justified
```

Model price alone is not workflow cost.

## Scoring

```bash
python scripts/score-behavioral-evals.py path/to/result.json
```

The scorer validates schema and controlled pairing first. Primary candidate-minus-baseline deltas are produced only for each workload's declared pair. Cross-workload mode aggregates are descriptive inventory and must not be treated as a controlled comparison.

## Release evidence rule

Do not claim that Routing V4 improves quality, reduces cost, prevents rework, makes Sol Solver superior, makes Terra beneficial, or improves review efficiency until named live workloads on named runtime versions support that claim.

The architecture defines where each role is allowed to operate. Behavioral evidence determines whether those routing hypotheses deliver user value in practice.
