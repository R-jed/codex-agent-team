# Final Review Gate

The Final Review Gate answers one question after the main session has a verified candidate:

```text
Does this exact deliverable require an independent second judgment before completion?
```

It is an assurance policy, not an execution stage, model-escalation rule, or reward/penalty for which roles were used earlier.

A Sol main session may cover ordinary planning and judgment. It does not satisfy a required independent review of its own integrated candidate.

## 1. Gate state

Track:

```text
review_requirement: not_required | required
review_reasons: <semantic reason codes>
review_artifact_id: <bound candidate identity or none>
review_verdict: none | ship | fix-first | rethink | insufficient_evidence
```

The main session owns this state. Children can surface evidence but cannot waive or satisfy the gate themselves.

Do not use numeric risk scores, retry counts, line counts, file counts, model confidence, or prior model identity as review triggers.

## 2. Mandatory semantic triggers

Set `review_requirement = required` when the current deliverable materially involves one or more of the current policy-contract reasons:

```text
user_requested
public_contract_change
persistent_state_change
security_boundary
authorization_boundary
data_integrity
concurrency_semantics
migration
verification_gap
```

Interpret them by consequence:

- `user_requested`: the user explicitly asks for independent/final/strict review.
- `public_contract_change`: externally relied-on API, protocol, schema, compatibility promise, or equivalent contract changes.
- `persistent_state_change`: durable state semantics or irreversible stored-format behavior changes.
- `security_boundary`: authentication, trust, secrets, injection resistance, privilege, cryptography, or another material security boundary changes.
- `authorization_boundary`: role/capability/permission enforcement or access-control behavior changes.
- `data_integrity`: correctness of durable or high-value data materially depends on the change.
- `concurrency_semantics`: locking, ordering, atomicity, races, concurrent retry effects, or shared-state consistency changes.
- `migration`: a material forward/rollback/compatibility/backfill/staged-transition behavior changes.
- `verification_gap`: deterministic verification cannot adequately cover a material residual consequence that a fresh independent judgment can usefully challenge.

A trigger is about the current artifact and its consequences, not how hard the journey was.

## 3. Process history is evidence, not a trigger

These facts do **not** make review mandatory by themselves:

```text
Terra was used
Sol Solver was used
a clean restart happened
material recovery happened
the diff is large
many files changed
Luna struggled
a stronger model was involved
```

They may reveal a `verification_gap` or another semantic trigger. If so, record the actual trigger. Do not encode process history as a proxy for risk.

Examples:

```text
Terra resolved a narrow synchronization fact and deterministic coverage fully closes the dependency
-> Terra use alone does not require review

A bounded Luna change passes tests but behavior correctness still depends on an unverified compatibility interpretation
-> verification_gap may require review
```

This keeps independent Sol review high-value and low-frequency.

## 4. Candidate Ready

Before final review, the main session establishes **Candidate Ready**:

```text
implementation complete enough for acceptance
actual complete diff/state inspected
scope and invariants checked
acceptance oracle evaluated
deterministic verification rerun as required
material residual risks recorded
review reasons finalized
candidate artifact identity captured when review is required
```

A child report or earlier model judgment cannot create Candidate Ready by itself.

If deterministic verification still fails in a way that blocks acceptance, continue normal dependency routing. Do not use Sol review as a substitute for unfinished execution.

## 5. Artifact binding

A required final-review verdict is valid only for the exact candidate reviewed.

For Git workspaces use the bundled read-only helper:

```bash
skill_dir=<directory-containing-this-SKILL.md>
artifact_helper="$skill_dir/../../scripts/review-artifact.py"
python "$artifact_helper" --repo <workspace>
```

It emits an identity including the current Git base/head state, tracked diff digest, non-ignored untracked entries, and `review_artifact_id`.

Immediately before reporting completion after a required review, verify the exact identity:

```bash
python "$artifact_helper" --repo <workspace> --verify '<review_artifact_id>'
```

A mismatch invalidates the old verdict.

If an ignored/generated artifact is itself part of the requested deliverable, bind it with additional deterministic identity. If the complete deliverable cannot be bound reliably, keep the gate unresolved.

Any deliverable mutation after `ship` requires affected deterministic verification, a new artifact identity, and a new fresh review.

## 6. Fresh independent Sol review

Use:

```text
agent_type: codex_delegate_advisor
fork_turns: none
```

The current managed profile pins GPT-5.6 Sol `high` with read-only intent.

Fresh review is required for independence even when:

- the main session itself is Sol;
- Sol Solver implemented the dependency;
- Sol Advisor previously answered a planning judgment.

Those earlier uses provide capability, not independent acceptance of the final integrated artifact.

Give the reviewer compressed valid facts and the actual candidate. Do not pass dead-end narration or tell the reviewer that another actor already believes the candidate is correct.

Use this packet:

```text
FINAL REVIEW

TASK
<observable user outcome>

REVIEW REASONS
<semantic trigger codes and material explanation>

ACCEPTANCE ORACLE
<conditions already evaluated by main>

INVARIANTS
<behavior, compatibility, persistence, safety, or other constraints>

CANDIDATE ARTIFACT
review_artifact_id: <exact identity>
base/head: <when applicable>
changed scope: <actual changed modules/files>

ESTABLISHED EVIDENCE
<compressed deterministic/repository facts; judgments remain labeled>

PRIMARY VERIFICATION
<exact checks and outcomes>

KNOWN RESIDUAL RISKS
<material risks after deterministic verification>

REVIEW
Inspect the actual repository state and complete accumulated diff.
Challenge correctness, completeness, regression risk, scope discipline,
interface preservation, test adequacy, and the stated semantic review reasons.
Remain read-only. Do not implement fixes.

RETURN ON A REVIEWABLE CANDIDATE
VERDICT: ship | fix-first | rethink
REVIEWED_ARTIFACT_ID: <supplied identity>
DECISIVE_EVIDENCE: <facts determining verdict>
FINDINGS: <required fixes or none>
RESIDUAL_RISK: <largest remaining risk or none>
```

If evidence needed for a justified conclusion is missing, the Advisor may return `INSUFFICIENT_EVIDENCE` with the exact missing dependency.

## 7. Verdict lifecycle

### `ship`

A required gate passes only when:

- `REVIEWED_ARTIFACT_ID` equals the current candidate identity;
- required route/isolation claims are supported by available runtime evidence;
- post-review artifact verification still matches;
- the main session still finds the acceptance oracle satisfied.

### `fix-first`

Convert precise findings into normal dependencies, classify them through Routing V4, apply corrections, rerun affected verification, capture a new artifact identity, and launch a new fresh review.

The old verdict is invalid after mutation.

### `rethink`

Invalidate affected architecture, contract, dependency, and evidence assumptions. Return control to the main session and rebuild only the affected task state from valid evidence.

Do not downgrade a material invalid premise into a local patch merely to preserve the current implementation.

### `INSUFFICIENT_EVIDENCE`

Keep the gate unresolved. Record the exact missing evidence dependency, gather only what is missing when possible, and launch a new fresh review. If the candidate changes, re-verify and rebind first.

`INSUFFICIENT_EVIDENCE` is not `fix-first`, `rethink`, or completion.

## 8. Consent

A required quality state does not silently authorize unlimited compute.

If the fresh Sol review is outside the current consent envelope, keep the candidate at Candidate Ready and request the smallest additional consent. If the user declines, report that independent review remains incomplete. Do not rewrite the semantic trigger to `not_required`.

Repeated correction/re-review cycles can become material compute expansion and are governed by `consent-policy.md`.

## 9. Completion invariant

For a deliverable with `review_requirement = required`:

```text
main-session acceptance
+ required deterministic verification
+ fresh independent Sol ship verdict
+ unchanged reviewed artifact
= completion
```

For `review_requirement = not_required`, normal main-session acceptance can complete without a decorative Sol pass.
