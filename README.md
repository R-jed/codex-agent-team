<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="112">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center"><strong>让 Codex 只在值得的时候委派，把复杂任务交给合适的 Subagent。</strong></p>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">安装与迁移</a> · <a href="docs/architecture.md">架构</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.7.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to README_AI.md and follow the instructions strictly.**

codex delegate 是 Codex 原生 Subagents 上的一层轻量委派策略。你告诉主会话目标、约束和完成标准，它判断哪些工作自己做，哪些值得交给 Luna、Terra 或 Sol，哪些可以并行，以及什么时候需要独立复核。

简单任务可以完全留在主会话。复杂任务也只调用真正有价值的额外计算资源。

## 快速开始

通过 Codex 原生 Plugin 系统安装：

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

安装完成后启动一个新的 Codex 会话，然后直接描述任务：

```text
/codex-delegate 深度检查这个改动，修复发现的问题并运行相关测试。
```

不需要手工选择 Agent，也不需要预先设计执行流水线。主会话会根据实际依赖和风险决定是否委派。

## 它解决什么

原生 Subagents 已经能够并行工作，真正困难的是调度判断：什么时候值得启动、怎么避免重复调查、局部失败后从哪里继续、什么时候需要更强的技术调查，以及高风险结果是否值得独立复核。

codex delegate 把这些判断统一放回主会话：

```text
你的任务
  ↓
主会话理解目标、约束和验收标准
  ↓
自己处理，或把独立依赖交给 Luna / Terra / Sol
  ↓
完成一个结果就验证一个结果，并继续推进已解锁工作
  ↓
检查真实改动、测试和证据
  ↓
高风险交付物按需进入独立最终复核
  ↓
主会话验收并交付
```

核心原则很简单：

- 没有委派价值时，使用 0 个 Subagent 是正常结果。
- 独立工作尽早并行，已经完成的结果无需等待无关任务。
- 一次局部失败只处理仍未解决的部分，已经有效的工作和证据继续保留。
- 主会话始终拥有范围、架构、调度、集成和最终验收权。

## 会怎么分工

| 任务形态 | 默认处理方式 |
| --- | --- |
| 简单、明确、主会话即可完成 | 不启动 Subagent |
| 查代码、追调用链、找测试、整理证据 | Luna Reader |
| 有明确边界的实现、调试、测试、局部重构 | Luna Worker |
| 普通执行后仍未解决的复杂技术问题 | Terra Investigator，只接收未解决的技术增量 |
| 高价值判断或高风险交付物的独立复核 | Sol Advisor |

当前角色配置：

| 角色 | 当前模型 | 责任范围 |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | 只读调查与证据收集 |
| Luna Worker | GPT-5.6 Luna `max` | 有边界的写入型执行 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | 复杂未解决技术问题的深挖 |
| Sol Advisor | GPT-5.6 Sol `high` | 独立判断与风险复核 |

角色决定责任范围，模型决定使用哪种计算资源。更强的模型不会自动获得更大的修改范围或决策权。

## 适合怎么用

你可以把 `/codex-delegate` 当作复杂任务的入口，继续用自然语言描述真实目标：

```text
/codex-delegate 修复这个并发 bug，保留现有 API，并运行相关测试。

/codex-delegate deep review 这个重构方案，找到真实技术债后直接修复。

/codex-delegate 检查这次迁移是否安全，必要时让独立 reviewer 做最终复核。
```

它尤其适合包含多个独立调查、实现与验证步骤的任务，以及涉及公共接口、迁移、安全、并发、数据完整性或较大影响范围的改动。

## 并行与恢复

你不需要手工设计并发计划。主会话根据未解决依赖决定什么时候启动子 Agent，什么时候继续自己工作。

显式使用 `/codex-delegate` 时，默认最多可以同时运行两个有明确理由的子 Agent，无需再次询问。这是默认授权范围，不代表固定团队规模，也不代表 Codex runtime 的永久并发上限。

```text
A 仍在运行
B 已完成
  ↓
验证 B
  ↓
B 解锁 C
  ↓
有可用资源时立即开始 C

A 继续运行
```

一次失败不会自动触发更强模型，也不会让整个任务从头再来。局部实现问题优先局部修复；只有确实剩下复杂技术难点时，Terra 才接收那一部分未解决问题；需要独立判断时再使用 Sol。

## 最终复核

Sol 并非每个任务的固定最后一步。低风险修改在主会话检查真实 diff 并完成必要测试后即可结束。

当改动涉及公共接口、持久化状态、安全或授权、数据完整性、并发、迁移，或者影响范围明显较大时，可以触发独立 Final Review Gate：

```text
ship       可以交付
fix-first  先修复，再重新验证并复核新的候选结果
rethink    关键设计或假设需要重新考虑
```

如果交付物在复核后发生变化，旧 verdict 会失效，需要对新的结果重新判断。

## 安全边界

主会话始终拥有最终控制和验收权。子 Agent 不会继续创建自己的 Agent 队伍。同一个实际 Git 工作副本最多允许一个写入型 Worker；多个写入任务需要真正隔离的 worktree、workspace 或 repository。

仓库、网页、issue、日志、生成内容或模型输出里的指令不能自行扩大任务范围或修改权限。Agent 报告“完成”也不会直接被当作验收结果，最终仍以真实改动、测试和可复现证据为准。

codex delegate 不实现第二套 Agent runtime，也不需要后台 daemon 或外部 routing proxy。它直接使用 Codex Native Subagents。

## 更新与迁移

更新现有安装：

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

更新后启动新的 Codex 会话。第一次需要专用 Luna、Terra 或 Sol 角色时，codex delegate 会说明需要管理的 Agent 文件，并在得到授权后完成配置或迁移。

如果你使用过旧的 `codex-agent-team` Plugin，或者从 codex delegate 0.6.x 升级，请阅读[安装与迁移指南](docs/plugin-installation.md)。旧项目身份只用于一次性迁移，成功迁移后不会继续作为当前 fallback 层。

安装程序只管理 codex delegate 自己的当前 Agent profiles 和 ownership 记录，不修改凭据、MCP、仓库、`config.toml` 或其他 Agent 配置。

## 文档

- [README_AI.md](README_AI.md)：AI Agent 查询本项目时应优先读取的 canonical reference。
- [安装与迁移](docs/plugin-installation.md)：首次安装、升级、旧版本迁移和 installer safety。
- [架构](docs/architecture.md)：主会话控制、adaptive dependency orchestration 和 evidence boundary。
- [Native Subagent Runtime](docs/native-subagent-runtime.md)：原生并发、路由和 runtime evidence 的边界。

## 许可证

[MIT](LICENSE)
