<p align="center">
  <img src="plugins/codex-delegate/assets/codex-delegate-logo.svg#gh-light-mode-only" alt="codex delegate" width="112">
  <img src="plugins/codex-delegate/assets/codex-delegate-logo-dark.svg#gh-dark-mode-only" alt="codex delegate" width="112">
</p>

<h1 align="center">codex-delegate-Plugin</h1>

<p align="center"><strong>一个Codex subagents框架。</strong></p>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="README_AI.md">AI Agent</a> · <a href="docs/plugin-installation.md">安装</a> · <a href="docs/architecture.md">架构</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.2.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/Codex-%E5%8E%9F%E7%94%9F%20Subagents-111827.svg" alt="Codex 原生 Subagents">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

> **If you are an AI Agent, jump to [README_AI.md](README_AI.md) and follow the instructions strictly.**

codex delegate 是一个 Codex Plugin。用户只需要给出开发目标，当前主会话负责判断哪些工作自己完成、哪些值得交给专门的 Agent，并负责最后的整合、验证和交付。

你不需要自己挑模型，不需要规定 Agent 数量，也不需要设计 Luna、Terra、Sol 的执行顺序。

## 安装

### 方式一：Codex 插件市场

1. 在 Codex 中打开 **Plugins**。Codex CLI 也可以输入 `/plugins`。
2. 搜索 `codex-delegate`。
3. 打开 **Codex Delegate**，点击 `+` 安装。
4. 安装后开启新的 Codex 会话。

### 方式二：命令行

```bash
codex plugin marketplace add R-jed/codex-delegate@main \
  --sparse .agents/plugins \
  --sparse plugins/codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

安装后开启新的 Codex 会话。

## 开始使用

直接把任务交给 Plugin：

```text
$codex-delegate:codex-delegate 深度检查这个改动，修复发现的问题并运行相关测试。
```

也可以输入 `/skills` 打开 Skill 选择器。Plugin 默认不会隐式触发。

## 更新

### 插件市场

打开 **Plugins**，在已安装插件中找到 **Codex Delegate** 并安装可用更新，然后开启新的 Codex 会话。

### 命令行

```bash
codex plugin marketplace upgrade codex-delegate && \
codex plugin add codex-delegate@codex-delegate
```

更新后开启新的 Codex 会话。

## 它怎么带队

主会话始终是技术负责人。它先判断任务是否真的需要委托，再为清楚、独立、当前可以推进的责任选择合适角色。

| 角色 | 主要工作 |
| --- | --- |
| Luna Reader | 读代码、追调用链、找测试、收集事实，不改文件 |
| Luna Worker | 完成需求和边界已经明确的实现、修复和测试 |
| Sol Solver | 处理实现过程中仍需要持续技术判断的复杂工作 |
| Terra Investigator | 做更大范围的只读技术调查和证据整理 |
| Sol Advisor | 做重要技术判断，或对高影响结果进行独立复核 |

有些任务完全由主会话完成，有些任务会同时使用多个 Agent。codex delegate 不预设固定 Agent 数量，也不会为了填满并发额度而创建 Agent。

任务之间存在依赖时，主会话负责决定启动顺序、写入范围和最终整合。修改不同文件也不自动等于可以安全并行。

## 安全边界

- 主会话始终负责用户目标、权限、团队组成、结果验收和最终回复。
- 子 Agent 不能继续创建自己的 Agent 团队。
- 同一个实际 Git checkout 同一时间只允许一个写入者。
- 子 Agent 不能自行扩大权限、修改范围或外部影响。
- Agent 自己说“完成了”不算验证，最终以实际文件、代码和测试结果为准。
- codex delegate 直接使用 Codex 原生 Subagents，不运行独立 Agent runtime、后台 daemon 或外部路由服务。

更完整的协调、恢复、运行证据和独立复核规则见 [架构说明](docs/architecture.md)。

## 项目结构

```text
.
├── .agents/plugins/                  # Codex Marketplace 注册
├── plugins/codex-delegate/           # 可安装的 Plugin 包
│   ├── .codex-plugin/                # Plugin manifest
│   ├── agent-profiles/               # 五个原生 Subagent 配置
│   ├── assets/                       # Plugin 图标与 README Logo
│   ├── policy-contract.json          # 机器可读的角色与核心约束
│   ├── scripts/                      # 确定性校验器与运行证据工具
│   └── skills/codex-delegate/
│       ├── SKILL.md                  # Plugin 入口与主控制循环
│       └── references/               # 路由、TeamPlan、恢复、安全与 Final Review
├── docs/                             # 安装、架构与运行边界文档
├── evals/                            # 静态与行为评估数据
├── scripts/                          # 仓库级验证工具
└── tests/                            # 回归、打包与跨平台测试
```

Plugin 的运行核心集中在 `plugins/codex-delegate/`。根目录的 `docs/`、`evals/`、`scripts/` 和 `tests/` 主要服务于说明、验证和发布质量。

## 文档

- [安装](docs/plugin-installation.md)
- [架构](docs/architecture.md)
- [Codex 原生 Subagent 运行边界](docs/native-subagent-runtime.md)
- [AI Agent 项目参考](README_AI.md)
- [Privacy Policy](PRIVACY.md) · [Terms of Use](TERMS.md)

## 许可证

[MIT](LICENSE)
