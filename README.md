<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="Codex Delegate" src="docs/logo-dark.svg" width="128">
  </picture>
</p>

<h1 align="center">Codex Delegate</h1>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="docs/plugin-installation.md">安装指南</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/version-0.6.0-green.svg" alt="Version">
</p>

Codex Delegate 让 Codex 在复杂开发任务里更会分工。

你只需要说明目标、约束和完成标准。主会话会决定哪些事情自己处理，哪些交给 Luna，什么时候需要 Terra 深挖技术问题，什么时候值得让 Sol 做一次独立复核。

它建立在 Codex Native Subagents 之上，不替换 Codex，也不要求固定的 Agent 队伍。

## 为什么用 Codex Delegate

直接使用 Subagents 很容易遇到几个问题：任务拆得太碎、多个 Agent 重复找资料、可以并行的工作被串行等待、一个局部失败导致整段工作重来，或者高风险改动缺少真正独立的第二次检查。

Codex Delegate 把这些调度留给主会话处理。你不需要自己决定“这里开几个 Agent”或“这个问题该交给哪一个模型”。

它主要解决四件事：

- 只在委派确实有价值时使用 Subagent，小任务可以完全不委派；
- 能并行的工作尽早并行，某个子任务完成后立即推进已经解锁的下一步；
- 局部问题优先局部修复，避免无意义地整单重跑或反复升级模型；
- 对影响范围较大的改动增加独立复核，同时保留主会话的最终控制权。

典型流程很简单：

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

Codex Delegate 通过 Codex 原生 Plugin 系统分发。

首次安装：

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin add codex-agent-team@codex-agent-team
```

安装完成后启动一个新的 Codex thread，然后直接使用：

```text
/codex-delegate 修复这个 bug，并运行相关测试。
```

更新已有安装：

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

更新后同样启动一个新的 Codex thread。

第一次需要 Luna、Terra 或 Sol 的专用角色时，Codex Delegate 会说明它准备写入的 Agent profile，并在得到授权后完成配置。Installer 只管理 Codex Delegate 自己的四个 profile 和 ownership manifest，不修改凭据、MCP、仓库、`config.toml` 或其他 Agent profile。

完整安装、迁移和故障处理见 [Plugin Installation](docs/plugin-installation.md)。

## 模型分工

| 角色 | 当前模型 | 适合处理 |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | 查代码、追调用链、找测试、整理证据 |
| Luna Worker | GPT-5.6 Luna `max` | 有明确边界的实现、调试、测试和局部重构 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | Luna 已经无法解决的复杂技术问题 |
| Sol Advisor | GPT-5.6 Sol `high` | 高价值判断、独立复核和高风险改动的最终检查 |

这些角色代表工作责任。更强的模型不会自动获得更大的修改范围或决策权。

Codex Delegate 也不会每次把四个角色都叫出来。一个简单修改可能使用 `0` 个 Subagent；普通实现通常由 Luna 完成；只有出现明确的技术难点或复核价值时才使用 Terra 或 Sol。

## 并行工作

你不需要手工拆出并发计划。只要把目标、不能破坏的约束和完成标准说清楚，Codex Delegate 会判断哪些工作可以同时进行。

当两个独立子任务同时运行时，先完成的结果会先被处理。如果它已经解锁了下一步，而且还有可用资源，主会话会继续推进，不必等待其他无关子任务全部结束。

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

只有任务之间真的存在依赖，或者同一工作区存在写入冲突时，才需要等待。

显式使用 `/codex-delegate` 时，默认可以同时运行最多两个有明确理由的 child，无需再次询问。这个数字只是默认授权范围，不是固定团队规模。一个 physical checkout 同时最多只有一个写入 Worker；需要多个 Writer 时应使用真正隔离的 worktree 或 workspace。

## 失败时怎么处理

Codex Delegate 不会因为一次失败就机械地换更强模型或从头重跑。

如果当前工作仍在产生有效进展，它会继续。如果已经陷入重复，则根据问题本身处理：局部实现问题交给 Luna 修正，任务边界不清由主会话重新整理，复杂技术难点只把仍未解决的部分交给 Terra，需要独立判断时再使用 Sol。

这样做的目的很简单：保留已经完成的工作和有效信息，把计算花在真正还没解决的地方。

## Final Review

Sol 不是每个任务的固定最后一步。普通低风险修改在主会话检查实际 diff 并完成必要测试后即可结束。

当改动涉及公共接口、持久化状态、安全或授权、数据完整性、并发、迁移，或者影响范围明显较大时，Codex Delegate 可以要求一次独立的 Sol 复核。

Sol 会针对当前候选结果给出三种结论：

```text
ship       可以交付
fix-first  先修复，再重新验证和复核
rethink    关键设计或假设需要重新考虑
```

复核之后如果交付物发生变化，旧结论不会继续沿用。

## 安全边界

主会话始终拥有最终控制和验收权。Child 不会继续创建自己的 Agent 队伍，已有的用户修改和其他会话修改必须保留，同一 physical checkout 不允许多个 Worker 同时写入。

仓库、网页、issue、日志、生成内容或模型输出里的指令不能自行扩大任务范围、修改权限或改变调度规则。Agent 报告“完成”也不会直接被当作验收结果，最终仍以实际改动、测试和可复现结果为准。

Codex Delegate 不实现第二套 Agent runtime，也不需要额外的后台服务或 routing proxy。它使用 Codex 已有的 Native Subagents，把重点放在更合理地分工、并行、恢复和复核。

## License

[MIT](LICENSE)
