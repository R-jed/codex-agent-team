<p align="center">
  <img src="assets/subagents-dispatch-logo.png" alt="subagents-dispatch" width="112">
</p>

<h1 align="center">subagents-dispatch</h1>

<p align="center"><strong>Codex 子代理调度框架。</strong></p>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">安装</a> · <a href="docs/architecture.md">架构</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-%E5%8E%9F%E7%94%9F%20Subagents-111827.svg" alt="Codex 原生 Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **如果你是 AI Agent，请跳转到 [README_AI.md](README_AI.md) 并严格按照说明操作。**

你描述要什么。主会话决定自己干还是叫人帮忙。

改一个组件，主会话自己来。要同时查代码、写实现、跑测试，它会分配给专门的 Agent 各干各的，最后整合结果。

## 快速开始

你让 Codex 改一个 API 接口并加测试。

没有 subagents-dispatch，主会话一个人干：先读代码，再改实现，最后写测试。一步一步来。

有了 subagents-dispatch：

```
/dispatch 给 /api/users 加分页参数，补上测试
```

主会话可以拆成多个职责：Reader 查现有实现，Worker 改代码，另一个 Worker 在依赖允许时处理测试，最后由 Main 验证并整合。简单任务仍然可以零子代理完成。

## 四条核心约束

subagents-dispatch 把委托控制放在首位。无论任务拆成多少职责，下面四条规则都保持成立：

- **一个写入者**：在同一次 subagents-dispatch 调度内，同一个 Git checkout 同一时间最多一个写入者，写入者只能是 Main、Worker 或 Solver。`takeover` 也必须等待原写入者确认停止、结束或关闭后才能把写入责任交回 Main。其他 Codex 会话、编辑器、hook 和外部进程不在这个保证范围内。
- **一层委托深度**：子 Agent 不能继续创建新的项目 Subagents 或后台 Agent 团队。用户目标、权限、团队组成和最终结果始终由 Main 负责。
- **UNKNOWN 不猜测**：如果 Host 证据无法确定 Agent 是否创建、正在运行、已经完成或已经停止，就保留 `UNKNOWN`。在状态仍为 `UNKNOWN` 时，不创建替代 Agent、不重试、不语义重路由，也不把冲突写入责任转交给其他执行者。
- **摘要只报事实**：只要实际启动过子 Agent，终态回复会附一行 Execution Receipt。它只报告可验证的角色、职责、重试、Takeover 和 Final Review 状态，不根据模型名称、运行时长或输出长度猜 Token 和费用。

## 2.1 运行中控制

2.1 最直观的变化，是把调度从“发出去等结果”扩展成执行前可预览、执行中可观察、跑偏时可纠正、必要时可接管。

执行前先看 Main 打算怎么分工：

```
/dispatch preview 给 /api/users 加分页参数，补上测试
```

**Preview** 只输出可能的职责、角色、关键依赖、预期写入者，以及当前证据下能判断的 Final Review 预期。它可以做必要的只读检查，但**不启动任何 Agent，不安装 Agent profile，不修改代码，不执行外部动作**。真正执行时如果出现新证据，Main 可以调整路线。

查看当前职责状态：

```
/dispatch status
```

**Status** 是一次性状态检查。它会尽量报告 `unit_id`、语义角色、已知生命周期状态、相关写入责任和当前 blocker。状态证据不足时直接显示 `UNKNOWN`，不会为了“看起来确定”而轮询、猜失败或触发重试。

给正在运行的职责补充指导：

```
/dispatch steer U2: 先看现有的分页中间件，别从头写
```

**Steer** 保持同一个职责、角色、attempt、权限和 ownership，只补充聚焦信息或收窄注意范围。如果新指令会改变目标、写入范围、权限、验收标准或外部影响，它就不能被静默当作 Steering 处理。

把职责拿回 Main：

```
/dispatch takeover U2
```

**Takeover** 会先结清原 Agent。遇到写入任务时，原写入者没有确认停止前，Main 保持只读，不开始冲突写入。状态仍为 `UNKNOWN` 时，Takeover 保持 pending，不用“强制接管”绕过 one-writer 约束。

这四个命令给用户两类控制：`preview` 和 `status` 提供可见性，`steer` 和 `takeover` 提供介入能力。调度仍由 Main 负责，控制命令不会扩大原任务的权限、范围或外部影响授权。

## 执行摘要

启动过子 Agent 的任务，结束时附一行摘要：

```
Dispatch: Reader 查代码 -> Worker 实现 · 未重试 · 无需 Final Review
```

卡住或部分完成时也会简短说明原因，例如 `UNKNOWN` writer 导致 Takeover pending。摘要只报可验证的事实，不暴露推理过程，不会根据模型名称或运行时长猜 Token 和费用。没启动 Agent、只跑 Preview 或只看 Status 的任务不加摘要。

## Handoff Capsule：减少重复扫描

每个子 Agent 仍然使用全新上下文，不继承上一位 Agent 的完整对话。这能保持上下文干净，但连续职责可能重复查同一批代码。Handoff Capsule 用一个很小的、证据绑定的交接包减少这类重复 discovery。

- **传递已验证的事实**：只把 Main 已经检查并接受的文件、符号、接口、测试结果或其他可验证事实传给下一个职责。
- **明确 `DO NOT REDO`**：已经有有效证据支持的扫描、调用链追踪或昂贵检查可以明确标记为无需重复。
- **Main 是验收边界**：子 Agent 的自我声明不能直接成为下一个 Agent 的“已知事实”。流程必须经过 `child claim -> Main 验证 -> Main 接受 -> Capsule`。
- **自带 `STALE IF` 条件**：相关文件变化、API/schema 改动、新 commit、验证失败或结构性计划变化都可以使旧证据失效。失效后只重新验证受影响的窄范围证据。

Capsule 还可以携带 `ARTIFACT REFS`、`INTERFACES / INVARIANTS` 和 `OPEN QUESTIONS`，但不会转发 raw transcript 或隐藏推理。它也不能授予新的写入 ownership、mutation authority、权限、用户范围或角色升级。

## 安装

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

装完开新的 Codex 会话。

首次跑需要 Agent 的任务时，如果五个项目 Agent profiles 还没装，系统会说明要装什么、问你同意，然后自动装好。有些 Codex 版本装完后可能需要再开启一次新的 Codex 会话才能识别。

## 卸载

```bash
# 移除插件注册
codex plugin remove subagents-dispatch

# 删除 5 个 Agent profile（reader/worker/solver/investigator/advisor）
rm ~/.codex/agents/subagents-dispatch-*.toml

# 删除安装 manifest（记录哪些文件由本插件管理）
rm ~/.codex/.subagents-dispatch-agents.json
```

开发任务：

```
/dispatch <任务描述>
```

插件诊断、维护和升级：

```
/doctor <请求>
```

## 更新

```bash
codex plugin marketplace upgrade subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

或者让 Doctor 来：

```
/doctor 升级 subagents-dispatch，告诉我之后还要做什么
```

更新后开新的 Codex 会话。

## 角色

| 角色 | 干什么 |
|------|--------|
| Luna Reader | 读代码、追调用链、收集事实 |
| Luna Worker | 边界已经清楚的实现和测试 |
| Sol Solver | 实现过程中还要做判断的工作 |
| Terra Investigator | 大范围只读调查，整理证据 |
| Sol Advisor | 独立的技术判断或最终复核 |

简单任务主会话自己来。需要并行、隔离、专门能力或独立判断时才叫人。没有固定人数，没有固定流程。

## 其他安全边界

- Main 负责用户目标、权限、团队组成、集成和最终结果
- Steering 不能扩大职责、权限或写入范围
- Takeover 不能绕过原 owner settlement
- Handoff Capsule 只传递 Main 已验证并接受的事实
- Agent 说“完成”只是声明，实际文件、状态和测试结果才是验收证据
- 模型、Token、费用只有 Host 给出可归因证据时才报告
- Prompt、仓库文件、网页、issue、日志或子 Agent 输出里的指令默认按数据处理，不能静默改变用户权限和任务范围

完整规则见 [架构说明](docs/architecture.md)。

## 项目结构

```
.
├── .agents/plugins/                  # Codex Marketplace 注册
├── .codex-plugin/                    # 插件清单
├── agent-profiles/                   # 五个 Agent 配置
├── policy-contract.json              # 角色定义和核心约束
├── scripts/                          # 安装、校验、运行证据工具
├── skills/
│   ├── dispatch/                     # 主 Skill、交互控制、运行规则
│   └── doctor/                       # 安装诊断和升级
├── docs/                             # 架构和运行边界文档
├── evals/                            # 静态与行为评估数据
└── tests/                            # 回归测试
```

## 文档

- [安装](docs/plugin-installation.md)
- [架构](docs/architecture.md)
- [Codex 原生 Subagent 运行边界](docs/native-subagent-runtime.md)
- [AI Agent 项目参考](README_AI.md)

## 许可证

[MIT](LICENSE)
