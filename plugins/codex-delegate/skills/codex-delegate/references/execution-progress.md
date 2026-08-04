# Execution Progress Policy

This file owns only execution evidence, progress semantics, stall detection, and the facts required for reclassification. `routing-policy.md` owns the effective next actor.

## 1. Evidence before narration

Prefer facts another actor can inspect:

- deterministic verification output;
- compiler, type-checker, test, build, formatter, or static-analysis results;
- repository facts tied to files, symbols, interfaces, or diffs;
- actual changed artifact state;
- runtime facts when exposed;
- acceptance-oracle checks;
- evidence that narrows the unresolved dependency.

A child summary is a claim until the main session can inspect the underlying artifact or evidence.

These do not establish progress by themselves:

- confidence language;
- more reasoning or explanation;
- a file write;
- an irrelevant successful command;
- a different patch with the same failing acceptance result;
- repeated discovery already present in valid evidence;
- another model agreeing.

## 2. Compact progress record

For each material attempt keep:

```text
DEPENDENCY ID
ATTEMPT ID
CURRENT KIND
CURRENT ARTIFACT
ACCEPTANCE STATE
FAILURE SIGNATURE
NEW / INVALIDATED EVIDENCE
UNRESOLVED DELTA
PROGRESS SIGNAL: advanced | unchanged | regressed | blocked
```

`advanced` requires material movement toward satisfaction, such as a smaller unresolved delta, improved acceptance state, or genuinely new evidence that removes uncertainty.

Do not use private chain-of-thought as task state.

## 3. Intervention question

Before changing context or actor, ask:

```text
Is this dependency still making evidence-supported forward progress
inside a valid classification, contract, and safe runtime boundary?
```

If yes, continue. A still-failing test can coexist with healthy progress.

If no, stop ordinary continuation and re-evaluate the dependency with the current evidence.

Do not intervene because an attempt is merely incomplete, a child sounds uncertain, a stronger model exists, or one test failed once.

## 4. Reclassification signals

The child may return:

```text
CONTRACT_GAP
JUDGMENT_REQUIRED
TECHNICAL_GAP
EXECUTION_STALL
```

The main session validates the evidence behind the signal and reruns the dependency classifier in `routing-policy.md`.

Typical interpretations:

- `CONTRACT_GAP`: repair task truth, scope, invariants, decision envelope, acceptance, or verification in the main session.
- `JUDGMENT_REQUIRED`: determine whether the same dependency is now `judgment` or `judgment_coupled_execution`.
- `TECHNICAL_GAP`: classify as `technical_investigation` only when semantic intent is already stable and the remaining delta is narrow and technically difficult.
- `EXECUTION_STALL`: confirm whether the classification is still correct before considering a clean same-role restart.

A child's proposed classification is not orchestration authority.

## 5. Stall evidence

Stall means another materially unchanged attempt is unlikely to add value. Signals include:

- the same factual failure signature persists without new evidence;
- write/verify/fail cycles repeat without improving acceptance;
- implementation directions oscillate while verification does not improve;
- the same repository discovery or deterministic command is repeated without invalidation;
- the unresolved delta does not shrink;
- scope churn grows while the dependency remains unchanged.

These are qualitative evidence signals, not numerical thresholds. Codex Delegate has no universal retry count.

## 6. Clean same-role restart

A clean restart is justified only when:

1. the dependency classification remains valid;
2. the assigned role still appears capable;
3. evidence indicates context pollution or repetition rather than a semantic/technical reclassification;
4. the new packet differs materially from the failed attempt by carrying corrected evidence, a correction hypothesis, or a cleaner current state.

Preserve:

```text
DEPENDENCY KIND
CURRENT ARTIFACT
VALID ESTABLISHED EVIDENCE
FAILURE SIGNATURE
UNRESOLVED DELTA
MATERIAL RECOVERY HISTORY
DO NOT REDO
ACCEPTANCE ORACLE
VERIFICATION
```

Drop dead-end narration and private reasoning. A clean restart is still the same dependency and does not authorize a second concurrent owner.

## 7. Recovery Ledger

Keep only material attempt facts needed to prevent semantic cycles:

```text
ATTEMPT ID
ROLE
DEPENDENCY KIND
CORRECTION HYPOTHESIS
FAILURE SIGNATURE
PROGRESS SIGNAL
NEW EVIDENCE IDS
UNRESOLVED DELTA
EFFECTIVE ACTION
DECISION SOURCE
```

Use it to detect a return to an earlier failed hypothesis when the relevant evidence has not changed.

## 8. Decision provenance

When a child proposes a next action, separate proposal from the main session's effective action:

```text
PROPOSED ACTION
EFFECTIVE ACTION
DECISION SOURCE
```

`DECISION SOURCE` may be:

```text
deterministic_evidence
main_session_judgment
user_decision
runtime_constraint
model_judgment
```

Model judgment never becomes deterministic evidence by agreement or repetition.

## 9. Event-driven evaluation

Re-evaluate progress on material events:

- a child returns or exposes a material update;
- acceptance verification changes;
- the failure signature changes;
- evidence is established, contradicted, or invalidated;
- a dependency becomes blocked or ready;
- workspace/runtime state materially changes;
- the user changes outcome, scope, or authorization.

Do not spend model turns busy-polling for progress the native runtime does not expose.

## 10. Acceptance

The main session marks a dependency satisfied only when its declared acceptance oracle is met or the user explicitly changes that oracle.

Repeated failure is evidence for reclassification or recovery. It is never permission to weaken success criteria.
