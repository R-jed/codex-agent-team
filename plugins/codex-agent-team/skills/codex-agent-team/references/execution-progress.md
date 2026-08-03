# Execution Progress Policy

Codex Delegate adapts execution from observable task progress. A model's narration about progress is not enough to justify another attempt, a stronger lane, or acceptance.

This policy separates three things:

```text
execution evidence
-> progress / stall signals
-> routing or recovery decision
```

Do not collapse them into one model judgment.

## 1. What counts as execution evidence

Prefer evidence that another actor can inspect independently:

- deterministic verification output;
- compiler, type-checker, test, build, formatter, or static-analysis results;
- repository facts tied to files, symbols, call paths, interfaces, or diffs;
- actual changed-file and artifact state;
- runtime facts when they are materially observable;
- acceptance-oracle checks;
- evidence that materially narrows an unresolved dependency.

A child may summarize this evidence, but its summary is still a claim until the main session can inspect the underlying artifact or result.

## 2. What does not count as progress by itself

Do not treat these as progress without supporting evidence:

- confidence language;
- longer reasoning or a more detailed explanation;
- a file write;
- a different patch that fails the same acceptance check in the same way;
- repeating the same command with the same outcome and no invalidation reason;
- rediscovering a repository fact already present in valid Shared Evidence State;
- another model agreeing with the previous model.

A write followed by the same failing verification can be motion without progress.

## 3. Responsibility progress record

For a delegated execution responsibility, keep only compact facts needed for the next decision:

```text
DEPENDENCY ID
ATTEMPT ID
CURRENT ARTIFACT
ACCEPTANCE STATE
FAILURE SIGNATURE
NEW EVIDENCE
INVALIDATED EVIDENCE
UNRESOLVED DELTA
PROGRESS SIGNAL
```

`FAILURE SIGNATURE` should be factual when possible, for example a failing test id, compiler error class, invariant breach, or deterministic verification outcome.

`PROGRESS SIGNAL` is one of:

```text
advanced
unchanged
regressed
blocked
```

Do not use private chain-of-thought as task state.

## 4. Deterministic stall signals

A stall is evidence that another unchanged attempt is unlikely to add value. Signals include:

- the same failure signature persists while no new evidence narrows the cause;
- write, verify, fail cycles repeat without improving the acceptance state;
- two competing artifact directions alternate while verification does not improve;
- the same repository discovery or deterministic command is repeated without an invalidation reason;
- the unresolved delta does not become smaller across materially similar attempts;
- scope churn grows while the accepted dependency remains unchanged.

These are signals, not fixed numerical thresholds. Codex Delegate does not define a universal retry count. The main session judges whether the evidence shows genuine new information or repeated motion without progress.

## 5. Recovery order

Before choosing a stronger model, classify why acceptance has not been reached.

### Mechanical defect

Use a focused Luna correction when the contract is still valid and the evidence identifies a concrete local correction path.

The next attempt must have a distinct correction hypothesis or changed evidence. Never resend an unchanged contract simply because the previous result failed.

### Contract gap

Return to the main session. Repair outcome, scope, interfaces, decision rights, acceptance, or verification before further writing.

### Execution stall or context pollution

Use a fresh same-lane packet when the lane still appears capable but accumulated context is producing unproductive repetition.

The clean restart packet carries:

```text
DEPENDENCY
CURRENT ARTIFACT
VALID ESTABLISHED EVIDENCE
CURRENT FAILURE SIGNATURE
UNRESOLVED DELTA
DO NOT REDO
ACCEPTANCE ORACLE
VERIFICATION
```

It does not carry dead-end narration, private reasoning, or a full transcript.

Use `fork_turns=none` for this fresh packet unless a specific user decision cannot be safely repacked.

### Capability gap

If the contract is clear and evidence shows the assigned execution lane cannot safely resolve the technical dependency, do not keep restarting the same lane. Send only the unresolved technical delta to Terra with valid evidence, the current artifact, and explicit `DO NOT REDO` items.

Capability takes precedence over retry when the evidence already supports that classification.

### Judgment gap

Keep the decision in the main session or use Sol when a bounded consequential judgment benefits from independent review. Do not turn a product or architecture decision into repeated implementation attempts.

## 6. Clean restart semantics

A clean restart preserves task truth and drops conversational dead ends.

Preserve:

- the user-authorized outcome;
- current artifacts and actual diff;
- still-valid deterministic and repository evidence;
- acceptance criteria;
- unresolved dependency;
- current failure signature;
- explicit constraints and `DO NOT REDO` facts.

Do not propagate:

- private reasoning;
- self-reported confidence;
- abandoned hypotheses that have no remaining evidence value;
- repeated narrative explaining failed approaches.

A clean restart is not a new dependency. It is a recovery mechanism for the same dependency, so only one execution lane should own it at a time.

## 7. Budget, consent, and safety stay outside model judgment

A child or reviewer does not decide whether it may exceed user-authorized fan-out, permissions, scope, or external impact.

Before any recovery or escalation:

1. apply current consent boundaries;
2. preserve workspace write safety;
3. verify exact role availability when a model-specific lane is required;
4. respect runtime slot availability;
5. stop when an external or permission boundary is not authorized.

Do not spend additional compute asking a model whether an already exhausted policy boundary should be ignored.

## 8. Fresh judgment at commitment boundaries

When a Sol decision or review is justified, use a fresh packet containing compressed established facts and the actual artifact or decision options. Fresh context is valuable because it reduces conversational anchoring.

Fresh context does not make the review independent evidence by itself. Sol judgment remains `model_judgment` until supported by deterministic or repository facts where applicable.

## 9. Acceptance

The main session accepts a dependency only when its declared acceptance oracle is satisfied or the user explicitly changes that oracle.

Do not weaken acceptance criteria because a lane repeatedly fails them. Repeated failure is evidence for recovery classification, not permission to redefine success.
