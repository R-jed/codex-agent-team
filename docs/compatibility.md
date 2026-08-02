# Runtime compatibility

Codex Agent Team sits above a fast-moving Codex Native Subagent runtime. Compatibility therefore has two layers: Plugin/package integrity, which this repository can test deterministically, and live Subagent capability, which requires active Codex runtime evidence.

Last reviewed: 2026-08-02.

## Evidence terminology

Runtime Truth v2 tracks three typed evidence objects:

```text
route_evidence
ancestry_evidence
permission_evidence
```

Missing evidence is represented as `not_observed` or `partial`, not as a successful match.

Compact grades remain derived summaries:

| Grade | Meaning |
| --- | --- |
| `C1_configuration_only` | no complete observed route |
| `L1_local_record_observed` | complete matching local route only |
| `R1_runtime_reported` | complete matching native role/model/effort |
| `R2_runtime_reported_and_local_record_agree` | complete native and local route evidence agree |
| `X0_conflicted` | expected facts mismatch or sources materially disagree |

No local rollout record is described as authoritative or cryptographic attestation.

## Capability matrix

| Capability | Repository can verify offline | Requires active Codex runtime |
| --- | --- | --- |
| Plugin manifest and Skill package integrity | yes | no |
| model/effort pins in shipped semantic profiles | yes | no |
| managed custom-Agent installer lifecycle | yes | no |
| `spawn_agent` exposes the required project role | no | yes |
| effective child role/model/effort | only from optional local record | yes for `R1_runtime_reported` |
| effective sandbox / permission profile | only if a record exposes it | yes for host-enforced claims |
| child parent-thread identity | only if a record exposes it | preferred from live metadata |
| local rollout adapter schema | fixture-tested | version-sensitive in real Codex |

## Recommended checks

The normal user path is `/codex-agent-team`. Profile readiness is checked after a responsibility has justified model-specific delegation.

Current roles:

```text
codex_agent_team_reader
codex_agent_team_worker
codex_agent_team_investigator
codex_agent_team_advisor
```

If profiles are missing, the Skill asks permission, runs the bundled managed installer and exactness check, then re-inspects live role discovery.

For a consequential child whose runtime facts matter:

1. collect normalized native metadata when exposed;
2. optionally collect the exact child local rollout record;
3. pass expected/native/local objects to `verify-runtime.py`;
4. inspect typed route, ancestry, and permission evidence;
5. use a compact grade only as a summary of those complete facts.

## Version-sensitive surfaces

Treat these Codex surfaces as version-sensitive:

- custom Agent discovery;
- MultiAgent model availability;
- effective sandbox and approval inheritance;
- public post-spawn model/effort metadata;
- parent-thread metadata;
- local session JSONL field names and semantics.

A parser continuing to run after a Codex upgrade does not prove semantic compatibility.

## Failure rule

```text
managed profile integrity failure
-> report installer error; keep responsibility in main session

profiles exact but current task cannot discover role
-> start a fresh task

configuration route unprovable
-> main session

runtime route proof required but native route is missing or partial
-> main session

complete local route without complete native route
-> at most L1_local_record_observed

material conflict
-> X0_conflicted -> quarantine
```
