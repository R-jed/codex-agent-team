---
name: codex-delegate
description: Build the smallest useful native Codex Subagent compute graph by classifying unresolved dependencies, accounting for main-session judgment coverage, routing bounded execution to Luna, judgment-coupled execution to Sol, difficult technical uncertainty to Terra, reusing evidence, and applying independent final review only when the deliverable's consequences require it.
---

# Codex Delegate

Use this Skill as a thin policy layer over Codex Native Subagents. The current main session remains the task-level control plane. Child Agents receive one classified unresolved dependency only when delegation creates concrete value.

Stable role/classification/review constants live in `../../policy-contract.json`. `references/routing-policy.md` is the single normative owner for dependency classification, actor selection, main-session judgment coverage, scheduling, and reclassification.

## Core invariants

1. Main session owns user intent, scope, authorization, task state, integration, acceptance, and final response.
2. Main-session authority is independent of model identity; main-session judgment coverage is not.
3. Every child call satisfies a distinct unresolved dependency that valid existing evidence does not already satisfy.
4. Zero children is normal. There is no mandatory model sequence, fixed team shape, or product hard child count.
5. Luna Worker receives only standardized bounded execution whose material behavior decisions are already made.
6. Sol Solver receives judgment-coupled implementation only when material judgment cannot be safely separated and the main session does not already cover that capability.
7. Terra receives only a narrow difficult technical uncertainty after semantic intent is stable.
8. Sol Advisor provides material judgment uplift or fresh independent final review. A Sol main session suppresses redundant capability-uplift Sol calls but never substitutes for required independent review.
9. One canonical physical checkout has at most one active writing project Agent. Delegation depth remains one.
10. Child reports are claims. Acceptance uses actual artifact state plus deterministic/reproducible evidence.
11. Failure does not imply escalation. New evidence reclassifies the same dependency when its nature changed.
12. Valid deterministic/repository evidence is reused until its dependencies change.
13. Consent governs material expansion in compute, concurrency, permission, scope, or external impact; it is not the scheduler.
14. A required Final Review Gate completes only on a fresh Sol `ship` verdict for the unchanged bound artifact.

## 1. Understand the task and initialize compact state

Identify the user's observable outcome, authorization, constraints, consequence of error, acceptance signals, and relevant repository/runtime facts.

Do not begin with a model, Agent count, or planned Luna -> Terra -> Sol sequence.

Maintain only:

```text
Dependency Ledger
- id / outcome / status / requires / produces
- kind: evidence | bounded_execution | judgment | judgment_coupled_execution | technical_investigation
- write intent / workspace / acceptance

Shared Evidence State
- id / type: deterministic | repository_fact | model_judgment
- claim / source / depends_on / validity

Recovery Ledger
- material attempt facts needed to avoid repeated dead ends

Main Judgment Coverage
- covered | uncovered | unknown
- source when actually observed
```

Do not duplicate a dependency already running or satisfied unless changed inputs invalidate it.

## 2. Classify what is actually unresolved

Use `references/routing-policy.md`.

The five dependency kinds are:

```text
evidence
-> missing inspectable facts

bounded_execution
-> desired behavior is decided; remaining discretion is local and independently verifiable

judgment
-> material architecture / behavior / compatibility / risk decision

judgment_coupled_execution
-> implementation and material semantic judgment cannot be safely separated

technical_investigation
-> semantics are stable; a narrow difficult technical uncertainty remains
```

A task being large, expensive, many-file, or contractable does not determine its kind.

The critical distinction is:

```text
contractable != Luna-suitable
```

If material semantic discretion is expected during implementation, do not disguise it as bounded Luna work.

## 3. Account for main-session judgment coverage only when it matters

When trusted current-session metadata exposes the main model and material judgment is unresolved, normalize it through `references/runtime-assurance.md` / `../../scripts/runtime-evidence.py`.

Routing V4 uses:

```text
covered   -> current main is trusted as GPT-5.6 Sol family for normal judgment placement
uncovered -> trusted current main is outside that family
unknown   -> route not observed completely or is conflicted
```

Do not inspect or ask for main-model metadata for routine bounded work merely to optimize cost.

When coverage is `covered`, keep normal judgment and judgment-coupled implementation in the main session by default. Do not spawn another Sol solely to recreate capability already present.

When coverage is `uncovered` or `unknown`, material judgment may justify Sol Advisor; judgment-coupled implementation may justify Sol Solver.

Independent Final Review is separate and may still require a fresh Advisor regardless of main model.

## 4. Select the smallest useful actor

Classification maps to role, subject to delegation benefit:

```text
evidence                    -> main or codex_delegate_reader
bounded_execution           -> main or codex_delegate_worker
judgment                    -> Sol main, or codex_delegate_advisor when coverage is uncovered/unknown
judgment_coupled_execution  -> Sol main, or codex_delegate_solver when coverage is uncovered/unknown
technical_investigation     -> main or codex_delegate_investigator
```

A child is justified only for concrete context isolation, useful parallelism, specialized capability, or independent judgment.

Cost is a constraint and tie-breaker among safe useful choices. Lower price does not make a role semantically appropriate.

## 5. Compile the responsibility, then ensure the exact role

Use `references/delegation-contract.md`.

Writing responsibilities require enforceable outcome, scope, interfaces, invariants, decision envelope, acceptance oracle, verification, and stop conditions.

Role availability is checked only after a dependency justifies that role. Exact current roles come from `../../policy-contract.json`.

If a required role is unavailable, resolve the bundled installer relative to this Skill:

```text
installer = skill_dir/../../scripts/install-agents.py
```

Explain its managed write scope and request permission before running:

```bash
python "$installer"
python "$installer" --check
```

It manages only the current project profiles and `.codex-delegate-agents.json`. It does not modify unrelated Agent profiles, credentials, MCP configuration, repositories, or `config.toml`.

Exact-route mismatch fails closed. Do not cross-route simply to keep work moving.

## 6. Dispatch completion-driven work

Dispatch the smallest useful set of ready dependencies that fits:

```text
classification
contractability
consent
workspace safety
exact route availability
native capacity
```

Scheduling is completion-driven. Process a child's exposed completion/update as soon as useful, merge supported evidence, close completed children, recompute the ready frontier, and refill safe capacity without waiting for unrelated work.

A barrier is used only for a real join dependency or when the tested native runtime exposes no finer completion surface.

At most one active writing project Agent may target one canonical checkout. Both Worker and Solver count as writers.

## 7. Verify and reclassify instead of escalating

When a child returns:

1. inspect actual artifact/diff/state;
2. inspect exact verification results;
3. merge only supported evidence;
4. update acceptance state;
5. decide whether the dependency is satisfied;
6. if unresolved, rerun the same classifier with the new evidence.

Use `references/execution-progress.md` for progress semantics.

Standard reclassification signals are:

```text
CONTRACT_GAP
JUDGMENT_REQUIRED
TECHNICAL_GAP
EXECUTION_STALL
```

Examples:

```text
bounded local defect, semantics unchanged
-> focused Luna correction

material semantic choice emerged
-> judgment or judgment_coupled_execution
-> main Sol / Advisor / Solver according to main coverage

narrow difficult technical uncertainty remains after semantics stabilize
-> technical_investigation
-> Terra gets only that delta

same bounded work stalls but classification remains correct
-> optional clean same-role restart with fresh evidence packet
```

Do not translate a failed Luna attempt directly into Terra or Sol. Reclassification is the decision point.

## 8. Apply boundary policies where relevant

- `references/safety-policy.md`: permission, trust, writer isolation, external impact, delegation depth
- `references/consent-policy.md`: material compute/fan-out/scope/permission expansion
- `references/runtime-assurance.md`: main-session coverage plus child route/ancestry/permission evidence

Do not manufacture runtime facts that the current Codex build did not expose.

## 9. Apply independent Final Review only to the candidate's consequences

After the main session has a Candidate Ready artifact, evaluate `references/final-review-gate.md`.

Mandatory triggers come from the current artifact's semantic consequences and verification gaps. Prior use of Terra, Solver, recovery, or a large diff is evidence to consider, not an automatic review trigger.

If review is required:

```text
Candidate Ready
-> bind review_artifact_id
-> fresh codex_delegate_advisor with fork_turns: none
-> ship | fix-first | rethink | INSUFFICIENT_EVIDENCE
```

Only `ship` for the unchanged current artifact satisfies a required gate.

## 10. Close and report

Close completed, superseded, rejected, or no-longer-needed children promptly.

Use `references/orchestration-receipt.md` when explicit `/codex-delegate` use, child execution, capability placement, reclassification, consent, or Final Review materially affected the workflow.

The receipt summarizes meaningful orchestration decisions and never replaces the normal completion report.

## References

- `references/routing-policy.md`: classification, actor selection, main coverage, scheduling, reclassification
- `references/delegation-contract.md`: responsibility and return packet
- `references/execution-progress.md`: progress/stall evidence and recovery facts
- `references/consent-policy.md`: resource authorization
- `references/safety-policy.md`: permission, trust, writer safety, external effects
- `references/runtime-assurance.md`: main and child runtime evidence
- `references/final-review-gate.md`: independent artifact-bound assurance
- `references/orchestration-receipt.md`: compact user-visible orchestration record
