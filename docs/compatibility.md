# Runtime compatibility

Codex Agent Team sits above a fast-moving Codex Native Subagent runtime. Compatibility therefore has two layers: package integrity, which this repository can test deterministically, and live Subagent capability, which must be checked in the active Codex session.

Last reviewed: 2026-08-02.

## Evidence terminology

| Grade | Meaning | Suitable claim |
| --- | --- | --- |
| `C1_configuration_only` | exact configuration path accepted; no post-spawn observation | configuration-assured only |
| `L1_local_record_observed` | mutable local rollout record matches | local record observed |
| `R1_runtime_reported` | live/public runtime reports effective facts | runtime reported |
| `R2_runtime_reported_and_local_record_agree` | public runtime and local record agree | corroborated runtime report |
| `X0_conflicted` | expected facts mismatch or sources disagree | quarantine |

No current local record grade is described as authoritative or cryptographic attestation.

## Capability matrix

| Capability | Repository can verify offline | Requires active Codex runtime |
| --- | --- | --- |
| Skill/profile file integrity | yes | no |
| model/effort pins in shipped profiles | yes | no |
| `spawn_agent` exposes the required role surface | no | yes |
| a requested model is available on the current MultiAgent backend | no | yes |
| effective child model/effort | only from optional local record | yes for `R1` |
| effective sandbox / permission profile | only if a record exposes it | yes for `runtime_enforced` |
| child parent-thread identity | only if a record exposes it | preferred from live metadata |
| local rollout adapter schema | fixture-tested | version-sensitive in real Codex |

## Recommended checks

Run after installation or upgrade:

```bash
python scripts/install.py --check
python scripts/doctor.py
```

`doctor.py` is intentionally non-mutating. It can report package/profile integrity, local sessions-store availability, installed Codex CLI version when discoverable, and whether the bundled evidence tools are present. It cannot prove live model routing without an active Subagent session.

For a consequential child whose route must be verified:

1. collect normalized native runtime metadata when the live Codex surface exposes it;
2. optionally collect the exact child local rollout record with `inspect-runtime.py`;
3. pass expected/native/local objects to `verify-runtime.py`;
4. accept only the evidence grade required by the task.

## Version-sensitive surfaces

The following Codex surfaces are explicitly treated as version-sensitive:

- MultiAgent model availability;
- visibility of explicit `model` / `reasoning_effort` spawn fields;
- custom Agent discovery and precedence;
- effective sandbox/approval inheritance;
- public post-spawn model/effort metadata;
- local session JSONL field names and semantics.

A parser continuing to run after a Codex upgrade does not by itself prove semantic compatibility. Prefer public runtime metadata whenever available and record the discovered Codex version alongside local-record evidence.

## Failure rule

```text
package integrity failure
-> repair before Profile Mode

configuration route unprovable
-> keep responsibility in Root

runtime report required but unavailable
-> keep responsibility in Root

local record available but no native report
-> at most L1_local_record_observed

source mismatch
-> X0_conflicted -> quarantine
```

This document records project compatibility policy. Current OpenAI source references are tracked separately in `openai-references.md`.
