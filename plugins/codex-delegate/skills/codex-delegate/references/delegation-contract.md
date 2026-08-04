# Delegation Contract

A child receives one classified unresolved dependency, not the user's raw task. This file owns the responsibility packet and return shape. Actor selection belongs to `routing-policy.md`.

## 1. Classification contract

Every delegated dependency must declare exactly one kind:

```text
evidence
bounded_execution
judgment
judgment_coupled_execution
technical_investigation
```

The role must match the kind:

```text
evidence                    -> Luna Reader
bounded_execution           -> Luna Worker
judgment                    -> Sol Advisor
judgment_coupled_execution  -> Sol Solver
technical_investigation     -> Terra Investigator
```

If the dependency changes kind during execution, the child stops and reports the smallest reclassification signal. It does not widen itself into another role.

## 2. Writing contractability

A writing child is allowed only when these fields are enforceable:

```text
OUTCOME
SCOPE
INTERFACES / DEPENDENCIES
INVARIANTS
DECISION ENVELOPE
ACCEPTANCE ORACLE
VERIFICATION
STOP CONDITIONS
```

For Luna Worker, the decision envelope must keep material product, architecture, compatibility, security, permission, and cross-module semantic choices outside the responsibility. If those choices are expected to be inseparable from implementation, the dependency is `judgment_coupled_execution`, not bounded Luna work.

For Sol Solver, the decision envelope may intentionally include material implementation-coupled semantic choices, but user intent, permission, external impact, and scope expansion remain with the main session.

## 3. Common packet

```text
TASK ID
<unique within the main task>

DEPENDENCY
ID: <dependency id>
Kind: evidence | bounded_execution | judgment | judgment_coupled_execution | technical_investigation
Requires:
- <satisfied dependency/evidence ids>
Produces:
- <observable artifact, evidence, or decision>

OUTCOME
<one observable result and why it matters>

SCOPE
Workspace: <working directory or none>
Workspace identity: <canonical checkout or isolated workspace>
Read scope:
- <smallest useful scope>
Write scope:
- <exact bounded scope or none>
Forbidden scope:
- <paths/responsibilities not granted>

INTERFACES / DEPENDENCIES
- <contracts, callers, schemas, state, or established facts that constrain the work>

INVARIANTS
- <behavior, compatibility, data, security, or state facts that must remain true>

DECISION ENVELOPE
May decide:
- <choices intentionally delegated>
Must return before deciding:
- <choices retained by main session or another dependency>

ACCEPTANCE ORACLE
- <observable conditions that satisfy this dependency>

VERIFICATION
- Run/inspect: <exact command, artifact, or behavior>
  Success: <concrete expected evidence>

ESTABLISHED EVIDENCE
- <id>: <fact> | type: deterministic | repository_fact | model_judgment | depends_on: <inputs>

CURRENT EXECUTION EVIDENCE
Attempt id: <id>
Failure signature: <factual failure or none>
Progress signal: advanced | unchanged | regressed | blocked | none
Do not redo:
- <still-valid evidence/discovery>

MATERIAL RECOVERY HISTORY
- <only decision-relevant prior attempts, or none>

STOP CONDITIONS
- contract/task truth is materially incomplete;
- a required decision lies outside the decision envelope;
- the dependency's kind changed;
- workspace drift invalidates the packet;
- materially similar work repeats without new evidence or acceptance progress.
```

Writing children additionally must preserve unrelated existing edits, re-read affected state before mutation when concurrent drift is plausible, and never use file-level ownership promises to bypass the one-writer-per-checkout rule.

## 4. Standard stop reasons

Use only these routing-relevant reasons:

```text
CONTRACT_GAP
JUDGMENT_REQUIRED
TECHNICAL_GAP
EXECUTION_STALL
```

Meaning:

- `CONTRACT_GAP`: outcome, scope, invariant, decision envelope, acceptance, or task truth is too incomplete to continue safely.
- `JUDGMENT_REQUIRED`: material semantic judgment is required outside the current role or granted decision envelope.
- `TECHNICAL_GAP`: semantic intent is sufficiently resolved, but a narrow difficult technical uncertainty remains.
- `EXECUTION_STALL`: materially similar work is repeating without new evidence or acceptance progress while the current classification may still be valid.

These are signals to the main session. They are not automatic model transitions.

## 5. Return packet

```text
RETURN
status: complete | partial | blocked
reason: none | CONTRACT_GAP | JUDGMENT_REQUIRED | TECHNICAL_GAP | EXECUTION_STALL
summary: <compact result>
files_changed: <actual files or none>
verification: <exact commands/checks and actual outcomes>
failure_signature: <current factual failure or none>
progress_signal: advanced | unchanged | regressed | blocked
new_evidence: <new supported facts with dependencies>
invalidated_evidence: <prior evidence no longer reusable, or none>
unresolved_delta: <smallest remaining dependency, or none>
judgment_calls: <material choices made inside granted rights, or none>
remaining_uncertainty: <material uncertainty, or none>
policy_violations: <violations observed, or none>
```

A file write, confidence statement, longer explanation, or successful irrelevant command is not evidence of progress.

## 6. Role-specific boundaries

### Luna Reader

Collect bounded reusable evidence. Do not redesign, implement, or convert ambiguous semantics into facts. Return `JUDGMENT_REQUIRED` when evidence gathering reaches a material decision boundary.

### Luna Worker

Execute only `bounded_execution`. Local implementation choices are allowed inside the contract. If material architecture, behavior, compatibility, or non-local semantic judgment emerges, stop with `JUDGMENT_REQUIRED` rather than guessing.

### Sol Solver

Execute `judgment_coupled_execution`. It may make the material implementation-coupled choices explicitly granted by the decision envelope and must report them. It remains bounded by user intent, scope, permission, external-impact, and safety policy. A narrow hard technical uncertainty can return `TECHNICAL_GAP` rather than turning Solver into an unbounded investigator.

### Terra Investigator

Resolve only a `technical_investigation` delta after semantic intent is stable. Reuse established evidence and challenge the premise that specialist investigation is actually required. Do not implement the whole task or make product/architecture decisions.

### Sol Advisor

Resolve one `judgment` dependency from compressed established facts and actual options/artifacts. It is read-only. For mandatory fresh final review, use the separate artifact-bound packet in `final-review-gate.md`.

## 7. Reuse and fresh context

Pass the smallest sufficient evidence set. Deterministic and repository facts remain reusable until their dependencies change. Model judgments remain labeled as judgment.

A clean same-role restart, when `execution-progress.md` justifies one, carries current task truth, artifact, valid evidence, failure signature, unresolved delta, acceptance oracle, verification, and `DO NOT REDO` facts. It drops dead-end narration and private reasoning.

The main session authorizes every effective next action after a child returns.
