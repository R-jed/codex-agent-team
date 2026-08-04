# Codex Delegate Local Validation Report

This is the evidence ledger for Codex Delegate. `HEADOFF.md` defines what must be tested next. This report records what was actually observed, on which revision/runtime, which evidence remains reusable, and what remains unverified.

Repository policy, static CI, an official Plugin validator, upstream source inspection, and model consultation are not substitutes for live Codex runtime evidence.

## Current reconciliation

Reconciled: 2026-08-04.

```text
Product: Codex Delegate
Plugin version: 0.6.0
Canonical user entry point: /codex-delegate
Compatibility repository/package namespace: R-jed/codex-agent-team / codex-agent-team
Current feature PR: #27
Validated v0.6.0 feature-candidate head: 6e5083e8fee26d92e63526413f620c566b4bf8f9
Validated workflow: 30876233050
Release posture: HOLD FOR RELEASE / LIVE VALIDATION PENDING
Known open reproducible PROJECT P0/P1: none
Static development posture: COMPLETE / ARCHITECTURE FROZEN
```

v0.6.0 is the accepted static architecture baseline once the final PR #27 closure head remains green. It adds a risk-triggered Final Review Gate without changing the four managed Agent profile bytes, installer ownership model, adaptive dependency scheduler, one-writer invariant, depth-one delegation, or exact semantic routes.

The validated feature-candidate workflow produced:

```text
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pytest: 164 passed
JSON Plugin/marketplace syntax: PASS
pinned official OpenAI Plugin validator: PASS
managed profile install: PASS
managed profile --check: PASS
idempotent managed profile reinstall: PASS
```

The final documentation/version closure must also pass CI before PR #27 is merged. That final static pass is regression evidence only and still cannot establish live Final Review Gate behavior.

The last accepted real Codex production-behavior baseline remains:

```text
revision: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

That live baseline predates v0.6.0. Do not relabel it as proof that a required final review uses the expected fresh Sol route, receives the expected artifact, invalidates a verdict after mutation, or respects the new consent lifecycle.

## Evidence classes

- **Repository fact**: source, manifest, policy, test, or commit state inspected directly.
- **Upstream source fact**: behavior established from a specific OpenAI Codex source revision; version-sensitive until matched to a tested runtime build.
- **Deterministic evidence**: reproducible test, validator, installer, verifier, hash, or filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/session/runtime.
- **Model judgment**: advisory conclusion that remains challengeable and cannot replace deterministic/runtime evidence.
- **Carried forward**: older evidence whose dependencies have not materially changed.
- **Pending revalidation**: code/policy exists but the corresponding current live claim has not yet been demonstrated.

## Accepted v0.6.0 static evidence

### Final Review Gate architecture

Repository facts establish this acceptance model:

```text
ordinary low-risk candidate
-> main-session inspection + deterministic acceptance
-> completion may remain main-session only

semantic risk trigger
-> review_requirement = required
-> main-session verification produces Candidate Ready
-> deterministic review_artifact_id
-> fresh codex_agent_team_advisor review
-> ship | fix-first | rethink
```

The existing Advisor profile may also return:

```text
INSUFFICIENT_EVIDENCE
```

That is a fail-closed unresolved state. It does not satisfy the quality gate and is not silently mapped to `fix-first` or `ship`.

Mandatory semantic trigger taxonomy includes:

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

The trigger policy is semantic. There is no numeric risk score, diff-line threshold, file-count threshold, retry threshold, or universal Sol stage.

### Artifact binding

`plugins/codex-agent-team/scripts/review-artifact.py` is deterministic repository tooling for candidate identity and post-review verification.

For repositories with `HEAD`, it binds:

- current HEAD;
- complete tracked staged + unstaged deliverable state against HEAD;
- Git-relevant executable-mode changes;
- non-ignored untracked files;
- untracked file kind/mode;
- symlink targets without following them.

For unborn repositories, it binds a canonical snapshot of index-tracked paths at current working-tree content plus non-ignored untracked content. This includes the staged-then-unstaged mutation case while remaining read-only.

The helper samples state twice and fails closed on concurrent mutation during capture. It emits `review_artifact_id = sha256:...` and supports `--verify`.

Static tests establish that tracked, staged, untracked, executable-mode, symlink, HEAD, unborn-repository, and post-capture mutation cases change or preserve the artifact identity according to policy.

Ignored/cache artifacts are excluded from the default source-deliverable identity. If an ignored/generated artifact is itself part of the requested deliverable, policy requires an additional deterministic digest or a fail-closed stop.

### Verdict lifecycle

Static contracts establish:

```text
ship
-> valid only for the exact unchanged reviewed artifact

fix-first
-> old review invalid
-> bounded correction
-> affected deterministic verification rerun
-> new artifact identity
-> new fresh review

rethink
-> invalidate affected architecture/contract/evidence assumptions
-> do not reduce to a local patch

INSUFFICIENT_EVIDENCE
-> gate unresolved
-> establish named missing evidence
-> new fresh review
```

No Worker, main-session self-review, or earlier Sol review of a different artifact can satisfy a currently required gate.

### Consent interaction

Static policy establishes:

- the first required read-only Sol review may fit inside explicit `/codex-delegate` baseline orchestration when it remains ordinary bounded completion work;
- implicit Skill invocation asks before adding Sol unless the request already authorized stronger review;
- `review_requirement = required` does not itself override compute consent;
- if the required review is declined, the candidate remains `Candidate Ready`, the requirement remains `required`, and no `ship` is fabricated;
- repeated `fix-first` review cycles cross the material-compute consent boundary when they materially exceed ordinary bounded execution.

These are policy facts, not yet live UX evidence.

### Behavioral evaluation support

Behavioral schema remains version `3.0` and now supports a distinct mandatory-gate mode:

```text
contract_luna_final_review_gate
```

This keeps mandatory Final Review Gate data separate from:

```text
contract_luna_selective_sol
```

New result fields include:

```text
final_review_requirement
final_review_trigger_reasons
final_review_attempts
final_review_verdict
final_review_gate_satisfied
review_artifact_verify_failures
post_review_mutations
```

The scorer reports final-review attempts, artifact invalidation, required/satisfied gate counts, material catches, false positives, and review yield without inventing missing telemetry.

Controlled static workload definitions now cover:

```text
public-contract-final-review-required
terra-escalation-final-review-required
material-recovery-final-review-required
fix-first-invalidates-old-review
post-review-mutation-invalidates-ship
rethink-invalidates-plan
implicit-required-review-declined
```

No live result yet proves that mandatory Final Review Gate use improves product outcomes or is economically optimal. Review-yield and cost claims remain pending measured live workloads.

## Accepted v0.5.1 historical static evidence

v0.5.1 remains the prior accepted static baseline for the dependency-driven scheduler, evidence-gated recovery, Plugin lifecycle, and four semantic routes.

Historical static chain:

```text
PR #24 final head: 7dadef8065f46bdb90accd38a3ffccfb75b23a51
PR #24 workflow: 30823406796
feature merge: 9adf8edd303be22506744d569e6552b8fdbc7574
post-merge main-equivalent verification: PR #25 / workflow 30824385799
final v0.5.1 docs-contract closure: PR #26
```

That baseline produced 131-test static closure before v0.6.0 Final Review Gate work began.

Historical v0.5.1 evidence remains usable only for facts whose dependencies did not change. In particular, it does not prove any v0.6.0 final-review lifecycle behavior.

## v0.6.0 architecture state

### Dependency-driven orchestration

The static control graph remains:

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
- up to two concurrently active justified children is only the normal no-extra-consent envelope for explicit `/codex-delegate` use;
- larger simultaneous fan-out requires consent unless already authorized;
- native slot capacity is runtime evidence, not a product constant;
- a running dependency has one owner and does not receive duplicate inference;
- one canonical physical checkout has at most one active Writing Worker;
- delegation depth remains one.

### Responsibility-first routing

Current configured routes remain:

| Role | Configured route | Sandbox intent | Current live evidence |
| --- | --- | --- | --- |
| Reader | GPT-5.6 Luna / max | read-only | historical L1 local corroboration |
| Worker | GPT-5.6 Luna / max | workspace-write | exact live route pending |
| Investigator | GPT-5.6 Terra / xhigh | read-only | exact live route pending |
| Advisor | GPT-5.6 Sol / high | read-only | exact live route pending |

v0.6.0 does not change the managed Agent profile template bytes from v0.5.0/v0.5.1. Configuration assurance remains separate from runtime observation.

Routing remains responsibility-first:

```text
responsibility / decision boundary / demonstrated capability
-> choose suitable safe lane
-> cost only breaks ties between equally suitable safe lanes
```

There is no cheap-first model ladder and no requirement that Luna fail before a dependency that clearly requires Terra investigation or Sol judgment can use that lane.

### Evidence-gated recovery

The recovery model remains:

```text
execution evidence
-> structured execution signals
-> Intervention Gate
-> recovery classification
-> proposed action / policy gates / effective action
-> bounded Recovery Ledger
```

Acceptance failure and need for intervention remain separate facts. No fixed retry count or fixed stall threshold exists.

A material Terra escalation or recovery event can now also change Final Review Gate state when it materially shapes the delivered implementation. That dynamic promotion is statically specified but awaits live evidence.

## Official Codex Plugin evidence

### Static Plugin contract

Repository shape remains:

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
- Plugin version is `0.6.0` and uses strict semver;
- Plugin manifest declares the Skill and supported interface metadata;
- Plugin manifest does not invent an unsupported `agents` component;
- marketplace source is `./plugins/codex-agent-team`;
- marketplace carries installation/authentication/category policy;
- the pinned official OpenAI Plugin validator passed on the validated v0.6.0 feature candidate;
- `review-artifact.py` is bundled under the Plugin root alongside `install-agents.py`.

Pinned official validator used in CI:

```text
repository: openai/codex
source revision: 7750465934d97dd3cbcb3b1655d2f622744010d3
validator: codex-rs/skills/src/assets/samples/plugin-creator/scripts/validate_plugin.py
target: plugins/codex-agent-team
result: PASS on validated v0.6.0 feature-candidate head
```

The RC gate still reruns the current official validator on exact release-candidate content.

### Fresh Git marketplace/install contract

Documented fresh-install path remains:

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin add codex-agent-team@codex-agent-team
```

Then start a new Codex thread before checking `/codex-delegate` discovery.

Documented existing-marketplace update path remains:

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

Then start a new Codex thread.

These are repository-contract/upstream facts until executed on the current local Codex build.

### Plugin versus custom-Agent boundary

The current Plugin spec does not provide a first-class custom-Agent bundle component. Codex Delegate therefore continues to separate Plugin installation from explicit user-approved profile provisioning.

The installer does not edit `config.toml`, credentials, MCP configuration, repositories, or unrelated profiles.

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

These facts do not prove v0.6.0 Plugin upgrade/install, current exact routes, required fresh Advisor behavior, or Final Review Gate completion semantics.

## Outstanding live gates

The finite mandatory sequence remains Checkpoints 1-6 in `HEADOFF.md`:

1. Worker / Investigator / Advisor exact routes and Runtime Truth cases, including one required fresh Final Review Gate Advisor spawn.
2. Contractability, concurrent-edit, prompt-injection, recursion, scope safety, and Final Review Gate policy-integrity cases.
3. Dependency Ledger, Shared Evidence, Intervention Gate, Recovery Ledger, clean restart, capability-before-retry, child-progress observability, and dynamic review-requirement promotion after material Terra/recovery events.
4. Raw-prompt versus compiled-contract pairs, controlled Terra/optional-Sol pairs, plus mandatory Final Review Gate cases for hard triggers, artifact binding, mutation invalidation, `fix-first`, `rethink`, and `INSUFFICIENT_EVIDENCE`.
5. Adaptive fan-out, consent, native slots/recovery, Final Review Gate consent decline/repeated-review cost boundaries, lifecycle, and M1-M4 workspace behavior.
6. Current official Plugin validator at RC time, real Git marketplace add/upgrade, `codex plugin add`, fresh-thread `/codex-delegate` discovery, installed bundle accessibility including `review-artifact.py`, custom-Agent provisioning/discovery, v0.5.x -> v0.6.0 migration, and I1-I3 installer concurrency.

No cross-session workspace lock or inter-process installer lock has been added before reproducible evidence establishes the need.

## Adversarial consultation

Required mechanism remains:

```text
/gpt56-sol-pro-consult
```

Exact target conversation remains:

```text
分支 · 分支 · 项目对比分析
```

Exact-title unique-match semantics fail closed. Consultation output remains `model_judgment` and cannot count as Codex Delegate runtime-route, Plugin-install, Agent-discovery, or Final Review Gate runtime evidence.

## Current takeover status

```text
STATIC DEVELOPMENT COMPLETE
ARCHITECTURE FROZEN AT v0.6.0
NEXT PHASE: HEADOFF CHECKPOINT 1-6 LIVE VALIDATION
TARGET: v1.0.0
```

Release posture remains **HOLD FOR RELEASE / LIVE VALIDATION PENDING** because mandatory live gates are unfinished, not because a currently known reproducible PROJECT P0/P1 is open.

Do not reopen architecture without reproducible evidence. Continue the finite Checkpoint 1-6 sequence in `HEADOFF.md`.
