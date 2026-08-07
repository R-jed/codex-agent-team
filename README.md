<p align="center">
  <img src="assets/subagents-dispatch-logo.svg#gh-light-mode-only" alt="subagents-dispatch" width="112">
  <img src="assets/subagents-dispatch-logo-dark.svg#gh-dark-mode-only" alt="subagents-dispatch" width="112">
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

> **If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly.**

你给目标，主会话负责判断哪些工作自己完成，哪些值得交给原生 Subagent，并负责最终整合和验证。

2.1 增加了四个面向日常使用的能力：执行前预览、运行中查看与控制、完成后的极简执行摘要，以及经过验证的上下文交接。

## 快速开始

直接执行任务：

```text
/dispatch 实现用户列表页面，支持分页和搜索
```

想先看它准备怎么分工，再决定是否执行：

```text
/dispatch preview 实现用户列表页面，支持分页和搜索
```

Preview 只给出可能的职责、依赖和写入安排。它不会启动子 Agent、安装 Agent 配置、修改源码或执行外部操作。

## 运行中控制

查看当前委派状态：

```text
/dispatch status
```

给某个正在运行的职责补充明确指导：

```text
/dispatch steer U2: 先看 crash log，别重复扫描已经确认过的调用链
```

把某个职责安全地收回主会话：

```text
/dispatch takeover U2
```

Takeover 会先处理原来的 Agent 所有权。遇到写入任务时，原写入者没有确认停止前，主会话不会开始冲突写入。运行状态无法确认时会保留 `UNKNOWN`，不会为了继续执行而猜测状态。

## 执行摘要

只要本次任务确实启动过子 Agent，本轮终态回复都会附上一行简短的 Dispatch 摘要。任务正常完成、部分完成或因阻塞停止时都适用，例如：

```text
Dispatch: Reader evidence -> Worker implementation · no retry · Final Review not required
```

遇到阻塞时也可以用同样简短的方式报告 blocker，并在运行状态无法确认时原样保留 `UNKNOWN`。

摘要只展示可以验证的调度事实，不展示隐藏推理、原始子 Agent 对话，也不会根据模型名称或运行时长猜 Token 和费用。

没有启动子 Agent、只做 Preview、只查 Status 时不会额外显示摘要。

## 减少重复扫描

连续职责之间可以使用 Handoff Capsule 传递已经由主会话确认过的事实、证据、接口约束和 `DO NOT REDO` 信息。

子 Agent 仍然使用新鲜上下文。系统不会把上一位 Agent 的整段对话直接塞给下一位，也不会把未经验证的 Agent 结论当成既定事实。相关文件发生变化后，依赖旧状态的交接信息需要重新验证。

## 安装

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

安装后开启新的 Codex 会话。

开发任务使用：

```text
/dispatch <你的任务描述>
```

诊断和维护使用：

```text
/doctor <诊断或维护请求>
```

Doctor 默认只读。也可以输入 `/skills` 打开 Skill 选择器。Dispatch 保持显式调用，不会在普通任务里自行介入。

## 更新

```bash
codex plugin marketplace upgrade subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

也可以让 Doctor 执行升级：

```text
/doctor 升级 subagents-dispatch，并告诉我升级后还需要做什么。
```

更新后开启新的 Codex 会话。

## 工作原理

主会话是技术负责人，按实际能力需求分配职责：

| 角色 | 干什么 |
|------|--------|
| Luna Reader | 读代码、追调用链、收集事实 |
| Luna Worker | 完成边界已经明确的实现和测试 |
| Sol Solver | 处理实现过程中仍需要重要技术判断的工作 |
| Terra Investigator | 大范围只读技术调查和证据整理 |
| Sol Advisor | 重要技术判断或独立最终复核 |

简单任务可以全部留在主会话。需要并行、隔离、专业能力或独立判断时才启动子 Agent。项目没有固定 Agent 数量，也没有固定 Luna → Terra → Sol 流程。

## 安全规则

- 主会话负责用户目标、权限、团队组成和最终结果
- 子 Agent 不能创建自己的项目团队
- 同一个 Git checkout 同一时间最多一个写入者
- Steering 不能偷偷扩大职责、写入权限或用户范围
- Takeover 必须先结清原所有者，`UNKNOWN` 不会被当成可安全抢占
- Handoff Capsule 只能传播主会话已经验证接受的事实
- Agent 说“完成”仍然只是一项声明，最终要看实际文件和验证结果
- 精确模型、Token 或费用只有在 Host 提供可靠证据时才会报告

完整规则见 [架构说明](docs/architecture.md)。

## 项目结构

```text
.
├── .agents/plugins/                  # Codex Marketplace 注册
├── .codex-plugin/                    # Plugin manifest
├── agent-profiles/                   # 五个原生 Subagent 配置
├── assets/                           # Plugin 图标与 README Logo
├── policy-contract.json              # 机器可读的角色与核心约束
├── scripts/                          # installer、校验器与运行证据工具
├── skills/
│   ├── dispatch/                     # 主委托 Skill、交互控制和运行规则
│   └── doctor/                       # 安装、配置、profiles 与升级诊断
├── docs/                             # 安装、架构与运行边界文档
├── evals/                            # 静态与行为评估数据
└── tests/                            # 回归、打包与跨平台测试
```

## 文档

- [安装](docs/plugin-installation.md)
- [架构](docs/architecture.md)
- [Codex 原生 Subagent 运行边界](docs/native-subagent-runtime.md)
- [AI Agent 项目参考](README_AI.md)
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## 许可证

[MIT](LICENSE)
