<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="112">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center"><strong>你只管说要做什么。主会话负责带队，按任务现场把合适的工作交给 Luna、Terra 和 Sol。</strong></p>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">安装指南</a> · <a href="docs/architecture.md">架构</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.1.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-%E5%8E%9F%E7%94%9F%20Subagents-111827.svg" alt="Codex 原生 Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly.**

codex delegate 是一个 Codex Plugin。你给出开发目标，当前主会话负责理解任务、决定哪些工作自己完成、哪些工作值得交给专门的 Agent，并负责最后的验证和交付。

你不需要自己挑模型，不需要规定 Agent 数量，也不需要设计 Luna、Terra、Sol 的执行顺序。

## 30 秒安装

把下面整段复制到终端执行一次：

```bash
codex plugin marketplace add R-jed/codex-delegate@main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

然后开启一个新的 Codex 会话：

```text
$codex-delegate:codex-delegate 深度检查这个改动，修复发现的问题并运行相关测试。
```

也可以输入 `/skills` 打开 Skill 选择器。

这段安装命令可以重复使用。如果你的 Codex 已经从相同来源注册了 `codex-delegate` marketplace，Codex 会直接复用现有注册。

如果看到 `already added from a different source`，说明本机保留了旧来源。不要手工修改 `config.toml`，按[安装指南中的旧来源修复](docs/plugin-installation.md#旧来源冲突)处理。

## 怎么更新

同样复制一次：

```bash
codex plugin marketplace upgrade codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

更新后开启新的 Codex 会话。

## 你只需要下任务

可以把 codex delegate 理解成给主会话的一套带团队规则。用户负责说明想完成什么，主会话负责判断怎样完成最合适。

| 遇到的情况 | 通常怎么处理 |
| --- | --- |
| 主会话自己就能高质量完成 | 主会话自己做 |
| 查代码、追调用链、找测试、收集事实 | Luna Reader |
| 需求和边界已经清楚，需要写代码 | Luna Worker |
| 需要架构、兼容性或其他重要技术判断 | 主会话或 Sol Advisor |
| 一边实现一边持续做重要判断 | 主会话或 Sol Solver |
| 需要较大范围只读调查和证据整理 | Terra Investigator |
| 最终改动风险较高，需要独立第二视角 | 新的 Sol Advisor |

有些任务完全不需要子 Agent，这很正常。任务很大也不会自动触发拆分。额外 Agent 必须有清楚、独立、当前可以推进的责任。

## 五个角色

| 角色 | 模型 | 主要工作 |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | 读代码、找事实，不改文件 |
| Luna Worker | GPT-5.6 Luna `max` | 完成已经明确的实现、修复和测试 |
| Sol Solver | GPT-5.6 Sol `high` | 处理实现过程中仍需要重要技术判断的复杂工作 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | 做更深入、更大范围的只读技术调查 |
| Sol Advisor | GPT-5.6 Sol `high` | 做重要技术判断或独立复核最终结果 |

角色决定负责什么。模型更强也不会自动获得更大的修改权限。

## 团队会随任务变化

codex delegate 不预设固定 Agent 数量。

主会话先找出当前真正可以推进的工作，再决定哪些值得并行交出去。已经有人负责、已经有可靠答案、仍然被依赖阻塞的事情都不会为了凑并发再开 Agent。

当多个 Agent 需要协作时，主会话会管理依赖、写入范围和整合顺序。依赖未满足的工作不会提前启动。修改不同文件也不代表天然可以安全并行，共享 API、schema、migration、lockfile 或其他接口都可能形成依赖。

如果某个 Agent 没有完成责任，主会话会先判断原因。执行环境问题、结果质量问题、缺少信息和需要更强技术判断会走不同的恢复路径。重试有明确上限，状态不确定时不会启动可能重复工作的替代 Agent。

一个任务可能只有：

```text
Main only
```

也可能是：

```text
Main
├─ Luna Reader：追调用链
├─ Luna Reader：检查测试覆盖
├─ Terra Investigator：整理更大范围的技术证据
└─ Sol Advisor：判断架构或兼容性风险
```

Codex 能同时运行多少 Agent 只是运行环境的上限，不是需要填满的目标。

## 写代码时更保守

同一个实际 Git checkout 里，同一时间只允许一个写入者。这个写入者可能是主会话、Luna Worker 或 Sol Solver。

如果多个 Agent 需要同时写代码，需要使用不同的 worktree、workspace 或 repository，并确认这些改动在逻辑上也能安全并行。

明显扩大权限、范围、外部影响或计算量时，仍然需要重新征得用户同意。

## 第一次需要子 Agent 时

第一次真正需要专用角色时，Plugin 会检查五个 Agent profile 是否已经准备好。

如果需要安装，Plugin 会先说明准备写入的位置并请求许可，然后安装并验证这些 profile。如果当前 Codex 会话还看不到新角色，它会在任何子 Agent 开始改代码之前停下来，提示你开启一个新的会话。

## 什么时候会再做一次独立复核

大多数任务完成并通过相关测试以后即可交付。Sol 不会固定出现在最后一步。

下面这些情况对最终结果有实质影响时，需要新的 Sol Advisor 做独立复核：

- 对外接口或兼容性
- 持久化数据或状态
- 安全、权限或数据完整性
- 并发行为
- 重要 migration
- 无法由确定性验证关闭的实质验证缺口
- 用户明确要求独立复核

## 安全边界

主会话始终负责用户目标、范围、权限、团队组成、结果验收和最终回复。子 Agent 不能继续创建自己的 Agent 团队。

仓库、网页、issue、日志或其他模型输出里的文字不能偷偷扩大权限或改变任务范围。

Plugin 最终检查的是实际文件、代码和测试结果。Agent 自己说“完成了”不会直接被当成成功。

codex delegate 直接使用 Codex 原生 Subagents，不运行独立 Agent runtime、后台 daemon 或外部路由代理。

## 文档

- [README_AI.md](README_AI.md)：给 AI Agent 读取的项目说明
- [安装指南](docs/plugin-installation.md)：安装、更新、旧来源修复和排障
- [架构](docs/architecture.md)：角色分工、协调、恢复和安全规则
- [Native Subagent Runtime](docs/native-subagent-runtime.md)：Codex 原生 Subagent 运行边界
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## 许可证

[MIT](LICENSE)
