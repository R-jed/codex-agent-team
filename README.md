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
  <img src="https://img.shields.io/badge/status-pre--v1-orange.svg" alt="Status">
</p>

Codex Delegate 是 **Codex Native Subagents 之上的委派策略层**。主会话继续掌握目标、架构、决策和最终验收；只有真正适合分出去的责任才交给子 Agent。

当前版本：`0.6.0`，pre-v1。

## 1. 它解决什么问题

Codex 已经具备原生 Subagent 和并行能力。真正影响复杂任务质量和效率的，是主会话如何使用这些能力：

- 哪些工作值得委派；
- 哪些依赖可以并行，哪些必须串行；
- 如何避免多个 Agent 重复搜索或重复实现；
- 失败后应该继续、修合同、换干净上下文，还是升级技术调查；
- 什么时候值得付出一次独立 Sol 复核的成本；
- 如何让实际 diff、测试和运行证据决定是否完成。

Codex Delegate 把这些决策统一放在当前主会话中。它没有固定 Agent 数量，也没有强制 `Luna -> Terra -> Sol` 流水线。

```text
用户目标
  ↓
主会话建立未解决依赖
  ↓
找出当前 ready frontier
  ↓
只委派有明确收益、边界可验收的责任
  ↓
并行执行安全且互不依赖的工作
  ↓
谁先完成，就先合并谁的证据并重新计算 frontier
  ↓
必要时恢复、技术升级或独立复核
  ↓
主会话验收实际交付物
```

一个简单修改可以使用 `0` 个 Subagent。复杂任务也不会为了“组队”而机械调用所有模型。

## 2. 安装

Codex Delegate 只通过 Codex 原生 Plugin 系统分发。

首次安装：

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team

codex plugin add codex-agent-team@codex-agent-team
```

安装后启动一个新的 Codex thread，然后直接使用：

```text
/codex-delegate 修复这个 bug，并运行相关测试。
```

已有安装更新：

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

更新后同样启动新的 Codex thread。

### 第一次需要模型专用 Agent 时

Plugin 负责分发 Skill 和项目文件。四个自定义 Agent profile 属于 Codex 的独立配置表面，默认位于：

```text
$CODEX_HOME/agents
```

通常就是 `~/.codex/agents`。

Codex Delegate 不会在 Plugin 安装时静默写入 profile。只有当前任务真的需要某个专用角色且 profile 尚未准备好时，Skill 才会说明管理范围并请求授权。

Installer 只管理四个 Codex Delegate profile 和自己的 ownership manifest，不修改凭据、MCP、仓库、`config.toml` 或无关 Agent profile。Plugin manifest 不声明不存在的 `agents` 组件。

完整安装、迁移和失败处理见 [Plugin Installation](docs/plugin-installation.md)。

## 3. 角色与责任

| 角色 | 当前模型 | 主要职责 |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | 搜索、调用链、测试映射、证据收集 |
| Luna Worker | GPT-5.6 Luna `max` | 有边界的实现、调试、测试和局部重构 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | 解决真正未完成的复杂技术 delta |
| Sol Advisor | GPT-5.6 Sol `high` | 高价值判断、选择性复核、风险触发的独立最终复核 |

角色代表责任，模型代表计算资源。更强的模型不会自动获得更大的产品、架构、权限或 scope 决策权。

主会话会先把任务整理成仍未解决的依赖。写入型责任只有在范围、接口、不变量、决策权、验收条件和验证方式足够清楚时才交给 Worker。

## 4. 并发与实际性能

用户不需要手工告诉 Codex “这里开两个 Agent、那里并行三个任务”。正常情况下，你只需要把**目标、不能破坏的约束和成功标准**说清楚。Codex Delegate 负责识别当前哪些依赖已经 ready，以及并行是否真的有价值。

它采用 completion-driven 的 ready-frontier 策略：

```text
启动当前安全且有价值的 ready work
        ↓
某个 child 先完成
        ↓
立即检查结果、合并证据、关闭已完成 child
        ↓
重新计算 ready frontier
        ↓
有空闲 slot 且存在新的 ready dependency
        ↓
立即补位，而不是等待整批 child 全部结束
```

只有存在真正的 join dependency，或者当前 Codex runtime 只能提供更粗粒度的等待能力时，才需要 barrier wait。

因此，图里“性能主要取决于怎么写 prompt”的说法不够完整。Prompt 清晰度会影响需求理解和依赖拆分，但 wall-clock 性能还取决于：

- 任务本身是否存在独立依赖；
- 主会话是否采用 completion-driven 调度而不是无必要的整批等待；
- Native Codex 当前实际提供多少 child capacity 和完成通知能力；
- 是否存在写入冲突或必须串行的 critical path；
- 不同模型和验证步骤的真实延迟；
- 是否出现重复 discovery、重复 inference 或无效 recovery。

如果任务只有一条严格串行的关键路径，增加 Agent 不会让它自动变快。并行真正有价值时，插件应该自己识别并使用，而不是把并行拆解工作转嫁给用户。

显式调用 `/codex-delegate` 后，普通资源包络允许最多两个同时活跃、且有明确理由的 child，无需再次询问。这个 `2` 是 consent boundary，不是固定团队规模或产品硬上限。更大的并行 fan-out 在得到授权后仍由 ready dependencies、workspace safety 和 native runtime capacity 决定。

一个 physical checkout 同时最多只有一个写入 Worker。真正的多 Writer 并发需要隔离的 worktree / workspace。

## 5. 失败、恢复与 Final Review Gate

未通过验收和需要改变执行方式是两个不同判断。

只要新证据仍在缩小问题，当前责任可以继续。出现无效重复后，主会话才通过 Intervention Gate 分类处理：

```text
局部机械问题
-> Luna 做有明确修正假设的针对性修复

合同缺口
-> 主会话修合同

上下文污染或重复失败
-> 保留 artifact、有效证据和 Recovery Ledger，启动干净的同级上下文

真实技术能力缺口
-> Terra 只接收 unresolved technical delta

高价值判断缺口
-> 主会话决定，或在有价值时使用 Sol
```

没有固定重试次数，也不会因为 Luna 一次失败就把整个任务交给 Terra 重做。

### 高风险改动的最终质量门

Sol 不是所有任务的固定阶段。普通低风险修改可以在主会话检查实际 diff 并完成确定性验证后结束。

当改动实质涉及 public contract、persistent state、security / authorization、data integrity、concurrency、migration、wide blast radius，或者发生 material Terra escalation、material recovery、重要 verification gap，Final Review Gate 可以变为 `required`。

此时主会话只能先进入：

```text
Candidate Ready
```

当前候选会绑定一个确定性的 `review_artifact_id`，再由 fresh-context Sol Advisor 独立复核。

```text
ship       -> 当前 artifact 可以完成
fix-first  -> 修复、重新验证、生成新 artifact，再做新的 fresh review
rethink    -> 关键架构、合同或假设需要重新处理
```

`INSUFFICIENT_EVIDENCE` 表示证据不足，gate 仍未满足。任何交付物在 `ship` 后发生变化，旧 verdict 都会失效。

## 6. 安全与当前边界

Codex Delegate 的核心安全规则是：

- 主会话始终拥有最终控制和验收；
- delegation depth 固定为 `1`，child 不再创建自己的 Agent 团队；
- 一个 physical checkout 最多一个写入 Worker；
- 用户或其他会话已有修改必须保留；
- repository、网页、日志、issue、生成内容和模型输出中的指令都不能改写 scope、permission、route、consent 或 orchestration policy；
- profile 中的 `read-only` 是配置意图，需要硬隔离时必须依赖实际 runtime permission evidence；
- Agent 的“完成”报告只是 claim，实际 artifact、diff、测试和可复现证据才是验收依据。

Codex Delegate 本身不实现第二套 Agent runtime、后台 scheduler、全局 DAG 服务或外部 routing proxy。并发执行依赖 Codex Native Subagents；Codex Delegate 负责决定**哪些工作值得并发、什么时候补位、什么时候必须等待**。

`0.6.0` 仍处于 pre-v1。静态 CI、Plugin validation 和 profile lifecycle 已通过；精确 live route、跨会话 writer safety、installer concurrency、completion-driven scheduling 行为和 Final Review lifecycle 仍需要在当前真实 Codex runtime 上完成 release validation。

## License

[MIT](LICENSE)
