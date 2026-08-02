# Routing Policy

## 1. Control model

The current user-facing Codex session is the main session and owns the task-level compute graph.

It owns intent, scope, architecture, decision rights, scheduling, evidence state, integration, acceptance, and the final answer. It does not need to be Sol.

Models are compute tiers, not mandatory stages.

## 2. No fixed pipeline

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

## 3. Delegation Benefit Gate

A child requires at least one concrete benefit:

- context isolation;
- useful parallelism across different dependencies;
- specialized execution or investigation capability;
- independent high-value judgment.

Task length, file count, lower price, spare concurrency, or generic desire for caution are insufficient by themselves.

## 4. Contractability Gate

Before a writing Worker is spawned, `delegation-contract.md` must define an enforceable outcome, scope, invariants, decision rights, acceptance oracle, verification, and stop/escalation conditions.

Missing acceptance or decision boundaries return the responsibility to the main session.

## 5. Minimum resource principle

- Zero children is normal.
- Default children: 1.
- Normal maximum: 2.
- Hard maximum: 4.
- At most one active writing Worker per shared workspace.
- Multiple writing Workers require runtime-backed isolated workspaces.
- One child receives at most one focused follow-up for the same responsibility.
- Delegation depth is 1.

The normal envelope is resource-based, not a fixed team shape: at most two justified children and at most one writer, without permission, scope, or external-impact expansion.

## 6. Semantic roles and route policy

Role identity is separate from model identity.

| Semantic responsibility | Agent type | Current route | Default permission | Purpose |
| --- | --- | --- | --- | --- |
| reader | `codex_agent_team_reader` | GPT-5.6 Luna `max` | read-only | bounded search, tracing, mapping, evidence collection |
| worker | `codex_agent_team_worker` | GPT-5.6 Luna `max` | workspace-write | contractable implementation, debugging, tests |
| investigator | `codex_agent_team_investigator` | GPT-5.6 Terra `xhigh` | read-only | unresolved complex technical delta |
| advisor | `codex_agent_team_advisor` | GPT-5.6 Sol `high` | read-only | judgment and selective review |

Luna Max is intentionally fixed for the current execution baseline. Terra and Sol routes remain policy hypotheses to validate with representative workloads.

Changing a route in the future must not require renaming the semantic role.

## 7. Luna execution tier

Use Luna Reader for bounded evidence gathering and Luna Worker for contractable writing work.

Luna owns execution choices explicitly granted in the Delegation Contract. It does not receive broader decision authority merely because the task is difficult.

When Luna fails acceptance, do not automatically upgrade the whole task. Classify the failure:

```text
mechanical defect -> focused Luna correction
contract gap -> main session repairs contract
capability gap -> Terra receives unresolved delta
judgment gap -> main session or Sol
```

## 8. Terra investigation tier

Terra is not a mandatory reviewer and not a generic second implementation attempt.

Use it when a clear task exposes a difficult technical dependency whose resolution requires materially more context synthesis or technical reasoning than the Luna contract can safely carry.

Terra receives:

- the unresolved delta;
- relevant valid evidence;
- current artifact or failure;
- explicit `DO NOT REDO` items.

By default Terra remains read-only. After it resolves the delta, the main session may update the contract and return implementation to Luna.

A mediocre Luna result with no identified capability gap is not sufficient reason to invoke Terra.

## 9. Sol judgment and review tier

Sol is the high-value judgment resource.

Use it when:

- a product, architecture, security, migration, or public-contract decision materially changes the task;
- competing judgments remain consequential after deterministic evidence is established;
- an implementation has clear acceptance criteria but the actual diff merits a stronger independent review;
- the user explicitly requests a stronger review.

Sol receives compressed facts and one decision/review question. It should not repeat repository discovery or deterministic tests already established unless their evidence is invalid, contradictory, or insufficient.

A common valid graph is:

```text
main -> Luna -> Sol -> main
```

Terra is not required between Luna and Sol.

## 10. Shared Evidence State

Evidence is reused across nodes while its dependencies remain valid.

Treat these categories differently:

- **deterministic**: command/test/compiler/build/hash output;
- **repository_fact**: file/symbol/call-path/interface facts;
- **model_judgment**: hypotheses, recommendations, interpretations.

Deterministic and repository facts may be cached with dependencies. Model judgments remain challengeable hypotheses.

A change invalidates only evidence that depends on the changed input. Do not rerun a full scan because one unrelated file changed.

## 11. Useful parallelism

Parallel execution is useful when concurrent outputs satisfy different dependencies.

Examples:

- two independent read-only Luna branches map separate subsystems;
- the main session prepares acceptance/risk checks while Luna implements;
- a long deterministic test command runs while independent read-only analysis progresses.

Do not launch Luna, Terra, and Sol over the same question simply to maximize concurrency.

## 12. Profile route assurance

The supported Plugin path uses only project custom-Agent profiles.

Before a model-specific child is spawned, require live role guidance to expose the exact semantic role with its expected locked route. Record:

```text
route_assurance = profile_locked
```

This is configuration assurance only.

There is no Portable Mode, built-in-role substitution, hidden model ladder, or inheritance-based exact route.

If the required project profile is unavailable or conflicting, keep the responsibility in the main session and report the limitation.

## 13. Runtime Evidence Gate

Runtime observation is demand-driven. Ordinary bounded execution does not require rollout inspection merely because it is available.

Use runtime evidence when:

- safety depends on effective host-enforced read-only isolation;
- route or parent-thread identity is material to the acceptance claim;
- a claimed independent model review must be proven;
- configured and observed facts conflict;
- the user explicitly requests runtime proof.

Use `runtime-assurance.md` and `scripts/verify-runtime.py`.

## 14. Context fork

Role-specific spawns set `fork_turns` explicitly.

- reader: `fork_turns = "none"`
- worker: `fork_turns = "none"` by default
- investigator: `fork_turns = "none"`
- advisor: `fork_turns = "none"`

A Worker may receive a small positive recent-N only when a user decision cannot be safely repacked into the contract. Never omit `fork_turns`; never combine `fork_turns = "all"` with an `agent_type` override on MultiAgentV2.

## 15. Failure behavior

### Route unavailable

Return the responsibility to the main session. Do not cross-role substitute.

### Luna acceptance failure

Classify before escalation. Preserve valid evidence and recompute only invalidated dependencies.

### Terra unable to resolve the delta

Return the unresolved delta to the main session. Do not expand Terra into the original task.

### Sol lacks sufficient evidence

Return `INSUFFICIENT_EVIDENCE` and name the missing dependency. Gather only that dependency before reconsidering the judgment.

### Runtime conflict

Quarantine the affected result.

### Policy violation

Reject or quarantine results involving nested delegation, unauthorized writes, scope expansion, credential exposure, wrong ancestry when material, or unapproved external side effects.
