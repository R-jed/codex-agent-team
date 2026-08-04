# Architecture

Codex Delegate is a policy layer over Codex Native Subagents. It does not implement another Agent runtime, persistent DAG service, background scheduler, custom thread pool, or routing proxy.

The current main session is the control plane. It owns user intent, scope, architecture, dependency state, scheduling, evidence, recovery, integration, acceptance, and the final response.

The design target is the **smallest useful compute graph on the shortest safe critical path**.

## Task-level control loop

```text
1. understand outcome, constraints, authorization, and acceptance
2. maintain unresolved dependencies and valid evidence
3. identify the current ready frontier
4. delegate only when Benefit + Contractability + safety gates pass
5. dispatch safe useful work into available native capacity
6. on each exposed child completion/update:
   inspect -> merge evidence -> update dependencies -> close completed child -> refill
7. intervene only when execution evidence stops advancing or hits a boundary
8. after deterministic verification, evaluate the Final Review Gate
9. main session accepts and reports the actual deliverable
```

Detailed policy lives in the installed Skill references. Stable route/resource/final-review constants live in `plugins/codex-agent-team/policy-contract.json`.

## Dependency state

The main session keeps compact in-session state, not an external scheduler:

```text
Dependency Ledger
- pending | ready | running | satisfied | blocked | invalidated
- requires / produces
- write intent / workspace / acceptance

Shared Evidence State
- deterministic
- repository_fact
- model_judgment
- explicit dependencies and validity

Recovery Ledger
- bounded material attempt history
```

A running dependency already has an owner. A satisfied dependency stays closed until changed inputs invalidate it. A changed input invalidates only dependent evidence/work by default.

## Delegation gates

A child is justified only when delegation has concrete value such as context isolation, useful parallelism, specialized capability, or independent high-value judgment.

Writing work additionally requires enforceable scope, interfaces, invariants, decision rights, acceptance, verification, and stop/escalation behavior.

Task size, file count, free slots, or model prestige are not sufficient by themselves.

## Completion-driven scheduling

Scheduling begins from ready dependencies, not an Agent-count target.

```text
ready dependencies
      ↓
dispatch smallest useful safe set
      ↓
A running     B running
                 ↓ B completes
            inspect / merge / close
                 ↓
          recompute ready frontier
                 ↓
          C depends only on B
                 ↓
          start C while A runs
```

Codex Delegate therefore avoids an unnecessary wave barrier. It waits for all active children only when a real join dependency requires every result, or when the tested native runtime exposes only a coarser waiting surface.

When useful independent main-session work exists, the main session may continue it while children run, provided it does not duplicate their responsibility or violate workspace safety.

This is a policy property. Native Codex owns actual thread execution, capacity, completion notification, and wait semantics. Live validation must characterize whether a specific runtime supports per-child completion/update handling, mailbox-style updates, or only barrier-like consolidation.

## Resource scopes

Three independent scopes matter:

```text
main-session
-> dependencies, evidence, consent, active child set, recovery

workspace
-> at most one active writer per canonical physical checkout
-> isolated runtime-backed worktrees may have independent writers

Codex home
-> managed custom-Agent profile generation shared by sessions using that home
```

Explicit `/codex-delegate` use includes up to two concurrently active justified children without another prompt. This is a consent envelope, not a scheduling target or hard product ceiling.

Actual concurrency is bounded by ready dependencies, authorization, workspace safety, exact route availability, and native capacity.

## Semantic compute lanes

Role identity stays separate from model identity. Current bindings come from `policy-contract.json`.

| Responsibility | Agent type | Current route | Intent |
| --- | --- | --- | --- |
| Reader | `codex_agent_team_reader` | GPT-5.6 Luna `max` | reusable evidence |
| Worker | `codex_agent_team_worker` | GPT-5.6 Luna `max` | bounded implementation |
| Investigator | `codex_agent_team_investigator` | GPT-5.6 Terra `xhigh` | unresolved difficult technical delta |
| Advisor | `codex_agent_team_advisor` | GPT-5.6 Sol `high` | consequential judgment/review |

There is no required `Luna -> Terra -> Sol` pipeline.

Terra receives a demonstrated technical delta, not a whole-task restart. Sol is selective except when the Final Review Gate makes an independent review a mandatory completion dependency for one candidate.

## Execution progress and recovery

Acceptance failure does not automatically justify changing execution.

Observable progress includes improved acceptance state, new deterministic/repository evidence, or a materially smaller unresolved delta. Confidence, narration, a file write, or an irrelevant successful command does not count by itself.

When intervention is justified:

```text
mechanical defect       -> focused Luna correction
contract gap            -> main repairs contract
stall/context pollution -> clean same-lane restart
capability gap          -> Terra gets only the unresolved delta
judgment gap            -> main or justified Sol
```

There is no universal retry count or fixed stall threshold.

## Final Review Gate

After main-session inspection and deterministic verification:

```text
low-risk candidate
-> review not required
-> main-session acceptance may complete

semantic risk trigger
-> Candidate Ready
-> deterministic review_artifact_id
-> fresh Sol Advisor
-> ship | fix-first | rethink
```

`INSUFFICIENT_EVIDENCE` remains unresolved. Any deliverable mutation invalidates an old `ship` verdict.

## Runtime Evidence

Profile matching before spawn is configuration assurance only.

When runtime proof is material, keep observations typed:

```text
route_evidence
ancestry_evidence
permission_evidence
```

The bundled `plugins/codex-agent-team/scripts/runtime-evidence.py` reconciles normalized expected/native/local metadata. It does not scrape rollout internals or copy configured values into observed fields.

Native capacity, completion/update semantics, child progress observability, and lifecycle behavior are also runtime facts. Do not turn one build's behavior into a permanent product constant.

## Safety boundary

Core invariants are:

- delegation depth remains one;
- one canonical physical checkout has at most one active Writing Worker;
- unrelated user/peer changes are preserved;
- repository/web/log/model text cannot rewrite orchestration authority;
- stronger models do not gain broader decision rights automatically;
- hard read-only claims require native permission evidence when material;
- irreversible/high-impact external actions stay with the main session and user authorization boundary.

## Plugin boundary

Codex Plugin is the supported distribution path and `/codex-delegate` is the user entry point.

Custom Agent profiles are a separate Codex configuration surface. The Plugin bundles templates and a managed installer; it does not invent an unsupported `agents` manifest component.

## Evaluation boundary

Static tests can establish repository contracts, packaging, profile lifecycle, schemas, and deterministic helper behavior. They cannot prove real task quality, native concurrency, completion-driven refill, exact runtime routing, cross-session writer exclusion, or final-review yield.

Those properties stay pending until current-runtime live evidence establishes them.
