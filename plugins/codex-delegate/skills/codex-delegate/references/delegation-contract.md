# Delegation Contract

A Subagent receives one bounded responsibility for an unresolved dependency, not the user's raw task.

This file owns the responsibility contract and return packet. Scheduling lives in `routing-policy.md`; progress/recovery lives in `execution-progress.md`; permission/workspace rules live in `safety-policy.md`.

## Contractability Gate

A writing responsibility is contractable only when these fields are explicit enough to enforce:

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
RETURN
```

If `ACCEPTANCE ORACLE` or `DECISION RIGHTS` is materially unclear, do not create a writing Worker. Keep the decision in the main session or establish the missing evidence first.

## Execution contract

```text
TASK ID
<unique within the main task>

DEPENDENCY
ID: <dependency id from the main-session Dependency Ledger>
Requires:
- <already-satisfied dependency ids and/or evidence ids>
Produces:
- <artifact, evidence, or bounded decision this responsibility must contribute>

OUTCOME
<one observable result and why it matters>

SCOPE
Workspace: <working directory>
Workspace identity: <canonical physical checkout or isolated worktree>
Read scope:
- <smallest useful scope>
Write scope:
- <exact files, directories, or bounded modules>
Forbidden scope:
- <paths/responsibilities the Worker must not change>

INTERFACES / DEPENDENCIES
- <callers, schemas, generated state, contracts, or dependency chains that constrain the work>
- <established facts the child may rely on>

CONCURRENCY / DRIFT
- Preserve unrelated existing edits; never revert unknown changes to recover an assumed baseline.
- Re-read affected state before mutation when concurrent change is plausible.
- If workspace drift invalidates scope, an interface, invariant, acceptance, or established evidence, stop and return the changed state and smallest unresolved delta.
- File-level ownership promises do not authorize a second writing Worker in the same physical checkout.

INVARIANTS
- <public API, compatibility, state semantics, schemas, security/safety, or behavior that must remain true>

DECISION RIGHTS
Worker may decide:
- <implementation choices intentionally delegated>
Worker must return before deciding:
- <product, architecture, permission, security, migration, public-contract, or scope decisions outside delegated authority>

ACCEPTANCE ORACLE
- <observable conditions that make this dependency satisfied>

VERIFICATION
- Run: <exact command>
  Success: <concrete expected evidence>
- Inspect: <actual diff, file, generated artifact, or behavior>
  Success: <concrete expected evidence>

ESTABLISHED EVIDENCE
- <evidence id>: <fact> | depends_on: <paths/artifacts> | source: <command/file/runtime>

CURRENT EXECUTION EVIDENCE
Attempt id: <first or follow-up attempt identifier>
Prior failure signature: <deterministic failure or none>
Prior progress signal: advanced | unchanged | regressed | blocked | none
Do not redo:
- <still-valid discovery, tests, or facts that must not be repeated without invalidation>

MATERIAL RECOVERY HISTORY
- <compact decision-relevant Recovery Ledger entries for this dependency, or none>

STOP / ESCALATE
Return `CONTRACT_GAP` when the contract is internally incomplete.
Return `JUDGMENT_REQUIRED` when progress requires a decision outside delegated rights.
Return `CAPABILITY_GAP` when the contract is clear but the assigned lane cannot safely resolve the remaining difficult technical dependency.
Return `EXECUTION_STALL` when materially similar work repeats without new evidence or acceptance progress even though the lane may remain capable.
Stop when concurrent workspace drift makes this contract or its evidence stale.
Do not widen scope, weaken acceptance, redesign the task, or repeat an unchanged contract merely to avoid a stop condition.

RETURN
status: complete | partial | blocked
reason: none | CONTRACT_GAP | JUDGMENT_REQUIRED | CAPABILITY_GAP | EXECUTION_STALL
summary: <compact result>
files_changed: <actual files changed>
verification: <exact commands and actual outcomes>
failure_signature: <current deterministic failure signature or none>
progress_signal: advanced | unchanged | regressed | blocked
new_evidence: <new supported facts with dependencies>
invalidated_evidence: <prior evidence no longer safe to reuse, or none>
unresolved_delta: <smallest remaining unresolved dependency, or none>
judgment_calls: <material choices made inside granted decision rights, or none>
suggested_next_action: <optional recommendation; never orchestration authority>
uncertainty: <remaining uncertainty, or none>
policy_violations: <violations observed, or none>
```

## Evidence carried into a child

Pass the smallest sufficient evidence set. Each reusable item should identify:

```text
evidence_id
type: deterministic | repository_fact | model_judgment
claim
source
depends_on
status: valid | invalidated
```

Deterministic/repository facts may be reused while dependencies remain valid. Model judgment stays labeled as judgment. Private reasoning is not task state.

A later child may verify or challenge existing evidence when needed, but it must not restart discovery merely to recreate still-valid facts.

## Follow-up contract rules

A follow-up attempt remains the same dependency unless task truth changed enough to invalidate it.

Do not resend an unchanged contract after failure. A new attempt requires at least one material change such as:

- a concrete correction hypothesis;
- repaired contract boundaries;
- new/invalidated evidence;
- changed artifact/runtime/workspace state;
- a different responsibility justified by `execution-progress.md`.

The main session, not the child, authorizes the effective next action.

## Clean same-lane restart packet

When `execution-progress.md` justifies a clean restart, preserve task truth and omit conversational dead ends:

```text
DEPENDENCY ID
CURRENT ARTIFACT
VALID ESTABLISHED EVIDENCE
CURRENT FAILURE SIGNATURE
UNRESOLVED DELTA
MATERIAL RECOVERY HISTORY
DO NOT REDO
ACCEPTANCE ORACLE
VERIFICATION
```

Use fresh context by default. Do not carry private reasoning, abandoned unsupported hypotheses, or the full transcript.

## Terra delta packet

When evidence establishes a genuine technical capability gap, Terra receives only the unresolved delta:

```text
DEPENDENCY ID
UNRESOLVED DELTA
ESTABLISHED EVIDENCE
CURRENT ARTIFACT / FAILURE
FAILURE SIGNATURE
MATERIAL RECOVERY HISTORY
DO NOT REDO
RETURN
- resolved_delta
- new_evidence
- invalidated_evidence
- remaining_uncertainty
- suggested_next_action
```

Low quality alone is not a Terra trigger. Do not ask Terra to redo valid Luna discovery or the whole user task by default.

## Sol judgment packet

For a bounded judgment outside the mandatory final-review packet:

```text
DEPENDENCY ID
QUESTION
ESTABLISHED FACTS
CURRENT ARTIFACT / DECISION OPTIONS
COMPETING JUDGMENTS <when relevant>
WHAT CHANGES WITH THE DECISION
RETURN
- verdict or recommendation
- decisive_evidence
- missing_evidence
- largest_residual_risk
```

Use `final-review-gate.md` for the separate risk-triggered final-review lifecycle and artifact-bound packet.

## Boundary references

Before applying this contract, use the normative owner for the boundary involved:

- readiness, dispatch, semantic routing: `routing-policy.md`;
- progress, Intervention Gate, Recovery Ledger: `execution-progress.md`;
- permissions, prompt injection, workspace/Codex-home safety: `safety-policy.md`;
- compute/concurrency authorization: `consent-policy.md`;
- post-spawn route/ancestry/permission evidence: `runtime-assurance.md`;
- mandatory artifact-bound final review: `final-review-gate.md`.
