# Codex Delegate

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="Codex Delegate" src="docs/logo-dark.svg" width="128">
  </picture>
</p>

<p align="center">
  Codex Native Subagents 之上的委派策略层。把开发任务变成最小的一组可验证委派。<br>
  <a href="README_EN.md">English</a> · <a href="docs/plugin-installation.md">安装指南</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/version-0.4.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/status-pre--v1-orange.svg" alt="Status">
</p>

Codex Delegate 把开发任务变成最小的一组可验证委派，并只在委派能增加实际价值时调用 Codex Native Subagents。

当前主会话始终负责理解需求、范围、关键决策、调度、验收和最终回复。Codex Delegate 在这个基础上决定哪些责任值得交给 Luna、Terra 或 Sol，以及什么时候直接由主会话完成更合适。

当前版本：`0.4.0`，pre-v1。

## 快速开始

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

重新打开 ChatGPT 桌面 App，在 Plugins Directory 中安装 `Codex Delegate`，然后直接给它任务：

```text
/codex-delegate 修复这个登录重试 bug，并运行相关测试。
/codex-delegate 重构这个模块，保持现有 public API 不变。
/codex-delegate review 这次改动，重点检查数据一致性和回归风险。
```

你不需要先决定调用哪个模型或安排调用顺序。

## 它如何工作

Codex Delegate 先判断委派是否真的有价值。如果任务已经足够明确，主会话可以直接完成，使用 `0` 个 Subagent 完全正常。

需要委派时，执行责任会先被整理成可验收的 Delegation Contract，明确结果、范围、不变量、决策权限、验收条件、验证方式和停止条件。然后只创建满足当前独立依赖所需要的 Agent。

没有固定的三级流水线。Luna、Terra 和 Sol 都不是必须经过的阶段。

| 角色 | 模型 | 主要职责 |
| --- | --- | --- |
| 主会话 | 当前 Codex 会话 | 理解需求、决策、编排、验收 |
| Luna Reader | GPT-5.6 Luna `max` | 搜索、追踪、测试映射、证据收集 |
| Luna Worker | GPT-5.6 Luna `max` | 实现、调试、测试、局部重构 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | 解决仍未完成的复杂技术依赖 |
| Sol Advisor | GPT-5.6 Sol `high` | 高价值判断和选择性复核 |

Luna 执行失败后会先判断失败类型。机械问题通常继续由 Luna 做局部修正；合同缺口返回主会话；真正的复杂技术缺口才交给 Terra；需要高价值判断时再使用 Sol。

## 已经确认的结果会尽量复用

在当前任务中，主会话会继续携带仍然有效的测试结果、接口事实和其他证据。后续 Agent 直接接收相关证据，只重新验证因文件、运行状态或冲突信息变化而失效的部分。

这个机制用于减少重复搜索、重复测试和完整任务重做。它不代表不同独立会话之间存在持久共享的全局证据库。

## 并发与多会话

每个主会话的 v1 资源边界是：

```text
0 个 Subagent：正常结果
默认：1 个
一般最多：2 个
硬上限：4 个
```

这个数量限制按主会话计算，不是整台机器或账号的全局 Agent 上限。不同项目可以分别运行自己的 Codex Delegate。

写入任务按 canonical workspace 管理。同一个 physical checkout 的产品规则是同时最多一个 Writing Worker。不同、真正隔离的 workspace 或 worktree 可以各自拥有 writer。

当前 `0.4.0` 仍在完成跨独立主会话的同 checkout writer exclusion 实测。在 v1.0.0 前，如果你同时开多个独立 Codex 会话，避免让两个会话同时写同一个 physical checkout。

## 首次运行

Codex Delegate 使用四个受项目管理的角色 profile：Reader、Worker、Investigator 和 Advisor。具体内部 profile 标识与迁移规则记录在[安装指南](docs/plugin-installation.md)。

当所需 profile 缺失时，Skill 会先说明将要管理的 Codex-home 文件范围并请求授权。Installer 可以在 ownership 规则允许时创建或更新当前四个项目 profile、维护自己的 ownership manifest，并在具有精确历史 ownership 证明时清理旧版项目 profile。

它不会修改凭据、MCP 配置、仓库文件、`config.toml` 或无关 Agent profile。

安装完成后，如果当前任务仍没有发现新角色，启动一个新的 Codex task，再调用 `/codex-delegate`。

## 安全边界

- 主会话始终保留用户意图、任务范围、关键决策和最终验收权
- 同一个 canonical checkout 的规则是同时最多一个 Writing Worker
- 子 Agent 不继续创建新的 Subagent，委派深度保持一层
- Skill 不会暗中切换主会话模型或 reasoning effort
- 缺少精确项目 profile 时，对应责任会停回主会话，不会自动换成相似角色
- Worker 必须保留用户或其他会话产生的无关修改；工作区变化使合同失效时，应停止并交回主会话
- Subagent 的完成报告属于执行声明，最终验收依据实际文件、diff、测试和可复现证据
- 发布、部署、支付、账号权限等高影响外部动作仍由主会话控制

## 当前版本与兼容性

`0.4.0` 使用 `Codex Delegate` 产品名和 `/codex-delegate` 作为正式用户入口。

为了降低 pre-v1 升级风险，GitHub 仓库 slug、Plugin package id 和内部 managed-profile namespace 暂时保留 `codex-agent-team` 兼容标识。用户无需手工重命名这些内部资源。

v1.0.0 发布前仍在完成三类与用户实际使用有关的 live validation：跨会话同 checkout 写入排他、同一 Codex home 的并发 installer 行为，以及从 `0.3.x` 到 `0.4.x` 的真实 Plugin 升级路径。当前 README 不对这些尚未完成的运行时保证做超出证据的承诺。

## 更多信息

- [安装与首次运行](docs/plugin-installation.md)
- [项目主页](https://github.com/R-jed/codex-agent-team)

## License

[MIT](LICENSE)
