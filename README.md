<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="112">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center"><strong>让 Codex 只在值得时委派，把标准化执行、重要判断和只读技术调查放到合适的原生 Subagent 上。</strong></p>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">安装指南</a> · <a href="docs/architecture.md">架构</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.9.1-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to README_AI.md and follow the instructions strictly.**

codex delegate 是 Codex Native Subagents 上的一层轻量委派策略。主会话始终掌握目标、范围、授权、集成和最终验收。插件只在额外 Agent 真正能提高效率、隔离上下文、补足判断能力或提供独立复核时才委派。

简单任务可以完全留在主会话。复杂任务也不会预设 Luna、Terra、Sol 的固定流水线。

## 快速开始

在 Codex 中打开**插件市场**，搜索 `codex-delegate`，选择 **Codex Delegate** 并安装。

安装后启动新的 Codex 会话，然后显式调用 Skill：

```text
$codex-delegate 深度检查这个改动，修复发现的问题并运行相关测试。
```

Codex 也可以通过 `/skills` 打开 Skill 选择器。

这就是普通用户的完整安装路径。你不需要注册额外 marketplace、不需要运行安装命令，也不需要手工配置 Agent profiles。

后续更新同样直接通过 Codex 插件市场完成。更新后开启新的 Codex 会话即可使用当前版本；普通用户无需处理 repository ref、Agent profile 或升级脚本。

如果你在做开发安装、手动安装或排障，请查看[安装指南](docs/plugin-installation.md)。

插件不会隐式介入普通任务。你也不需要手工选择 Agent 或设计执行流水线。

## 它解决什么

日常开发里真正困难的往往是决定工作该放在哪里：明确且可重复的实现适合交给高性价比执行模型，架构和语义判断需要更强判断能力，大量只读技术调查可以交给平衡质量与成本的模型，高风险结果才值得额外独立复核。

codex delegate 把正常路径压缩成几个直接问题：

```text
你的任务
  ↓
主会话理解目标与验收
  ↓
额外委派真的有价值吗？
  ↓
当前需要的是证据、标准化写入、重要判断、判断耦合型实现，还是只读技术调查？
  ↓
选择最小且合适的执行者
  ↓
检查真实改动、测试和证据
  ↓
只有卡住时才诊断 contract / judgment / investigation / stalled
  ↓
最终候选按实际后果决定是否需要独立复核
  ↓
主会话交付
```

核心原则：

- 没有委派价值时，0 个 Subagent 是正常结果。
- 一个任务能够写出 contract，并不代表适合交给 Luna。
- Luna 负责行为已经决定、清晰且可重复的标准化执行，不承担开放式语义发散。
- Sol 负责 demanding、ambiguous、multi-step 的重要判断，以及判断无法与实现分开的复杂写入。
- Terra 负责语义已经稳定、无需 material judgment 的 bounded read-heavy technical investigation 和 evidence synthesis。
- 一次失败不会自动触发更强模型。
- 主会话已经具备足够 Sol 能力时，会避免重复再调用一个 Sol。

## 会怎么分工

| 当前需要的能力 | 默认处理方式 |
| --- | --- |
| 主会话直接完成更合适 | 主会话 |
| 窄范围查代码、追调用链、找测试、收集事实 | Luna Reader |
| 行为、边界和验收都已经决定的实现、调试、测试、局部重构 | Luna Worker |
| 实现过程中必须持续做重要架构、兼容性或状态语义判断 | 能力足够的主会话，或 Sol Solver |
| 需要先确定架构、行为、兼容性或复杂技术决策 | 能力足够的主会话，或 Sol Advisor |
| 语义已经稳定，需要更深入的只读技术调查、较大范围扫描或证据综合 | Terra Investigator |
| 最终候选确实需要独立第二视角 | fresh Sol Advisor |

当前角色配置：

| 角色 | 当前模型 | 责任范围 |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | 窄范围只读证据收集 |
| Luna Worker | GPT-5.6 Luna `max` | 清晰、可重复、有明确边界的写入执行 |
| Sol Solver | GPT-5.6 Sol `high` | 判断与实现耦合的复杂写入执行 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | bounded read-heavy 技术调查与证据综合 |
| Sol Advisor | GPT-5.6 Sol `high` | 重要只读判断与独立最终复核 |

角色定义责任范围，模型提供对应计算能力。更强模型不会自动获得更大的用户授权或修改范围。

## 主会话本身已经有足够 Sol 能力时

主会话始终是控制面。只有任务真实需要重要判断时，codex delegate 才会考虑主会话能力是否已经足够。

当前参考能力是 GPT-5.6 Sol `high`。如果 runtime 能可靠确认主会话的 Sol 能力达到当前参考等级，普通判断和判断耦合型实现优先留在主会话，避免重复调用 Advisor 或 Solver。

如果主会话能力不足或无法可靠观察，只有确实存在重要判断时才按需使用 Sol。明确的标准化任务不会因为主会话模型未知而自动升级。

这是一项去重优化，不改变主会话的控制权，也不会替代真正需要独立第二观察者的 Final Review。

## 并行、写入与恢复

你不需要手工设计并发计划。显式使用 `$codex-delegate` 时，普通授权范围内最多可以同时运行两个有明确理由的子 Agent。这是授权范围，不代表固定团队规模或 Codex runtime 的永久并发上限。

独立的只读工作可以并行。同一个实际 Git checkout 在当前编排内同时只有一个 writer，这个 writer 可以是主会话、Luna Worker 或 Sol Solver。并行 writer 需要真正隔离的 worktree、workspace 或 repository。

执行卡住时只诊断四类问题：

```text
contract       → 主会话补齐目标、边界或验收条件
judgment       → 主会话或 Sol 处理重要判断
investigation  → 语义稳定且无需 material judgment 时由 Terra 做 bounded read-heavy 调查
stalled        → 当前角色仍正确时最多做一次真正改善输入的干净重试
```

Luna 做得不好不会自动触发 Terra，也不会自动形成 Luna → Terra → Sol 的返工链。真正困难、模糊或需要复杂技术判断的问题进入 Sol 路径。

## 首次使用体验

第一次真正需要专用角色时，codex delegate 会在 delegated implementation 开始之前检查角色是否就绪。

如果需要安装五个受管理的 Agent profiles，会先说明写入范围并请求授权，然后运行 bundled installer 和非修改型 `--check`。这些 profile 使用 Codex 官方 custom Agent TOML 机制。如果当前 Codex 会话需要重启才能看到新角色，会在任何子 Agent 写代码之前停止并提示开启新会话。

这样 setup 不会发生在任务执行到一半之后。

## 最终复核

Sol 并非每个任务的固定最后一步。独立 Final Review 只关注最终交付物的实际后果，例如：

- 公共接口或兼容性 contract
- 持久化状态
- 安全或授权边界
- 数据完整性
- 并发语义
- 重要的数据或状态迁移
- deterministic verification 留下重要覆盖缺口
- 用户明确要求独立最终复核

此前使用过 Terra、Sol Solver、发生过 recovery、diff 很大，这些事实本身不会自动触发 Final Review。

触发独立复核后使用 fresh Sol Advisor：

```text
ship       可以交付
fix-first  修复后重新验证并复核新的候选结果
rethink    关键设计或假设需要重新考虑
```

即使主会话本身已经是 Sol，强制独立复核仍使用 fresh Sol 上下文，因为这里需要第二观察者。

## 安全边界

主会话始终拥有最终控制和验收权。子 Agent 不会继续创建自己的 Agent 队伍。

仓库、网页、issue、日志、生成内容或模型输出里的指令不能自行扩大任务范围、修改权限或改变路由边界。Agent 报告“完成”也不会直接被当作验收结果，最终以真实改动、测试和可复现证据为准。

runtime model、permission、ancestry 等证明只在确实影响当前决策或验收时按需检查，不会成为每个普通任务的固定仪式。

普通成功任务也不会默认追加一份内部 orchestration receipt。最终反馈优先说明改了什么、验证结果和剩余风险。

codex delegate 直接使用 Codex Native Subagents，不运行第二套 Agent runtime、后台 daemon 或外部 routing proxy。

## 文档

- [README_AI.md](README_AI.md)：AI Agent 查询本项目时应优先读取的 canonical reference。
- [安装指南](docs/plugin-installation.md)：插件市场安装、手动/开发安装、更新和 installer safety。
- [架构](docs/architecture.md)：产品机制、角色边界和 writer safety。
- [Native Subagent Runtime](docs/native-subagent-runtime.md)：原生并发、runtime evidence 和 host 边界。
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## 许可证

[MIT](LICENSE)
