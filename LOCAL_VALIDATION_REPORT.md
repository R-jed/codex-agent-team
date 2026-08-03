# Codex Delegate Local Validation Report

This is the evidence ledger for Codex Delegate. `HEADOFF.md` defines what must be tested next. This report records what was actually observed, on which revision/runtime, which evidence remains reusable, and what remains unverified.

Repository policy, static CI, an official Plugin validator, upstream source inspection, and model consultation are not substitutes for live Codex runtime evidence.

## Current reconciliation

Reconciled: 2026-08-03.

```text
Product: Codex Delegate
Plugin version: 0.5.1
Canonical user entry point: /codex-delegate
Compatibility repository/package namespace: R-jed/codex-agent-team / codex-agent-team
Accepted v0.5.1 feature merge: 9adf8edd303be22506744d569e6552b8fdbc7574
PR #24 final tested head: 7dadef8065f46bdb90accd38a3ffccfb75b23a51
Final PR workflow run: 30823406796
Post-merge HEADOFF reconciliation: 0fd04f9535baa57c64e824b8d556021087fd05fb
Release posture: HOLD FOR RELEASE / VALIDATION INCOMPLETE
Known open reproducible PROJECT P0/P1: none
```

v0.5.1 is now the accepted **static repository baseline**. It is no longer a candidate branch state. The remaining work is the finite live-validation sequence in `HEADOFF.md`.

The last accepted real Codex production-behavior baseline remains:

```text
revision: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

Do not relabel v0.5.1 static evidence as current live runtime proof.

## Evidence classes

- **Repository fact**: source, manifest, policy, test, or commit state inspected directly.
- **Upstream source fact**: behavior established from a specific OpenAI Codex source revision; version-sensitive until matched to a tested runtime build.
- **Deterministic evidence**: reproducible test, validator, installer, verifier, hash, or filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/session/runtime.
- **Model judgment**: advisory conclusion that remains challengeable and cannot replace deterministic/runtime evidence.
- **Carried forward**: older evidence whose dependencies have not materially changed.
- **Pending revalidation**: code/policy exists but the corresponding current live claim has not yet been demonstrated.

## Accepted v0.5.1 static CI evidence

PR #24 final head `7dadef8065f46bdb90accd38a3ffccfb75b23a51` completed GitHub Actions run `30823406796` successfully.

```text
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pytest: 131 passed
JSON Plugin/marketplace syntax: PASS
pinned official OpenAI Plugin validator: PASS
managed profile install: PASS
managed profile --check: PASS
idempotent managed profile reinstall: PASS
```

Pinned official validator:

```text
repository: openai/codex
source revision: 7750465934d97dd3cbcb3b1655d2f622744010d3
validator: codex-rs/skills/src/assets/samples/plugin-creator/scripts/validate_plugin.py
target: plugins/codex-agent-team
result: PASS
```

This proves compatibility with that official validator revision. The RC gate still reruns the then-current official validator on the exact release candidate.

## v0.5.1 architecture state

### Dependency-driven orchestration

The accepted static control graph remains:

```text
Dependency Ledger
-> ready frontier
-> Delegation Benefit Gate
-> Contractability Gate
-> consent / workspace / exact-route / runtime-capacity gates
-> smallest useful scheduling wave
```

Repository facts:

- zero Subagents is a normal valid outcome;
- there is no product-level hard child ceiling;
- the old `default 1 / normal max 2 / hard max 4` scheduling semantics remain removed;
- up to two concurrently active justified children is only the normal no-extra-consent envelope for explicit `/codex-delegate` use;
- larger simultaneous fan-out requires consent unless already authorized;
- native slot capacity is runtime evidence, not a product constant;
- a running dependency has one owner and does not receive duplicate inference;
- one canonical physical checkout has at most one active Writing Worker;
- delegation depth remains one.

### Evidence-gated recovery

v0.5.1 adds the accepted static recovery model:

```text
execution evidence
-> structured execution signals
-> Intervention Gate
-> recovery classification
-> proposed action / policy gates / effective action
-> bounded Recovery Ledger
```

Acceptance failure and need for intervention are separate facts. Healthy incomplete execution may continue when deterministic/repository evidence materially narrows the cause or unresolved delta.

These do not establish progress by themselves:

- model confidence or narration;
- a file write;
- a successful command that does not improve acceptance, establish useful evidence, or narrow the delta;
- repeated discovery already covered by valid Shared Evidence State;
- another model repeating the same judgment.

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

They are observations, not fixed auto-routing thresholds. No rule such as `three repeats -> Terra` exists.

### Recovery Ledger and decision provenance

A bounded Recovery Ledger may retain:

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

It is not a transcript and contains no private chain-of-thought.

Recovery also separates:

```text
proposed_action
effective_action
decision_source
policy_transform
```

A child, Terra, or Sol recommendation remains `model_judgment`. The main session owns the effective action after consent, workspace, route, permission, runtime, and user-decision gates.

Recovery evaluation is event-driven rather than turn-count-driven.

## Child-progress observability

Codex Delegate does not assume a SageRoute-style live trajectory stream from a running child.

The tested runtime must be characterized as:

```text
none
terminal_only
periodic_summary
structured_live
```

No level is yet accepted for the current live-validation cycle.

If only terminal evidence is exposed, recovery remains dependency-level/return-level. A mid-run anti-thrashing claim is forbidden without structured live runtime evidence.

## Official Codex Plugin evidence

### Static Plugin contract

Accepted repository shape:

```text
.agents/plugins/marketplace.json
plugins/codex-agent-team/
  .codex-plugin/plugin.json
  skills/
  scripts/
  agent-profiles/
```

Static facts:

- Plugin folder and `plugin.json` name are both `codex-agent-team`;
- Plugin version is `0.5.1` and uses strict semver;
- Plugin manifest declares the Skill and supported interface metadata;
- Plugin manifest does not invent an unsupported `agents` component;
- marketplace source is `./plugins/codex-agent-team`;
- marketplace carries `policy.installation`, `policy.authentication`, and `category`;
- pinned official OpenAI Plugin validator passes.

### Fresh Git marketplace/install contract

Current documented fresh-install path:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin add codex-agent-team@codex-agent-team
```

Then start a new Codex thread before checking `/codex-delegate` discovery.

### Existing Git marketplace upgrade/reinstall contract

Current documented update path:

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

Then start a new Codex thread.

Current upstream Codex CLI source supports Git `owner/repo` marketplace sources, `--ref`, repeatable `--sparse`, marketplace `upgrade`, and `plugin add PLUGIN@MARKETPLACE`.

These are upstream source and repository-contract facts. They remain pending live execution on the user's current Codex build.

### Full Plugin bundle availability

Current upstream OpenAI Codex `PluginStore` source stages installation by recursively copying the complete Plugin source directory into the versioned Plugin cache and rejects symlink entries.

This upstream source fact supports the project's installed relative paths:

```text
installed Skill
-> ../../scripts/install-agents.py
-> bundled agent-profiles/
```

Checkpoint 6 must still verify that the tested local Codex build actually exposes these bundled files after real installation.

### Plugin versus custom-Agent boundary

The current Plugin spec does not provide a first-class custom-Agent bundle component. Codex Delegate therefore separates:

```text
Plugin install
-> distributes Skill + bundled project files

explicit user-approved first-run provisioning
-> writes four exact semantic profiles into the active personal Codex Agent directory
-> writes one ownership manifest under Codex home
```

The public default personal custom-Agent location is `~/.codex/agents`. When Codex home is explicitly overridden, the project installer targets that active Codex home's `agents` directory and requires live native discovery before claiming success.

The installer does not edit `config.toml`, credentials, MCP configuration, repositories, or unrelated profiles.

## Exact semantic route state

Configured routes remain:

| Role | Configured route | Sandbox intent | Live evidence carried forward |
| --- | --- | --- | --- |
| Reader | GPT-5.6 Luna / max | read-only | historical L1 local corroboration |
| Worker | GPT-5.6 Luna / max | workspace-write | discovery only, exact live route pending |
| Investigator | GPT-5.6 Terra / xhigh | read-only | discovery only, exact live route pending |
| Advisor | GPT-5.6 Sol / high | read-only | discovery only, exact live route pending |

v0.5.1 does not change the managed Agent profile template bytes from v0.5.0. Configuration assurance remains separate from runtime observation.

## Historical live evidence carried forward

Still-valid historical facts include:

- prior Git marketplace registration succeeded;
- Plugin `codex-agent-team@codex-agent-team` v0.3.0 installed successfully;
- missing project roles failed closed before provisioning;
- provisioning wrote four project profiles plus one ownership manifest;
- installer `--check` passed;
- a pre-provisioning task did not refresh role discovery on Codex 0.146.0;
- a fresh task after provisioning discovered all four semantic roles;
- a real Reader used `fork_turns=none`;
- local rollout inspection reported Reader role, Luna model, max effort, read-only sandbox, managed permission profile, expected parent, and runtime 0.146.0;
- no independent complete native route attestation was exposed, so historical Reader evidence remains L1 rather than R1/R2;
- CAT-LOCAL-001 direct Codex-home endpoint-symlink defect remains closed.

These historical facts do not prove the v0.5.1 Git marketplace upgrade/install path, fresh-thread Skill pickup, bundled-script accessibility, current custom-Agent discovery, or current exact routes.

## Behavioral evaluation state

Behavioral schema remains version `3.0` and now records:

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

Controlled workloads now include:

```text
healthy-failure-no-intervention
successful-command-no-progress
recovery-ledger-oscillation
proposed-action-policy-transform
child-progress-observability
```

No live result yet proves that compiled contracts, adaptive fan-out, clean restart, Recovery Ledger, Terra delta, selective Sol, or a particular child-observability level improves product outcomes.

## Outstanding live gates

The finite mandatory sequence remains Checkpoints 1-6 in `HEADOFF.md`:

1. Worker / Investigator / Advisor exact routes and Runtime Truth cases.
2. Contractability, concurrent-edit, prompt-injection, recursion, and scope safety.
3. Dependency Ledger, Shared Evidence, Intervention Gate, Recovery Ledger, clean restart, capability-before-retry, and child-progress observability.
4. Raw-prompt versus compiled-contract pairs plus controlled Terra/Sol pairs.
5. Adaptive fan-out, consent, native slots/recovery, lifecycle, and M1-M4 workspace behavior.
6. Current official Plugin validator at RC time, real Git marketplace add/upgrade, `codex plugin add`, fresh-thread `/codex-delegate` discovery, installed bundle accessibility, custom-Agent provisioning/discovery, migration, and I1-I3 installer concurrency.

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
