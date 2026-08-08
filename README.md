<p align="center">
  <img src="assets/subagents-dispatch-logo.png" alt="subagents-dispatch" width="112">
</p>

<h1 align="center">subagents-dispatch</h1>

<p align="center"><em>一个指令，多人并行，结果可控。</em></p>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">安装</a> · <a href="docs/architecture.md">架构</a> · <a href="LICENSE">MIT</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-%E5%8E%9F%E7%94%9F%20Subagents-111827.svg" alt="Codex 原生 Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

---

> **如果你是 AI Agent，请跳转到 [README_AI.md](README_AI.md) 并严格按照说明操作。**

## 快速开始

你让 Codex 改一个 API 接口并加测试。

没有 subagents-dispatch，主会话一个人干：先读代码，再改实现，最后写测试。一步一步来。

有了 subagents-dispatch：

```
/dispatch 给 /api/users 加分页参数，补上测试
```

Main 可以先让两个只读 Reader 分别查现有实现和相关测试，这两个职责可以并行。证据收齐后，由一个 Worker 统一修改实现和测试，Main 最后验收。

## 运行中控制

执行前预览分工方案：

```
/dispatch preview 给 /api/users 加分页参数，补上测试
```

执行中查看状态：

```
/dispatch status
```

给正在跑的 Agent 补充指导：

```
/dispatch steer U2: 先看现有的分页中间件
```

拿回控制权：

```
/dispatch takeover U2
```

## 执行摘要

启动过子 Agent 的任务，结束时附一行摘要：

```
Dispatch: Reader 查代码 -> Worker 实现 · 未重试 · 无需 Final Review
```

摘要只报可验证的事实，不暴露推理过程。

## Handoff Capsule：减少重复扫描

每个子 Agent 使用全新上下文。Handoff Capsule 用一个很小的、证据绑定的交接包减少重复 discovery。

- **传递已验证的事实**：只把 Main 已经检查并接受的事实传给下一个职责
- **明确 `DO NOT REDO`**：已有有效证据的扫描可以标记为无需重复
- **Main 是验收边界**：子 Agent 的自我声明不能直接成为已知事实
- **自带 `STALE IF` 条件**：文件变化可以使旧证据失效

## 四条核心约束

不管任务拆成多少职责，这四条规则始终成立：

- **一个写入者** — 同一次 subagents-dispatch 调度内，同一 Git checkout 同一时间最多一个写入者，写入者只能是 Main、Worker 或 Solver。原写入者没有确认停止前，Main 不开始冲突写入。其他 Codex 会话、编辑器、hook 和外部进程不在这个保证范围内。
- **一层委托深度** — 子 Agent 不能再创建子 Agent。用户目标、权限、团队组成和最终结果始终由 Main 负责。
- **UNKNOWN 不猜测** — 状态不明就不乱动。不创建替代 Agent、不重试、不语义重路由。
- **摘要只报事实** — 不会根据模型名称或运行时长猜 Token 和费用。

## 角色

| 角色 | 干什么 |
|------|--------|
| Luna Reader | 读代码、追调用链、收集事实 |
| Luna Worker | 边界已经清楚的实现和测试 |
| Sol Solver | 实现过程中还要做判断的工作 |
| Terra Investigator | 大范围只读调查，整理证据 |
| Sol Advisor | 独立的技术判断或最终复核 |

简单任务主会话自己来。需要并行、隔离、专门能力或独立判断时才叫人。没有固定人数，没有固定流程。

## 安装

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

装完开新的 Codex 会话。首次需要 Agent 时，如果五个项目 Agent profiles 还没装，系统会说明要装什么、问你同意，然后自动装好。有些 Codex 版本装完后可能需要再开启一次新的 Codex 会话才能识别。

## 卸载

```bash
# 移除插件注册
codex plugin remove subagents-dispatch@subagents-dispatch
```

如果之前运行过需要 Agent 的任务，还需删除相关文件：

```bash
# 删除 5 个 Agent profile
rm ~/.codex/agents/subagents-dispatch-reader.toml
rm ~/.codex/agents/subagents-dispatch-worker.toml
rm ~/.codex/agents/subagents-dispatch-solver.toml
rm ~/.codex/agents/subagents-dispatch-investigator.toml
rm ~/.codex/agents/subagents-dispatch-advisor.toml

# 删除安装 manifest
rm ~/.codex/.subagents-dispatch-agents.json
```

## 更新

```bash
codex plugin marketplace upgrade subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

或者让 Doctor 来：

```
/doctor 升级 subagents-dispatch
```

更新后开新的 Codex 会话。

## 项目结构

```
.
├── .agents/plugins/                  # Codex Marketplace 注册
├── .codex-plugin/                    # 插件清单
├── agent-profiles/                   # 五个 Agent 配置
├── policy-contract.json              # 角色定义和核心约束
├── scripts/                          # 安装、校验、运行证据工具
├── skills/
│   ├── dispatch/                     # 主 Skill、交互控制、运行规则
│   └── doctor/                       # 安装诊断和升级
├── docs/                             # 架构和运行边界文档
├── evals/                            # 静态与行为评估数据
└── tests/                            # 回归测试
```

## 文档

- [安装](docs/plugin-installation.md)
- [架构](docs/architecture.md)
- [Codex 原生 Subagent 运行边界](docs/native-subagent-runtime.md)
- [AI Agent 项目参考](README_AI.md)

## 许可证

[MIT](LICENSE)
