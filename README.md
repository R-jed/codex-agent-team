# Codex Delegate

[English](README_EN.md) · [安装指南](docs/plugin-installation.md) · [MIT License](LICENSE)

Codex Delegate 是一个面向 Codex 的原生 Subagent 委派工作流。你只需要描述开发任务，当前 Codex 会话会继续作为**主会话**，判断哪些责任值得委派、应该交给谁、哪些证据可以复用，以及最后如何验收。

它的目标很简单：把任务交给最小且真正有价值的 Agent 组合，同时减少重复搜索、无意义的多模型并跑和失控的写入范围。

当前版本：`0.4.0`，v1.0.0 发布前预览版。

## 安装

先把仓库加入 Codex Plugin marketplace：

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main
```

重新打开 ChatGPT Desktop，在 Plugins Directory 中安装 `Codex Delegate`。

需要使用时，在 Codex 会话中调用：

```text
/codex-delegate
```

GitHub 仓库和 Plugin package 目前仍保留 `codex-agent-team` 兼容标识，因此安装源地址暂时没有变化。

## 怎么用

直接给它正常的开发任务即可，例如：

```text
/codex-delegate 修复这个登录重试 bug，并运行相关测试。
```

```text
/codex-delegate 重构这个模块，保持现有 public API 不变。
```

```text
/codex-delegate review 这次改动，重点检查数据一致性和回归风险。
```

你不需要手工决定 Luna、Terra、Sol 的调用顺序，也不需要为了“组成一个团队”强制启用多个 Agent。

## 它会怎么处理任务

主会话先理解目标、范围、风险和验收标准，然后选择最小可用路径。

| 角色 | 当前路由 | 用途 |
| --- | --- | --- |
| 主会话 | 当前 Codex 会话 | 理解需求、做关键决策、安排工作、验收结果 |
| Luna Reader | GPT-5.6 Luna `max` | 搜索、追踪、测试映射、证据收集 |
| Luna Worker | GPT-5.6 Luna `max` | 边界明确的实现、调试、测试和局部重构 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | 处理仍未解决的复杂技术依赖 |
| Sol Advisor | GPT-5.6 Sol `high` | 高价值判断和选择性复核 |

常见路径可能只有：

```text
主会话
```

或者：

```text
主会话 -> Luna -> 主会话
```

复杂任务也可能出现：

```text
主会话 -> Luna -> Terra（只处理未决技术问题）-> Luna / 主会话
```

以及：

```text
主会话 -> Luna -> Sol -> 主会话
```

没有固定的三级流水线。每次 Subagent 调用都需要解决一个当前仍未满足的独立依赖。

## 写入任务会先收紧边界

当任务需要修改文件时，主会话会先把工作整理成可验收的 Delegation Contract，明确：

```text
要完成什么
可以读写哪些范围
哪些行为必须保持不变
Worker 可以自行决定什么
怎样才算完成
需要运行哪些验证
什么情况必须停止并交回主会话
```

如果关键决策或验收标准还不清楚，Writing Worker 不会直接开始猜测式修改。

## 已经确认的结果会尽量复用

同一个任务中，主会话会保存仍然有效的测试结果、调用路径、接口事实和其他可复用证据。

后续 Agent 默认使用这些已确认信息。只有相关文件、产物或前提发生变化时，受影响的证据才需要重新验证。

这样可以减少模型切换后从头搜索仓库、重复跑相同命令和重复推理同一个问题。

## Luna 遇到问题时

工作流会先判断问题类型：

```text
机械错误        -> Luna 定点修正
任务边界不完整  -> 主会话补齐合同
复杂技术缺口    -> Terra 只调查未解决部分
关键判断问题    -> 主会话决定，必要时调用 Sol
```

Terra 不会因为 Luna 的结果“看起来一般”就自动重做整个任务。

Sol 也不会成为每次任务都必须经过的最终关卡。测试和验收已经足够明确时，主会话可以直接完成验收。

## 并行与多个会话

默认资源边界是：

```text
0 个 Subagent 也属于正常结果
默认 1 个
通常最多 2 个
v1 硬上限 4 个
```

两个独立项目可以各自运行自己的 Codex Delegate。项目没有设置整台机器或整个账号共享的 Agent 总数上限。

对于写入任务，当前策略以工作区为边界：同一个 canonical physical checkout 同时只允许一个 Writing Worker。真实隔离的独立 worktree 或独立项目可以分别拥有自己的 Writer。

当前 `0.4.0` 仍处于 v1 发布前验证阶段。如果你同时打开多个独立 Codex 会话，建议在 v1.0.0 发布前避免让两个会话同时对同一个 physical checkout 执行写入任务。

## 第一次运行

Codex Delegate 当前使用四个项目管理的 custom Agent profiles：

```text
codex_agent_team_reader
codex_agent_team_worker
codex_agent_team_investigator
codex_agent_team_advisor
```

这些 profile 名称暂时保留兼容标识，不影响 `/codex-delegate` 的使用。

如果 profile 尚未安装，Skill 会先说明将要写入的 managed 文件范围并请求你的授权。Installer 只管理这四个 profiles 和自己的 ownership manifest，不会借此修改你的凭据、MCP 配置、仓库文件或其他 Agent profiles。

安装完成后，如果当前任务仍没有发现新角色，启动一个新的 Codex task 再调用 `/codex-delegate`。

## 安全边界

- 主会话始终保留任务范围、关键决策和最终验收权。
- 同一个共享 checkout 同时最多一个 Writing Worker。
- 子 Agent 不继续创建新的 Subagent，委派深度保持一层。
- Skill 不会暗中切换主会话模型或 reasoning effort。
- 缺少精确项目 profile 时，对应责任会停回主会话，不会偷偷换成相似角色。
- Worker 会保留用户或其他会话产生的无关修改；工作区状态发生变化并影响当前合同时，它应停止并把变化交回主会话处理。
- Subagent 的完成报告只是声明，最终结果仍由主会话根据实际文件、diff、测试和可复现证据验收。
- 发布、部署、支付、账号权限修改等高影响外部动作仍由主会话控制，并遵循当前用户授权范围。

## 当前版本说明

`0.4.0` 已采用 `Codex Delegate` 产品名和 `/codex-delegate` 入口，同时暂时保留原仓库、Plugin package、Agent profile 和 ownership manifest 的兼容标识，避免品牌迁移破坏现有安装状态。

v1.0.0 发布前仍在验证少数真实运行边界，包括多个独立会话同时面对同一 checkout，以及同一 Codex home 下的并发 profile 安装行为。因此当前 README 不承诺未经实测证明的吞吐量、成本降低、延迟改善或跨会话互斥保证。

不同 Plugin 版本同时期望不同 managed profile generation 的场景不属于 v1 支持范围。遇到精确 route 不匹配时，受影响的 delegation 应停止并提示处理，不会跨角色替换。

## 更多信息

- [安装与首次运行](docs/plugin-installation.md)
- [项目主页](https://github.com/R-jed/codex-agent-team)

## License

[MIT](LICENSE)
