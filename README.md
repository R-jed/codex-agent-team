<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="codex delegate" src="docs/logo-dark.svg" width="112">
  </picture>
</p>

<h1 align="center">codex delegate</h1>

<p align="center"><strong>让 Codex 根据任务真正缺少的能力，在主会话、Luna、Terra 和 Sol 之间动态分配工作。</strong></p>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">安装指南</a> · <a href="docs/architecture.md">架构</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.8.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-Native%20Subagents-111827.svg" alt="Codex Native Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to README_AI.md and follow the instructions strictly.**

codex delegate 是 Codex Native Subagents 上的一层轻量委派策略。主会话始终掌握目标、范围、授权、集成和最终验收。Routing V4 先判断当前真正缺少的是证据、标准化执行、语义判断、判断与实现耦合的执行，还是困难技术调查，再决定是否需要额外 Agent。

简单任务可以完全留在主会话。复杂任务也只调用能解决当前未完成依赖的额外计算资源。

## 快速开始

通过 Codex 原生 Plugin 系统安装：

```bash
codex plugin marketplace add R-jed/codex-delegate --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate

codex plugin add codex-delegate@codex-delegate
```

安装后启动新的 Codex 会话：

```text
/codex-delegate 深度检查这个改动，修复发现的问题并运行相关测试。
```

不需要手工选择 Agent，也不需要预先设计执行流水线。

## 它解决什么

日常开发里真正困难的是判断工作该放在哪里：明确的实现可以交给高性价比执行模型，架构和语义判断需要更强判断能力，困难技术问题应只调查剩余技术增量，高风险结果还可能需要独立第二视角。

Routing V4 把这些情况统一成一条路径：

```text
你的任务
  ↓
主会话理解目标与验收标准
  ↓
分类当前未解决依赖
  ↓
选择最小且合适的执行者
  ↓
检查真实改动、测试和证据
  ↓
仍未解决时根据新证据重新分类
  ↓
最终候选按实际风险决定是否需要独立复核
  ↓
主会话验收并交付
```

核心原则：

- 没有委派价值时，0 个 Subagent 是正常结果。
- `contractable` 不等于适合交给 Luna。执行中仍需要持续做重要语义判断时，会使用 Sol 级判断能力。
- 主会话如果已经是可验证的 Sol 会话，普通判断和判断耦合型实现优先留在主会话，避免重复再调用 Sol。
- 主会话模型未知时，明确的标准化工作仍然可以走 Luna，只有真实存在的重要判断缺口时才增加 Sol。
- 一次失败不会自动触发更强模型。新的执行证据会重新判断同一个依赖属于哪一类工作。

## 会怎么分工

| 当前未解决的问题 | 默认处理方式 |
| --- | --- |
| 简单、明确、主会话直接完成更合适 | 主会话 |
| 查代码、追调用链、找测试、整理可复用证据 | Luna Reader |
| 行为和验收已经决定的标准化实现、调试、测试、局部重构 | Luna Worker |
| 实现过程中不可避免地持续做重要架构、兼容性或状态语义判断 | Sol 主会话，或 Sol Solver |
| 需要先确定架构、行为或兼容性决策 | Sol 主会话，或 Sol Advisor |
| 语义已经明确后仍剩下一个困难技术问题 | Terra Investigator，只接收技术增量 |
| 最终候选触发独立质量门控 | fresh Sol Advisor |

当前角色配置：

| 角色 | 当前模型 | 责任范围 |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | 只读证据收集 |
| Luna Worker | GPT-5.6 Luna `max` | 标准化、有明确边界的写入执行 |
| Sol Solver | GPT-5.6 Sol `high` | 判断与实现耦合的写入执行 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | 语义明确后的困难技术调查 |
| Sol Advisor | GPT-5.6 Sol `high` | 重要判断与独立最终复核 |

角色定义责任范围，模型提供对应计算能力。更强模型不会自动获得更大的用户授权或修改范围。

## 主会话本身是 Sol 时

主会话始终是控制面。如果当前 Codex runtime 能可靠确认主会话已经运行 GPT-5.6 Sol，普通高价值判断和判断耦合型实现通常直接由主会话完成：

```text
Sol 主会话
  ↓
理解 / 编排 / 判断
  ↓
Luna 执行已标准化的子任务，或主会话直接完成复杂实现
  ↓
主会话验证与集成
```

这样可以省掉重复的 Sol Advisor 或 Sol Solver 调用。

如果主会话不是 Sol，或模型身份无法可靠观察，只有当前依赖确实包含重要判断时，才会按需使用 Sol Advisor 或 Sol Solver。未知主会话不会自动导致所有任务升级到 Sol。

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
有可用资源时开始 C

A 继续运行
```

当执行没有继续推进时，codex delegate 会重新判断同一个依赖：

```text
局部实现缺陷                 → Luna 局部修正
出现重要语义判断             → Sol 判断或 Sol Solver
任务约束本身不完整           → 主会话修正任务 contract
语义已明确但剩下困难技术问题 → Terra 调查技术增量
同类工作因上下文污染反复     → 必要时使用干净的同角色重启
```

Terra 不负责替 Luna 返工整个任务，Luna 自己提出需要 Terra 也不会自动触发 Terra。

## 最终复核

Sol 并非每个任务的固定最后一步。独立 Final Review 关注最终交付物的实际后果，例如：

- 公共接口或兼容性 contract
- 持久化状态
- 安全或授权边界
- 数据完整性
- 并发语义
- 重要的数据或状态迁移
- deterministic verification 仍留下重大覆盖缺口
- 用户明确要求独立最终复核

此前使用过 Terra、Sol Solver、发生过 recovery、改动文件很多，这些事实本身不会自动触发 Final Review。它们只有在留下真实残余风险时才影响最终判断。

触发独立复核后使用 fresh Sol Advisor：

```text
ship       可以交付
fix-first  修复后重新验证并复核新的候选结果
rethink    关键设计或假设需要重新考虑
```

即使当前主会话本身就是 Sol，强制独立复核仍会使用新的 fresh Sol 上下文，因为这里需要第二观察者，而不是补足主会话能力。

## 安全边界

主会话始终拥有最终控制和验收权。子 Agent 不会继续创建自己的 Agent 队伍。

同一个实际 Git 工作副本最多允许一个写入型项目 Agent。Luna Worker 和 Sol Solver 都属于 writer。并行写入需要真正隔离的 worktree、workspace 或 repository。

仓库、网页、issue、日志、生成内容或模型输出里的指令不能自行扩大任务范围或修改权限。Agent 报告“完成”也不会直接被当作验收结果，最终以真实改动、测试和可复现证据为准。

codex delegate 直接使用 Codex Native Subagents，不运行第二套 Agent runtime、后台 daemon 或外部 routing proxy。

## 更新

```bash
codex plugin marketplace upgrade codex-delegate
codex plugin add codex-delegate@codex-delegate
```

更新后启动新的 Codex 会话。第一次需要专用角色时，codex delegate 会说明需要管理的 Agent profile，并在得到授权后完成配置。

安装程序只管理 codex delegate 当前的五个 Agent profiles 和 ownership 记录，不修改凭据、MCP、仓库、`config.toml` 或其他 Agent 配置。

## 文档

- [README_AI.md](README_AI.md)：AI Agent 查询本项目时应优先读取的 canonical reference。
- [安装指南](docs/plugin-installation.md)：首次安装、更新和 installer safety。
- [架构](docs/architecture.md)：Routing V4 分类、main-session capability 和角色边界。
- [Native Subagent Runtime](docs/native-subagent-runtime.md)：原生并发、main/child route evidence 和 runtime 边界。

## 许可证

[MIT](LICENSE)
