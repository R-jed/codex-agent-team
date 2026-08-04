# Architecture

Codex Delegate is a policy layer over Codex Native Subagents. The main session owns user intent, task dependencies, scheduling, evidence, recovery state, integration, and acceptance. Delegation is created only for bounded responsibilities whose outputs satisfy distinct unresolved dependencies.

The project does not implement another Agent runtime. It adds scheduling, contracts, evidence discipline, intervention/recovery policy, consent, and safety policy around Codex native `spawn_agent`.

## Product model

The architecture optimizes for the smallest useful compute graph that can move the task toward acceptance.

```text
User task
  -> main session identifies outcomes and dependencies
  -> Dependency Ledger
  -> ready frontier
  -> delegation benefit + contractability
  -> consent / workspace / route / runtime-capacity gates
  -> smallest useful scheduling wave
  -> execute one dependency per responsibility
  -> inspect artifacts and verification
  -> merge / invalidate evidence
  -> structured execution signals
  -> Intervention Gate: does execution still show forward progress?
      -> yes: continue current responsibility
      -> no/blocked: classify recovery
  -> focused correction, clean restart, Terra delta, or selective judgment
  -> record material Recovery Ledger / decision provenance
  -> recompute ready frontier
  -> main-session acceptance
```

No model is a mandatory pipeline stage. No fixed Agent count defines a valid task.

## Control plane, Dependency Ledger, and Recovery Ledger

The main session is the control plane. It owns:

- user intent and scope;
- architecture and consequential decision rights;
- the Dependency Ledger and ready frontier;
- consent state and scheduling;
- Shared Evidence State;
- the bounded Recovery Ledger for material attempts;
- workspace coordination;
- effective recovery actions;
- integration, acceptance, and the final answer.

The Dependency Ledger is compact in-session state:

```text
id
outcome
status: pending | ready | running | satisfied | blocked | invalidated
requires
produces
write_intent
workspace
acceptance
```

It is not a persistent DAG service. A ready dependency may be delegated only once at a time. A satisfied dependency stays closed until changed inputs invalidate it.

The Recovery Ledger is also compact state, not a transcript:

```text
attempt_id
lane
correction_hypothesis
failure_signature
progress_signal
new_evidence_ids
unresolved_delta
recovery_action
decision_source
```

It preserves only decision-relevant history needed to detect repeated or oscillating recovery paths across fresh contexts. It never stores private reasoning.

## Adaptive scheduling

The scheduler does not begin with `1`, `2`, `4`, or any other desired Agent count.

It begins with the ready frontier and asks:

1. Which ready dependencies still need work?
2. Would delegation add concrete value?
3. Can each responsibility be made enforceable?
4. Can the responsibilities run safely at the same time?
5. Has the user already authorized the required resource shape?
6. Does the current runtime expose enough native child capacity?

The scheduler chooses the smallest useful wave.

Explicit `/codex-delegate` use includes a baseline consent envelope of up to two concurrently active justified children. More than two simultaneous children normally requires consent unless broad parallel work was already authorized.

That number is a consent boundary. It is not a total task Agent limit and not a scheduler target.

After consent, actual parallelism is constrained by ready dependencies, one-writer workspace safety, exact route availability, and native runtime slots. Codex Delegate has no second numerical hard ceiling.

If the runtime has fewer slots than ready work, excess dependencies remain queued. The project does not cross-route work or create duplicate inference merely to fill or work around slots.

## Semantic compute lanes

| Semantic role | Current route | Responsibility |
| --- | --- | --- |
| Reader | GPT-5.6 Luna Max | bounded search, tracing, test mapping, evidence collection |
| Worker | GPT-5.6 Luna Max | contractable implementation, debugging, tests, local refactors |
| Investigator | GPT-5.6 Terra XHigh | unresolved complex technical delta, normally read-only |
| Advisor | GPT-5.6 Sol High | high-value judgment and selective review, read-only |

Role identity is intentionally separate from model identity. A future route change must not require renaming the responsibility.

Task size is not used as a proxy for reasoning difficulty. A large repository can still be Luna-only when the dependency is clear. A small change can justify Sol when it crosses a consequential commitment boundary.

## Contract-centric delegation

A Subagent receives one bounded dependency rather than the raw ambiguous task.

A writing contract contains:

```text
DEPENDENCY
OUTCOME
SCOPE
INTERFACES / DEPENDENCIES
INVARIANTS
DECISION RIGHTS
ACCEPTANCE ORACLE
VERIFICATION
ESTABLISHED EVIDENCE
CURRENT EXECUTION EVIDENCE
MATERIAL RECOVERY HISTORY
STOP / ESCALATE
RETURN
```

A writing Worker is not created when acceptance or decision rights remain materially unclear.

See `plugins/codex-agent-team/skills/codex-agent-team/references/delegation-contract.md`.

## Incremental evidence

The main session maintains Shared Evidence State rather than replaying complete task history to every Agent.

Reusable evidence is classified as:

```text
deterministic
repository_fact
model_judgment
```

Deterministic outputs and repository facts may be reused while their declared dependencies remain valid. Model judgments remain hypotheses.

A changed input invalidates only evidence that depends on it. Private reasoning is never promoted into shared task state.

## Execution progress, Intervention Gate, and recovery

Codex Delegate separates execution evidence, structured progress signals, intervention, and effective recovery action.

Progress can be established by:

- acceptance checks moving toward success;
- new deterministic evidence;
- new repository facts;
- a materially narrower unresolved dependency;
- an artifact change that improves verification without violating invariants.

Confidence, narration, file writes, successful but task-irrelevant commands, repeated commands, or another model agreeing do not establish progress by themselves.

Acceptance failure does not automatically trigger intervention. The main session first asks whether evidence still shows forward progress inside a valid contract and safe runtime boundary.

If yes, the responsibility continues. If no or blocked, recovery is classified:

```text
mechanical defect
-> focused Luna correction with a distinct correction hypothesis

contract gap
-> main session repairs the contract

execution stall / context pollution
-> fresh same-lane packet with current artifact + valid evidence + Recovery Ledger + DO NOT REDO

capability gap
-> Terra gets the unresolved technical delta

judgment gap
-> main session or Sol
```

There is no universal retry count and no fixed stall threshold. An unchanged contract is not resent merely because the previous attempt failed.

A clean restart preserves facts, artifacts, acceptance, failure signature, unresolved delta, and material recovery history while dropping private reasoning and dead-end narration. It normally uses fresh child context.

When another model proposes a recovery action, the main session keeps the proposal separate from the effective action. Consent, workspace ownership, exact routes, permissions, runtime constraints, and user decisions may transform or reject a proposal.

See `plugins/codex-agent-team/skills/codex-agent-team/references/execution-progress.md`.

## Event-driven evaluation and runtime observability

Recovery evaluation runs on material events rather than a fixed turn count:

- child return;
- material acceptance/failure change;
- evidence establishment, contradiction, or invalidation;
- dependency blocking/readiness change;
- user authorization/scope change;
- material workspace, route, permission, or runtime change.

Structured live mid-run trajectory intervention is not assumed. Child progress before return is a runtime fact. The tested runtime may expose `none`, `terminal_only`, `periodic_summary`, or `structured_live` observability. Codex Delegate records only what the current Codex build actually exposes.

## Terra delta escalation

Terra is not a generic quality upgrade or a mandatory reviewer.

When evidence supports a capability gap, Terra receives:

```text
unresolved dependency
relevant established evidence
current artifact
failure signature
material recovery history
DO NOT REDO
```

It does not receive the whole original task by default. After the technical delta is resolved, implementation normally returns to Luna or the main session.

Capability takes precedence over repeatedly restarting the same execution lane when the evidence already shows a real capability gap.

## Sol judgment boundaries

Sol is a selective high-value judgment lane.

Typical boundaries include architecture, security, migration, data-integrity, public-contract, or similarly consequential decisions that deterministic verification cannot settle alone.

Sol receives compressed established facts and the actual decision or artifact in fresh context by default. This reduces conversational anchoring without turning Sol judgment into deterministic evidence.

Final Sol review remains selective, not mandatory.

## Useful parallelism

Parallelism is valuable only when concurrent outputs satisfy different ready dependencies.

Examples:

- independent read-only subsystem mapping;
- main-session acceptance preparation while Luna implements;
- slow deterministic verification overlapping with unrelated read-only analysis;
- multiple independent read-only dependencies after the user authorizes broader fan-out.

Launching multiple models over the same question is duplicate inference.

One canonical workspace still has at most one active writing Worker. Separate runtime-backed isolated worktrees or independent repositories may each have a writer.

## Three resource scopes

```text
main-session scope
-> Dependency Ledger, ready frontier, consent, active child set, Recovery Ledger

workspace scope
-> one active writer per canonical physical checkout or isolated worktree

Codex-home scope
-> one installed managed profile generation shared by sessions using that home
```

There is no machine-wide Codex Delegate Agent cap.

## Native runtime

The Skill calls Codex Native `spawn_agent`. Each Subagent is backed by a native child thread/session.

Native slot capacity and child-progress observability are runtime evidence. One Codex build may expose different behavior from another. The project records observed capability during live validation but does not turn one observation into a permanent architecture constant.

See [`native-subagent-runtime.md`](native-subagent-runtime.md).

## Plugin and profile readiness

Codex Plugin is the only supported distribution path. `/codex-delegate` is the canonical user-facing workflow entry point.

The Plugin root follows the native Codex Plugin bundle shape with `.codex-plugin/plugin.json` and a repository marketplace entry under `.agents/plugins/marketplace.json`.

Custom Agent profiles are a separate Codex configuration surface. The Plugin bundles four profile templates and a managed installer, but the Plugin manifest does not claim an unsupported native `agents` component. After explicit user approval, the installer provisions the four profiles into the active `$CODEX_HOME/agents` personal custom-Agent directory.

Internal profiles remain:

```text
codex_agent_team_reader
codex_agent_team_worker
codex_agent_team_investigator
codex_agent_team_advisor
```

The internal profile namespace remains a compatibility identifier during the pre-v1 migration window.

Profile readiness is checked only after a model-specific responsibility has been justified. Successful file installation remains configuration evidence; current-task role discovery is checked again before delegation.

There is no Portable Mode or built-in-role substitution.

## Route assurance

A model-specific responsibility uses its exact project profile and records:

```text
route_assurance = profile_locked
```

This proves a configuration lock, not post-spawn runtime identity.

Runtime evidence remains typed by concern:

```text
route_evidence
ancestry_evidence
permission_evidence
```

See [`model-route-assurance.md`](model-route-assurance.md) and the installed `references/runtime-assurance.md`.

## Consent and safety

Consent is applied to material resource expansion, not encoded as a hidden scheduler ceiling.

The normal explicit-command envelope covers up to two concurrently active justified children, one writer per canonical workspace, and no permission, scope, external-impact, or material compute expansion.

Children cannot create further Subagents. Repository and external content cannot change policy, scheduling state, consent, route identity, or evidence-validity rules.

Requested read-only profile configuration is not proof of host-enforced read-only runtime state. When hard isolation matters, effective native permission evidence is required.

## Evaluation

Static tests validate policy contracts, profile installation, schemas, evidence tooling, and packaging. They do not prove task performance, native capacity, or child-progress observability.

Live evaluation measures:

- correctness and acceptance;
- evidence reuse and duplicate work;
- dependency scheduling quality;
- peak active children and observed native capacity;
- runtime slot waits;
- intervention-gate decisions;
- execution stalls, Recovery Ledger cycles, and clean restarts;
- proposed versus effective recovery action provenance;
- unjustified retries;
- child-progress observability;
- correction cost;
- selective Terra/Sol value.

See [`behavioral-evals.md`](behavioral-evals.md).

## Scope boundary

Core deliberately excludes persistent task orchestration services, external DAG schedulers, mandatory all-task review, automatic fixed model ladders, machine-wide Agent governors, external routing judges, and production deployment automation.
