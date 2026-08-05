# Live Behavioral Evaluation Protocol

Static tests prove repository contracts, packaging, profile lifecycle, schemas, and deterministic tooling. They do not prove model quality, cost, native runtime behavior, onboarding quality, or the value of a routing choice.

The live suite uses controlled paired workloads to test product hypotheses without turning experimental labels into runtime policy.

## Measurement boundary

`evals/` is a measurement surface.

Some schema/mode names remain from earlier Routing V4 experiments so historical runs stay comparable. They are experiment labels only. The current runtime router is defined by the compact Skill policy in:

```text
router-core.md
guardrails.md
final-review.md
```

Do not make the Skill maintain an ontology merely because an eval field exists.

## Primary product questions

The live suite asks:

1. Does a bounded Luna responsibility reduce correction work versus giving Luna the raw task?
2. For implementation where material judgment is coupled to writing, does one Sol Solver outperform an Advisor -> Luna handoff in total quality/correction cost?
3. When the main session already meets the Sol reference capability, does keeping ordinary judgment-coupled work in Main avoid redundant Sol calls without reducing quality?
4. When main-route telemetry is unavailable, does the product avoid buying Sol for routine bounded work while still protecting genuine material judgment?
5. When Luna encounters a material semantic blocker, does correct rerouting reduce wrong edits/rework compared with simply continuing Luna?
6. For stable semantics and read-only work, does Terra provide useful quality/context depth at lower total cost than a Sol judgment lane, and when does narrow Luna Reader remain sufficient?
7. Does consequence-driven Final Review catch material issues while avoiding decorative review caused only by process history?
8. Does explicit `/codex-delegate` invocation plus pre-execution role readiness reduce onboarding interruption compared with discovering missing roles mid-task?
9. Does removing default orchestration receipts improve completion clarity without hiding consequential routing/consent/review information?

These are separate questions. Do not collapse them into one global score.

## Comparison modes

Schema `4.0` currently recognizes historical measurement labels:

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

`adaptive_routing_v4` and `terra_delta` are retained as experiment identifiers. They do not define the current runtime taxonomy or imply that Terra is an escalation rung.

`execution_route` records actual primary execution placement and may differ across paired strategies by design.

## Freeze controlled inputs

Before the first run in a pair, freeze:

```text
exact user prompt bytes
repository + base revision
setup / starting state
acceptance rubric + id
allowed verification commands
main-session route, when exposed
main capability state, when material
permissions / approval posture
tool surface
Codex runtime version
```

Hash the frozen definition into `workload_definition_hash`. If a controlled input changes, create a new pair id/hash.

Do not require the same `execution_route` across a pair when execution placement is the experimental variable.

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

Existing `reclassification_events` may remain as a compatibility field for old runs; for current runs interpret it simply as a meaningful actor/capability reroute after new evidence.

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

```text
raw_prompt_luna
vs
bounded_luna
```

Use the same Luna route and frozen task. The bounded case must have desired behavior, important invariants, and acceptance already resolved.

Measure correctness, scope discipline, material judgment violations, correction work, repeated discovery, and total resource use.

## Experiment B: judgment-coupled implementation

```text
advisor_then_luna
vs
sol_solver
```

Use a workload where implementation repeatedly exposes consequential semantic choices that cannot safely be decided once up front.

The question is whether one write-capable Sol responsibility reduces handoff/review loops. Do not assume Solver wins.

## Experiment C: Sol main capability reuse

On the same judgment-heavy writing workload with trusted main-session capability at or above the current policy reference, compare:

```text
main_session_only
vs
sol_solver
```

Measure whether the extra Sol child is redundant. This does not apply to independent Final Review, which intentionally requires a second fresh context.

## Experiment D: unknown main route

For routine bounded work when main route telemetry is unavailable, compare bounded Luna against an unnecessary Sol Solver strategy.

The purpose is to prove missing telemetry does not become “always buy Sol.”

Separately exercise a material-judgment workload under unknown telemetry to ensure quality protection remains intact.

## Experiment E: material judgment emerges during Luna work

Start with genuinely bounded work, then introduce evidence showing a consequential semantic choice is now required.

Compare blindly continuing Luna with the current product behavior, which stops bounded execution and routes the actual judgment need to Main/Sol.

Measure wrong edits, correction turns, repeated work, and whether the unresolved problem narrows.

## Experiment F: Terra read-heavy investigation

Use a workload where desired semantics are already fixed, no material decision remains, and the task is read-only but benefits from broader technical exploration or evidence synthesis than a narrow Reader task.

Compare at least:

```text
Luna Reader
vs
Terra Investigator
vs
Sol Advisor when the task is deliberately framed as judgment-heavy
```

The current product hypothesis is that Terra can provide a useful middle lane for intelligence/cost balance on read-heavy work. Do not assume that hypothesis is true until measured.

Also test two negative controls:

```text
routine narrow factual lookup
-> should remain Luna Reader / Main

demanding, ambiguous, multi-step technical reasoning with material decisions
-> should route to Main/Sol, not Terra
```

Weak Luna output alone must never become a Terra trigger.

## Experiment G: consequence-driven Final Review

Required-review population should exercise public contract, security, authorization, concurrency, persistent state, data integrity, material migration, user-requested review, and verification-gap reasons.

Record:

```text
Candidate Ready
-> review_artifact_id
-> fresh Sol Advisor
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

For the process-history negative control, use a candidate where Terra/Solver/recovery happened but no semantic review reason remains. Compare no review with the legacy forced-review strategy. Process history alone must not become a trigger.

## Experiment H: first-use readiness

Measure the first explicit `/codex-delegate` experience when project Agent profiles are absent.

The current candidate should:

```text
identify that delegation will be useful
-> check required role readiness
-> request provisioning permission
-> install + --check
-> if restart is needed, stop before child write
-> resume delegated task in fresh thread
```

Record user prompts, interrupted work, repeated discovery, and whether any implementation had to be abandoned because setup occurred too late.

## Experiment I: completion clarity

Compare ordinary successful tasks with and without a separate orchestration receipt.

The current candidate should focus the normal completion report on:

```text
what changed
verification
remaining material risk
```

Routing detail should still appear when consent, meaningful rerouting, a limitation, required review, or an explicit user question makes it consequential.

## Scoring

```bash
python scripts/score-behavioral-evals.py path/to/result.json
```

The scorer validates schema and controlled pairing first. Primary candidate-minus-baseline deltas are produced only for each workload's declared pair. Cross-workload mode aggregates are descriptive inventory, not controlled comparisons.

## Release evidence rule

Do not claim improved quality, lower cost, reduced rework, Solver superiority, Terra value, onboarding improvement, or review efficiency until named live workloads on named runtime versions support that claim.

The runtime mechanism defines where each role is allowed to operate. Behavioral evidence determines whether those choices create user value in practice.
