# Routing Policy

## 1. Control model

The current user-facing Codex session is the main session and owns the task-level dependency state and compute graph.

It owns intent, scope, architecture, decision rights, scheduling, evidence state, integration, acceptance, and the final answer. It does not need to be Sol.

Models are compute lanes, not mandatory stages.

## 2. No fixed pipeline and no fixed team size

Valid task graphs include:

```text
main
main -> Luna -> main
main -> Luna -> Sol -> main
main -> Terra -> Luna -> main
main -> Luna -> Terra(delta) -> Luna -> main
main -> Sol -> main
```

`Luna -> Terra -> Sol` is never required merely because all three tiers exist.

Every Agent call must satisfy a distinct unresolved dependency. If valid existing evidence already satisfies that dependency, do not create another Agent for it.

Codex Delegate defines no product-level hard child count. Zero children is normal. The scheduler creates only the smallest useful wave from currently ready dependencies.

## 3. Dependency Ledger and ready frontier

The main session tracks material task dependencies in a compact in-session ledger:

```text
id
outcome
status: pending | ready | running | satisfied | blocked | invalidated
requires: dependency ids and/or evidence ids
produces: artifact, decision, or evidence
write_intent
workspace
acceptance
```

A dependency is ready only when all declared prerequisites are satisfied.

Scheduling rules:

- never run two children for the same dependency at the same time;
- never rerun a satisfied dependency unless changed inputs invalidate it;
- recompute readiness after evidence, artifact, user, or runtime changes;
- combine ready work into one child when that is cheaper and does not sacrifice context isolation, independent judgment, or critical-path progress;
- split work only when each packet has a distinct dependency and independent acceptance value.

The ledger is logical task state. The project does not add a persistent DAG service, background scheduler, or second Agent runtime.

## 4. Delegation Benefit Gate

A child requires at least one concrete benefit:

- context isolation;
- useful parallelism across different ready dependencies;
- specialized execution or investigation capability;
- independent high-value judgment.

Task length, file count, lower price, spare concurrency, or generic desire for caution are insufficient by themselves.

## 5. Contractability Gate

Before a writing Worker is spawned, `delegation-contract.md` must define an enforceable dependency, outcome, scope, interfaces/dependencies, invariants, decision rights, acceptance oracle, verification, and stop/escalation conditions.

Missing acceptance or decision boundaries return the responsibility to the main session.

## 6. Adaptive resource principle

The orchestration policy separates scheduling from consent and runtime capacity.

### Scheduling

The scheduler asks how many distinct ready dependencies can add value now. It does not start from a default Agent count.

### Consent

Explicit `/codex-delegate` invocation includes a baseline of up to two concurrently active justified child Agents. More than two simultaneously active children normally requires consent unless broad parallel work was already authorized.

This is a consent boundary, not a total child lifetime limit and not an orchestration target. Serial delegation can continue when new dependencies become ready, but repeated serial calls that materially expand expected compute also require consent.

### Runtime capacity

Native Codex decides how many child threads can actually run. If ready work exceeds available slots, queue or serialize the excess work. Do not invent a product ceiling from one runtime build, and do not cross-route a responsibility merely to fill an available slot.

### Workspace safety

At most one active writing Worker may target one canonical shared workspace. Multiple writers require runtime-backed isolated workspaces, worktrees, or independent repositories.

Delegation depth remains 1.

## 6A. Concurrency scopes

Treat concurrent state in three separate scopes:

```text
main-session scope
- Dependency Ledger
- ready frontier
- consent state
- active child set
- no product-level hard child count

workspace scope
- identified by the canonical physical checkout or runtime-backed isolated worktree
- at most one active writing Worker per canonical workspace
- independent workspaces may have independent writers when runtime isolation is real

Codex-home scope
- custom-Agent profiles and the managed ownership manifest are shared configuration
- one installed Codex Delegate managed profile generation is visible to sessions using that Codex home
- mixed concurrent profile generations are unsupported for v1.0.0; an exact-route mismatch stops the affected delegation rather than cross-routing
```

Repository identity alone is not the writer lock domain. Two runtime-backed isolated worktrees may be independent workspaces even when they belong to the same repository. Two sessions pointing at the same physical checkout are the same workspace even when their task scopes or intended file sets differ.

File-level ownership promises are insufficient to justify multiple writing Workers in one physical checkout. Shared generated state, lockfiles, formatters, git metadata, tests, or dependency chains may couple nominally disjoint files.

Current policy defines the invariant. Release validation must determine whether the native runtime already enforces cross-session writer exclusivity. Do not add a project lock or global scheduler until a reproducible live failure demonstrates that the invariant is otherwise unenforceable.

## 7. Semantic roles and route policy

Role identity is separate from model identity.

| Semantic responsibility | Agent type | Current route | Default permission | Purpose |
| --- | --- | --- | --- | --- |
| reader | `codex_agent_team_reader` | GPT-5.6 Luna `max` | read-only | bounded search, tracing, mapping, evidence collection |
| worker | `codex_agent_team_worker` | GPT-5.6 Luna `max` | workspace-write | contractable implementation, debugging, tests |
| investigator | `codex_agent_team_investigator` | GPT-5.6 Terra `xhigh` | read-only | unresolved complex technical delta |
| advisor | `codex_agent_team_advisor` | GPT-5.6 Sol `high` | read-only | judgment and selective review |

Luna Max is intentionally fixed for the current execution baseline. Terra and Sol routes remain policy hypotheses to validate with representative workloads.

Changing a route in the future must not require renaming the semantic role.

## 8. Initial routing by responsibility

Use the least expensive safe lane that can satisfy the bounded dependency. Do not require a lower-tier failure when the dependency itself clearly needs technical investigation or consequential judgment.

### Luna execution

Use Luna Reader for bounded evidence gathering and Luna Worker for contractable writing work.

Luna owns execution choices explicitly granted in the Delegation Contract. It does not receive broader decision authority merely because the task is difficult.

### Terra investigation

Terra is not a mandatory reviewer and not a generic second implementation attempt.

Use it when a clear task exposes a difficult technical dependency whose resolution requires materially more technical investigation or synthesis than the Luna contract can safely carry.

Terra receives the unresolved delta, relevant valid evidence, current artifact or failure, and explicit `DO NOT REDO` items. By default Terra remains read-only.

### Sol judgment and review

Sol is the high-value judgment resource.

Use it when:

- a product, architecture, security, migration, data-integrity, or public-contract decision materially changes the task;
- competing judgments remain consequential after deterministic evidence is established;
- an implementation has clear acceptance criteria but the actual diff merits a stronger independent review;
- the user explicitly requests stronger review.

Sol receives compressed facts and one decision/review question in fresh context by default. It should not repeat repository discovery or deterministic tests already established unless their evidence is invalid, contradictory, or insufficient.

Final Sol review is selective, not mandatory.

## 9. Evidence-guided recovery

Use `execution-progress.md` before repeating or escalating an execution responsibility.

A model saying it made progress is not a progress signal. Prefer deterministic verification, repository facts, artifact state, and a materially narrowed unresolved delta.

When acceptance fails, classify the evidence:

```text
mechanical defect -> focused Luna correction with a new correction hypothesis
contract gap -> main session repairs contract
execution stall/context pollution -> fresh same-lane packet with valid evidence and DO NOT REDO
capability gap -> Terra receives unresolved technical delta
judgment gap -> main session or Sol
```

Do not impose a universal retry count. Do not resend an unchanged contract. Repeated same-failure work with no new evidence is a stall signal.

If evidence already shows a capability gap, escalate the delta instead of repeatedly restarting the same execution lane.

A clean same-lane restart preserves current artifacts, valid established evidence, the failure signature, acceptance oracle, and unresolved delta. It drops private reasoning and dead-end narration.

## 10. Shared Evidence State

Evidence is reused across nodes while its dependencies remain valid.

Treat these categories differently:

- **deterministic**: command/test/compiler/build/hash output;
- **repository_fact**: file/symbol/call-path/interface facts;
- **model_judgment**: hypotheses, recommendations, interpretations.

Deterministic and repository facts may be cached with dependencies. Model judgments remain challengeable hypotheses.

A change invalidates only evidence that depends on the changed input. Do not rerun a full scan because one unrelated file changed.

Changes made by the user or another independent session are ordinary dependency changes. Reconcile the current artifact and invalidate affected evidence before continuing delegated work.

## 11. Useful parallelism

Parallel execution is useful when concurrent outputs satisfy different ready dependencies.

Examples:

- several independent read-only Luna branches map separate subsystems after broad fan-out has been authorized when needed;
- the main session prepares acceptance/risk checks while Luna implements;
- a long deterministic test command runs while independent read-only analysis progresses;
- independent projects or runtime-backed isolated worktrees may each have one writing Worker without creating a machine-wide writer bottleneck.

Do not launch Luna, Terra, and Sol over the same question simply to maximize concurrency.

Do not treat disjoint intended file lists as proof that two writers are safe in the same physical checkout.

When runtime slots are saturated, leave remaining ready dependencies pending. Slot pressure is not a reason for duplicate inference or lower-quality role substitution.

## 12. Profile route assurance

The supported Plugin path uses only project custom-Agent profiles.

Before a model-specific child is spawned, require live role guidance to expose the exact semantic role with its expected locked route. Record:

```text
route_assurance = profile_locked
```

This is configuration assurance only.

There is no Portable Mode, built-in-role substitution, hidden model ladder, or inheritance-based exact route.

If the required project profile is unavailable or conflicting, keep the responsibility in the main session and report the limitation.

The profiles are Codex-home scoped shared configuration. A session whose expected profile generation no longer matches the installed exact route must fail closed for that lane. It must not silently reinstall, downgrade, or cross-route merely to keep a concurrent older/newer project session working.

## 13. Runtime Evidence Gate

Runtime observation is demand-driven. Ordinary bounded execution does not require rollout inspection merely because it is available.

Use runtime evidence when:

- safety depends on effective host-enforced read-only isolation;
- route or parent-thread identity is material to the acceptance claim;
- a claimed independent model review must be proven;
- configured and observed facts conflict;
- native capacity or lifecycle behavior is being characterized for release validation;
- the user explicitly requests runtime proof.

Use `runtime-assurance.md` and `scripts/verify-runtime.py`.
