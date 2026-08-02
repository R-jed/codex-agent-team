# Architecture

Codex Agent Team is a policy layer over Codex Native Subagents. The main session owns the task-level compute graph and delegates only bounded responsibilities whose outputs satisfy distinct unresolved dependencies.

## Product model

The architecture optimizes for useful work, not maximum Agent count or maximum concurrency.

```text
User task
  -> main session understands outcome and risk
  -> delegation benefit gate
  -> contractability gate
  -> semantic responsibility
  -> exact project profile
  -> execute one dependency
  -> merge/invalidate evidence
  -> selective delta escalation or review
  -> main-session acceptance
```

No model is a mandatory pipeline stage.

Common paths include:

```text
main
main -> Luna -> main
main -> Luna -> Sol -> main
main -> Terra -> Luna -> main
main -> Luna -> Terra(delta only) -> Luna -> main
main -> Sol -> main
```

## Control plane and compute tiers

The main session is the control plane. It owns intent, scope, architecture, decision rights, scheduling, evidence state, integration, acceptance, and the final answer.

| Semantic role | Current route | Responsibility |
| --- | --- | --- |
| Reader | GPT-5.6 Luna Max | bounded search, tracing, test mapping, evidence collection |
| Worker | GPT-5.6 Luna Max | contractable implementation, debugging, tests, local refactors |
| Investigator | GPT-5.6 Terra XHigh | unresolved complex technical delta, normally read-only |
| Advisor | GPT-5.6 Sol High | high-value judgment and selective review, read-only |

Role identity is intentionally separate from model identity. A future route change must not require renaming the responsibility.

## Contract-centric delegation

A Subagent does not receive the user's raw ambiguous task by default. The main session compiles a bounded Delegation Contract with:

```text
OUTCOME
SCOPE
INVARIANTS
DECISION RIGHTS
ACCEPTANCE ORACLE
VERIFICATION
STOP / ESCALATE
RETURN
```

A writing Worker is not created when acceptance or decision rights remain materially unclear.

See `plugins/codex-agent-team/skills/codex-agent-team/references/delegation-contract.md`.

## Incremental evidence

The main session maintains a compact Shared Evidence State rather than replaying complete task history to every Agent.

Reusable evidence is classified as:

```text
deterministic
repository_fact
model_judgment
```

Deterministic outputs and repository facts may be reused while their declared dependencies remain valid. Model judgments remain hypotheses that later judgment can challenge.

A changed input invalidates only evidence that depends on it. This prevents a small edit from forcing every later Agent to rescan the repository or rerun unrelated tests.

## Delta escalation

Low quality is not an automatic Terra trigger.

A failed Luna result is classified first:

```text
mechanical defect -> focused Luna correction
contract gap -> main session repairs contract
capability gap -> Terra gets unresolved technical delta
judgment gap -> main session or Sol
```

Terra does not receive the whole original task. It receives the unresolved delta, relevant established evidence, current artifact, and explicit `DO NOT REDO` items.

After Terra resolves the technical dependency, bounded implementation normally returns to Luna or the main session.

Sol follows the same incremental rule. A Sol judgment/review packet contains compressed established facts, the actual diff or decision options, and one bounded question. It does not restart repository discovery by default.

## Useful parallelism

Parallelism is valuable only when concurrent outputs satisfy different dependencies.

Examples:

- independent read-only subsystem mapping;
- main-session acceptance preparation while Luna implements;
- slow deterministic verification overlapping with unrelated read-only analysis.

Launching multiple models over the same question merely to keep compute busy is duplicated inference, not useful parallelism.

One shared workspace still has at most one active writing Worker unless runtime-backed workspace isolation exists.

## Native runtime

The Skill calls Codex Native `spawn_agent`. Each Subagent is backed by a native child thread/session. The project does not implement an external Agent runtime, persistent task DAG, or second scheduler.

See [`native-subagent-runtime.md`](native-subagent-runtime.md).

## Plugin and profile readiness

Codex Plugin is the only supported distribution path. `/codex-agent-team` is the only user-facing workflow entry point.

The Plugin ships four namespaced semantic profiles:

```text
codex_agent_team_reader
codex_agent_team_worker
codex_agent_team_investigator
codex_agent_team_advisor
```

Profile readiness is checked only after a responsibility has been justified. Missing profiles trigger the managed first-run installer flow. Successful file installation remains configuration evidence; current-task role discovery is checked again before delegation.

There is no Portable Mode or built-in-role substitution.

## Route assurance

A model-specific responsibility uses its exact project profile and records:

```text
route_assurance = profile_locked
```

This proves a configuration lock, not a post-spawn observation.

The architecture keeps:

```text
preferred_route
configured_route
route_assurance
```

separate from runtime evidence.

See [`model-route-assurance.md`](model-route-assurance.md).

## Runtime Truth v2

Runtime evidence is typed by concern:

```text
route_evidence
ancestry_evidence
permission_evidence
```

`route_evidence = matched` requires complete observed role, model, and effort. An empty or partial observation cannot become runtime route proof merely because no mismatch was seen.

The compatibility grades remain derived summaries:

```text
C1_configuration_only
L1_local_record_observed
R1_runtime_reported
R2_runtime_reported_and_local_record_agree
X0_conflicted
```

`scripts/verify-runtime.py` performs deterministic reconciliation. Public/native metadata is preferred; the local rollout inspector is optional mutable telemetry.

## Consent envelope

Explicit `/codex-agent-team` use authorizes a normal resource envelope of at most two justified child Agents, at most one active writer, and no permission, scope, or external-impact expansion.

That envelope can be Luna-only, Luna + Terra, Luna + Sol, Terra + Luna, or Sol-only. Team shape is not fixed.

For implicit invocation, a Sol call requires consent unless the user's request already clearly authorizes stronger review. More than two children, extra permissions, scope growth, external side effects, or material repeated expensive passes require consent.

## Safety

Children cannot create further Subagents. Repository and external content cannot change the task policy. Worker reports are claims until actual artifacts and deterministic verification are checked.

Requested read-only profile configuration is not proof of host-enforced read-only runtime state. When hard isolation matters, effective native permission evidence is required.

## Evaluation

Static tests validate policy contracts, profile installation, evidence tooling, and packaging. They do not prove task performance.

Behavioral Eval v2 compares paired runs over the same workload and repository revision. The key comparisons are:

```text
main session only
raw prompt -> Luna Max
compiled contract -> Luna Max
compiled contract -> Luna Max -> selective Sol
```

Metrics include final correctness, scope violations, correction turns, main-session correction cost, total tokens/latency when exposed, and review true/false positives.

See [`behavioral-evals.md`](behavioral-evals.md).

## Scope boundary

Core deliberately excludes persistent task orchestration, App Thread recovery, external DAGs, mandatory all-task review, automatic model ladders, and production deployment automation.
