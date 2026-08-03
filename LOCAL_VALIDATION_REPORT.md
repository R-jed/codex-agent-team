# Codex Delegate Local Validation Report

This is the evidence ledger for Codex Delegate. `HEADOFF.md` defines what must be tested next. This file records what was actually observed, on which revision/runtime, which evidence remains reusable, and what remains unverified.

Repository policy, static CI, an official manifest validator, and model consultation are not substitutes for live Codex runtime evidence.

## Current reconciliation

Reconciled: 2026-08-03.

Current candidate state:

```text
Product: Codex Delegate
Candidate Plugin version: 0.5.1
Canonical user entry point: /codex-delegate
Compatibility repository/package namespace: R-jed/codex-agent-team / codex-agent-team
Candidate PR: #24
Candidate static-tested head: 5a556839624e58708279c6ab88c29e9f531678c8
Release posture: HOLD FOR RELEASE / VALIDATION INCOMPLETE
Known open reproducible PROJECT P0/P1: none
```

The candidate is not an accepted release baseline until PR #24 is merged and the final `origin/main` SHA is recorded. The static-tested head above is evidence for the exact branch content tested by GitHub Actions run `30822277936`.

Static CI result:

```text
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pytest on Ubuntu / Python 3.11: 131 passed
JSON manifest syntax checks: PASS
pinned official OpenAI Plugin validator: PASS
managed profile install: PASS
managed profile --check: PASS
idempotent managed profile reinstall: PASS
```

Official validator source used by that CI run:

```text
repository: openai/codex
source revision: 7750465934d97dd3cbcb3b1655d2f622744010d3
validator: codex-rs/skills/src/assets/samples/plugin-creator/scripts/validate_plugin.py
target: plugins/codex-agent-team
result: PASS
```

This proves compatibility with that pinned official Plugin ingestion validator. It does **not** prove that the current user's Codex build successfully registers the Git marketplace, installs the Plugin, refreshes a new thread, discovers `/codex-delegate`, provisions custom Agents, or spawns the expected effective routes.

The last accepted real Codex production-behavior baseline remains:

```text
c6020db903b35f0d57677b131bf35b0580144ab9
```

Last accepted live environment:

```text
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

## Evidence classes

Use these distinctions throughout validation:

- **Repository fact**: source, manifest, policy, test, or commit state inspected directly.
- **Deterministic evidence**: reproducible tests, verifier output, validator output, installer behavior, hashes, or filesystem results.
- **Live runtime evidence**: behavior observed from a real Codex task/session/runtime.
- **Model judgment**: advisory conclusion that remains challengeable and cannot replace deterministic/runtime evidence.
- **Carried forward**: older evidence whose declared dependencies have not materially changed.
- **Pending revalidation**: code/policy exists but the corresponding current live claim has not yet been demonstrated.

## v0.5.1 static architecture evidence

### Dependency-driven scheduling remains unchanged

v0.5.1 preserves the accepted v0.5.0 scheduling model:

```text
Dependency Ledger
-> ready frontier
-> Delegation Benefit Gate
-> Contractability Gate
-> consent / workspace / exact-route / runtime-capacity gates
-> smallest useful scheduling wave
```

Repository/deterministic facts remain:

- zero children is valid;
- there is no product-level hard child ceiling;
- the former `default 1 / normal max 2 / hard max 4` scheduler model remains absent;
- up to two concurrently active justified children is only the normal no-extra-consent envelope for explicit `/codex-delegate` use;
- larger simultaneous fan-out normally requires consent unless already authorized;
- runtime slot capacity is observed rather than hardcoded;
- one running dependency has one owner and must not receive duplicate inference;
- one canonical physical checkout has at most one active Writing Worker;
- delegation depth remains one.

No new Agent-count or retry-count constant was introduced by v0.5.1.

## v0.5.1 recovery refinement

The main change from v0.5.0 is the separation of execution state from intervention authority.

Static product contract now defines:

```text
execution evidence
-> structured execution signals
-> Intervention Gate
-> recovery classification
-> proposed action / policy gates / effective action
-> bounded Recovery Ledger
```

### Intervention Gate

Acceptance failure and need for intervention are separate facts.

The current responsibility may continue when it remains inside a valid/safe boundary and evidence shows material forward progress, for example:

- acceptance improves;
- deterministic evidence narrows the failure space;
- a repository fact removes uncertainty;
- the unresolved delta materially shrinks.

Static tests now protect the counterexample where a test still fails while new evidence narrows the root cause: that state must not automatically trigger restart or escalation.

### False-progress prevention

Static policy explicitly rejects these as progress by themselves:

- model confidence or narration;
- a file write;
- a successful command that neither improves acceptance nor establishes useful evidence nor narrows the delta;
- repeated discovery already covered by valid Shared Evidence State;
- a different patch that reproduces the same failure without new evidence.

### Structured execution signals

Current policy may record observations such as:

```text
verification_failures
same_failure_repeat
rewrite_verify_cycles
oscillation_signal
repeated_discovery
unresolved_delta_trend
scope_churn
```

These signals are evidence inputs, not automatic routing rules. No fixed threshold such as `three repeats -> Terra` or `four cycles -> restart` exists.

### Recovery Ledger

A bounded semantic Recovery Ledger may retain material entries:

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

It is not a transcript and contains no private chain-of-thought. Its purpose is to prevent fresh-context recovery from revisiting an established semantic dead end such as `hypothesis A -> B -> A`.

### Proposed versus effective action

The current contract distinguishes:

```text
proposed_action
effective_action
decision_source
policy_transform
```

A child, Terra, or Sol suggestion remains `model_judgment`. The main session owns the effective orchestration action after consent, workspace, route, permission, runtime, and user-decision gates.

### Event-driven recovery

Recovery classification is reevaluated after material events such as child return, acceptance/failure/evidence changes, dependency blocking/readiness, user changes, or material workspace/runtime changes. There is no fixed turn cadence.

These are static contracts. Real Intervention Gate behavior, Recovery Ledger behavior, clean restart value, semantic-cycle handling, and recovery economics remain live-validation items.

## Child-progress observability

A key v0.5.1 boundary is now explicit: Codex Delegate does not assume it can see a child's structured execution trajectory before the child returns.

The tested runtime must be characterized as one of:

```text
none
terminal_only
periodic_summary
structured_live
```

No level has yet been established for the current validation cycle.

If only terminal evidence is exposed, Codex Delegate recovery remains dependency-level/return-level. This is a valid architecture boundary. A SageRoute-style mid-run anti-thrashing claim is forbidden without structured live evidence.

## Official Codex Plugin compliance evidence

### Repository bundle shape

Repository facts:

```text
.agents/plugins/marketplace.json
plugins/codex-agent-team/
  .codex-plugin/plugin.json
  skills/
  scripts/
  agent-profiles/
```

The Plugin outer folder and `plugin.json` name are both `codex-agent-team`.

Current manifest version is `0.5.1` and uses strict semver.

The manifest declares the supported `skills` component and interface metadata. It does not declare an invented custom-Agent component.

The repository marketplace points to:

```text
./plugins/codex-agent-team
```

and declares:

```text
policy.installation = AVAILABLE
policy.authentication = ON_INSTALL
category = Productivity
```

The pinned official OpenAI validator passed the candidate Plugin root.

### Supported Git marketplace/install command contract

Current repository docs use:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin add codex-agent-team@codex-agent-team
```

The current OpenAI Codex CLI source reviewed for this iteration exposes:

- `codex plugin marketplace add` for local or Git marketplaces;
- `owner/repo` marketplace sources;
- `--ref` for the Git ref;
- repeatable `--sparse` paths;
- `codex plugin add PLUGIN@MARKETPLACE`.

These are current upstream/source facts. The exact command sequence still requires live execution on the user's current Codex build before it is accepted as a working product install path.

### Plugin versus custom-Agent boundary

Codex custom Agent configuration is treated separately from Plugin packaging.

Current project behavior:

```text
Plugin
-> distributes Skill + bundled project files

explicit user-approved first-run provisioning
-> writes four exact semantic profiles to the active personal Codex Agent directory
-> writes one ownership manifest under Codex home
```

The default personal location corresponds to `~/.codex/agents`; the project installer uses the active Codex-home `agents` directory so an explicitly overridden Codex home can be tested consistently.

The installer does not edit `config.toml`, credentials, MCP configuration, repositories, or unrelated profiles.

Live validation must confirm that the tested Codex build actually discovers those profiles from the active Codex home after provisioning. Static path policy does not prove discovery.

## Exact semantic route state

Current shipped route configuration remains unchanged from v0.5.0:

| Role | Configured route | Sandbox intent | Live evidence carried forward |
| --- | --- | --- | --- |
| Reader | GPT-5.6 Luna / max | read-only | historical L1 local corroboration |
| Worker | GPT-5.6 Luna / max | workspace-write | discovery only, exact live route pending |
| Investigator | GPT-5.6 Terra / xhigh | read-only | discovery only, exact live route pending |
| Advisor | GPT-5.6 Sol / high | read-only | discovery only, exact live route pending |

v0.5.1 does not change managed Agent profile bytes from v0.5.0. Recovery policy changes are carried by the Skill/contracts rather than by another profile-generation rewrite.

Configuration assurance remains separate from runtime observation.

## Historical live Plugin/profile evidence carried forward

Historical evidence still useful where dependencies remain valid:

- marketplace registration succeeded under the earlier documented path;
- Plugin `codex-agent-team@codex-agent-team` v0.3.0 installed successfully;
- missing project roles failed closed before profile provisioning;
- profile provisioning wrote four project profiles plus one ownership manifest;
- installer `--check` passed;
- a task created before provisioning did not refresh role discovery on Codex 0.146.0;
- a fresh task after provisioning discovered all four semantic roles;
- a real Reader used `fork_turns=none` and returned its bounded result;
- local rollout inspection reported Reader role, Luna model, max effort, read-only sandbox, managed permission profile, runtime 0.146.0, and expected parent id;
- no independent native complete-route attestation was exposed, so that historical Reader evidence remains L1 rather than R1/R2.

These historical facts do not prove the v0.5.1 CLI marketplace/install path or fresh-thread behavior on the current Codex build.

## Runtime Truth evidence carried forward

Static verifier coverage remains valid for:

- incomplete expected exact route fails closed;
- route, ancestry, and permission evidence are typed independently;
- missing/partial observations do not become affirmative proof;
- configuration/local/native conflicts can be quarantined;
- exact role/model/effort proof is two-sided.

Still pending where runtime exposes enough facts:

- Worker/Investigator/Advisor exact route observation;
- native complete route observation;
- native/local agreement;
- partial native route behavior;
- role/model/effort/parent/sandbox conflict characterization;
- duplicate rollout/schema drift on current Codex build.

## Behavioral evaluation state

Behavioral schema remains version `3.0` and now includes v0.5.1 recovery measurements:

```text
intervention_gate_evaluations
interventions_taken
recovery_ledger_entries
attempt_cycle_detected
proposed_recovery_action
effective_recovery_action
recovery_decision_source
policy_transform
child_progress_observability
```

New controlled workloads include:

```text
healthy-failure-no-intervention
successful-command-no-progress
recovery-ledger-oscillation
proposed-action-policy-transform
child-progress-observability
```

No live behavioral result yet establishes that compiled contracts, adaptive fan-out, clean restart, Recovery Ledger, Terra delta, selective Sol, or any particular child-observability level improves product outcomes. Those remain measurements.

## Workspace and concurrency status

The live matrix remains:

```text
M1 different sessions + different projects/checkouts
M2 different sessions + isolated worktrees
M3 different sessions + same canonical physical checkout
M4 writer session + read-only session on same checkout
```

No cross-session workspace lock has been added. A project-side coordination mechanism remains conditional on reproducible M3 failure.

Native fan-out capacity, slot recovery, queued dependency resumption, cancellation, orphan ownership, and lifecycle stress remain pending.

## Installer status

Historical CAT-LOCAL-001 direct Codex-home endpoint-symlink defect remains closed at:

```text
c6020db903b35f0d57677b131bf35b0580144ab9
```

v0.5.1 deterministic CI proves fresh managed profile install, exact `--check`, and idempotent reinstall for the unchanged current profile templates.

Still pending:

```text
real v0.3.x -> current Plugin migration
real v0.4.x -> current Plugin migration
real v0.5.0 -> v0.5.1 reinstall/update and fresh-thread Skill pickup
user-modified/unproven profile -> untouched + route fail closed
I1 two same-generation installers on one clean CODEX_HOME
I2 forced-failure transaction concurrent with peer success
I3 competing managed profile generations in one CODEX_HOME
```

No inter-process lock has been added before evidence establishes the need.

## Adversarial review contract

`gpt56-sol-pro-consult` remains required at Review Checkpoints A-E and for any P0/P1 candidate.

The exact target conversation is:

```text
分支 · 分支 · 项目对比分析
```

Exact-title unique-match semantics fail closed. Consultation output is model judgment and cannot count as Codex Delegate runtime-route, Plugin-install, or custom-Agent-discovery evidence.

## Current takeover status

**HOLD FOR RELEASE / VALIDATION INCOMPLETE**

This is caused by unfinished mandatory live gates, not by a currently known reproducible PROJECT P0/P1.

Highest-priority remaining evidence follows `HEADOFF.md`:

1. exact Worker, Investigator, and Advisor live routes plus Runtime Truth cases;
2. contractability, concurrent-edit, prompt-injection, and scope simulations;
3. Dependency Ledger, evidence reuse, Intervention Gate, Recovery Ledger, clean restart, capability-before-retry, and child-progress observability;
4. raw-prompt versus compiled-contract pairs plus controlled Terra/Sol pairs;
5. adaptive fan-out, consent, native slots/recovery, lifecycle, and M1-M4;
6. current official Plugin validator at RC time, real CLI marketplace/install + fresh-thread discovery, real profile provisioning/discovery, migration, and I1-I3 installer concurrency.

Continue the finite Checkpoint 1-6 sequence. Do not reopen architecture without reproducible evidence.
