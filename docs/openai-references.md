# OpenAI references used by Codex Delegate

This page records the OpenAI sources that materially influence the current design. It separates OpenAI runtime, Plugin, Skill, and model facts from Codex Delegate policy choices.

Last reviewed: 2026-08-04.

## Codex Plugin structure and validation

### Official Codex Plugin Creator sample

https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/plugin-creator/SKILL.md

Used for:

- the required `.codex-plugin/plugin.json` Plugin root structure;
- the rule that the outer Plugin folder and manifest `name` match;
- repo/team marketplace structure under `.agents/plugins/marketplace.json` when that distribution target is intentional;
- required marketplace `policy.installation`, `policy.authentication`, and `category` metadata;
- relative marketplace `source.path` such as `./plugins/<plugin-name>`;
- omitting unsupported Plugin-manifest fields;
- validating the Plugin root with the current `plugin-creator` `scripts/validate_plugin.py` before handoff or release.

### Official Plugin manifest and marketplace reference

https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/plugin-creator/references/plugin-json-spec.md

Used for:

- required Plugin metadata and strict semver;
- `https://` requirements for URL metadata when present;
- declaring `apps` or `mcpServers` only when their companion files exist;
- keeping unsupported fields such as `hooks` out of `plugin.json`;
- repository marketplace policy and nested Plugin source-path shape.

### Official Plugin update/reinstall reference

https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/plugin-creator/references/installing-and-updating.md

Used for:

- installing/reinstalling a Plugin with `codex plugin add <plugin>@<marketplace>`;
- using CLI marketplace operations instead of hand-editing marketplace/config state during install/update flows;
- starting a new thread after reinstall so updated skills/tools are picked up;
- using the official cachebuster helper for local-development iteration when that flow applies.

Codex Delegate uses a repository Git marketplace rather than the default personal marketplace. Release validation therefore tests the configured Git marketplace path and installed Plugin id explicitly.

## Codex Native Subagent runtime contract

### Official Codex Subagents documentation

https://developers.openai.com/codex/subagents

Used for:

- the distinction between a Subagent and the Agent thread/session where it runs;
- Codex native delegation and custom Agent roles;
- personal custom-Agent discovery from `$CODEX_HOME/agents` (normally `~/.codex/agents`);
- project custom-Agent discovery from `.codex/agents`;
- required custom-Agent fields such as `name`, `description`, and `developer_instructions`;
- optional model, reasoning-effort, and sandbox configuration;
- model/reasoning precedence and runtime-owned effective behavior;
- native concurrency configuration such as `max_concurrent_threads_per_session` being a runtime setting rather than a Codex Delegate product constant;
- the explicit recommendation that independent read-heavy work can run in parallel and may save time;
- the current public orchestration description that Codex waits until all requested results are available before returning a consolidated multi-agent response.

The last two points must be kept separate. Native Codex supports parallel child execution, but the public documentation's consolidated wait model does not by itself prove that a tested client/runtime exposes per-child completion events suitable for completion-driven frontier refill. That behavior remains a live runtime fact.

Codex runtime details are version-sensitive. The live tool contract exposed by the user's current Codex session remains the decisive runtime surface.

Codex Delegate does not claim that Plugin installation natively installs custom Agent roles. The Plugin distributes the Skill and bundled project files. The managed profile installer is a user-approved post-install provisioning step that writes the four exact semantic profiles into the official personal custom-Agent configuration location.

### Public Codex issue telemetry: wait/polling overhead

https://github.com/openai/codex/issues/35259

This is **public user-reported telemetry in the OpenAI Codex repository, not an OpenAI runtime guarantee or benchmark**.

The report describes repeated model turns whose only action was agent/process wait or status polling. In one corrected full usage window, the reporter attributes 19.8% of raw local token volume to wait/status-only turns and argues that waiting should be event-driven or harness-managed so unchanged state does not trigger another model call.

Codex Delegate uses this only as evidence that coordination overhead and model-mediated polling are real risks worth measuring. It does not copy the reported percentage into product claims and does not assume the same behavior exists in every Codex build/client.

### Public Codex issue telemetry: child close/lifecycle blocking

https://github.com/openai/codex/issues/24389

This is also **version-scoped user-reported issue evidence**. The report describes a `multi_agent_v1.close_agent` call blocking a parent thread for roughly eight hours on an unresponsive child.

Codex Delegate uses this as a reason to test child close/slot-recovery behavior explicitly instead of assuming lifecycle operations are instantaneous or harmless. It is not evidence that current supported runtimes still have the same defect.

### MultiAgentV2 spawn handler

https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs

Used for:

- `spawn_agent` V2 arguments such as `agent_type`, model/reasoning overrides, and `fork_turns`;
- `fork_turns` semantics;
- child thread/session creation and parent/depth metadata;
- why project role-specific spawns set `fork_turns` explicitly.

### Native model/effort validation and runtime-owned child state

https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_common.rs

Used for:

- validation of explicit model/reasoning requests against the active backend;
- configured defaults affecting omitted values;
- runtime-owned permission/approval state being reapplied to children;
- why configured profile sandbox intent is not proof of effective host-enforced permissions.

### Agent roles, profile locks, and precedence

https://github.com/openai/codex/blob/main/codex-rs/core/src/config/agent_roles.rs

https://github.com/openai/codex/blob/main/codex-rs/core/src/agent/role.rs

https://github.com/openai/codex/blob/main/codex-rs/core/src/agent/role_tests.rs

Used for:

- discovery of custom Agent files;
- role-file configuration and precedence;
- role-level model/reasoning locks;
- live role guidance exposing locked settings;
- why Codex Delegate uses exact namespaced semantic profiles and fails closed when the required profile cannot be established.

The current architecture has no Portable Mode and no built-in-role substitution path.

### Multi-agent tool surface and observability

https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_spec.rs

Used for:

- native Agent spawn/list/wait/message/interrupt/close lifecycle tools;
- model/reasoning overrides potentially being hidden by runtime configuration;
- the absence of a universal post-spawn effective-model receipt on every runtime surface;
- why configured route facts and observed runtime facts stay separate;
- why child-progress observability and completion/wait semantics must be characterized on the tested runtime rather than assumed from orchestration policy.

### Agent thread creation

https://github.com/openai/codex/blob/main/codex-rs/core/src/agent/control/spawn.rs

Used for:

- spawned children receiving their own native thread identities;
- native parent/child structure;
- why a child thread is the runtime container for the Subagent rather than a second user-facing App Thread created by this project.

## Codex Skill structure

### OpenAI Skill Creator sample

https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md

Used for:

- `SKILL.md` as the installable entry point;
- concise YAML frontmatter;
- progressive disclosure;
- moving detailed policy into `references/`;
- keeping repository/community documentation outside the installed Skill body.

### `agents/openai.yaml` reference

https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/references/openai_yaml.md

Used for `display_name`, `short_description`, `default_prompt`, and implicit invocation policy.

## GPT-5.6 model family

### GPT-5.6 launch announcement

https://openai.com/index/gpt-5-6/

Used for GPT-5.6 family positioning, Codex availability, reasoning-effort support, and published coding-evaluation context.

OpenAI-published coding results are supporting model-family context only. They are not Codex Delegate benchmarks and do not prove that one route/effort is optimal for this workflow.

### Current OpenAI API pricing

https://developers.openai.com/api/docs/pricing

Pricing is time-sensitive. Use the current pricing page when evaluating workflow economics instead of copying an old price table into routing policy.

Codex Delegate currently keeps Luna Max as the execution baseline, but price alone never authorizes delegation or model escalation. Route/effort changes require representative workload evidence.

### GPT-5.6 model guidance

https://developers.openai.com/api/docs/guides/latest-model

Used for:

- GPT-5.6 capability-tier positioning;
- supported reasoning-effort choices;
- evaluating reasoning settings on representative workloads instead of assuming the highest effort is always optimal;
- autonomy and approval boundaries for normal local actions versus destructive, external, costly, or scope-expanding actions.

### Individual model pages

- Luna: https://developers.openai.com/api/docs/models/gpt-5.6-luna
- Terra: https://developers.openai.com/api/docs/models/gpt-5.6-terra
- Sol: https://developers.openai.com/api/docs/models/gpt-5.6-sol

Used for model identity, supported reasoning settings, capability descriptions, context/output limits, and tool support. For live pricing, prefer the central pricing page.

## Current Codex Delegate policy choices

The following are project policy, not claims that OpenAI requires this exact workflow:

- the current user-facing Codex session owns the task-level compute graph and final acceptance;
- no Luna, Terra, or Sol stage is mandatory;
- Luna Max is the current Reader/Worker execution baseline;
- Terra XHigh is a read-only Investigator for one unresolved complex technical delta, not a default reviewer or whole-task retry;
- Sol High is a selective Advisor for high-value judgment/review and may appear directly after Luna;
- writing delegation requires a bounded Delegation Contract with decision rights and an acceptance oracle;
- valid deterministic/repository evidence is reused until its dependencies are invalidated;
- every Agent call must satisfy a distinct unresolved dependency;
- zero children is normal; up to two concurrently active justified children is the normal no-extra-consent envelope, not a scheduler target or lifetime cap;
- Codex Delegate defines no product-level hard child ceiling; actual parallelism is limited by ready dependencies, consent, workspace safety, exact routes, and native runtime capacity;
- completion-driven ready-frontier refill is the desired scheduling policy when the tested runtime exposes useful individual child completion/update events;
- a real join dependency or coarser native wait surface may require barrier waiting, and that limitation must be recorded rather than hidden;
- model-mediated polling is coordination overhead to measure and minimize, not productive task progress;
- acceptance failure and need for intervention are separate facts;
- recovery uses a bounded Recovery Ledger, event-driven evaluation, and evidence rather than fixed retry/stall thresholds;
- one shared workspace has at most one active writing Worker;
- delegation depth remains one;
- exact project-profile routing fails closed without cross-role substitution;
- runtime route, ancestry, permission, capacity, completion/wait semantics, and child-progress observability remain runtime facts that must be measured where material;
- Terra XHigh and Sol High remain route hypotheses until representative paired live workloads justify them.

These choices must be evaluated against real Codex runtime behavior and representative developer workloads. Static repository tests establish policy/tooling consistency only.
