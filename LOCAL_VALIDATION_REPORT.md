# codex delegate Local Validation Report

This file is the maintainer evidence ledger. `HEADOFF.md` owns the finite remaining execution plan. Public users and AI Agents should use README/README_AI instead.

## Current accepted/candidate baseline

```text
Product: codex delegate
Repository: R-jed/codex-delegate
Marketplace id: codex-delegate
Plugin id: codex-delegate
Canonical command: /codex-delegate
Plugin version: 0.7.0
Current roles: codex_delegate_reader / codex_delegate_worker / codex_delegate_investigator / codex_delegate_advisor
Current profile files: codex-delegate-*.toml
Current ownership manifest: .codex-delegate-agents.json
Architecture posture: FROZEN
Release posture: HOLD FOR RELEASE / LIVE VALIDATION PENDING
Known open reproducible PROJECT P0/P1: none
```

The current repository tree has one project identity and one managed Agent generation. Runtime policy, installer code, public/AI documentation, architecture references, tests, and release gates are all defined in terms of `codex-delegate` / `codex_delegate_*` only.

Static validation for the exact current tree is pending a maintained full-suite run and current Plugin validation. Do not convert an older green run into evidence for files changed by the current cleanup.

## Repository review on 2026-08-04

Repository inspection and direct-main cleanup established:

- `README.md` and `README_EN.md` present only the current product identity and current install/update path;
- `README_AI.md` is the canonical AI-facing reference and tells Agents to use only the canonical identities declared there;
- active policy/profile/routing/eval surfaces use only the current `codex_delegate_*` role namespace;
- the managed installer owns only the four current profiles plus `.codex-delegate-agents.json`;
- unrelated Agent profiles are user-owned and left untouched;
- current-profile replacement is allowed only when the current ownership receipt proves the exact previous managed bytes;
- architecture, runtime, safety, installation, Skill, handoff, and evidence documentation no longer carry retired project identity semantics;
- repository tests include a tree-wide retired-identity guard so historical package identifiers cannot silently re-enter current text/config/code surfaces;
- remote branch cleanup is complete and `main` is the only remaining branch;
- there are no open pull requests at the time of the repository check.

This review is repository fact only. It does not substitute for deterministic test execution, official Plugin validation, or the live Codex checkpoints below.

## Evidence classes

- **Repository fact**: inspected source/manifest/policy/test state.
- **Deterministic evidence**: reproducible test, validator, installer/verifier/digest/filesystem result.
- **Live runtime evidence**: behavior observed from a real Codex task/runtime.
- **Upstream source fact**: behavior established from a specific official source revision/documentation.
- **Model judgment**: advisory only.
- **Carried forward**: older evidence whose declared dependencies did not change.
- **Pending revalidation**: implementation exists but current-runtime proof is absent.

## Current evidence matrix

| Claim | Status | Boundary |
| --- | --- | --- |
| repo/marketplace/Plugin identity is `codex-delegate` | repository fact | current tree |
| current role namespace is exclusively `codex_delegate_*` | repository fact, deterministic revalidation pending | policy/profile/test tree |
| current ownership receipt is `.codex-delegate-agents.json` | repository fact, deterministic revalidation pending | installer/profile lifecycle |
| installer manages only current project profiles | repository implementation fact, deterministic validation pending | fresh/update/adopt/check cases |
| unrelated Agent profiles are preserved | repository implementation fact, deterministic validation pending | installer safety |
| retired project identity is absent from current text/config/code surfaces | repository implementation fact, deterministic validation pending | tree-wide identity guard |
| Plugin structure/current official validator | pending current CI/RC validation | RC reruns then-current validator |
| exact current Reader/Worker/Investigator/Advisor routes | live pending | Checkpoint 1 |
| host-enforced read-only | live pending | configuration intent is not proof |
| completion-driven refill/wait surface | live pending | Checkpoint 3 |
| same-checkout multi-session writer safety | live pending | Checkpoint 5 |
| installer multi-process safety | live pending | Checkpoint 6 I1-I3 |
| Final Review lifecycle and product value | live pending | Checkpoint 4 |

## Last accepted real Codex runtime baseline

```text
revision: c6020db903b35f0d57677b131bf35b0580144ab9
platform: Apple Silicon macOS 27.0 (26A5388g)
Python: 3.14.6
Git: 2.50.1
Codex CLI/runtime: 0.146.0
```

That evidence predates the current profile/installer cleanup and cannot prove the exact current role-discovery or installer behavior.

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

For completion/concurrency also record child ids, start/completion times, wait surface, slot-refill timing, and model-mediated polling. For Final Review also record requirement, triggers, artifact id, Advisor route evidence, verdict, post-review mutation, and gate status.

## Adversarial consultation

Use `/gpt56-sol-pro-consult` with exact target conversation `R-jed/codex-delegate`. Exact-title unique-match is fail-closed. Consultation is model judgment only and never runtime/install evidence.
