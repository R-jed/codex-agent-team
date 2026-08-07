<p align="center">
  <img src="assets/subagents-dispatch-logo.svg#gh-light-mode-only" alt="subagents-dispatch" width="112">
  <img src="assets/subagents-dispatch-logo-dark.svg#gh-dark-mode-only" alt="subagents-dispatch" width="112">
</p>

<h1 align="center">subagents-dispatch</h1>

<p align="center"><strong>Codex 子代理调度框架。</strong></p>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">安装</a> · <a href="docs/architecture.md">架构</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-%E5%8E%9F%E7%94%9F%20Subagents-111827.svg" alt="Codex 原生 Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **如果你是 AI Agent，请跳转到 [README_AI.md](README_AI.md) 并严格按照说明操作。**

> **If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly.**

你给目标，主会话决定怎么做。简单的自己来，复杂的叫人帮忙，最后负责整合和验证。

## 效果对比

你让 Agent 做一个用户列表页面。没有 subagents-dispatch，它可能：

- 自己写所有代码
- 一个一个文件改
- 遇到问题卡住

有了 subagents-dispatch：

```text
/dispatch 实现用户列表页面，支持分页和搜索
```

主会话会：
1. 判断任务需要几个 Agent
2. 分配职责（读代码、写实现、跑测试）
3. 协调依赖，整合结果

## 安装

```bash
codex plugin marketplace add R-jed/subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

开启新的 Codex 会话即可使用。

## 使用

开发任务：

```text
/dispatch <你的任务描述>
```

诊断和维护：

```text
/doctor <诊断或维护请求>
```

Doctor 默认只读，不会主动修改状态。也可以输入 `/skills` 打开 Skill 选择器。

## 更新

```bash
codex plugin marketplace upgrade subagents-dispatch
codex plugin add subagents-dispatch@subagents-dispatch
```

也可以让 Doctor 执行升级：

```text
/doctor 升级 subagents-dispatch，并告诉我升级后还需要做什么。
```

## 工作原理

主会话是技术负责人，按需分配任务：

| 角色 | 干什么 |
|------|--------|
| Luna Reader | 读代码、追调用链、收集事实 |
| Luna Worker | 写实现、修 bug、跑测试 |
| Sol Solver | 处理需要持续判断的复杂工作 |
| Terra Investigator | 大范围技术调查 |
| Sol Advisor | 重要技术判断或独立复核 |

不是每个任务都需要 Agent。简单的主会话自己来，复杂的才会叫人。

## 安全规则

- 主会话负责用户目标、权限和最终结果
- 子 Agent 不能创建自己的团队
- 同一个 Git checkout 同一时间只有一个写入者
- Agent 说"完成"不算数，要看实际文件和测试结果

完整规则见 [架构说明](docs/architecture.md)。

## 项目结构

```text
.
├── .agents/plugins/                  # Codex Marketplace 注册
├── .codex-plugin/                    # Plugin manifest
├── agent-profiles/                   # 五个原生 Subagent 配置
├── assets/                           # Plugin 图标与 README Logo
├── policy-contract.json              # 机器可读的角色与核心约束
├── scripts/                          # installer、校验器与运行证据工具
├── skills/
│   ├── dispatch/                     # 主委托 Skill 与运行规则
│   └── doctor/                       # 安装、配置、profiles 与升级诊断
├── docs/                             # 安装、架构与运行边界文档
├── evals/                            # 静态与行为评估数据
└── tests/                            # 回归、打包与跨平台测试
```

## 文档

- [安装](docs/plugin-installation.md)
- [架构](docs/architecture.md)
- [Codex 原生 Subagent 运行边界](docs/native-subagent-runtime.md)
- [AI Agent 项目参考](README_AI.md)
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## 许可证

[MIT](LICENSE)
