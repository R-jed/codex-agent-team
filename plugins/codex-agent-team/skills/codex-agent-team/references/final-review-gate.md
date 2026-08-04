# Final Review Gate

The Final Review Gate separates a candidate that the main session has verified from a deliverable that may be reported complete when the change carries material residual risk.

It preserves Codex Delegate's adaptive model: Sol is not a globally mandatory stage. A fresh Sol review becomes mandatory only when a semantic trigger makes independent judgment part of the acceptance path.

## 1. Gate state

Track a compact task-level state for deliverable mutations:

```text
review_requirement: not_required | required
review_reasons: <semantic reason codes>
review_artifact_id: <bound candidate identity or none>
review_verdict: none | ship | fix-first | rethink
```

The main session owns this state. A child may surface facts that trigger review, but it cannot waive or satisfy the gate itself.

Do not use a numeric risk score, retry count, diff-line threshold, file-count threshold, or model confidence threshold to decide whether review is required.

When `review_requirement = required`, main-session verification creates only a **Candidate Ready** state. Task completion additionally requires a fresh Sol `ship` verdict bound to the unchanged candidate artifact.

## 2. Mandatory semantic triggers

Set `review_requirement = required` when a deliverable mutation materially involves any of these conditions:

```text
user_requested
public_contract_change
persistent_state_change
security_boundary
authorization_boundary
data_integrity
concurrency_semantics
migration
wide_blast_radius
terra_escalation
material_recovery
verification_gap
```

Interpret them semantically:

- `user_requested`: the user explicitly asks for independent, final, strict, or Sol review.
- `public_contract_change`: public API, protocol, schema consumed externally, compatibility promise, or other externally relied-on contract changes.
- `persistent_state_change`: stored state semantics, durable format, database behavior, or irreversible state transition changes.
- `security_boundary`: trust boundary, authentication, secrets, injection resistance, privilege, cryptographic use, or other security-sensitive behavior changes.
- `authorization_boundary`: permission checks, role/capability enforcement, account access, or privilege delegation changes.
- `data_integrity`: correctness of durable or high-value data depends on the change.
- `concurrency_semantics`: locking, ordering, atomicity, races, retries with concurrent effects, distributed coordination, or shared-state consistency changes.
- `migration`: forward migration, rollback, compatibility transition, backfill, or staged rollout behavior changes.
- `wide_blast_radius`: a broad refactor or cross-module change can create material regressions outside one locally verifiable boundary.
- `terra_escalation`: a Terra Investigator was required to resolve a capability gap that materially shaped the delivered implementation.
- `material_recovery`: recovery changed architecture, invariants, acceptance, or the core correction strategy after implementation began.
- `verification_gap`: deterministic verification cannot cover a material residual risk that independent judgment can usefully challenge.

A trigger is about consequence and dependency structure, not task size. A small authorization edit may require review while a large mechanical generated-file update may not.

Once a trigger makes review required for the current deliverable, keep it required unless a later user scope change or deterministic/repository evidence proves that the triggering condition is no longer present in the candidate. Record that invalidation explicitly; do not silently downgrade the gate to save compute.

## 3. Candidate Ready

Before final review, the main session must establish Candidate Ready:

```text
implementation complete enough for acceptance
actual complete diff inspected
scope and invariants checked
acceptance oracle evaluated
deterministic verification rerun as required
material residual risks recorded
review reasons finalized
candidate artifact identity captured
```

A Worker report or previous model judgment cannot create Candidate Ready by itself.

If deterministic verification is still failing in a way that blocks the acceptance oracle, do not use Sol review as a substitute for unfinished execution.

## 4. Artifact binding

A final-review verdict is valid only for the exact candidate Sol reviewed.

For a Git workspace, use the bundled read-only helper as the canonical v0.6 candidate identity mechanism. Resolve it relative to this Skill:

```bash
skill_dir=<directory-containing-this-SKILL.md>
artifact_helper="$skill_dir/../../scripts/review-artifact.py"
python "$artifact_helper" --repo <workspace>
```

The helper emits JSON containing:

```text
schema_version
head
tracked_diff_sha256
untracked[]
review_artifact_id
```

The identity binds current `HEAD`, the complete tracked working-tree diff against `HEAD`, and every non-ignored untracked file with its path, kind, and content digest. It is read-only and does not update the index, create a commit, or mutate the workspace.

Pass the emitted `review_artifact_id` to the reviewer. Immediately before reporting a reviewed deliverable complete, run:

```bash
python "$artifact_helper" --repo <workspace> --verify '<review_artifact_id>'
```

A mismatch exits nonzero and invalidates the prior verdict.

Ignored build/cache artifacts are deliberately excluded from the standard source-deliverable identity. If an ignored/generated artifact is itself part of the requested deliverable, bind it with an additional deterministic digest and include that identity in the review packet. If the complete deliverable cannot be bound reliably, stop rather than claim that the mandatory gate succeeded.

For a non-Git workspace, use an equivalent deterministic identity that can detect every deliverable mutation. A label, branch name, timestamp, model statement, or list of filenames alone is not an artifact identity.

Any deliverable mutation after a `ship` verdict invalidates that verdict. Re-run required deterministic verification, capture a new artifact identity, and obtain a new fresh review.

## 5. Fresh Sol review

Use the existing exact Advisor route:

```text
agent_type: codex_agent_team_advisor
fork_turns: none
```

The managed profile pins GPT-5.6 Sol `high` with read-only sandbox intent. Apply the normal route-assurance and Runtime Evidence Gate rules when route or enforced isolation is material to the acceptance claim.

Fresh review means no inherited conversational turns. Give Sol compressed established facts and the actual candidate. Do not include dead-end narration or tell the reviewer that the main session already believes the change is correct.

Use this packet:

```text
FINAL REVIEW

TASK
<the user's observable outcome>

REVIEW REASONS
<the semantic trigger codes and short material explanation>

ACCEPTANCE ORACLE
<observable conditions already evaluated by the main session>

INVARIANTS
<public behavior, compatibility, persistence, safety, or other constraints>

CANDIDATE ARTIFACT
review_artifact_id: <exact identity>
base: <revision or starting identity>
head: <revision when applicable>
changed scope: <actual changed files/modules>

ESTABLISHED EVIDENCE
<compressed valid deterministic and repository facts; model judgments stay labeled as judgments>

PRIMARY VERIFICATION
<exact commands/checks and actual outcomes>

KNOWN RESIDUAL RISKS
<material risks that remain after deterministic verification>

REVIEW
Inspect the actual repository state and complete accumulated diff for this candidate.
Challenge correctness, completeness, regression risk, scope discipline, interface preservation,
test adequacy, and the stated review reasons. Do not implement fixes. Remain read-only.

RETURN EXACTLY
VERDICT: ship | fix-first | rethink
REVIEWED_ARTIFACT_ID: <the supplied candidate identity>
DECISIVE_EVIDENCE: <facts that determine the verdict>
FINDINGS: <precise required fixes or none>
RESIDUAL_RISK: <largest remaining material risk or none>
```

Established discovery may be reused to control cost. The reviewer may challenge stale or insufficient evidence, but it should not repeat repository discovery merely to recreate still-valid facts. Inspection of the actual final artifact is never replaced by evidence reuse.

## 6. Verdict lifecycle

### `ship`

`ship` satisfies the independent review dependency only when:

- the returned `REVIEWED_ARTIFACT_ID` equals the current candidate identity;
- required route/isolation claims are supported by the runtime evidence actually available;
- the post-review artifact verification still matches;
- the main session still finds the acceptance oracle satisfied.

Only then may a required-review task transition from Candidate Ready to complete.

### `fix-first`

A `fix-first` verdict creates one or more unresolved correction dependencies. Convert precise findings into bounded Dependency Ledger items, route implementation normally, rerun affected verification, capture a new artifact identity, and launch a new fresh Sol review.

The old verdict is invalid after any fix. The main session must not repair the code and report completion without re-review, and a Worker correction does not inherit the old review.

### `rethink`

`rethink` means the current architecture, contract, invariant set, or acceptance framing is materially unsound. Invalidate the affected Dependency Ledger and Shared Evidence entries, return the decision to the main session, and rebuild only the affected plan from valid evidence.

Do not downgrade `rethink` into a local bug-fix ticket merely to preserve the existing implementation.

## 7. Relationship to recovery

The Final Review Gate runs after implementation recovery has produced a Candidate Ready artifact. It is not another retry mechanism.

Recovery history may itself trigger mandatory review when it materially changed the solution. Pass only compact decision-relevant facts into the review packet. Do not pass private reasoning or a transcript.

If review finds a bounded defect, `fix-first` returns work to normal dependency scheduling. If it exposes an invalid premise, `rethink` returns control to architecture/contract work.

## 8. Completion invariant

For a deliverable with `review_requirement = required`:

```text
main-session acceptance
+ deterministic verification required by the acceptance oracle
+ fresh Sol ship verdict
+ reviewed artifact unchanged
= task completion
```

Without all four, report the task as incomplete or blocked. Do not describe a selective Sol consultation, an earlier review of a different artifact, or the main session's own judgment as satisfying the mandatory final quality gate.
