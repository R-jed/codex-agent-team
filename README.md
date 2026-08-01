# Codex Agent Team

<p align="center">
  <img src="assets/readme/hero.svg" alt="Codex Agent Team" width="100%">
</p>

<p align="center">
  <a href="README_EN.md">English</a> ·
  <a href="docs/architecture.md">Architecture</a> ·
  <a href="docs/native-subagent-runtime.md">Native Runtime</a> ·
  <a href="docs/model-route-assurance.md">Route Assurance</a>
</p>

让 Codex 只在真正值得的时候组建一支小型 Native Subagent 团队。

当前会话始终是 Root。GPT-5.6 Luna Max 负责重执行和探索，GPT-5.6 Terra XHigh 负责独立复核。高后果问题仍有实质分歧时，非 Sol Root 可以在用户明确同意后增加一次 GPT-5.6 Sol High 裁决。

## 什么时候值得用

- 大量源码、日志或测试会挤占当前会话上下文。
- 实现工作可以清楚限定范围，并交给独立 Worker 完成。
- 重要修改需要一个没有参与实现的 Reviewer 再看一遍。
- 复杂任务存在真正可以并行处理的独立分支。

已经定位清楚的小修改通常直接留在 Root。Skill 不会为了展示多 Agent 能力而额外组队。

## 快速开始

需要 Python >= 3.11、Git，以及支持 Native Subagents 的 Codex 环境。

默认安装器会一次完成两件事：安装 Skill，并写入 4 个锁定模型的 Agent profiles 到 `~/.codex/agents/`。

```bash
git clone https://github.com/R-jed/codex-agent-team.git
cd codex-agent-team
python scripts/install.py
```

安装后重新打开 Codex。默认 profiles：`luna_explorer`、`luna_worker`、`terra_reviewer`、`sol_judge`。

只安装 Skill，使用 Portable Mode：

```bash
python scripts/install.py --skill-only
```

显式调用：

```text
$codex-agent-team
```

也可以直接描述任务：

```text
帮我修复这个认证问题，运行相关测试，再独立检查是否影响现有 Session 行为。
```

## 它怎么工作

<p align="center">
  <img src="assets/readme/workflow.svg" alt="Codex Agent Team 工作流程" width="100%">
</p>

Root 先判断委派有没有具体收益。需要执行或探索时交给 Luna，需要独立复核时交给 Terra。所有结果都回到 Root 验证和整合。

模型、权限、范围或外部影响无法安全确认时，任务留在 Root。高影响操作也始终由 Root 控制。

## 角色分工

<p align="center">
  <img src="assets/readme/roles.svg" alt="Codex Agent Team 角色分工" width="100%">
</p>

| 角色 | 默认路由 | 负责什么 |
| --- | --- | --- |
| Root Controller | 当前会话 | 目标、规划、风险、验收、最终回答 |
| Explorer / Worker | GPT-5.6 Luna `max` | 搜索、追踪、实现、调试、测试 |
| Independent Critic | GPT-5.6 Terra `xhigh` | detached review、冲突证据、重大假设检查 |
| Senior Judge | GPT-5.6 Sol `high` | 少量高后果裁决，需要用户授权 |

## 核心规则

- Minimum Team：0 个 Subagent 很正常，默认 1 个，通常最多 2 个。
- Root stays in control：Skill 不会暗中切换当前 Root 的模型或 reasoning effort。
- One Writer：一个共享 Workspace 同时最多 1 个 Writing Worker。
- Depth 1：Worker 不继续创建新的 Subagent 团队。
- Fail closed：精确路由或必要权限无法证明时，任务回到 Root。
- Evidence first：Root 根据文件、命令、测试和可复现证据验收结果。

Codex Agent Team 直接使用 Codex 原生 `spawn_agent`，不会建立第二套 Agent Runtime、持久 Task DAG 或后台调度器。

默认安装推荐使用 model-locked profiles。`--skill-only` 依赖当前 `spawn_agent` 是否支持精确 model / effort 配置。路由细节见 [Model Route Assurance](docs/model-route-assurance.md)。

## 文档

- [Architecture](docs/architecture.md)：控制模型、生命周期与范围边界。
- [Native Subagent Runtime](docs/native-subagent-runtime.md)：`spawn_agent`、Subagent 与 Agent thread。
- [Model Route Assurance](docs/model-route-assurance.md)：Profile Mode、Portable Mode 与 fail-closed 路由。
- [OpenAI References](docs/openai-references.md)：模型、定价、Codex runtime 与设计依据。
- Policy：[Routing](skill/codex-agent-team/references/routing-policy.md) · [Safety](skill/codex-agent-team/references/safety-policy.md) · [Consent](skill/codex-agent-team/references/consent-policy.md)

## 验证状态

仓库包含 policy regression tests 和 routing eval cases。Native runtime 行为仍以当前 Codex build 实际暴露的能力为准。

## License

[MIT](LICENSE)
