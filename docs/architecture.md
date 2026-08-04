# Architecture

Codex Delegate is a policy layer over Codex Native Subagents. It does not implement another Agent runtime, persistent DAG service, background scheduler, routing proxy, or model ladder.

The main session is always the task-level control plane. It owns user intent, scope, authorization, dependency state, integration, acceptance, and final response.

Routing V4 targets the **smallest useful compute graph that preserves the required judgment quality and independent assurance**.

## First-principles control loop

```text
1. understand the user outcome and acceptance
2. identify what is actually unresolved
3. classify each dependency
4. account for main-session judgment coverage only when material judgment exists
5. choose the smallest useful actor
6. execute and collect inspectable evidence
7. if unresolved, reclassify from new evidence instead of climbing a model ladder
8. verify the integrated candidate
9. add fresh independent Sol review only when the candidate's consequences require it
10. main session accepts and reports
```

Stable current role/classification/review constants live in `plugins/codex-delegate/policy-contract.json`. Detailed normative behavior lives in the installed Skill references.

## Dependency model

The main session keeps compact in-session state:

```text
Dependency Ledger
- status: pending | ready | running | satisfied | blocked | invalidated
- kind: evidence | bounded_execution | judgment | judgment_coupled_execution | technical_investigation
- requires / produces
- write intent / workspace / acceptance

Shared Evidence State
- deterministic
- repository_fact
- model_judgment
- explicit dependencies and validity

Recovery Ledger
- only material attempt facts needed to prevent repeated dead ends

Main Judgment Coverage
- covered | uncovered | unknown
```

A running dependency has one active owner. A satisfied dependency stays closed until changed inputs invalidate it.

## Classification is the routing primitive

### Evidence

Missing inspectable facts such as code tracing, symbol mapping, test mapping, or bounded research.

Typical delegated actor: Luna Reader.

### Bounded execution

Desired behavior and material invariants are already decided. Remaining discretion is local and independently verifiable.

Typical delegated actor: Luna Worker.

The important invariant is:

```text
contractable does not imply Luna-suitable
```

If implementation is expected to require material architecture, behavior, compatibility, or cross-module semantic choices, the dependency is judgment-coupled execution.

### Judgment

A material decision must be resolved before implementation can safely proceed.

If the current main session already has trusted Sol judgment coverage, normal judgment stays in main. Otherwise a Sol Advisor supplies capability uplift.

### Judgment-coupled execution

Implementation and material judgment cannot be safely separated up front.

If the current main session is trusted Sol, main normally handles it directly. Otherwise a write-capable Sol Solver owns the bounded dependency.

This avoids repeated Advisor -> Luna -> Advisor loops for work whose design evolves with implementation evidence.

### Technical investigation

Semantic intent is already stable and a narrow difficult technical uncertainty remains.

Typical delegated actor: Terra Investigator.

Terra is not a generic stronger retry for weak Luna output.

## Main-session model awareness

Authority never depends on model identity. Compute placement can.

Trusted current-session model metadata is normalized through `plugins/codex-delegate/scripts/runtime-evidence.py`:

```text
covered   -> trusted GPT-5.6 Sol main
uncovered -> trusted non-Sol main
unknown   -> route not fully observed or conflicted
```

Routine bounded work does not need main-model inspection. Unknown coverage does not mean “always spawn Sol.” It matters only when material judgment is unresolved.

A Sol main suppresses redundant capability-uplift Sol calls. It does not satisfy independent Final Review of its own candidate.

## Current semantic roles

| Responsibility | Agent type | Route | Intent |
| --- | --- | --- | --- |
| Reader | `codex_delegate_reader` | GPT-5.6 Luna `max` | bounded reusable evidence |
| Worker | `codex_delegate_worker` | GPT-5.6 Luna `max` | standardized bounded implementation |
| Solver | `codex_delegate_solver` | GPT-5.6 Sol `high` | judgment-coupled implementation |
| Investigator | `codex_delegate_investigator` | GPT-5.6 Terra `xhigh` | narrow difficult technical uncertainty |
| Advisor | `codex_delegate_advisor` | GPT-5.6 Sol `high` | material judgment or fresh independent review |

Role identity remains separate from model identity so future model changes do not redefine responsibility semantics.

## Completion-driven scheduling

Scheduling starts from ready dependencies, not an Agent-count target.

```text
ready frontier
-> classify
-> choose smallest useful safe actor set
-> dispatch into available native capacity
-> process each exposed completion/update
-> merge evidence / close completed child
-> reclassify if needed
-> recompute ready frontier
-> refill safe capacity
```

A wave barrier is used only for a real join dependency or when the tested runtime exposes no finer wait surface.

Explicit `/codex-delegate` use includes up to two concurrently active justified children without another prompt. This is a consent envelope, not a target or product ceiling.

## Writer safety

One canonical physical checkout has at most one active writing project Agent.

Current writers are:

```text
codex_delegate_worker
codex_delegate_solver
```

Multiple writing Agents require genuine filesystem isolation such as separate worktrees/workspaces/repositories. Intended disjoint file lists in one checkout are not sufficient.

## Recovery through reclassification

Failure is not a model-escalation event.

When progress stops, the main session asks whether the dependency is still classified correctly given the new evidence.

```text
bounded local defect
-> bounded_execution
-> focused Luna correction

material semantic choice emerged
-> judgment / judgment_coupled_execution
-> main Sol / Advisor / Solver according to main coverage

contract truth missing
-> main repairs task state

semantics stable + narrow hard technical question
-> technical_investigation
-> Terra receives only that delta

same bounded work stalls while classification remains valid
-> optional clean same-role restart
```

Standard child stop signals are:

```text
CONTRACT_GAP
JUDGMENT_REQUIRED
TECHNICAL_GAP
EXECUTION_STALL
```

There is no universal retry count or fixed stronger-model progression.

## Final Review is independent assurance

After main-session verification creates a Candidate Ready artifact, evaluate consequences:

```text
no semantic review trigger
-> main acceptance can complete

material review trigger
-> bind review_artifact_id
-> fresh Sol Advisor
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

Current mandatory trigger classes are user-requested review, public contract, persistent state, security, authorization, data integrity, concurrency semantics, material migration, and verification gap.

Process history is not itself a trigger. Terra use, Solver use, recovery, or a large diff may reveal residual risk, but only the actual semantic consequence or verification gap makes review mandatory.

Fresh independent review remains required when triggered even if the main session is Sol or Sol Solver implemented the candidate.

## Runtime evidence

The bundled `plugins/codex-delegate/scripts/runtime-evidence.py` has two subjects:

```text
main_session
child
```

Main-session mode derives conservative judgment coverage only from complete trusted native model/effort metadata.

Child mode keeps route, ancestry, and permission evidence typed separately. Configuration is never copied into observed fields.

Native capacity, wait semantics, child progress observability, and cross-session coordination remain runtime facts that live validation must characterize.

## Safety and consent boundaries

Safety owns permission, trust, delegation depth, writer isolation, and high-impact external actions.

Consent owns material expansion in compute, concurrency, scope, permission, or external impact.

A stronger model never gains broader user authorization automatically.

## Plugin boundary

Codex Plugin is the supported distribution path and `/codex-delegate` is the user entry point.

Current managed profiles are installed into Codex home separately from Plugin manifest components. The installer manages only the current project generation and `.codex-delegate-agents.json`, leaving unrelated Agent configuration untouched.

## Evaluation boundary

Static tests prove contracts and deterministic helpers. Live paired workloads test Routing V4 hypotheses, including bounded Luna quality, Sol Solver value, Sol-main redundancy avoidance, Terra technical-delta value, reclassification behavior, and consequence-driven Final Review.

No quality/cost superiority claim is valid until named live workloads on named runtime versions support it.
