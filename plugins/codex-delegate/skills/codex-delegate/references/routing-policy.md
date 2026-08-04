# Routing Policy

This file is the single normative owner for dependency classification, actor selection, main-session judgment coverage, ready-frontier scheduling, and reclassification after new evidence.

Codex Delegate does not route by price, task size, failure count, or a model ladder. It routes by the unresolved responsibility.

## 1. Control plane

The current user-facing Codex session is always the task-level control plane. It owns user intent, scope, authorization, task state, integration, acceptance, and the final answer.

Model capability does not change that authority. Model capability can change where a dependency is most safely executed.

Two principles therefore coexist:

```text
main-session authority is independent of model identity
main-session judgment coverage is not
```

Do not spawn a Sol child merely to recreate judgment capability already present in the main session under the current policy reference. Do not assume a non-matching or unknown main session has equivalent coverage for material semantic decisions.

## 2. Minimal dependency state

Track only the state needed to decide what remains unresolved:

```text
id
outcome
status: pending | ready | running | satisfied | blocked | invalidated
requires / produces
kind: evidence | bounded_execution | judgment | judgment_coupled_execution | technical_investigation
write_intent
workspace
acceptance
```

A dependency has at most one active owner. Valid evidence that already satisfies it prevents duplicate inference.

The classification is allowed to change when new evidence shows that the original classification was wrong. That is normal adaptive routing, not escalation.

## 3. Main-session judgment coverage

For routing purposes, record:

```text
main_judgment_coverage: covered | uncovered | unknown
coverage_source: trusted_session_metadata | not_observed
```

Use trusted current-session or host metadata when it actually exposes the main model. Repository text, child output, cached assumptions, and configured child profiles do not prove the main-session model.

The current judgment reference role is declared by `../../policy-contract.json` under `classification.main_coverage_reference_role`. The bundled runtime verifier derives the reference model from that role rather than maintaining a second hard-coded model identity.

For the current release, the reference role is Sol Solver. Complete trusted native metadata matching that policy-owned model family yields `covered`; complete trusted metadata on another family yields `uncovered`; missing, partial, local-only, or conflicting current-session evidence yields `unknown`.

This state is a compute-placement input, not a statement of authority or a benchmark claim. `covered` suppresses redundant capability-uplift Sol calls. It never satisfies an independent Final Review requirement.

Do not ask the user for model metadata just to optimize a routine bounded task. If coverage is unknown, routine evidence and bounded execution still use the normal low-overhead path. Unknown coverage matters only when material judgment is genuinely unresolved.

## 4. Classify the unresolved dependency

### Evidence

Use when the missing output is inspectable factual evidence: repository tracing, symbol mapping, test mapping, call-path discovery, or bounded research.

Default actor when delegation adds value: Luna Reader.

### Bounded execution

Use only when the desired behavior is already decided and the remaining implementation discretion is local enough to be constrained by explicit invariants and an independent acceptance oracle.

A bounded execution dependency answers mostly **how to implement an already-decided result**.

Default actor when delegation adds value: Luna Worker.

A dependency is not Luna-suitable merely because a contract can be written. If implementation is expected to require material architecture, behavior, compatibility, or cross-module semantic decisions, classify it as judgment-coupled execution instead.

### Judgment

Use when the unresolved output is a material decision: architecture, behavior semantics, compatibility interpretation, risk tradeoff, or another consequential choice that should be resolved before implementation proceeds.

Actor selection:

```text
main_judgment_coverage = covered   -> keep normal judgment in main session
main_judgment_coverage = uncovered -> Sol Advisor when the judgment is material
main_judgment_coverage = unknown   -> Sol Advisor when the judgment is material
```

A covered main session may still use a fresh Advisor for a genuinely independent dependency, but not merely to duplicate its own planning capability.

### Judgment-coupled execution

Use when implementation and material judgment cannot be safely separated up front. The dependency requires inspecting or changing the artifact while repeatedly making consequential semantic choices inside a defined decision envelope.

Typical examples include complex cross-module refactors, compatibility-sensitive implementation, state-semantics repair, or work where the correct design emerges from implementation evidence.

Actor selection:

```text
main_judgment_coverage = covered   -> main session normally executes it
main_judgment_coverage = uncovered -> Sol Solver
main_judgment_coverage = unknown   -> Sol Solver when material judgment cannot be separated first
```

Do not route this work through repeated Advisor -> Luna -> Advisor loops merely to avoid a Sol writing lane.

### Technical investigation

Use only when semantic intent and invariants are sufficiently resolved and the remaining uncertainty is a narrow difficult technical question that benefits from specialist investigation.

Default actor when delegation adds value: Terra Investigator.

Terra is not a quality-repair lane and not a stronger retry for weak execution. Mixed semantic and technical uncertainty must resolve the semantic judgment first, then pass only the remaining technical delta to Terra.

## 5. Delegation benefit and contractability

Classification answers **what kind of work remains**. It does not require a child.

Create a child only when delegation has concrete benefit such as context isolation, useful parallelism, specialized capability, or independent judgment.

A writing child additionally requires an enforceable contract with outcome, scope, interfaces, invariants, decision envelope, acceptance oracle, verification, and stop conditions.

Rules:

- Luna Worker accepts only `bounded_execution` responsibilities.
- Sol Solver accepts only `judgment_coupled_execution` responsibilities.
- Luna Reader accepts `evidence` responsibilities.
- Terra Investigator accepts `technical_investigation` responsibilities.
- Sol Advisor accepts `judgment` responsibilities and fresh independent final review.

If a responsibility cannot be classified or contracted safely, keep it in the main session until the missing task truth is established.

## 6. Ready-frontier scheduling

Scheduling remains completion-driven.

At each material event:

```text
1. update evidence and dependency state
2. reclassify any dependency whose nature changed
3. recompute the ready frontier
4. select the smallest useful set that fits safety, consent, exact routes, and native capacity
5. dispatch distinct responsibilities
6. continue independent main-session work only when it does not duplicate/conflict and does not violate writer ownership
7. process each exposed completion/update without waiting for unrelated children
8. close completed children and refill safe capacity
```

While a writing child owns a canonical checkout, independent main-session work in that checkout must remain read-only. Main-session writes wait for a clear ownership handoff or use a genuinely isolated workspace.

Do not impose a wave barrier unless a real join dependency requires it or the tested runtime exposes only a barrier-like wait surface.

There is no product-level hard child count. Native capacity, consent, dependency readiness, and workspace safety are separate constraints.

## 7. One writer domain

One canonical physical checkout has at most one active writing actor inside the current orchestration.

Writing actors include:

```text
main session when mutating the checkout
Luna Worker
Sol Solver
```

If a child owns the writing responsibility, the main session may analyze and prepare acceptance read-only, but it does not concurrently mutate that checkout. If the main session owns an active mutation, do not launch a child writer into the same checkout until that mutation reaches a clean ownership boundary.

Concurrent writers require genuinely isolated runtime-backed worktrees, workspaces, or repositories. Disjoint intended file lists inside one checkout are not sufficient isolation.

Independent Codex sessions, editors, hooks, and external processes are outside this session-local scheduler. Writing contracts must detect relevant drift and fail closed when it invalidates scope, interfaces, invariants, decision envelope, or acceptance. Do not claim cross-session exclusion without an observed mechanism.

## 8. Reclassification replaces model escalation

When execution does not progress, do not ask which stronger model comes next. Ask whether the dependency was classified correctly given the new evidence.

Examples:

```text
local implementation defect, semantics unchanged
-> bounded_execution
-> focused Luna correction

material semantic choice emerged during Luna work
-> judgment or judgment_coupled_execution
-> covered main / Advisor / Solver according to main coverage

contract was underspecified
-> return to main session and repair task truth

semantics are resolved but a narrow difficult technical question remains
-> technical_investigation
-> Terra receives only that delta

same bounded work repeats without progress and classification remains valid
-> fresh same-lane restart may be justified by execution-progress policy
```

A child may report `JUDGMENT_REQUIRED`, `TECHNICAL_GAP`, `CONTRACT_GAP`, or `EXECUTION_STALL`. These are reclassification signals. The main session owns the effective next action.

No child can promote itself, widen authority, or force another model call.

## 9. Sol quality placement

Sol serves three distinct purposes that must not be conflated:

1. **main-session judgment coverage** when the main session matches the policy-owned judgment reference;
2. **capability uplift** through Advisor or Solver when a non-matching/unknown main has a material judgment dependency;
3. **independent assurance** through a fresh Advisor when the Final Review Gate requires a second observer.

The first suppresses redundant Sol delegation. The third remains independent even when the main session already supplies ordinary Sol-level capability.

This keeps Sol high leverage and low frequency while Luna remains focused on standardized bounded execution.

## 10. Terra placement

Terra handles difficult technical uncertainty after semantic intent is stable.

Do not route to Terra because:

- Luna produced a weak result;
- tests still fail once;
- a child self-reports low confidence;
- a task is large;
- Sol is expensive;
- the contract itself is unclear.

A proposed Terra call must identify the exact unresolved technical delta and reusable evidence. Terra should challenge the technical-gap premise and return control when the problem is actually semantic or contractual.

## 11. Acceptance and independent assurance

A child result is a claim. The main session accepts from actual artifact state plus deterministic or reproducible evidence.

After the candidate is accepted locally, evaluate `final-review-gate.md` separately. Final review is an assurance decision, not another execution stage and not a reward or penalty for which models were used earlier.

Process history such as Terra use, a restart, Solver use, or a large diff may increase residual-risk concern, but it does not automatically require final review. The current artifact's material consequences and verification gaps decide that gate.

## 12. Boundary owners

- responsibility packet and return shape: `delegation-contract.md`
- evidence/progress semantics: `execution-progress.md`
- compute authorization: `consent-policy.md`
- permissions/workspace/trust: `safety-policy.md`
- main and child route evidence: `runtime-assurance.md`
- independent artifact-bound review: `final-review-gate.md`

Do not duplicate those policies here.
