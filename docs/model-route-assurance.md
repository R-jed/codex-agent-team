# Model Route Assurance

Codex Delegate uses model-specific Subagents only through namespaced custom-Agent profiles. Semantic responsibility, configured route, and post-spawn runtime evidence are separate layers.

The machine-readable source of truth for the current role/profile/model/effort/sandbox tuple is [`plugins/codex-agent-team/policy-contract.json`](../plugins/codex-agent-team/policy-contract.json). Documentation may explain those routes, but tests and installer validation should derive stable constants from that contract rather than maintaining another independent table.

## Configuration facts

Keep these facts distinct:

```text
preferred_route
configured_route
route_assurance
```

A role name such as `codex_agent_team_worker` describes responsibility. Its current model route may change in a future version without changing the responsibility contract.

## Supported route path: Profile Locked

Current roles are:

```text
codex_agent_team_reader        -> gpt-5.6-luna / max
codex_agent_team_worker        -> gpt-5.6-luna / max
codex_agent_team_investigator  -> gpt-5.6-terra / xhigh
codex_agent_team_advisor       -> gpt-5.6-sol / high
```

When live role guidance exposes the required project role with the expected locked configuration, record:

```text
route_assurance = profile_locked
```

Role-specific spawns set semantic `agent_type` and `fork_turns` explicitly. The managed profile owns model, reasoning effort, and sandbox intent.

```text
agent_type = codex_agent_team_worker
fork_turns = none
```

`profile_locked` proves configuration assurance only. It does not prove the effective post-spawn route.

## No Portable Mode

The supported policy does not use built-in roles plus ad hoc model/effort overrides as a compatibility route.

If a required project profile cannot be established:

```text
keep responsibility in main session
or repair managed profile readiness
```

Do not silently substitute another role, model, effort, or inherited default.

## Effective Codex precedence

Current Codex documentation defines setting resolution broadly as:

```text
custom Agent file value
  -> explicit spawn value
  -> corresponding [agents] default
  -> parent value
```

Codex Delegate intentionally uses the custom-profile path for exact model-specific routing. It does not rely on omission or inheritance for a required route.

## Route choices remain hypotheses

Luna Max is the current v1 execution baseline. Terra XHigh and Sol High are policy choices to validate on representative workloads; stronger reasoning settings are not assumed globally optimal.

Native slot pressure never changes route identity. If the exact role is unavailable, the dependency waits, remains in the main session, or fails closed according to the task boundary.

Future route tuning should change `policy-contract.json`, matching profile bytes, and benchmark evidence together. Semantic role names and delegation contracts should stay stable.

## Post-spawn evidence

Runtime evidence stays typed by concern:

```text
route_evidence
ancestry_evidence
permission_evidence
```

Exact route proof is two-sided: the expected object must declare complete `agent_role`, `model`, and `effort`, and the accepted observation source must expose all three. Missing expected fields fail closed; missing observed fields remain partial or not observed.

Compatibility grades remain derived summaries:

```text
C1_configuration_only
L1_local_record_observed
R1_runtime_reported
R2_runtime_reported_and_local_record_agree
X0_conflicted
```

The bundled deterministic verifier is `plugins/codex-agent-team/scripts/runtime-evidence.py`. It consumes normalized expected/native/local JSON and does not scrape Codex rollout internals. See the installed Skill reference `references/runtime-assurance.md`.

Native child capacity is a separate runtime observation. A successful fan-out does not prove route identity, and a route observation does not establish a universal capacity ceiling.

## Failure rule

```text
project profile missing -> managed readiness flow
profile exact but current task cannot discover role -> fresh task
profile route provable -> spawn may proceed when dependency is ready and resources allow
profile route unprovable -> main session
runtime-evidence expected route incomplete -> fail closed
post-spawn route partial when runtime proof is required -> main session
post-spawn evidence conflict -> quarantine
runtime slot unavailable -> queue/serialize dependency, do not cross-route
```
