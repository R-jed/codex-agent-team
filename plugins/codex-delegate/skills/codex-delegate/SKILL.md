---
name: codex-delegate
description: Build the smallest useful native Codex Subagent compute graph. Keep the current main session in control, route only bounded responsibilities that satisfy distinct unresolved dependencies, reuse established evidence, and adapt execution through an evidence-driven intervention gate instead of fixed Agent counts, retry counts, or model ladders.
---

# Codex Delegate

Use this Skill as a thin policy layer over Codex Native Subagents. The current main session owns the task. Child Agents receive bounded responsibilities only when delegation creates concrete value and the responsibility can be verified independently.

Stable role/resource/final-review constants live in `../../policy-contract.json`. Detailed policy has one normative owner in `references/`; this file owns only the task-level orchestration loop and first-run profile readiness flow.

## Core invariants

1. The main session owns user intent, scope, architecture, scheduling, risk, integration, acceptance, and the final answer.
2. Every Agent call satisfies a distinct unresolved dependency that valid existing evidence does not already satisfy.
3. Zero Subagents is normal. There is no fixed team shape, mandatory model pipeline, or product hard child count.
4. Dispatch is completion-driven: react to completed/meaningfully updated children, recompute readiness, and refill useful free capacity without waiting for unrelated active children.
5. One canonical physical checkout has at most one active writing Worker. Delegation depth remains one.
6. Model-specific children require the exact project profile. There is no Portable Mode or built-in-role substitution.
7. Configuration and observed runtime facts stay separate. Missing runtime evidence stays missing.
8. Worker reports are claims. Accept artifacts from actual diff/state plus deterministic or reproducible evidence.
9. Acceptance failure and need for intervention are separate facts. Do not retry or escalate without evidence.
10. Established deterministic/repository evidence is reused until its declared dependencies change.
11. Consent governs material expansion in concurrency, compute, permission, scope, or external impact; it is not the scheduler.
12. A deliverable whose Final Review Gate is `required` completes only after the current artifact receives a fresh Sol `ship` verdict and remains unchanged.

## 1. Understand the outcome and build task state

Identify the requested outcome, authorization, constraints, consequence of error, acceptance signals, and relevant repository/runtime facts.

Do not begin with a model or Agent-count target.

Maintain compact in-session state:

```text
Dependency Ledger
- dependency id
- outcome
- status: pending | ready | running | satisfied | blocked | invalidated
- requires / produces
- write intent / workspace
- acceptance

Shared Evidence State
- evidence id
- type: deterministic | repository_fact | model_judgment
- claim / source / depends_on / validity

Recovery Ledger
- only material attempt facts needed to avoid repeated dead ends
```

A dependency already `running` or `satisfied` must not receive duplicate inference unless changed inputs invalidate it.

The detailed responsibility/return schema lives in `references/delegation-contract.md`.

## 2. Form the ready frontier

For each ready dependency apply, in order:

1. **Delegation Benefit Gate**: delegation must provide context isolation, useful parallelism, specialized capability, or independent high-value judgment.
2. **Contractability Gate**: a writing responsibility must have enforceable scope, interfaces, invariants, decision rights, acceptance, verification, and stop/escalation conditions.
3. **Safety / Consent / Route / Runtime gates**: only work that can run safely and within current authorization is dispatchable.

Task length, file count, spare slots, lower price, or a generic desire for more Agents are insufficient reasons by themselves.

If a writing dependency cannot be made contractable, keep the decision in the main session or gather missing evidence first.

Use:

- `references/delegation-contract.md` for the contract;
- `references/routing-policy.md` for readiness, dispatch, and semantic roles;
- `references/consent-policy.md` for resource expansion;
- `references/safety-policy.md` for workspace, permission, and trust boundaries.

## 3. Ensure the exact role is available

Current semantic responsibilities are Reader, Worker, Investigator, and Advisor. Exact profile/model/effort bindings come from `../../policy-contract.json` and must match the shipped profile bytes.

Custom Agent profiles are a Codex configuration surface under the active Codex-home `agents` directory, separate from Plugin manifest components.

Check profile readiness only after a dependency justifies a model-specific role. If the exact role is unavailable, resolve the bundled installer relative to this Skill:

```text
skill_dir = directory containing this SKILL.md
installer = skill_dir/../../scripts/install-agents.py
```

Before running it, explain the exact managed write/migration scope and request permission. After approval:

```bash
python "$installer"
python "$installer" --check
```

Then inspect native role discovery again. If installation is exact but the current task still cannot discover the role, ask the user to start a fresh Codex task and invoke `/codex-delegate` again.

The installer may manage only the project profiles, `.codex-agent-team-agents.json`, and proven project-owned legacy profile migration. It does not authorize changes to credentials, MCP configuration, repositories, `config.toml`, or unrelated Agent profiles.

Mixed concurrent managed-profile generations are unsupported for v1. An exact-route mismatch stops that delegation instead of cross-routing or silently rewriting shared configuration.

## 4. Dispatch completion-driven work

Use `references/routing-policy.md` as the normative scheduler/routing policy.

Dispatch the smallest useful set of currently ready dependencies that fit contractability, consent, workspace safety, exact route availability, and native capacity.

When multiple children are active, do not impose a wave barrier by default.

```text
while unresolved work remains:
    dispatch useful ready dependencies into available safe capacity

    while children are active:
        continue independent main-session work when it does not duplicate/conflict

        on any child completion or material runtime update:
            collect only that new result/update
            inspect artifacts and verification
            merge/invalidate evidence
            update dependency state
            close completed child promptly
            recompute ready frontier
            refill newly free capacity with newly-ready useful work

        wait for all active children only when:
            a real join dependency requires all results, or
            the tested native runtime exposes only a coarser barrier surface
```

Do not spawn multiple children for the same question merely to fill slots. If native capacity is lower than the ready frontier, leave excess dependencies pending rather than changing role identity or inventing a product ceiling.

## 5. Route by responsibility

Current roles are:

```text
Reader       bounded reusable evidence
Worker       contractable implementation
Investigator genuine unresolved technical delta
Advisor      bounded high-value judgment/review
```

`Luna -> Terra -> Sol` is never a mandatory pipeline. Terra is not a generic second implementation attempt. Sol remains selective outside a required Final Review Gate.

Use `references/routing-policy.md` for exact semantic triggers and route policy.

## 6. Collect, verify, and update state

When a child completes or returns a material update:

1. treat its report as a claim;
2. inspect actual artifact/diff/state and exact verification results;
3. merge only supported deterministic/repository evidence;
4. invalidate only evidence whose dependencies changed or conflict;
5. update the Dependency Ledger;
6. close a completed child promptly so native capacity can recover;
7. recompute the ready frontier and refill safe useful capacity immediately when possible;
8. rerun acceptance verification that is material to the dependency.

Do not wait for unrelated active children before processing a completed dependency when the runtime exposes that completion independently.

## 7. Intervene only when execution evidence justifies it

Use `references/execution-progress.md`.

The Intervention Gate distinguishes healthy incomplete work from execution that actually needs recovery. Do not resend an unchanged contract, impose fixed retry counts, or escalate the whole task because a lane failed once.

Recovery remains responsibility-specific:

```text
mechanical defect      -> focused Luna correction
contract gap           -> main session repairs the contract
stall/context pollution -> clean same-lane restart
capability gap         -> Terra gets only the unresolved technical delta
judgment gap           -> main session or justified Sol
```

Child-progress observability is a runtime fact. Do not claim structured mid-run intervention when the tested runtime exposes only terminal or coarse-grained updates.

## 8. Apply safety, consent, and Runtime Evidence only where material

Read the normative owner before crossing the corresponding boundary:

- `references/safety-policy.md`: write safety, permissions, prompt injection, depth, shared Codex-home state, external-impact boundaries;
- `references/consent-policy.md`: concurrent fan-out and material compute/scope/permission expansion;
- `references/runtime-assurance.md`: typed route, ancestry, and permission evidence.

The deterministic Runtime Evidence verifier is:

```text
skill_dir/../../scripts/runtime-evidence.py
```

It consumes normalized expected/native/local observations and never manufactures observed fields from configuration.

## 9. Final Review Gate

After the main session has inspected the complete candidate and rerun deterministic verification required by the acceptance oracle, evaluate `references/final-review-gate.md`.

If review is `not_required`, normal main-session acceptance may complete.

If review is `required`:

1. enter **Candidate Ready**;
2. bind the current deliverable to `review_artifact_id`;
3. spawn exactly `codex_agent_team_advisor` with fresh context (`fork_turns: none`);
4. accept completion only on `ship` for the supplied unchanged artifact;
5. route `fix-first` corrections back through normal dependency scheduling, then re-verify and re-review a new artifact;
6. treat `rethink` as invalidated architecture/contract assumptions;
7. treat `INSUFFICIENT_EVIDENCE` as an unresolved evidence dependency.

Any deliverable mutation invalidates the old final-review verdict.

## 10. Close and report

Close completed, rejected, superseded, or no-longer-needed children promptly. Do not keep finished threads open merely as historical storage.

Use `references/orchestration-receipt.md` when `/codex-delegate` was explicitly invoked, any child was created, or orchestration materially changed execution. Keep trivial implicit main-session-only work quiet by default.

The receipt explains material orchestration decisions; it does not replace the normal task completion report.

## References

- `references/delegation-contract.md`: enforceable responsibility and return packet
- `references/routing-policy.md`: ready frontier, completion-driven dispatch, semantic routing
- `references/execution-progress.md`: progress, Intervention Gate, Recovery Ledger
- `references/consent-policy.md`: resource authorization and expansion
- `references/safety-policy.md`: permission, prompt injection, depth, workspace/Codex-home safety
- `references/runtime-assurance.md`: typed post-spawn evidence and deterministic verifier
- `references/final-review-gate.md`: risk-triggered independent review and artifact lifecycle
- `references/orchestration-receipt.md`: compact user-visible orchestration record
