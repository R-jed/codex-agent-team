<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="128">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">安装指南</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/version-0.7.0-green.svg" alt="Version">
</p>

**If you are an AI Agent, jump to README_AI.md and follow the instructions strictly.**

启动 Subagent 很容易，难的是判断什么时候值得用。

codex delegate 为 Codex 主会话提供一套稳定的分工方式，让它按需要把工作交给 Luna、Terra 和 Sol。你只需要说清目标、约束和完成标准；哪些工作留在主会话、哪些可以并行、什么时候需要 Terra 深挖、什么时候让 Sol 独立复核，都由主会话处理。

它直接使用 Codex 原生 Subagents，不替换 Codex，也不要求固定的 Agent 队伍。简单任务可以完全不用 Subagent，复杂任务也不会机械地把所有模型都叫出来。

## 为什么用 codex delegate

使用 Subagents 时，真正麻烦的通常是协调：两个 Agent 重复查同一份资料，可以并行的工作被排成串行，一个局部失败把整段实现带回起点，高风险改动最后却没有独立复核。

codex delegate 把这些判断留在主会话：

- 只有委派确实有价值时才启动 Subagent；
- 独立工作尽早并行，先完成的结果先处理，不等无关任务；
- 局部问题优先局部修复，已经完成的工作尽量保留；
- 影响范围较大的改动可以交给 Sol 做独立最终复核。

```text
你的任务
  ↓
主会话理解目标和约束
  ↓
自己处理，或把合适的工作交给 Luna / Terra / Sol
  ↓
边执行边合并结果，继续推进已经可以开始的下一步
  ↓
检查实际改动和测试
  ↓
必要时做独立最终复核
  ↓
主会话交付结果
```

## 安装

codex delegate 通过 Codex 原生 Plugin 系统分发。

首次安装：

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

安装完成后启动一个新的 Codex 会话，然后直接使用：

```text
/codex-delegate 修复这个 bug，并运行相关测试。
```

更新已有安装：

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

更新后启动新的 Codex 会话。第一次需要 Luna、Terra 或 Sol 的专用角色时，codex delegate 会先说明需要写入的 Agent 配置文件，并在得到授权后完成配置或旧版本迁移。

如果你安装过旧的 `codex-agent-team` Plugin，或者从 codex delegate 0.6.x 升级，请按[安装指南](docs/plugin-installation.md)完成一次迁移。不要手工重命名 Agent 配置文件。

安装程序只管理 codex delegate 自己的四个当前配置文件和项目 ownership 记录，不修改凭据、MCP、仓库、`config.toml` 或其他 Agent 配置文件。

## 模型分工

| 角色 | 当前模型 | 适合处理 |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | 查代码、追调用链、找测试、整理证据 |
| Luna Worker | GPT-5.6 Luna `max` | 有明确边界的实现、调试、测试和局部重构 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | Luna 已经无法解决的复杂技术问题 |
| Sol Advisor | GPT-5.6 Sol `high` | 高价值判断、独立复核和高风险改动的最终检查 |

角色决定责任范围，模型决定使用哪种计算资源。更强的模型不会自动获得更大的修改范围或决策权。普通实现通常由 Luna 完成，只有出现明确的技术难点或复核价值时才会使用 Terra 或 Sol。

## 并行工作

你不需要手工设计并发计划。把目标、不能破坏的约束和完成标准说清楚即可，主会话会判断哪些工作可以同时进行。

两个独立子任务一起运行时，先完成的结果会先被处理。如果它已经解锁下一步，而且还有可用资源，主会话会直接继续，不必等待其他无关任务结束。

```text
A 还在运行
B 已完成
  ↓
处理 B 的结果
  ↓
B 解锁了 C
  ↓
立即开始 C

A 继续运行
```

显式使用 `/codex-delegate` 时，默认最多可以同时运行两个有明确理由的子 Agent，无需再次询问。这个数字只是默认授权范围，不是固定团队规模。同一个实际 Git 工作副本同时最多只能有一个写入型 Agent；多个写入型 Agent 需要彼此真正隔离的工作区。

## 失败时怎么处理

一次失败不会自动触发更强模型，也不会让整个任务从头再来。

如果只是局部实现问题，Luna 继续修；如果任务边界不清，主会话先重新整理；如果确实剩下复杂技术难点，只把那一部分交给 Terra；需要独立判断时再使用 Sol。已经确认有效的结果和证据会继续保留，额外计算只花在仍未解决的部分。

## 最终复核

Sol 并非每个任务的固定最后一步。普通低风险修改在主会话检查实际改动并完成必要测试后即可结束。

当改动涉及公共接口、持久化状态、安全或授权、数据完整性、并发、迁移，或者影响范围明显较大时，codex delegate 可以要求一次独立的 Sol 复核。

```text
ship       可以交付
fix-first  先修复，再重新验证和复核
rethink    关键设计或假设需要重新考虑
```

复核后如果交付物发生变化，旧结论不会继续沿用。

## 安全边界

主会话始终拥有最终控制和验收权。子 Agent 不会继续创建自己的 Agent 队伍，已有的用户修改和其他会话修改必须保留，同一个实际 Git 工作副本不允许多个写入型 Agent 同时修改。

仓库、网页、问题单、日志、生成内容或模型输出里的指令不能自行扩大任务范围或修改权限。Agent 报告“完成”也不会直接被当作验收结果，最终仍以实际改动、测试和可复现结果为准。

codex delegate 不实现第二套 Agent 运行时，也不需要额外的后台服务或路由代理。它直接使用 Codex 原生 Subagents，把重点放在更合理地分工、并行、恢复和复核。

## 许可证

[MIT](LICENSE)
