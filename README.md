# Codex Agent Team

[English](README_EN.md) · [安装](docs/plugin-installation.md) · [架构](docs/architecture.md) · [评测](docs/behavioral-evals.md) · [本地真测交接](HEADOFF.md)

Codex 已经能创建 Subagent。日常开发真正难的是调度：哪些工作值得交出去，交出去之前要说明到什么程度，前一个 Agent 已经查清的东西要不要重算，什么时候需要更强的模型，最后由谁验收。

Codex Agent Team 把这些问题收进一套工作流。当前 Codex 会话始终是**主会话**，负责理解需求、划定边界、安排计算、维护有效证据和最终验收。Luna、Terra、Sol 是按未解决依赖调用的计算资源，没有固定出场顺序。

## 快速开始

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

重新打开 ChatGPT Desktop，在 Plugins Directory 中安装 `Codex Agent Team`。

需要显式调用时：

```text
/codex-agent-team
```

## 当前状态

仓库已经完成当前架构周期的静态收口。静态测试覆盖 Plugin packaging、managed Agent profile lifecycle、Delegation Contract、调度 policy、Runtime Truth 和 paired behavioral eval tooling。

当前远端分支审计共发现 11 个分支。`main` 之外的 10 个分支全部对应已经合并的历史 PR，没有任何分支需要再次合并。它们只剩远端 ref 清理，具体命令写在 [`HEADOFF.md`](HEADOFF.md)。

下一阶段固定为**本地真实运行验证**。静态 CI 无法证明真实 Codex runtime 的角色发现、模型路由、sandbox、parent thread、Agent lifecycle、证据复用、成本或质量表现。接手本地测试前请先完整执行 `HEADOFF.md`，不要先重构当前 orchestration model。

## 这套工作流怎么分工

| 层 | 当前路由 | 主要用途 |
| --- | --- | --- |
| 主会话 | 当前 Codex 会话 | 理解任务、定范围、做关键决策、调度、验收 |
| Luna Reader | GPT-5.6 Luna `max` | 搜索、追踪、测试映射、证据收集 |
| Luna Worker | GPT-5.6 Luna `max` | 边界明确的实现、调试、测试、局部重构 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | 只处理尚未解决的复杂技术依赖 |
| Sol Advisor | GPT-5.6 Sol `high` | 高价值判断和选择性复核 |

模型没有固定流水线。常见路径可以很短：

```text
主会话
主会话 -> Luna -> 主会话
主会话 -> Luna -> Sol -> 主会话
主会话 -> Luna -> Terra（只处理未决问题）-> Luna / 主会话
```

`Luna -> Terra -> Sol` 从来不要求完整走完。

## 先把任务变成可委派的合同

写文件的任务不会把一段模糊需求直接丢给 Worker。主会话会先明确：

```text
OUTCOME          最后要得到什么
SCOPE            可以读什么、改什么
INVARIANTS       哪些行为不能改变
DECISION RIGHTS  Worker 可以自己决定什么
ACCEPTANCE       怎样才算完成
VERIFICATION     用什么命令或证据验证
STOP / ESCALATE  什么情况必须停下来交回主会话
```

验收标准或决策权限说不清时，不创建 Writing Worker。

主会话负责 `WHAT / WHY / SCOPE / RISK / ACCEPTANCE`，Luna 在合同内解决 `HOW TO EXECUTE`。

## 已经算过的东西尽量不再算一遍

主会话维护一份精简的 Shared Evidence State。它保存已经确认的测试结果、文件关系、调用路径、接口事实和其他可复用证据，并记录这些证据依赖哪些文件或产物。

后续 Agent 默认复用仍然有效的证据。只有依赖变化、证据冲突，或者当前问题确实需要重新验证时才重算。

模型判断和事实证据分开处理。一个 Agent 的推测可以被后续模型挑战，不会因为重复出现就自动成为事实。

## Luna 做不好时，先分类失败

```text
机械错误 -> Luna 定点修正
合同缺口 -> 主会话补齐合同，再继续受影响的部分
能力缺口 -> Terra 只接收尚未解决的技术问题
判断缺口 -> 主会话决定，或在确有价值时交给 Sol
```

Terra 默认是 read-only 的复杂问题调查层。它会收到已经确认的证据、当前 artifact、未决问题和明确的 `DO NOT REDO` 项，不会因为 Luna 输出质量一般就重新扫描整个仓库或把实现从头做一遍。

Terra 解决技术依赖后，具体实现通常再回到 Luna 或主会话。

## Luna + Sol 是一条正常的短路径

有些任务实现标准很明确，Luna 完成后只需要一次更高价值的判断或复核。这时可以直接：

```text
主会话
-> Luna Max 实现
-> Sol 检查实际 diff 和证据
-> 主会话验收
```

Terra 不需要为了补齐三级结构加入。

如果 deterministic oracle 已经足够强，也可能只有：

```text
主会话 -> Luna -> 主会话
```

甚至 0 个 Subagent。

## 并行只解决独立依赖

适合并行的例子包括两个互不依赖的 read-only 调查，或者 Luna 实现时主会话提前准备验收清单和风险检查。

让 Luna、Terra、Sol 同时分析同一个问题，只会重复消耗上下文和推理算力。每次 Agent 调用都必须增加一项已有结果无法替代的价值。

## 你会看到什么

实际创建 Subagent，或者调度决策明显改变执行路径时，Skill 会附上一段简短说明：

```text
Agent Team
Luna Worker: implemented the bounded retry fix
Sol Advisor: reviewed the final diff because payment-state semantics were high consequence
Reused evidence: E03 reproduction, E07 caller trace, E11 baseline tests
Verification: 38 tests passed
```

主会话直接完成时：

```text
Agent Team: Main session only
Why: the change was already isolated and delegation added no useful dependency
Verification: 12 tests passed
```

## 边界

- 0 个 Subagent 是正常结果，默认 1 个，通常最多 2 个，硬上限 4 个。
- 一个共享 Workspace 同时最多 1 个 Writing Worker。
- 子 Agent 不继续创建新的 Subagent，委派深度保持 1 层。
- Skill 不会暗中切换主会话模型或 reasoning effort。
- 缺少精确 project profile 时，责任留在主会话，不跨角色替换。
- Runtime route proof 要求 expected route 和 observed route 都完整包含 role、model、effort；缺字段时 fail closed。
- Subagent 的完成报告只是声明，最终验收看实际文件、diff、命令、测试和可复现证据。

项目直接使用 Codex 原生 `spawn_agent`，没有第二套 Agent Runtime、持久 Task DAG 或后台调度器。

<details>
<summary>第一次运行会检查哪些 Agent profiles？</summary>

```text
codex_agent_team_reader
codex_agent_team_worker
codex_agent_team_investigator
codex_agent_team_advisor
```

缺少 profile 时，Skill 会先说明完整的项目管理文件范围并请求授权。Installer 只管理这 4 个当前 profiles 和 ownership manifest。旧版本的 model-named profiles 只有在当前文件字节能够由上一轮项目 ownership manifest 精确证明时才会清理。用户修改过、无法证明归属，或者在迁移完成后重新创建的 legacy 文件不会因为陈旧 manifest 被再次删除。

</details>

## 接下来验证什么

[`HEADOFF.md`](HEADOFF.md) 是本地 Codex 接手的唯一测试合同，重点分为四组：

- Plugin 安装、profile consent、真实 route / sandbox / ancestry 和 Runtime Truth；
- Contractability、Shared Evidence、Luna 失败分类、Terra delta 和 selective Sol；
- raw prompt 对 compiled contract 的 paired A/B，以及 useful parallelism 和 Agent lifecycle 压力；
- installer fault injection、远端历史分支清理和最终 release gate。

Luna Max 目前是执行 baseline。Terra XHigh 和 Sol High 仍属于需要真实 workload 证明的 route hypotheses。没有真实数据前，不发布成本、延迟或质量提升结论。

## 文档

- [本地真实运行交接](HEADOFF.md)
- [安装与首次运行](docs/plugin-installation.md)
- [整体架构](docs/architecture.md)
- [Codex 原生 Subagent Runtime](docs/native-subagent-runtime.md)
- [模型路由与证据](docs/model-route-assurance.md)
- [Delegation Contract](plugins/codex-agent-team/skills/codex-agent-team/references/delegation-contract.md)
- [Runtime Evidence](plugins/codex-agent-team/skills/codex-agent-team/references/runtime-assurance.md)
- [Behavioral Evals](docs/behavioral-evals.md)
- [OpenAI References](docs/openai-references.md)

## License

[MIT](LICENSE)
