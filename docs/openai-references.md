# OpenAI references used by Codex Agent Team

This page records the OpenAI sources that materially influence the current design. It deliberately separates OpenAI runtime/model facts from Codex Agent Team policy choices.

Last reviewed: 2026-08-02.

## GPT-5.6 model family

### GPT-5.6 launch announcement

https://openai.com/index/gpt-5-6/

Used for the GPT-5.6 family positioning, Codex availability, reasoning-effort support, and published coding-evaluation context.

OpenAI-published coding results are supporting model-family context only. They are not Codex Agent Team benchmarks and do not prove that one route/effort is optimal for this workflow.

### Current OpenAI API pricing

https://developers.openai.com/api/docs/pricing

Pricing is time-sensitive. Use the current pricing page when evaluating workflow economics instead of copying an old price table into routing policy.

Codex Agent Team currently keeps Luna Max as the execution baseline, but price alone never authorizes delegation or model escalation. Route/effort changes require representative workload evidence.

### GPT-5.6 model guidance

https://developers.openai.com/api/docs/guides/latest-model

Used for:

- GPT-5.6 capability-tier positioning;
- supported reasoning-effort choices;
- the recommendation to evaluate reasoning settings on representative workloads instead of assuming the highest effort is always optimal;
- autonomy and approval boundaries for normal local actions versus destructive, external, costly, or scope-expanding actions.

### Individual model pages

- Luna: https://developers.openai.com/api/docs/models/gpt-5.6-luna
- Terra: https://developers.openai.com/api/docs/models/gpt-5.6-terra
- Sol: https://developers.openai.com/api/docs/models/gpt-5.6-sol

Used for model identity, supported reasoning settings, capability descriptions, context/output limits, and tool support. For live pricing, prefer the central pricing page.

## Codex Native Subagent runtime contract

### Official Codex Subagents documentation

https://developers.openai.com/codex/subagents

Used for:

- the distinction between a Subagent and the Agent thread/session where it runs;
- Codex native delegation and custom Agent roles;
- personal/project Agent discovery;
- model and reasoning precedence;
- parent permission behavior;
- why this project is a policy layer over Codex Native Subagents rather than a second Agent runtime.

Codex runtime details are version-sensitive. The live tool contract exposed by the user's current Codex session remains the decisive runtime surface.

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
- why Codex Agent Team uses exact namespaced semantic profiles and fails closed when the required profile cannot be established.

The current architecture has no Portable Mode and no built-in-role substitution path.

### Multi-agent tool surface and observability

https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_spec.rs

Used for:

- native Agent spawn/list/wait/message/interrupt/close lifecycle tools;
- model/reasoning overrides potentially being hidden by runtime configuration;
- the absence of a universal post-spawn effective-model receipt on every runtime surface;
- why configured route facts and observed runtime facts stay separate.

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

## Current Codex Agent Team policy choices

The following are project policy, not claims that OpenAI requires this exact workflow:

- the current user-facing Codex session owns the task-level compute graph and final acceptance;
- no Luna, Terra, or Sol stage is mandatory;
- Luna Max is the current Reader/Worker execution baseline;
- Terra XHigh is a read-only Investigator for one unresolved complex technical delta, not a default reviewer or whole-task retry;
- Sol High is a selective Advisor for high-value judgment/review and may appear directly after Luna;
- writing delegation requires a bounded Delegation Contract with decision rights and an acceptance oracle;
- valid deterministic/repository evidence is reused until its dependencies are invalidated;
- every Agent call must satisfy a distinct unresolved dependency;
- zero children is normal, the normal resource envelope is at most two justified children, and the hard maximum is four;
- one shared workspace has at most one active writing Worker;
- delegation depth remains one;
- exact project-profile routing fails closed without cross-role substitution;
- runtime route, ancestry, and permission evidence are typed separately;
- Terra XHigh and Sol High remain route hypotheses until representative paired live workloads justify them.

These choices must be evaluated against real Codex runtime behavior and representative developer workloads. Static repository tests establish policy/tooling consistency only.
