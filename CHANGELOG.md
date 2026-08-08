# Changelog

本文件记录 subagents-dispatch 的重要变更。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [Unreleased]

### Changed

- Quick Start 改为“只读职责可并行，一个 Worker 统一写入”，与单 checkout 单写入者约束保持一致

### Removed

- 删除无人使用的 legacy current-lock 常量
- 删除过时且重复的 `CLAUDE.md` 工程说明，工程入口继续由 `README_AI.md` 和 canonical owner 文档维护

## [2.1.0] - 2026-08-07

### Added

- **运行中控制面**：`/dispatch preview`、`/dispatch status`、`/dispatch steer`、`/dispatch takeover` 四个命令，支持执行前预览、执行中监控、实时指导和职责接管
- **Handoff Capsule**：证据绑定的交接包，包含 `ACCEPTED FACTS`、`DO NOT REDO`、`STALE IF` 等语义字段，减少子 Agent 间的重复发现
- **执行摘要**：任务结束时附加一行事实性摘要，报告角色、重试、复核状态，不暴露推理过程
- **四条核心约束**明确文档化：一个写入者、一层委托深度、UNKNOWN 不猜测、摘要只报事实

### Changed

- README 重写为直接人类语音风格，去除 AI 写作痕迹
- 补充所有 README 的卸载说明

## [2.0.0] - 2026-07-22

### Changed

- **产品重命名**：从 Codex Delegate 更名为 subagents-dispatch
- **插件迁移到根目录**：遵循 Codex Marketplace 标准布局
- **旧版迁移工具**：支持从 codex-delegate 自动迁移，含回滚机制

### Added

- **Doctor 技能**：安装诊断、配置检查、插件升级
- **Legacy Migration**：两阶段迁移，支持事务回滚

## [1.2.0] - 2026-07-15

### Added

- **发布门控**：强化的发布候选验证流程
- **Final Review Gate**：基于后果触发的独立复核机制

### Fixed

- 跨代安装器状态序列化
- 旧版迁移事务硬编码

## [1.1.0] - 2026-06-28

### Added

- **编排恢复**：TeamPlan 验证器和有界恢复合约
- **Recovery Ledger**：原生恢复状态验证
- **TeamPlan**：多职责并行时的依赖 DAG 协调

### Changed

- 路由策略与当前 MultiAgentV2 合约对齐
- 原生能力和上下文 fork 规则强化

## [1.0.0] - 2026-06-15

### Added

- **正式发布**：完整的五角色 Agent 团队
- **Final Review**：风险触发的独立复核
- **运行时保障**：从运行时保障到运行时真相的演进
- **一键安装器**：Skill 和锁定 Agent profiles 的确定性安装

### Changed

- 锁定路由 profiles 成为默认安装路径

## [0.10.0] - 2026-06-01

### Added

- **自适应委派合约**：渐进式扇出，无固定波次
- **确定性辅助工具**：install-agents.py、validate_team_plan.py 等

## [0.9.1] - 2026-05-20

### Added

- **路由验证**：路由行为评估 schema 和用例
- **策略回归套件**：策略文档和运行时合约回归覆盖

## [0.8.0] - 2026-05-10

### Added

- **Routing V4**：精确路由绑定和动态团队选择
- **Sol 判断耦合求解器**：实现过程中需要判断的工作
- **主会话路由证据**：路由事实的三层分离（requested/accepted/observed）

### Changed

- 路由绑定从观察到精确
- 团队选择从静态到动态

## [0.5.0] - 2026-04-15

### Added

- **渐进任务包**：自适应扇出调度
- **安全策略**：权限、变更权限、写入安全
- **同意策略**：用户授权和信任边界
- **路由策略**：角色选择和职责分配

## [0.3.0] - 2026-03-20

### Added

- **核心 Skill**：Codex Agent Team 主技能
- **Agent Profiles**：Luna Worker、Luna Explorer、Terra Reviewer
- **Skill UI 元数据**：插件清单和市场注册

## [0.1.0] - 2026-03-01

### Added

- 项目初始化
- 架构文档
- 贡献指南和安全策略
- CI 工作流和测试配置

---

## 版本说明

- **主版本 (X.0.0)**：重大架构变更或产品重命名
- **次版本 (0.X.0)**：新功能或重要改进
- **修订版本 (0.0.X)**：Bug 修复和小改动

## 链接

- [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
- [语义化版本](https://semver.org/lang/zh-CN/)
