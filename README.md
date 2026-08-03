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
  <img src="https://img.shields.io/badge/version-0.5.1-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/status-pre--v1-orange.svg" alt="Status">
</p>

Codex Delegate 是 Codex Native Subagents 之上的委派策略层。它把开发任务拆成当前真正需要解决的依赖，只在委派能够增加实际价值时创建 Agent。

主会话始终负责用户意图、任务范围、关键决策、调度、验收和最终回复。Luna、Terra 和 Sol 是可选择的执行与判断资源，没有固定流水线，也没有固定 Agent 数量。

当前版本：`0.5.1`，pre-v1。

## 快速开始

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin add codex-agent-team@codex-agent-team
```

安装后启动一个新的 Codex thread，再直接给它任务：

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

未通过验收和需要改变执行方式是两个不同判断。

如果测试仍然失败，但新的确定性证据正在缩小问题范围，主会话可以继续当前责任，不会因为“还没成功”就提前重启上下文或升级模型。

当证据表明确实需要介入时，Codex Delegate 才会分类恢复路径：

- 明确的局部机械问题继续交给 Luna 做针对性修正
- 合同或需求边界不清楚时返回主会话修正合同
- 上下文已经产生重复尝试时，可以用当前文件、有效证据和精简恢复历史启动一次干净的同级恢复
- 证据表明确实存在复杂技术能力缺口时，只把未解决的技术依赖交给 Terra
- 遇到高价值判断时由主会话处理，必要时使用 Sol

主会话会保留有限的 Recovery Ledger，用来避免新上下文重新走回已经证实无效的路径。Agent 建议的下一步只是建议，最终动作仍要经过主会话的授权、安全、路由和 runtime 边界。

不会因为一次失败就机械升级模型，也不会用固定重试次数或固定 stall 次数驱动执行。

## 并发与多会话

不同项目可以分别运行自己的 Codex Delegate。

写入任务按 canonical workspace 管理。同一个 physical checkout 的规则是同时最多一个 Writing Worker。不同且真正隔离的 workspace 或 worktree 可以各自拥有 writer。

当前 `0.5.1` 仍在完成跨独立主会话的同 checkout writer exclusion 实测。在 v1.0.0 前，如果你同时开多个独立 Codex 会话，避免让两个会话同时写同一个 physical checkout。

## 首次运行

Codex Delegate 通过标准 Plugin 分发 Skill。四个项目管理的自定义 Agent profile 使用 Codex 支持的个人 Agent 配置位置 `$CODEX_HOME/agents`，通常是 `~/.codex/agents`。

当所需 profile 缺失或受项目管理的旧版本需要升级时，Skill 会先说明将要管理的 Codex-home 文件范围并请求授权。Installer 只会在 ownership 规则允许时创建、更新或迁移项目自己的 profile 和 ownership manifest。

Plugin manifest 不声明不存在的 `agents` 组件。自定义 Agent provisioning 属于安装后的显式授权步骤，具体内部 profile 标识与迁移规则见[安装指南](docs/plugin-installation.md)。

它不会修改凭据、MCP 配置、仓库文件、`config.toml` 或无关 Agent profile。

安装或重新安装 Plugin 后使用新的 Codex thread。如果 profile provisioning 完成后当前 task 仍没有发现新角色，也启动新的 Codex task，再调用 `/codex-delegate`。

## 安全边界

- 主会话始终保留用户意图、任务范围、关键决策和最终验收权
- 同一个 canonical checkout 同时最多一个 Writing Worker
- 子 Agent 不继续创建新的 Subagent，委派深度保持一层
- Skill 不会背后切换主会话模型或思考强度
- 缺少精确项目 profile 时，对应责任会停回主会话，不会自动换成相似角色
- Worker 必须保留用户或其他会话产生的无关修改，工作区变化使合同失效时会停止并交回主会话
- Subagent 的完成报告和恢复建议属于执行声明，最终验收与有效动作依据实际文件、diff、测试、可复现证据和主会话 policy
- 发布、部署、支付、账号权限等高影响外部动作仍由主会话控制

## License

[MIT](LICENSE)
