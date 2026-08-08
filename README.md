<p align="center">
  <img src="assets/subagents-dispatch-logo.png" alt="subagents-dispatch" width="112">
</p>

<h1 align="center">subagents-dispatch</h1>

<p align="center"><em>一个指令，多人并行，结果可控。</em></p>

<p align="center">
  <a href="README_EN.md">英文</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">安装</a> · <a href="docs/architecture.md">架构</a> · <a href="LICENSE">MIT</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.1-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-%E5%8E%9F%E7%94%9F%20Subagents-111827.svg" alt="Codex 原生 Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

---

> **如果你是 AI Agent，请跳转到 [README_AI.md](README_AI.md) 并严格按照说明操作。**

## 快速开始

比如你让 Codex 给一个 API 加分页，并把测试补上。

没有 subagents-dispatch 时，主会话通常要自己一步步做完：先读代码，再改实现，最后写测试。

有了 subagents-dispatch，只要这样说：

```
/dispatch 给 /api/users 加分页参数，补上测试
```

主会话会判断哪些工作适合分开做。比如让 Reader 先查清现有代码，让 Worker 负责修改，再让另一个 Worker 补测试。能并行的工作会同时推进，最后仍由主会话负责检查、整合和给出最终结果。

简单任务不会为了“多人协作”硬拆。只有确实能更快、更稳或更适合分工时，才会启动子 Agent。

## 运行中控制

想先看看准备怎么分工，不真正启动 Agent：

```
/dispatch preview 给 /api/users 加分页参数，补上测试
```

任务已经在跑，想看看现在做到哪一步：

```
/dispatch status
```

想给正在工作的 Agent 补一句新要求：

```
/dispatch steer U2: 先看现有的分页中间件
```

想停止某个职责，改由主会话接手：

```
/dispatch takeover U2
```

## 执行摘要：最后告诉你刚才做了什么

只要这次任务真的启动过子 Agent，结束时会多一行简单说明，例如：

```
Dispatch: Reader 查代码 -> Worker 实现 · 未重试 · 无需最终复核
```

这行摘要只写系统能确认的事实，比如用了哪些角色、有没有重试、有没有做最终复核。它不会把 Agent 的内部思考过程写出来，也不会根据模型名称或运行时长猜 Token 用量和费用。

## 交接包（Handoff Capsule）：避免后一个 Agent 从头再查一遍

每个子 Agent 都从一份新的上下文开始。如果什么都不传，后一个 Agent 很可能又把前一个 Agent 已经查清的内容重新检查一遍。

Handoff Capsule 就是一份很小的“交接便签”。主会话会把已经核实过、后面还能继续用的信息整理进去，再交给下一个职责。

- **已经确认的事实可以直接接着用**：只有主会话检查并接受过的内容，才会放进交接包
- **`DO NOT REDO` 表示“这部分不用重做”**：已经有可靠证据的检查，可以明确告诉下一个 Agent 不要重复
- **主会话负责把关**：子 Agent 自己说“我完成了”还不够，主会话要检查证据后才会把它当成已知事实
- **`STALE IF` 表示“出现这些变化后，旧结论要作废”**：比如相关文件后来被改了，就需要重新检查

你不需要记住 `DO NOT REDO` 和 `STALE IF` 这些英文标签。它们只是系统内部用来减少重复工作的标记。

## 四条必须守住的规则

系统可以并行干活，但不会为了并行把安全规则丢掉。核心就是下面四条：

- **同一份代码，同一时间只让一个写入者修改**：同一次 subagents-dispatch 调度里，同一个 Git 工作目录同一时间最多只有一个写入者真正改文件，这个写入者只能是主会话、Worker 或 Solver。前一个写入者还没有确认停止，主会话不会抢着改同一份代码。其他独立的 Codex 会话、编辑器、自动化脚本和外部程序不受这个规则控制
- **子 Agent 不能继续叫更多子 Agent**：所有分工都只由主会话安排。用户的目标、权限、团队组成和最终结果始终由主会话负责
- **`UNKNOWN` 就停下来确认，不靠猜**：`UNKNOWN` 表示系统现在无法确认某个职责的真实状态。遇到这种情况，不会随便换一个 Agent 顶上，不会自动重试，也不会偷偷改变任务路线
- **只报告确认过的事实**：执行摘要不会根据模型名称、运行时间或输出长度去猜 Token 用量和费用

## 角色

| 角色 | 干什么 |
|------|--------|
| Luna Reader | 读代码、追调用链、收集事实 |
| Luna Worker | 需求和做法已经清楚时，负责实现和测试 |
| Sol Solver | 一边实现、一边还需要做技术判断的工作 |
| Terra Investigator | 范围较大的只读调查和证据整理 |
| Sol Advisor | 独立技术判断，或需要时做最终复核 |

简单任务由主会话自己完成。需要并行、隔离、专门能力或独立判断时才会叫不同角色来帮忙。没有固定人数，也没有固定流水线。

## 安装

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

插件装好后，先开一个新的 Codex 会话。

第一次 `/dispatch` 真正需要子 Agent 时，subagents-dispatch 会自动准备自己的 5 个 Agent 配置文件。你不需要理解 TOML，也不用为这些内部配置多点一次确认。

Codex 会在任务启动时读取可用的 Agent 列表，所以刚刚新建的配置不能在当前任务里立刻生效。第一次准备完成后，系统会请你新开一个任务，再运行刚才那条 `/dispatch`。当前任务不会先做一次明知道看不到新 Agent 的失败尝试。以后这些配置已经提前存在，正常任务就可以直接委托。

如果发现同名文件有冲突、文件被改过、无法确认文件归谁管理，或者路径本身不安全，系统不会直接覆盖，而会停止并让 `/doctor` 告诉你该怎么处理。

## 卸载

```bash
# 移除插件注册
codex plugin remove subagents-dispatch@subagents-dispatch

# 移除插件市场注册和缓存
codex plugin marketplace remove subagents-dispatch
```

如果之前运行过需要 Agent 的任务，还需要删除相关文件：

```bash
# 删除 5 个 Agent 配置文件
rm ~/.codex/agents/subagents-dispatch-reader.toml
rm ~/.codex/agents/subagents-dispatch-worker.toml
rm ~/.codex/agents/subagents-dispatch-solver.toml
rm ~/.codex/agents/subagents-dispatch-investigator.toml
rm ~/.codex/agents/subagents-dispatch-advisor.toml

# 删除安装记录文件
rm ~/.codex/.subagents-dispatch-agents.json
```

## 更新

```bash
codex plugin marketplace upgrade subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

也可以让 Doctor 帮你升级：

```
/doctor 升级 subagents-dispatch
```

更新后开一个新的 Codex 会话。

## 项目结构

```
.
├── .agents/plugins/                  # Codex 插件市场注册
├── .codex-plugin/                    # 插件清单
├── agent-profiles/                   # 五个 Agent 配置文件
├── policy-contract.json              # 角色定义和核心规则
├── scripts/                          # 安装、检查和运行记录工具
├── skills/
│   ├── dispatch/                     # 主调度功能、运行中控制和运行规则
│   └── doctor/                       # 安装诊断和升级
├── docs/                             # 架构和运行边界文档
├── evals/                            # 评估用例
└── tests/                            # 回归测试
```

## 文档

- [安装说明](docs/plugin-installation.md)
- [架构说明](docs/architecture.md)
- [Codex 原生 Subagent 运行边界](docs/native-subagent-runtime.md)
- [AI Agent 项目参考](README_AI.md)

## 许可证

[MIT](LICENSE)
