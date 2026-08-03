# Codex Delegate Local Validation Report

This is the evidence ledger for Codex Delegate. `HEADOFF.md` defines what must be tested next. This report records what was actually observed, on which revision/runtime, which evidence remains reusable, and what remains unverified.

Repository policy, static CI, an official Plugin validator, upstream source inspection, and model consultation are not substitutes for live Codex runtime evidence.

## Current reconciliation

Reconciled: 2026-08-03.

```text
Product: Codex Delegate
Candidate Plugin version: 0.5.1
Canonical user entry point: /codex-delegate
Compatibility repository/package namespace: R-jed/codex-agent-team / codex-agent-team
Candidate PR: #24
Exact static-tested branch head: 0254f112e7345ca4abc800d68340a9f576472d18
GitHub Actions run: 30823045269
Release posture: HOLD FOR RELEASE / VALIDATION INCOMPLETE
Known open reproducible PROJECT P0/P1: none
```

The candidate becomes the accepted repository baseline only after PR #24 is merged and the resulting `origin/main` SHA is recorded. This report update follows the exact tested branch head and is documentation-only.

## Static CI evidence

GitHub Actions run `30823045269` produced:

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

Official Plugin validator used in CI:

```text
repository: openai/codex
source revision: 7750465934d97dd3cbcb3b1655d2f622744010d3
validator: codex-rs/skills/src/assets/samples/plugin-creator/scripts/validate_plugin.py
target: plugins/codex-agent-team
result: PASS
```

This is deterministic compatibility evidence for that official validator revision. It is not evidence that a particular local Codex build completed marketplace registration, Plugin installation, fresh-thread discovery, custom-Agent discovery, or exact route spawning.

## Evidence classes

- **Repository fact**: source, manifest, policy, test, or commit state inspected directly.
- **Upstream source fact**: behavior established from a specific OpenAI Codex source revision; version-sensitive until matched to a tested runtime build.
- **Deterministic evidence**: reproducible test, validator, installer, verifier, hash, or filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/session/runtime.
- **Model judgment**: advisory conclusion that remains challengeable and cannot replace deterministic/runtime evidence.
- **Carried forward**: older evidence whose dependencies have not materially changed.
- **Pending revalidation**: code/policy exists but the corresponding current live claim has not yet been demonstrated.

## v0.5.1 architecture evidence

v0.5.1 is a bounded refinement of v0.5.0. It does not reopen fixed Agent counts, route tuning, or the six-checkpoint release scope.

### Scheduling remains dependency-driven

```text
Dependency Ledger
-> ready frontier
-> Delegation Benefit Gate
-> Contractability Gate
-> consent / workspace / exact-route / runtime-capacity gates
-> smallest useful scheduling wave
```

Static facts remain:

- zero children is valid;
- no product-level hard child ceiling exists;
- the old `default 1 / normal max 2 / hard max 4` scheduler model remains removed;
- up to two concurrently active justified children is only the normal no-extra-consent envelope for explicit `/codex-delegate` use;
- larger simultaneous fan-out normally requires consent unless already authorized;
- native slot capacity is observed instead of hardcoded;
- one running dependency has one owner;
- one canonical physical checkout has at most one active Writing Worker;
- delegation depth remains one.

### Recovery now has an explicit Intervention Gate

The static control model is:

```text
execution evidence
-> structured execution signals
-> Intervention Gate
-> recovery classification
-> proposed action / policy gates / effective action
-> bounded Recovery Ledger
```

Acceptance failure and need for intervention are separate facts. A still-failing responsibility may continue when deterministic/repository evidence materially narrows the cause or unresolved delta.

These do not establish progress by themselves:

- model confidence or narration;
- a file write;
- a successful command that does not improve acceptance, establish useful evidence, or narrow the delta;
- repeated discovery already covered by valid Shared Evidence State;
- a different patch that reproduces the same failure without useful new evidence.

Structured signals may include:

```text
verification_failures
same_failure_repeat
rewrite_verify_cycles
oscillation_signal
repeated_discovery
unresolved_delta_trend
scope_churn
```

They are evidence inputs, not numeric auto-routing rules. No fixed rule such as `three repeats -> Terra` exists.

### Recovery Ledger

Material semantic history may retain:

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

The ledger is bounded, is not a transcript, and contains no private chain-of-thought. Its main purpose is to prevent a fresh context from unknowingly returning to a previously established dead end such as `A -> B -> A`.

### Proposed action is not orchestration authority

Current contract distinguishes:

```text
proposed_action
effective_action
decision_source
policy_transform
```

A child, Terra, or Sol recommendation remains `model_judgment`. The main session owns the effective action after user consent, workspace ownership, exact-route, permission, runtime, and other policy gates.

### Event-driven recovery

Recovery is reevaluated on material events such as child return, acceptance/failure/evidence changes, dependency blocking/readiness, user changes, or material workspace/runtime changes. There is no fixed turn cadence.

## Child-progress observability

Codex Delegate no longer assumes that a parent can inspect a child's structured trajectory before child return.

The tested runtime must be characterized as exactly one of:

```text
none
terminal_only
periodic_summary
structured_live
```

No level has yet been established for the current v0.5.1 validation cycle.

If the runtime exposes only terminal evidence, recovery remains dependency-level/return-level. No SageRoute-style mid-run anti-thrashing claim is allowed without structured live runtime evidence.

## Official Plugin contract evidence

### Bundle and marketplace shape

Current repository facts:

```text
.agents/plugins/marketplace.json
plugins/codex-agent-team/
  .codex-plugin/plugin.json
  skills/
  scripts/
  agent-profiles/
```

The Plugin folder and manifest `name` both equal `codex-agent-team`.

The manifest version is `0.5.1`, uses strict semver, declares the supported Skill component and interface metadata, and does not invent an `agents` Plugin-manifest component.

The repository marketplace points to:

```text
./plugins/codex-agent-team
```

with:

```text
policy.installation = AVAILABLE
policy.authentication = ON_INSTALL
category = Productivity
```

The pinned official OpenAI Plugin validator passed this candidate.

### Git marketplace CLI contract

Current upstream Codex CLI source inspected during this iteration supports:

- `codex plugin marketplace add` with Git `owner/repo` sources;
- `--ref` for the Git ref;
- repeatable `--sparse` arguments;
- `codex plugin marketplace upgrade [MARKETPLACE_NAME]`;
- `codex plugin add PLUGIN@MARKETPLACE`.

Current documented fresh-install command:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin add codex-agent-team@codex-agent-team
```

Current documented update/reinstall command:

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

A new Codex thread is required before testing the installed/reinstalled Skill surface.

These are upstream/source and repository-contract facts. Real execution on the user's current Codex build remains pending.

### Full Plugin bundle availability

Current OpenAI Codex `PluginStore` source was inspected directly. Its install path stages the Plugin by recursively copying the entire source directory into the versioned Plugin cache, not only the declared Skill. The recursive copy accepts normal files/directories and rejects symlinks.

This upstream source fact supports the project's relative-path design:

```text
installed Skill
-> ../../scripts/install-agents.py
-> ../agent-profiles templates through the bundled installer
```

It means bundled `scripts/` and `agent-profiles/` are expected to survive Plugin installation under that implementation. Live Checkpoint 6 must still verify this on the tested Codex build before treating it as a runtime guarantee.

### Plugin versus custom-Agent boundary

Current upstream Plugin manifest does not provide a first-class custom-Agent bundle component. The project therefore keeps these responsibilities separate:

```text
Plugin install
-> distributes Skill + bundled project files

explicit user-approved first-run provisioning
-> writes four exact semantic profiles into the active personal Codex Agent directory
-> writes one ownership manifest under Codex home
```

The public default personal Agent directory is `~/.codex/agents`. When Codex home is explicitly overridden, the project installer targets that active Codex home's `agents` directory and requires live role discovery to confirm behavior.

The installer does not edit `config.toml`, credentials, MCP configuration, repositories, or unrelated profiles.

## Exact semantic route state

Configured routes remain unchanged from v0.5.0:

| Role | Configured route | Sandbox intent | Live evidence carried forward |
| --- | --- | --- | --- |
| Reader | GPT-5.6 Luna / max | read-only | historical L1 local corroboration |
| Worker | GPT-5.6 Luna / max | workspace-write | discovery only, exact live route pending |
| Investigator | GPT-5.6 Terra / xhigh | read-only | discovery only, exact live route pending |
| Advisor | GPT-5.6 Sol / high | read-only | discovery only, exact live route pending |

v0.5.1 does not change the managed Agent profile template bytes from v0.5.0. Recovery behavior is refined in the Skill/contracts rather than by another profile-generation rewrite.

## Historical live evidence carried forward

Last accepted production-behavior baseline:

```text
revision: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

Carried-forward live facts where dependencies remain valid:

- prior marketplace registration succeeded;
- Plugin `codex-agent-team@codex-agent-team` v0.3.0 installed successfully;
- missing project roles failed closed before provisioning;
- provisioning wrote four profiles plus one ownership manifest;
- installer `--check` passed;
- a task created before provisioning did not refresh roles on Codex 0.146.0;
- a fresh task after provisioning discovered all four semantic roles;
- a real Reader used `fork_turns=none`;
- local rollout inspection reported Reader role, Luna model, max effort, read-only sandbox, managed permission profile, expected parent, and runtime 0.146.0;
- no independent complete native route attestation was exposed, so the historical Reader remains L1 rather than R1/R2.

These historical facts do not prove the v0.5.1 marketplace-upgrade/install path, fresh-thread pickup, bundled-script accessibility, or current custom-Agent discovery.

## Behavioral evaluation state

Schema remains version `3.0` and now records:

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

No live result yet establishes that compiled contracts, adaptive fan-out, clean restart, Recovery Ledger, Terra delta, selective Sol, or any particular observability level improves product outcomes. Those remain measurements.

## Outstanding live gates

The mandatory finite sequence remains Checkpoints 1-6 in `HEADOFF.md`:

1. Worker / Investigator / Advisor exact routes and Runtime Truth adversarial cases.
2. Contractability, concurrent edits, prompt injection, recursion, and write-scope safety.
3. Dependency Ledger, Shared Evidence, Intervention Gate, Recovery Ledger, clean restart, capability-before-retry, and child-progress observability.
4. Raw-prompt versus compiled-contract pairs plus controlled Terra/Sol pairs.
5. Adaptive fan-out, consent, native slots/recovery, lifecycle, and M1-M4 workspace behavior.
6. Current official Plugin validator at RC time, real Git marketplace add/upgrade, `codex plugin add`, fresh-thread `/codex-delegate` discovery, bundled provisioning-script/template availability, custom-Agent provisioning/discovery, migrations, and I1-I3 installer concurrency.

No cross-session workspace lock or inter-process installer lock has been added before reproducible evidence establishes the need.

## Adversarial consultation

Required mechanism:

```text
/gpt56-sol-pro-consult
```

Exact target conversation:

```text
分支 · 分支 · 项目对比分析
```

Exact-title unique-match semantics fail closed. Consultation output remains `model_judgment` and cannot count as Codex Delegate runtime-route, Plugin-install, or Agent-discovery evidence.

## Current takeover status

**HOLD FOR RELEASE / VALIDATION INCOMPLETE**

This status is caused by unfinished mandatory live gates, not by a currently known reproducible PROJECT P0/P1.

Do not reopen architecture without reproducible evidence. Continue the finite Checkpoint 1-6 sequence in `HEADOFF.md`.
