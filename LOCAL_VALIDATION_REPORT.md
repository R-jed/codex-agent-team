# Codex Delegate Local Validation Report

This file is the release evidence ledger for Codex Delegate.

`HEADOFF.md` owns the remaining execution plan. This report records the accepted baseline, evidence classes, established claims, pending live claims, and compact live records. Git history and pull requests own development history. This file is not a changelog or second handoff plan.

## Current accepted baseline

```text
Product: Codex Delegate
Public README name: codex delegate
Repository: R-jed/codex-delegate
Marketplace id: codex-delegate
Plugin id: codex-delegate
Canonical entry point: /codex-delegate
Plugin version: 0.6.0
Internal compatibility roles: codex_agent_team_*
Internal ownership manifest: .codex-agent-team-agents.json
Release posture: HOLD FOR RELEASE / LIVE VALIDATION PENDING
Architecture posture: FROZEN AT v0.6.0
Repository maintenance posture: ENGINEERING CONSOLIDATION + POLICY REDUCTION + DEAD-SURFACE SWEEP COMPLETE
Known open reproducible PROJECT P0/P1: none
```

Latest accepted branding evidence:

```text
PR: #35
exact tested head: d21ad5800b110f20824cc5633b291d29b093d9cb
workflow: 30905709284
pytest: 159 passed
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pinned official OpenAI Plugin validator: PASS
managed profile install / --check / idempotent reinstall: PASS
```

Public-identity migration implementation evidence before the final handoff/ledger bookkeeping:

```text
PR: #36
exact tested migration head: faf854cb9862bedf97a6789c7216163e54d6f104
workflow: 30910901175
pytest: 160 passed
Ubuntu / Python 3.11: PASS
Ubuntu / Python 3.12: PASS
macOS / Python 3.11: PASS
pinned official OpenAI Plugin validator against plugins/codex-delegate: PASS
managed profile install / --check / idempotent reinstall: PASS
```

That evidence establishes the static package migration and compatibility tests. It does not establish a real user's legacy marketplace removal/reinstall, fresh-thread discovery, same-version refresh, runtime routes, or other live claims owned by HEADOFF.

## Evidence classes

- **Repository fact**: source, manifest, policy, test, or commit state inspected directly.
- **Deterministic evidence**: reproducible test, validator, installer, verifier, digest, or filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/session/runtime.
- **Upstream source fact**: behavior established from a specific OpenAI source revision or official documentation.
- **Public issue telemetry**: user-reported upstream evidence used for risk discovery only.
- **Model judgment**: advisory conclusion; never deterministic/runtime proof.
- **Carried forward**: older evidence whose declared dependencies have not materially changed.
- **Pending revalidation**: policy/tooling exists but the current runtime claim has not been demonstrated.

## Evidence matrix

| Claim / invariant | Evidence class | Current status | Boundary |
| --- | --- | --- | --- |
| Current repo/marketplace/Plugin public id is `codex-delegate` | Repository fact + tests | STATIC PASS | Real legacy migration remains live work |
| Plugin brand assets are packaged and accepted by official validator | Deterministic | PASS | Rendering in a real installed catalog remains Checkpoint 6 |
| Plugin structure and marketplace metadata | Deterministic | PASS | Static only; real CLI install remains live work |
| Four managed profile templates match policy contract | Deterministic | PASS | Configuration assurance only |
| Legacy `codex_agent_team_*` profile/ownership ids remain stable across public-ID migration | Repository fact + tests | PASS | Real legacy install reuse remains live work |
| Managed profile install / check / idempotent reinstall | Deterministic | PASS | Single-process CI path only |
| `policy-contract.json` owns stable route/resource/final-review constants | Repository fact + tests | PASS | Does not prove post-spawn runtime facts |
| `runtime-evidence.py` keeps route / ancestry / permission evidence separate | Deterministic | PASS | Normalized input only; no rollout scraping |
| `review-artifact.py` binds the source deliverable deterministically | Deterministic | PASS | Ignored/generated deliverables may need additional digest |
| Dead duplicate route-assurance document removed | Repository fact + tests | PASS | Normative route owners remain intact |
| Behavioral scorer dead abstractions removed | Deterministic | PASS | Output/schema semantics unchanged |
| Completion-driven ready-frontier refill | Repository fact + tests | STATIC PASS / LIVE PENDING | Native completion/wait surface is not yet proven |
| No unnecessary batch barrier when a dependency becomes ready | Policy contract | LIVE PENDING | Checkpoint 3 A/B/C timing case owns proof |
| Required Final Review Gate lifecycle | Repository fact + tests | STATIC PASS / LIVE PENDING | Fresh Sol route/artifact/verdict lifecycle need live proof |
| Exact Reader route | Historical live evidence | CARRIED FORWARD WITH LIMITS | Revalidate when material |
| Exact Worker / Investigator / Advisor routes | Live runtime evidence | PENDING | Current runtime must expose sufficient facts |
| Host-enforced read-only | Live runtime evidence | PENDING | Configuration intent is not permission proof |
| Cross-session same-checkout one-writer safety | Live runtime evidence | PENDING | No global lock before reproduction |
| Native child capacity / slot refill / close behavior | Live runtime evidence | PENDING | Runtime-version specific |
| Same-`CODEX_HOME` installer concurrency | Live filesystem evidence | PENDING | I1-I3 in HEADOFF |
| Real current marketplace add / upgrade / same-version refresh | Live CLI evidence | PENDING | Checkpoint 6 |
| Real legacy `codex-agent-team` -> `codex-delegate` public-ID migration | Live CLI evidence | PENDING | Remove old Plugin/marketplace, then add current identity |
| Contract / Terra-delta / Final Review product value | Controlled live pairs | PENDING | No quality/cost claim before measurement |

## Accepted static design boundaries

```text
main session = task-level control plane
no fixed Agent count
no mandatory Luna -> Terra -> Sol pipeline
delegation depth = 1
baseline no-extra-consent envelope = up to 2 concurrently active justified children
one active writing Worker per canonical physical checkout
exact model-specific routing fails closed without cross-role substitution
acceptance failure != intervention requirement
no universal retry count or stall threshold
completion-driven ready-frontier refill is preferred when native events permit
required Final Review Gate cannot be silently downgraded
post-review deliverable mutation invalidates an old ship verdict
public package id = codex-delegate
internal managed role/profile ownership ids remain legacy-compatible
```

Stable route/resource/final-review constants live in `plugins/codex-delegate/policy-contract.json`.

## Last accepted real Codex runtime baseline

```text
revision: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

This baseline predates v0.6.0 and the public-ID migration. It is not proof of current route identity, permission enforcement, completion wakeups, one-writer behavior across sessions, Final Review lifecycle, current Plugin install/upgrade, legacy public-ID migration, or concurrent installer safety.

## Pending live claims

The live evidence backlog is exactly the six release checkpoints in `HEADOFF.md`:

1. exact route, ancestry, and permission evidence where material;
2. contractability, scope safety, and prompt-injection resistance;
3. dependency scheduling, completion/wait behavior, evidence reuse, intervention, and recovery;
4. controlled product-value pairs plus required Final Review lifecycle;
5. adaptive fan-out, consent, native capacity, lifecycle, and multi-session writer safety;
6. current official Plugin validation, real `codex-delegate` install/upgrade, legacy public-ID migration, same-version refresh, and installer concurrency.

Do not add a second planning checklist here.

## Adversarial consultation

```text
/gpt56-sol-pro-consult
TARGET_CHATGPT_CONVERSATION_TITLE: 分支 · 分支 · 项目对比分析
TARGET_MODE: continue_existing_conversation
MATCH_POLICY: exact_title_unique_match
```

Consultation output is `model_judgment`; it never counts as Plugin-install, route, permission, filesystem, or runtime evidence.

## Live validation record format

```text
TEST_ID
CHECKPOINT
TESTED_REVISION
RUNTIME_VERSION / PLATFORM
WORKLOAD / FIXTURE
EXPECTED INVARIANT
CONFIGURED ROUTE / RESOURCE STATE
OBSERVED RUNTIME EVIDENCE
COMMANDS / VERIFICATION
RESULT: PASS | FAIL | PARTIAL | NOT_EXPOSED
EVIDENCE CLASS
DEPENDENCIES
UNRESOLVED
```

For completion/concurrency cases record:

```text
CHILD IDS
START / COMPLETION TIMES
WAIT SURFACE: barrier_only | per_child_terminal | any_child_update
SLOT REFILL TIMING
MODEL-MEDIATED POLLING OBSERVED: yes | no | unknown
```

For Final Review cases record requirement, triggers, `REVIEW_ARTIFACT_ID`, Advisor route evidence, verdict, post-review mutation, and gate satisfaction.

## Minimal provenance

```text
PR #27 -> v0.6.0 Final Review Gate feature baseline
PR #28 -> policy/runtime-evidence engineering consolidation
PR #30 -> README/policy reduction + completion-driven scheduling contract
PR #32 -> dead-code/dead-surface sweep + evidence-ledger compaction
PR #33/#34 -> release README + Chinese localization
PR #35 -> Codex-native Plugin brand assets
PR #36 -> public repository/marketplace/Plugin identity migration to codex-delegate
```

Historical v0.5.x and detailed development evidence remains in Git/PR history. Copy it forward only when a current claim explicitly depends on it.
