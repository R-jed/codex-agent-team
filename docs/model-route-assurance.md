# Model Route Assurance

Codex Agent Team uses model-specific Subagents only through its namespaced custom-Agent profiles. Route policy is separate from semantic responsibility, and post-spawn runtime evidence is a separate layer again.

## Why this exists

Keep three configuration facts distinct:

```text
preferred_route
configured_route
route_assurance
```

Runtime observation is recorded separately in typed evidence objects.

A role name such as `codex_agent_team_worker` describes responsibility. Its current route may change in a future version without changing the role contract.

## Supported route path: Profile Locked

The Plugin provisions four custom Agent profiles:

```text
codex_agent_team_reader        -> gpt-5.6-luna / max
codex_agent_team_worker        -> gpt-5.6-luna / max
codex_agent_team_investigator  -> gpt-5.6-terra / xhigh
codex_agent_team_advisor       -> gpt-5.6-sol / high
```

When live role guidance exposes the exact required project role with its expected lock, record:

```text
route_assurance = profile_locked
```

The spawn supplies the semantic `agent_type` and explicit `fork_turns`; the profile owns model and reasoning effort.

Example:

```text
agent_type = codex_agent_team_worker
fork_turns = none
```

`profile_locked` is configuration assurance. It does not mean the effective route has been observed after spawn.

## No Portable Mode

The public and internal policy no longer uses built-in roles plus explicit model/effort as a compatibility route.

If a required project profile cannot be proven available:

```text
keep responsibility in main session
or repair managed profile readiness
```

Do not substitute another role, another model, another effort, or inherited defaults.

This removes an unnecessary second routing system from the supported architecture.

## Effective Codex precedence

Current Codex documentation defines setting resolution broadly as:

```text
custom Agent file value
  -> explicit spawn value
  -> corresponding [agents] default
  -> parent value
```

Codex Agent Team intentionally uses the first path for model and effort. It does not rely on omission or inheritance for exact model-specific routing.

## Current policy routes are hypotheses

Luna Max is fixed as the current default execution baseline.

Terra XHigh and Sol High remain policy choices that must be evaluated on representative workloads. The project does not claim they are globally optimal simply because they are stronger reasoning settings.

Future route tuning should change profile contents and benchmark evidence, not semantic role names or task contracts.

## Post-spawn evidence

Runtime Truth v2 tracks:

```text
route_evidence
ancestry_evidence
permission_evidence
```

A complete matched route requires observed role, model, and effort. A partial observation is explicitly partial.

Compatibility grades remain derived summaries:

```text
C1_configuration_only
L1_local_record_observed
R1_runtime_reported
R2_runtime_reported_and_local_record_agree
X0_conflicted
```

See the installed Skill reference `references/runtime-assurance.md` and `scripts/verify-runtime.py`.

## Failure rule

```text
project profile missing -> managed readiness flow
profile exact but current task cannot discover role -> fresh task
profile route provable -> spawn may proceed
profile route unprovable -> main session
post-spawn route partial when runtime proof is required -> main session
post-spawn evidence conflict -> quarantine
```
