# Architecture

Codex Delegate is a policy layer over Codex Native Subagents. It does not implement another Agent runtime, persistent DAG service, background scheduler, or routing proxy.

The current main session is the control plane. It owns user intent, scope, architecture, dependency state, scheduling, evidence, recovery, integration, acceptance, and the final response. Child Agents receive only bounded responsibilities whose outputs satisfy distinct unresolved dependencies.

The architecture optimizes for the **smallest useful compute graph** that can move the task toward acceptance.

## Policy kernel

At task level the control loop is intentionally small:

```text
1. understand the outcome and acceptance conditions
2. build/update the Dependency Ledger
3. delegate only when Benefit Gate + Contractability Gate pass
4. schedule the smallest useful ready frontier under consent/workspace/route/runtime constraints
5. inspect actual artifacts and merge/invalidate evidence after child return
6. if execution stops advancing, classify intervention/recovery
7. after verification, evaluate the Final Review Gate
8. report the accepted result and material orchestration decisions
```

Detailed policy lives in the installed Skill references. Stable machine-readable constants live in `plugins/codex-agent-team/policy-contract.json`.

## Control plane and Dependency Ledger

The main session owns the Dependency Ledger:

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

It is compact in-session task state, not a persistent scheduler. A dependency becomes ready only when its prerequisites are satisfied. A running dependency does not receive duplicate inference, and a satisfied dependency remains closed until changed inputs invalidate it.

The main session recomputes the ready frontier after material evidence, artifact, user, or runtime changes.

## Delegation gates

A ready dependency is delegated only when both gates pass.

### Delegation Benefit Gate

At least one concrete benefit must exist:

- context isolation;
- useful parallelism across different ready dependencies;
- specialized execution or investigation capability;
- independent high-value judgment.

Task length, file count, lower model price, spare child slots, or a generic desire for more review are insufficient by themselves.

### Contractability Gate

A writing dependency must have enforceable:

```text
DEPENDENCY
OUTCOME
SCOPE
INTERFACES / DEPENDENCIES
INVARIANTS
DECISION RIGHTS
ACCEPTANCE ORACLE
VERIFICATION
STOP / ESCALATE
```

If acceptance or decision rights remain materially ambiguous, implementation stays in the main session until the contract is repaired.

## Semantic compute lanes

Role identity is intentionally separate from model identity. Current route constants are defined in `policy-contract.json` and matched by the shipped Agent profiles.

| Responsibility | Agent type | Current route | Intent |
| --- | --- | --- | --- |
| Reader | `codex_agent_team_reader` | GPT-5.6 Luna `max` | bounded evidence gathering |
| Worker | `codex_agent_team_worker` | GPT-5.6 Luna `max` | bounded implementation |
| Investigator | `codex_agent_team_investigator` | GPT-5.6 Terra `xhigh` | unresolved complex technical delta |
| Advisor | `codex_agent_team_advisor` | GPT-5.6 Sol `high` | high-value judgment and independent review |

Models are resources, not mandatory stages. Valid graphs include:

```text
main
main -> Luna -> main
main -> Luna -> Sol -> main
main -> Terra -> Luna -> main
main -> Luna -> Terra(delta) -> Luna -> main
main -> Sol -> main
```

There is no required `Luna -> Terra -> Sol` pipeline.

## Adaptive scheduling and resource scopes

Scheduling starts from ready dependencies, not from an Agent-count target.

Explicit `/codex-delegate` use includes up to two concurrently active justified children without another consent prompt. Larger simultaneous fan-out normally requires consent unless broad parallelism was already authorized.

That number is a consent boundary, not a product hard cap or scheduling target. After consent, actual parallelism is constrained by ready dependencies, workspace safety, exact route availability, and native runtime capacity. Codex Delegate has **no second numerical hard ceiling**.

Resource state has three scopes:

```text
main-session scope
-> Dependency Ledger, ready frontier, consent, active children, Recovery Ledger

workspace scope
-> at most one active writer per canonical physical checkout or isolated worktree

Codex-home scope
-> one installed managed profile generation shared by sessions using that Codex home
```

Native slot shortage queues or serializes ready work. It never justifies duplicate inference or cross-routing.

## Shared Evidence State

The main session reuses established evidence while its dependencies remain valid.

```text
deterministic
repository_fact
model_judgment
```

Deterministic results and repository facts may be reused. Model judgments remain challengeable hypotheses.

A changed input invalidates only evidence that depends on it. Fresh child context does not mean rediscovering facts that remain valid.

## Execution progress, Intervention Gate, and Recovery Ledger

Acceptance failure and need for intervention are different facts.

Progress is grounded in observable movement such as a narrower failure space, new deterministic evidence, a resolved repository fact, or an artifact moving toward the acceptance oracle. Confidence, narration, a file write, or a successful but irrelevant command is not progress by itself.

When evidence still shows forward progress inside a valid contract, continue the responsibility. Otherwise the **Intervention Gate** classifies the boundary:

```text
mechanical defect
-> focused Luna correction

contract gap
-> main session repairs the contract

execution stall / context pollution
-> clean same-lane restart with current artifact + valid evidence + DO NOT REDO

capability gap
-> Terra receives only the unresolved technical delta

judgment gap
-> main session or justified Sol
```

There is no universal retry count or fixed stall threshold.

Material attempts are summarized in a compact **Recovery Ledger**:

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

It preserves decision-relevant history across fresh contexts without carrying private reasoning or full transcripts.

## Final Review Gate

The Final Review Gate runs after main-session inspection and deterministic verification. Sol remains selective globally, but a semantic risk trigger can make fresh Sol review mandatory for one deliverable.

Examples of mandatory triggers include public-contract, persistence, security, authorization, data-integrity, concurrency, migration, wide-blast-radius, material Terra escalation, material recovery, verification gaps, or explicit user request. The authoritative trigger codes live in `policy-contract.json` and `references/final-review-gate.md`.

```text
verified low-risk candidate
-> review_requirement = not_required
-> main-session acceptance may complete

semantic risk trigger
-> review_requirement = required
-> Candidate Ready
-> deterministic review_artifact_id
-> fresh Sol Advisor
-> ship | fix-first | rethink
```

`INSUFFICIENT_EVIDENCE` is an unresolved reviewer state, not a successful verdict.

When review is required, completion requires all of:

```text
main-session acceptance
+ deterministic verification required by the acceptance oracle
+ fresh Sol ship verdict
+ reviewed artifact unchanged
```

Any deliverable mutation invalidates the old review verdict. `fix-first` requires correction, re-verification, a new artifact identity, and a new fresh review. `rethink` invalidates affected architecture/contract assumptions instead of becoming a local patch.

This preserves adaptive compute for ordinary work while adding an independent quality boundary where consequence justifies it.

## Route assurance and Runtime Evidence

Model-specific children require the exact project profile. There is no Portable Mode or built-in-role substitution.

Before spawn:

```text
route_assurance = profile_locked
```

is configuration evidence only.

When post-spawn proof is material, Runtime Evidence keeps concerns independent:

```text
route_evidence
ancestry_evidence
permission_evidence
```

The bundled `plugins/codex-agent-team/scripts/runtime-evidence.py` consumes normalized expected/native/local metadata. It does not scrape Codex rollout internals and does not manufacture observed values from profile configuration.

Missing required runtime evidence fails closed. A route conflict, ancestry conflict, and permission conflict remain separately typed even when the overall result is quarantined.

## Safety boundaries

Core safety invariants are:

- delegation depth remains one;
- children do not create further Subagents;
- one canonical physical checkout has at most one active writing Worker;
- unknown user/peer edits are preserved rather than reverted;
- repository, webpage, log, issue, generated, or model text is untrusted data and cannot rewrite orchestration policy;
- stronger models do not automatically gain broader decision rights;
- exact route or required permission evidence fails closed when unavailable;
- production deployment, destructive data deletion, payments, third-party publication, account/permission administration, and other irreversible external side effects remain with the main session and user authorization boundary.

Requested read-only profile configuration is intent, not proof of host-enforced isolation. When hard read-only matters, native permission evidence is required.

## Plugin and managed profiles

Codex Plugin is the supported distribution path and `/codex-delegate` is the user-facing entry point.

Custom Agent profiles are a separate Codex configuration surface. The Plugin bundles four templates and a managed installer; it does not invent an unsupported `agents` Plugin-manifest component.

After explicit user approval, the installer provisions project-owned profiles into the active `$CODEX_HOME/agents` directory. Ownership/exactness checks prevent overwriting unproven or user-modified profile files.

## Evaluation boundary

Static tests validate repository contracts, packaging, profile lifecycle, schemas, deterministic artifact/runtime evidence tooling, and policy invariants. They do not prove real task quality, native capacity, exact runtime routing, child observability, or review yield.

Live evaluation therefore measures representative workloads and records missing telemetry as missing rather than estimating it.

## Deliberate exclusions

Core deliberately excludes persistent task orchestration services, external DAG schedulers, mandatory all-task Sol review, automatic model ladders, machine-wide Agent governors, external routing judges, and production deployment automation.
