# Codex Agent Team

<p align="center">
  <img src="assets/readme/hero-zh.svg" alt="Codex Agent Team：只在真正值得时组建子代理团队" width="100%">
</p>

<p align="center">
  <a href="README_EN.md">English</a> ·
  <a href="docs/plugin-installation.md">安装</a> ·
  <a href="docs/architecture.md">架构</a> ·
  <a href="docs/model-route-assurance.md">路由与证据</a>
</p>

**让 Codex 只在真正值得时组队。**

你继续在一个主会话里开发。小而清楚的任务由主会话直接完成；需要大量搜索、边界明确的实现或独立复核时，再把合适的部分交给 Luna、Terra 或 Sol。你不需要先规划要开几个 Agent，也不需要为每个任务手动拼一条工作流。

> 「主会话」就是你当前正在使用的 Codex 会话。架构文档内部称它为 `Root Controller`；这份 README 后文统一使用更直观的「主会话」。

## 30 秒开始

Codex Plugin 是唯一支持的安装方式。先注册这个仓库提供的 marketplace：

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

重新打开 ChatGPT desktop app，在 Plugins Directory 中选择 `Codex Agent Team` marketplace 并安装插件。之后只需要记住一个入口：

```text
/codex-agent-team
```

也可以直接描述开发任务，Skill 会自行判断有没有必要创建子代理（Subagent）。

```text
帮我修复这个认证问题，运行相关测试，再判断是否值得做一次独立复核。
```

<details>
<summary>第一次运行会发生什么？</summary>

插件第一次需要模型专用子代理时，会检查这 4 个 managed custom Agent profiles：

```text
luna_explorer
luna_worker
terra_reviewer
sol_judge
```

如果缺失，Skill 会先说明写入范围并请求授权。获得授权后，它只安装并校验这 4 个 profiles 及其 ownership manifest，不修改 `config.toml`、MCP 配置、凭据或其他 Agent profiles。

安装完成后会重新检查当前 native `spawn_agent` role surface。当前 task 已经能发现新 roles 时直接继续；仍未刷新时，才会提示新建一个 Codex task 后再次运行 `/codex-agent-team`。

</details>

## 它怎么决定要不要组队

<p align="center">
  <img src="assets/readme/workflow-zh.svg" alt="Codex Agent Team 的任务分流逻辑" width="100%">
</p>

| 任务情况 | 默认处理 |
| --- | --- |
| 小而明确，主会话已经掌握上下文 | 主会话直接完成 |
| 搜索量大、上下文很重，或实现边界清楚 | Luna 负责探索、实现、调试与测试 |
| 修改风险高，独立视角能明显提高置信度 | Terra 做一次 detached review |
| 高后果分歧仍未解决 | 先征得用户授权，再让 Sol 做一次裁决 |

0 个子代理是正常结果。Codex Agent Team 的目标是用最小团队完成任务，不为了「多 Agent」本身增加流程。

## 谁负责什么

<p align="center">
  <img src="assets/readme/roles-zh.svg" alt="Codex Agent Team 的主会话、Luna、Terra 与 Sol 分工" width="100%">
</p>

| 角色 | 默认路由 | 负责什么 |
| --- | --- | --- |
| 主会话 | 当前 Codex 会话 | 理解需求、规划、控制范围与风险、验收结果、最终回答 |
| Luna 执行者 | GPT-5.6 Luna `max` | 搜索、代码追踪、有边界实现、调试、测试 |
| Terra 复核者 | GPT-5.6 Terra `xhigh` | 独立检查高风险修改、冲突证据和关键假设 |
| Sol 裁决者 | GPT-5.6 Sol `high` | 处理少量仍有争议的高后果判断，需要用户授权 |

Luna 是日常执行路线。Terra 只在独立复核有实际价值时加入。Sol 不承担常规实现，也不充当每个任务的固定终审。

## 你会看到什么

只要显式调用 `/codex-agent-team`、实际创建了子代理，或关键 gate 改变了执行路径，Skill 会给出一条简短 receipt。它告诉你发生了什么，不把内部编排过程铺满对话。

```text
Agent Team
Luna Worker: implemented bounded auth refresh change
Terra Reviewer: triggered by security boundary; verdict clear
Verification: 38 tests passed
```

如果主会话自己完成更合适：

```text
Agent Team: Main session only
Why: change already isolated; delegation had no concrete benefit
Verification: 12 tests passed
```

## 这套工作流守住什么

- **Minimum Team**：0 个子代理很正常，默认 1 个，通常最多 2 个。
- **主会话掌控最终结果**：Skill 不会暗中切换主会话的模型或 reasoning effort；模型、权限或范围无法确认时，任务留在主会话。
- **单写入者、单层委派**：一个共享 Workspace 同时最多 1 个 Writing Worker；Worker 不继续创建新的 Subagent 团队。
- **证据优先**：Worker 的报告只是声明。主会话根据实际文件、diff、命令、测试和可复现证据验收结果。

Codex Agent Team 直接使用 Codex 原生 `spawn_agent`。它不会建立第二套 Agent Runtime、持久 Task DAG 或后台调度器，也不会把每个任务都强制送去独立 review。

## 深入文档

README 只保留日常使用需要知道的内容。实现与证据语义放在下面这些文档中：

- [Plugin Installation](docs/plugin-installation.md)
- [Architecture](docs/architecture.md)
- [Native Subagent Runtime](docs/native-subagent-runtime.md)
- [Model Route Assurance](docs/model-route-assurance.md)
- [Runtime Evidence](plugins/codex-agent-team/skills/codex-agent-team/references/runtime-assurance.md)
- [Compatibility](docs/compatibility.md)
- [Behavioral Evals](docs/behavioral-evals.md)
- [OpenAI References](docs/openai-references.md)
- Policy：[Routing](plugins/codex-agent-team/skills/codex-agent-team/references/routing-policy.md) · [Safety](plugins/codex-agent-team/skills/codex-agent-team/references/safety-policy.md) · [Consent](plugins/codex-agent-team/skills/codex-agent-team/references/consent-policy.md)

## 验证状态

CI 覆盖 Plugin packaging、custom-Agent installer lifecycle、routing policy、runtime evidence 与 deterministic verifier，并在 Ubuntu Python 3.11 / 3.12 和 macOS Python 3.11 上运行。静态测试只能证明仓库契约，真实 Codex 行为仍以 live behavioral evaluation 和 runtime evidence 为准。

## License

[MIT](LICENSE)
