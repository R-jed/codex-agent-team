# Codex Agent Team

[English](README_EN.md) · [安装](docs/plugin-installation.md) · [架构](docs/architecture.md) · [评测](docs/behavioral-evals.md)

Codex 原生 Subagent 已经可以把工作拆给其他 Agent。真正容易失控的是委派本身：什么时候该拆，交给谁，谁可以写文件，什么时候需要第二个视角，最后谁对结果负责。

Codex Agent Team 是一套运行在 Codex 原生 `spawn_agent` 之上的工作流规则。当前 Codex 会话作为**主会话**，始终掌握完整任务，负责范围、风险和最终验收；Luna、Terra、Sol 只在条件满足时接手边界明确的局部工作。

## 快速开始

先把项目 marketplace 加到 Codex：

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

重新打开 ChatGPT desktop app，在 Plugins Directory 中安装 `Codex Agent Team`。

需要显式调用时运行：

```text
/codex-agent-team
```

也可以直接描述开发任务。Skill 会先判断是否有必要委派，再决定要不要创建 Subagent。

## 工作方式

| 角色 | 什么时候出现 | 默认路由 | 负责什么 |
| --- | --- | --- | --- |
| 主会话 | 始终存在 | 当前 Codex 会话 | 理解需求、定范围、控制风险、验收、最终回答 |
| Luna | 搜索量大、代码追踪重，或有边界清楚的实现任务 | GPT-5.6 Luna `max` | 探索、实现、调试、测试 |
| Terra | 高风险修改值得增加一个独立视角 | GPT-5.6 Terra `xhigh` | 独立复核修改、冲突证据和关键假设 |
| Sol | 高后果分歧仍未解决，且用户明确授权 | GPT-5.6 Sol `high` | 给出一次高级判断 |

Luna 有 `luna_explorer` 和 `luna_worker` 两个 profile。Terra 使用 `terra_reviewer`，只承担独立复核。Sol 使用 `sol_judge`，不会固定出现在每个任务末尾。

这套工作流没有固定流水线。小任务可以从头到尾都留在主会话；Terra 和 Sol 也只在各自条件满足时加入。

## 看一个实际任务

例如你给 Codex 这样一个任务：

```text
检查支付回调里的并发问题，修好后跑测试。
如果改动触及安全边界，再安排一次独立复核。
```

主会话会先确认影响范围、风险点和验收条件。

1. 如果问题已经定位清楚，主会话直接修改、测试并完成回答。
2. 如果需要大量搜索或代码追踪，主会话可以把这一段工作交给 Luna。
3. 如果修改触及安全边界，Terra 再独立检查这次修改。
4. 无论中间用了几个 Subagent，最终都回到主会话检查实际 diff、测试结果和证据。

Sol 通常不会参与这个流程。只有在高后果判断仍有实质分歧时，主会话才会先向用户请求授权，再增加一次 Sol 判断。

## 0 个 Subagent 也很正常

任务已经很小、上下文清楚、修改位置已经找到时，继续委派通常只会增加上下文切换和验证成本。改一处配置、修一个局部函数、补一个明确测试，都可能直接由主会话完成。

任务长、文件多，或者某个模型成本更低，都不足以单独成为委派理由。Codex Agent Team 的默认目标是使用完成任务所需的最小团队。

## 你会看到什么

实际创建了 Subagent，或者某个关键检查改变了执行路径时，Skill 会附上一小段执行说明：

```text
Agent Team
Luna Worker: implemented bounded auth refresh change
Terra Reviewer: triggered by security boundary; verdict clear
Verification: 38 tests passed
```

主会话直接完成时：

```text
Agent Team: Main session only
Why: change already isolated; delegation had no concrete benefit
Verification: 12 tests passed
```

这段说明只记录已经发生的事。没有创建的 Agent 不会被写进去，没观察到的运行时证据也不会被当成事实。

## 边界

- 0 个 Subagent 是正常结果。默认 1 个，通常最多 2 个，硬上限为 4 个。
- 一个共享 Workspace 同时最多 1 个 Writing Worker。
- Worker 不继续创建新的 Subagent 团队，委派深度保持在 1 层。
- Skill 不会暗中切换主会话的模型或 reasoning effort。
- Luna 无法使用时，不会把 Terra 改成实现 Worker；Terra 无法使用时，由主会话承担复核。
- 精确路由、权限边界或任务范围无法确认时，责任回到主会话。
- Subagent 的完成报告只是声明。主会话仍要根据实际文件、diff、命令、测试和可复现证据验收。

项目直接使用 Codex 原生 `spawn_agent`。仓库里没有第二套 Agent Runtime、持久 Task DAG 或后台调度器。

<details>
<summary>第一次运行为什么会检查 4 个 Agent profiles？</summary>

模型专用 Subagent 通过 4 个 managed custom Agent profiles 固定路由：

```text
luna_explorer
luna_worker
terra_reviewer
sol_judge
```

缺少 profile 时，Skill 会先说明准备写入的范围并请求授权。获得授权后，只安装和校验这 4 个 profiles 及其 ownership manifest。`config.toml`、MCP 配置、凭据和其他 Agent profiles 都不会被改动。

安装后会重新检查当前 `spawn_agent` 能发现哪些 roles。当前 task 还没有刷新 role discovery 时，才需要新建一个 Codex task 再运行 `/codex-agent-team`。

</details>

## 文档

README 只保留日常使用需要知道的内容。实现细节在这里：

- [安装与首次运行](docs/plugin-installation.md)
- [整体架构](docs/architecture.md)
- [Codex 原生 Subagent Runtime](docs/native-subagent-runtime.md)
- [模型路由与证据](docs/model-route-assurance.md)
- [Runtime Evidence](plugins/codex-agent-team/skills/codex-agent-team/references/runtime-assurance.md)
- [兼容性](docs/compatibility.md)
- [Behavioral Evals](docs/behavioral-evals.md)
- [OpenAI References](docs/openai-references.md)
- Policy：[Routing](plugins/codex-agent-team/skills/codex-agent-team/references/routing-policy.md) · [Safety](plugins/codex-agent-team/skills/codex-agent-team/references/safety-policy.md) · [Consent](plugins/codex-agent-team/skills/codex-agent-team/references/consent-policy.md)

## 当前验证范围

CI 覆盖 Plugin packaging、custom-Agent installer lifecycle、routing policy、runtime evidence 和 deterministic verifier，并在 Ubuntu Python 3.11 / 3.12 与 macOS Python 3.11 上运行。

这些测试证明仓库里的规则和工具满足当前契约。真实 Codex 行为仍需要 live behavioral evaluation 和运行时证据，项目不会把静态测试结果当成真实任务表现。

## License

[MIT](LICENSE)
