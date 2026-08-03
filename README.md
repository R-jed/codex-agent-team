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
  <img src="https://img.shields.io/badge/version-0.5.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/status-pre--v1-orange.svg" alt="Status">
</p>

Codex Delegate 是 Codex Native Subagents 之上的委派策略层。它把开发任务拆成当前真正需要解决的依赖，只在委派能够增加实际价值时创建 Agent。

主会话始终负责用户意图、任务范围、关键决策、调度、验收和最终回复。Luna、Terra 和 Sol 是可选择的执行与判断资源，没有固定流水线，也没有固定 Agent 数量。

当前版本：`0.5.0`，pre-v1。

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

你不需要预先选择模型、Agent 数量或调用顺序。

## 它如何工作

Codex Delegate 会先判断当前有哪些未完成依赖，以及哪些依赖值得委派。

如果任务已经足够明确，主会话可以直接完成，使用 `0` 个 Subagent 完全正常。

需要委派时，责任会先整理成可验收的 Delegation Contract，明确依赖、结果、范围、接口、不变量、决策权限、验收条件、验证方式和停止条件。随后只调度当前已经准备好、能够增加新价值的责任。

| 角色 | 模型 | 主要职责 |
| --- | --- | --- |
| 主会话 | 当前 Codex 会话 | 理解需求、依赖、决策、调度、验收 |
| Luna Reader | GPT-5.6 Luna `max` | 搜索、追踪、测试映射、证据收集 |
| Luna Worker | GPT-5.6 Luna `max` | 实现、调试、测试、局部重构 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | 解决仍未完成的复杂技术依赖 |
| Sol Advisor | GPT-5.6 Sol `high` | 高价值判断和选择性复核 |

任务大小不会自动决定使用更强模型。清楚的大任务可以继续由 Luna 处理，小改动遇到关键架构、安全、迁移或公开接口判断时也可能使用 Sol。

## 没有固定 Agent 数量

Codex Delegate 根据当前已经准备好的独立依赖决定是否并行，不预设 `1 / 2 / 4` 这样的团队规模。

显式调用 `/codex-delegate` 时，最多两个同时活跃且确有价值的 child Agents 属于正常免再次确认的资源范围。需要同时运行更多 Agent 时，如果你尚未授权大规模并行，Codex Delegate 会先说明原因并征求同意。

获得同意后，实际能够同时运行多少 Agent 由三件事共同决定：

```text
当前独立依赖
工作区安全边界
Codex runtime 当前可用 child slots
```

如果 runtime 暂时没有足够 slot，剩余依赖会等待或分批执行。Codex Delegate 不会为了填满 slot 重复同一个问题，也不会因为 slot 不足偷偷切换到其他角色。

## 已经确认的结果会尽量复用

在当前任务中，主会话会继续携带仍然有效的测试结果、接口事实和其他证据。后续 Agent 直接接收相关证据，只重新验证因文件、运行状态或冲突信息变化而失效的部分。

这个机制减少重复搜索、重复测试和完整任务重做。不同独立会话之间目前没有持久共享的全局证据库。

## 卡住时如何处理

Agent 自己说“有进展”不会自动触发继续执行。主会话会检查实际文件、测试、错误签名和新的证据。

当执行没有通过验收时，Codex Delegate 会根据证据选择恢复路径：

- 明确的局部机械问题继续交给 Luna 做针对性修正
- 合同或需求边界不清楚时返回主会话修正合同
- 上下文已经产生重复尝试时，可以用当前文件和有效证据启动一次干净的同级恢复
- 证据表明确实存在复杂技术能力缺口时，只把未解决的技术依赖交给 Terra
- 遇到高价值判断时由主会话处理，必要时使用 Sol

不会因为一次失败就机械升级模型，也不会用固定重试次数驱动执行。

## 并发与多会话

不同项目可以分别运行自己的 Codex Delegate。

写入任务按 canonical workspace 管理。同一个 physical checkout 的规则是同时最多一个 Writing Worker。不同且真正隔离的 workspace 或 worktree 可以各自拥有 writer。

当前 `0.5.0` 仍在完成跨独立主会话的同 checkout writer exclusion 实测。在 v1.0.0 前，如果你同时开多个独立 Codex 会话，避免让两个会话同时写同一个 physical checkout。

## 首次运行

Codex Delegate 使用四个受项目管理的角色 profile：Reader、Worker、Investigator 和 Advisor。具体内部 profile 标识与迁移规则记录在[安装指南](docs/plugin-installation.md)。

当所需 profile 缺失或受项目管理的旧版本需要升级时，Skill 会先说明将要管理的 Codex-home 文件范围并请求授权。Installer 只会在 ownership 规则允许时创建、更新或迁移项目自己的 profile 和 ownership manifest。

它不会修改凭据、MCP 配置、仓库文件、`config.toml` 或无关 Agent profile。

安装完成后，如果当前任务仍没有发现新角色，启动一个新的 Codex task，再调用 `/codex-delegate`。

## 安全边界

- 主会话始终保留用户意图、任务范围、关键决策和最终验收权
- 同一个 canonical checkout 同时最多一个 Writing Worker
- 子 Agent 不继续创建新的 Subagent，委派深度保持一层
- Skill 不会暗中切换主会话模型或 reasoning effort
- 缺少精确项目 profile 时，对应责任会停回主会话，不会自动换成相似角色
- Worker 必须保留用户或其他会话产生的无关修改，工作区变化使合同失效时会停止并交回主会话
- Subagent 的完成报告属于执行声明，最终验收依据实际文件、diff、测试和可复现证据
- 发布、部署、支付、账号权限等高影响外部动作仍由主会话控制

## 当前版本与兼容性

`0.5.0` 保持 `Codex Delegate` 产品名和 `/codex-delegate` 正式用户入口，并将调度升级为依赖与执行证据驱动。

为了降低 pre-v1 升级风险，GitHub 仓库 slug、Plugin package id 和内部 managed-profile namespace 暂时保留 `codex-agent-team` 兼容标识。用户无需手工重命名这些内部资源。

v1.0.0 发布前仍在完成真实 Plugin 升级、跨会话同 checkout 写入排他、同一 Codex home 并发 installer、native fan-out 容量与 slot 恢复等 live validation。README 只描述当前已经定义的产品边界，不把尚未完成的 runtime 测试写成既有保证。

## License

[MIT](LICENSE)
