# Release Candidate Final Verification Prompt

Use this prompt only after implementation closure is complete. It is a release-verification checklist, not an instruction to redesign routing or migration logic.

Repository:

```text
R-jed/subagents-dispatch
```

Current packaging model:

```text
Plugin directory: repository root (`.`)
Manifest: .codex-plugin/plugin.json
Marketplace: .agents/plugins/marketplace.json
Skills: skills/dispatch and skills/doctor
```

Current user/runtime identity model:

```text
User command       /dispatch
User command       /doctor
Internal identity  /subagents-dispatch:dispatch
Internal identity  /subagents-dispatch:doctor
Alternate picker   /skills
```

Read these files before verification:

```text
docs/deep-review-report.md
README.md
README_EN.md
README_AI.md
docs/plugin-installation.md
.codex-plugin/plugin.json
.agents/plugins/marketplace.json
policy-contract.json
skills/dispatch/SKILL.md
skills/doctor/SKILL.md
scripts/install-agents.py
scripts/legacy_migration.py
scripts/doctor.py
scripts/pre-push-ci.sh
.github/workflows/ci.yml
```

## Verification rules

Do not create, move, or delete a version tag. Do not create a GitHub Release unless the user explicitly authorizes release creation in a later instruction.

Do not alter the Luna/Terra/Sol routing architecture merely to make release verification easier.

Do not treat a green local run as a replacement for GitHub Actions. Do not treat green GitHub Actions as proof of a real Codex Marketplace installation.

Keep `UNKNOWN` when evidence is unavailable.

## Repository checks

Confirm the Plugin remains root-packaged and the Marketplace source resolves that root. Reject stale references that expect an installable package under `plugins/subagents-dispatch/`.

Confirm public docs use:

```text
/dispatch
/doctor
/skills
```

Keep namespaced identities only where host/internal identity is being described.

Confirm Doctor still delegates exact managed-profile health to:

```bash
python "$installer" --check
```

Confirm legacy migration still enforces:

```text
legacy compatibility OS lock
then current installer OS lock
ownership-proven deletion only
snapshot revalidation before deletion
rollback for partial cleanup/install failure
no overwrite of external drift during rollback
preserved modified/unowned/corrupt legacy state
explicit preserved-state terminal diagnostics
```

## CI evidence

Run or inspect the complete GitHub Actions matrix on the exact candidate/main SHA:

```text
Ubuntu Python 3.11
Ubuntu Python 3.12
macOS Python 3.11
Windows Python 3.11
```

Required results:

```text
JSON manifest validation PASS
pinned official OpenAI Plugin validator PASS
full pytest PASS
managed Agent profile install PASS
managed Agent profile --check PASS
repeat install lifecycle PASS
```

Record the exact SHA, workflow run ID, pytest count, and any platform skips.

Any CI failure invalidates the candidate until a new SHA passes the complete matrix.

## Clean Codex install smoke

After the candidate is on `main`, use a clean/fresh Codex environment where practical.

Record:

```text
Codex version
codex plugin marketplace add R-jed/subagents-dispatch result
codex plugin add subagents-dispatch@subagents-dispatch result
fresh session started
Dispatch visible
Doctor visible
/dispatch selection works
/doctor selection works
```

If a clean environment cannot be used, record `UNKNOWN` and the exact reason. Do not fabricate a PASS.

## Governance

Check `main` branch protection/ruleset. Required release CI should not be bypassable for a formal release candidate.

If branch protection cannot be changed with available permissions/tools, report it as the remaining manual governance gate.

Check current tags and GitHub Releases immediately before release. Do not reuse or mutate an existing version identity without explicit user approval.

## Completion output

Return exactly the evidence needed for a release decision:

```text
Candidate SHA: <sha>
Plugin version: <version>
Verdict: GO | NO-GO
GitHub Actions: <run id + conclusion>
Ubuntu 3.11: <result>
Ubuntu 3.12: <result>
macOS 3.11: <result>
Windows 3.11: <result>
Pytest: <exact result/count>
OpenAI validator: <result>
Managed-profile lifecycle: <result>
Legacy migration: <result>
Marketplace clean install: <result or UNKNOWN + reason>
/dispatch: <result>
/doctor: <result>
Branch protection: <result>
Tags: <current state>
GitHub Releases: <current state>
Remaining blockers: <none or exact blockers>
```

A `GO` authorizes only the statement that the candidate is ready for a release decision. It does not itself authorize creating the tag or GitHub Release.
