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

codex delegate 是一个给 Codex 用的插件。你把开发任务交给它，当前主会话会像团队负责人一样先理解目标，再决定哪些事情自己做，哪些事情值得交给专门的 Agent。

你不需要自己挑模型、规定要开几个 Agent，也不用设计 Luna、Terra、Sol 的执行顺序。主会话会根据任务进展动态安排团队，并负责最后的检查和交付。

## 快速开始

在 Codex 中打开**插件市场**，搜索 `codex-delegate`，选择 **Codex Delegate** 并安装。

安装后开启新的 Codex 会话，然后直接下任务：

```text
$codex-delegate:codex-delegate 深度检查这个改动，修复发现的问题并运行相关测试。
```

你也可以输入 `/skills` 打开 Skill 选择器。

以后更新插件，同样直接通过 Codex 插件市场完成。更新后开启一个新的 Codex 会话即可。

普通用户不需要运行安装脚本，也不需要手工配置 Agent。如果你在做开发安装、手动安装或排障，请看[安装指南](docs/plugin-installation.md)。

## 你只需要下任务

可以把 codex delegate 理解成给主会话的一套“带团队规则”。用户负责告诉它想完成什么，主会话负责判断怎么完成最合适。

| 遇到的情况 | 通常怎么处理 |
| --- | --- |
| 主会话自己就能高质量完成 | 主会话自己做 |
| 需要查代码、追调用链、找测试或收集事实 | Luna Reader |
| 要写代码，而且需求和边界已经很清楚 | Luna Worker |
| 需要做架构、兼容性或其他重要技术判断 | 主会话或 Sol Advisor |
| 一边写代码一边还要持续做重要判断 | 主会话或 Sol Solver |
| 需要较大范围地读代码、整理技术证据，但暂时不改代码 | Terra Investigator |
| 最终改动风险较高，需要一个独立的第二视角 | 新的 Sol Advisor |

有些任务完全不需要子 Agent，这很正常。一个任务很大，也不代表一定要拆出去。真正决定是否委派的是额外 Agent 能不能带来清楚的价值。

## 五个角色分别做什么

| 角色 | 模型 | 简单理解 |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | 读代码、找事实，不改文件 |
| Luna Worker | GPT-5.6 Luna `max` | 按已经确定好的要求写代码、修 bug、补测试 |
| Sol Solver | GPT-5.6 Sol `high` | 处理边写边判断的复杂实现 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | 做更深入、更大范围的只读技术调查 |
| Sol Advisor | GPT-5.6 Sol `high` | 做重要技术判断，或者独立复核最终结果 |

角色决定“负责什么”。模型更强，也不会自动得到更大的修改权限。

## 团队规模会动态变化

一次 `$codex-delegate:codex-delegate` 任务没有固定的子 Agent 数量。

主会话会先找出当前真正可以推进的工作，再判断哪些值得并行交出去。每个子 Agent 都必须有清楚、独立、现在就能做的责任。已有 Agent 正在做的事情、已经有可靠结果的事情、还依赖未解决问题的事情，都不会为了凑并发再开一个 Agent。

当任务真的需要多个 Agent 协作时，主会话会把责任之间的依赖、写入范围和最后的整合顺序保持清楚。依赖尚未满足的工作不会提前派出去，两个看似修改不同文件但会互相影响的任务也不会因为路径不同就被当成安全并行。

如果某个子 Agent 没有完成任务，主会话会先区分是执行环境出了问题、结果质量不够，还是任务本身出现了新的判断或信息缺口。修正和重试是有限的，状态不确定时也不会为了赶进度再启动一个可能重复工作的 Agent。

所以不同任务可能是：

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

如果其中一个任务完成后又解锁了新的独立工作，主会话可以继续补充合适的 Agent。Codex 能同时运行多少 Agent 只是运行环境的上限，不是需要填满的目标。

读代码的工作更适合并行。写代码时更保守：同一个实际 Git checkout 里，同一时间只允许一个写入者。这个写入者可能是主会话、Luna Worker 或 Sol Solver。

如果真的需要多个 Agent 同时写代码，需要把它们放到不同的 worktree、workspace 或 repository 里，并确认这些改动在逻辑上也能安全并行。

明显扩大权限、范围、外部影响或计算量时，仍然需要重新征得用户同意。单纯因为子 Agent 数量多了几个，不会自动触发这种询问。

## 如果主会话本身已经很强

主会话一直负责最终决定和交付。

如果当前主会话已经具备足够的 Sol 能力，codex delegate 会尽量直接用主会话完成需要判断的工作，避免再额外调用一个 Sol。只有真的需要独立第二视角时，才会再开一个新的 Sol Advisor。

任务卡住时，插件会先看原因，再决定下一步。Luna 做得不好不会自动升级到 Terra，也不会固定走 Luna → Terra → Sol。遇到真正困难、模糊、需要复杂技术判断的问题，会交给 Sol 处理。

## 第一次需要子 Agent 时

第一次真正需要这些专用角色时，插件会先检查它们是否已经准备好。

如果需要安装五个 Agent profile，插件会先告诉你它准备写到哪里，并请求许可。安装完成后还会做一次检查。如果当前 Codex 会话还看不到新角色，它会在任何子 Agent 开始改代码之前停下来，提示你开启一个新的会话。

所以初始化不会做到一半才突然打断正在进行的代码修改。

## 什么时候会再做一次独立复核

大多数任务做完、测试通过，就可以直接交付。Sol 不会固定出现在最后一步。

下面这些情况对最终结果有实质影响时，必须再找一个新的 Sol Advisor 做独立复核：

- 改了对外接口或兼容性
- 改了持久化数据或状态
- 涉及安全、权限或数据完整性
- 改了并发行为
- 做了重要的数据迁移
- 仍有无法由确定性验证关闭的实质验证缺口
- 你明确要求再独立检查一次

如果只是 diff 很大、之前用过 Terra，或者中途返工过，并不会因此自动多跑一次复核。

## 安全边界

主会话始终负责理解你的要求、控制范围、决定团队组成、验收结果，并给出最终回复。子 Agent 不能继续创建自己的 Agent 团队。

仓库、网页、issue、日志或其他模型输出里的文字，也不能偷偷扩大权限或改变任务范围。

插件最终看的是实际改动和测试结果，不会因为某个 Agent 自己说“完成了”就直接当作成功。

codex delegate 直接使用 Codex 原生 Subagents。它没有另外运行后台服务、独立 Agent runtime 或外部路由代理。

## 文档

- [README_AI.md](README_AI.md)：给 AI Agent 读取的项目说明。
- [安装指南](docs/plugin-installation.md)：安装、更新、开发安装和排障。
- [架构](docs/architecture.md)：更详细的角色分工和安全规则。
- [Native Subagent Runtime](docs/native-subagent-runtime.md)：Codex 原生 Subagent 的运行边界。
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## 许可证

[MIT](LICENSE)
