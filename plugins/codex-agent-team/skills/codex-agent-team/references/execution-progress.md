# Execution Progress Policy

Codex Delegate adapts execution from observable task progress. A model's narration about progress is not enough to justify another attempt, a stronger lane, or acceptance.

This policy separates four things:

```text
execution evidence
-> structured progress signals
-> intervention gate
-> recovery classification and effective action
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
- a successful command that does not improve acceptance, establish useful new evidence, or narrow the unresolved delta;
- a different patch that fails the same acceptance check in the same way;
- repeating the same command with the same outcome and no invalidation reason;
- rediscovering a repository fact already present in valid Shared Evidence State;
- another model agreeing with the previous model.

A write or successful tool call followed by the same failing verification can be motion without progress.

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

`advanced` means the dependency moved materially toward acceptance, for example the acceptance state improved, the unresolved delta shrank, or genuinely new evidence removed uncertainty. A command succeeding by itself does not establish `advanced`.

Do not use private chain-of-thought as task state.

## 4. Structured execution signals

When available from actual artifacts or runtime output, record compact observations such as:

```text
verification_failures
same_failure_repeat
rewrite_verify_cycles
oscillation_signal
repeated_discovery
unresolved_delta_trend
scope_churn
```

These are observations, not automatic routing rules. Codex Delegate does not encode fixed values such as "three repeats means Terra" or "four cycles means restart".

Signals are useful only when their underlying evidence is available to the main session. Do not fabricate mid-run telemetry that the current Codex runtime does not expose.

## 5. Intervention Gate

Failure to satisfy acceptance and need for intervention are different facts.

Before changing lane, restarting context, or escalating judgment, ask:

```text
Does the current responsibility still show evidence-supported forward progress
inside a valid contract and safe runtime boundary?
```

If **yes**, continue the current responsibility. A still-failing test can coexist with healthy progress when new evidence is narrowing the root cause or the unresolved delta is materially shrinking.

If **no**, or the responsibility is blocked by a contract, capability, judgment, permission, workspace, or runtime boundary, enter recovery classification.

Do not intervene merely because an attempt has not completed yet, because a child sounds uncertain, or because a stronger model is available.

## 6. Deterministic stall signals

A stall is evidence that another unchanged attempt is unlikely to add value. Signals include:

- the same failure signature persists while no new evidence narrows the cause;
- write, verify, fail cycles repeat without improving the acceptance state;
- two competing artifact directions alternate while verification does not improve;
- the same repository discovery or deterministic command is repeated without an invalidation reason;
- the unresolved delta does not become smaller across materially similar attempts;
- scope churn grows while the accepted dependency remains unchanged.

These are signals, not fixed numerical thresholds. Codex Delegate does not define a universal retry count. The main session judges whether the evidence shows genuine new information or repeated motion without progress.

## 7. Recovery classification

Only after the Intervention Gate says intervention is justified should the main session classify the reason.

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
MATERIAL RECOVERY HISTORY
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

## 8. Recovery Ledger

The main session maintains a bounded semantic history for the current dependency so a fresh context cannot accidentally revisit an earlier dead end.

Record only material attempts:

```text
ATTEMPT ID
LANE
CORRECTION HYPOTHESIS
FAILURE SIGNATURE
PROGRESS SIGNAL
NEW EVIDENCE IDS
UNRESOLVED DELTA
RECOVERY ACTION
DECISION SOURCE
```

The Recovery Ledger is not a transcript and does not contain private reasoning. Keep only entries that remain decision-relevant; compact older entries when their detailed form no longer helps detect repetition, oscillation, or invalidated hypotheses.

Use it to detect semantic cycles such as `hypothesis A -> hypothesis B -> hypothesis A` even when a clean restart removed conversational history.

A clean restart is still the same dependency. Only one execution lane owns that dependency at a time.

## 9. Proposed action, effective action, and decision provenance

A child, Investigator, or Advisor may suggest a next action. That suggestion is not orchestration authority.

When recovery materially changes execution, distinguish:

```text
PROPOSED ACTION
EFFECTIVE ACTION
DECISION SOURCE
POLICY TRANSFORM
```

`DECISION SOURCE` is one of:

```text
deterministic_evidence
main_session_judgment
user_decision
runtime_constraint
model_judgment
```

Examples:

- Terra may be proposed, but the effective action remains Luna because no capability gap is established.
- A model may propose continuing, but the effective action is stop because another writer already owns the canonical workspace.
- A clean restart may be selected from deterministic stall evidence even when the child did not request one.

Record `POLICY TRANSFORM` only when a policy or runtime boundary changes the proposed action. Do not present model judgment as deterministic evidence.

## 10. Evidence burden scales with intervention impact

More disruptive interventions require stronger evidence.

Use this ordering as a qualitative principle, not a numeric scoring formula:

```text
focused local correction
< clean same-lane restart
< capability-lane escalation
< consequential independent judgment
< user/external-boundary escalation
```

A low-cost reversible correction can proceed from a concrete local hypothesis. A context reset requires stall or pollution evidence. Terra requires evidence of a technical capability gap. Sol requires a consequential judgment dependency. User escalation is reserved for a real authorization or decision boundary.

Do not convert this principle into hard retry counts or fixed probability thresholds.

## 11. Event-driven recovery evaluation

Recovery evaluation itself has cost. Re-evaluate when a material event occurs, not after every ordinary tool call.

Typical events are:

- a child returns;
- acceptance verification materially changes;
- the failure signature materially changes;
- relevant evidence is established, contradicted, or invalidated;
- a dependency becomes blocked or newly ready;
- the user changes outcome, scope, or authorization;
- workspace ownership or runtime capacity changes materially.

If the native runtime exposes structured child progress before return, record that capability and use only facts actually exposed. If it does not, recovery remains dependency-level or return-level. Do not claim structured live mid-run intervention without runtime evidence.

## 12. Clean restart semantics

A clean restart preserves task truth and drops conversational dead ends.

Preserve:

- the user-authorized outcome;
- current artifacts and actual diff;
- still-valid deterministic and repository evidence;
- acceptance criteria;
- unresolved dependency;
- current failure signature;
- material Recovery Ledger entries;
- explicit constraints and `DO NOT REDO` facts.

Do not propagate:

- private reasoning;
- self-reported confidence;
- abandoned hypotheses that have no remaining evidence value;
- repeated narrative explaining failed approaches.

A clean restart is not a new dependency. It is a recovery mechanism for the same dependency, so only one execution lane should own it at a time.

## 13. Budget, consent, and safety stay outside model judgment

A child or reviewer does not decide whether it may exceed user-authorized fan-out, permissions, scope, or external impact.

Before any recovery or escalation:

1. apply current consent boundaries;
2. preserve workspace write safety;
3. verify exact role availability when a model-specific lane is required;
4. respect runtime slot availability;
5. stop when an external or permission boundary is not authorized.

Do not spend additional compute asking a model whether an already exhausted policy boundary should be ignored.

## 14. Fresh judgment at commitment boundaries

When a Sol decision or review is justified, use a fresh packet containing compressed established facts and the actual artifact or decision options. Fresh context is valuable because it reduces conversational anchoring.

Fresh context does not make the review independent evidence by itself. Sol judgment remains `model_judgment` until supported by deterministic or repository facts where applicable.

## 15. Acceptance

The main session accepts a dependency only when its declared acceptance oracle is satisfied or the user explicitly changes that oracle.

Do not weaken acceptance criteria because a lane repeatedly fails them. Repeated failure is evidence for intervention and recovery classification, not permission to redefine success.
