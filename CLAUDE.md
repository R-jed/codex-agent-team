# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Codex 子代理调度框架 — 一个 Codex 插件，让主会话按需分配任务给专门的子 Agent（Reader、Worker、Solver、Investigator、Advisor），而非自己完成所有工作。

## Commands

```bash
# 测试（必须用 venv 的 pytest，系统 pytest 缺少依赖）
.venv/bin/pytest                        # 全部测试
.venv/bin/pytest tests/test_policy.py   # 单个文件
.venv/bin/pytest -k "test_name"         # 按名称筛选

# Agent 安装
python scripts/install-agents.py
python scripts/install-agents.py --check  # 仅校验，不修改

# 验证
python scripts/validate_team_plan.py <plan.json>
python scripts/validate_team_ledger.py <ledger.json>
python scripts/runtime-evidence.py <evidence.json>
python scripts/review-artifact.py     # 生成候选交付物的确定性身份

# Doctor 诊断
python scripts/doctor.py
```

## Architecture

**插件结构：** Codex Marketplace 插件，通过 `.codex-plugin/manifest.json` 注册，skills 定义在 `skills/` 下。

**核心流程：**
- `skills/dispatch/SKILL.md` — 主委托 skill，决定任务分配策略与交互控制入口
- `skills/dispatch/agents/` — 子 agent 的 prompt 定义
- `skills/dispatch/references/` — 运行规则参考文档（router-core、team-plan、recovery、guardrails、final-review、interaction、handoff-capsule）
- `skills/doctor/` — 安装诊断与配置检查

**Agent 角色（定义在 `agent-profiles/`，角色/模型/effort 由 `policy-contract.json` 机器可读约束）：**
- Luna Reader: 读代码、追调用链（gpt-5.6-luna, max）
- Luna Worker: 写实现、修 bug（gpt-5.6-luna, max）
- Sol Solver: 复杂判断任务（gpt-5.6-sol, high）
- Terra Investigator: 大范围调查（gpt-5.6-terra, xhigh）
- Sol Advisor: 技术判断与复核（gpt-5.6-sol, high）

**交互控制（2.1 新增）：**
- `/dispatch preview <task>` — 非执行预测，不触发子 agent
- `/dispatch status` — 单次状态快照
- `/dispatch steer <unit_id>: <guidance>` — 向当前执行中的子 agent 提供引导
- `/dispatch takeover <unit_id>` — 主会话接管指定职责

**安全约束（`policy-contract.json`）：**
- 主会话持有用户目标和权限，子 agent 不能自建团队
- 同一 Git checkout 同一时间只有一个写入者
- Agent 声称"完成"必须有文件/测试证据支撑
- UNKNOWN 状态不等于 FAILED，不授权创建替代任务

## Testing

测试在 `tests/`，用 pytest。覆盖：策略合规、安装安全、运行证据、review artifact、交互策略、handoff capsule 等。测试数据 fixture 在 `evals/`。

## Key Files

- `policy-contract.json` — 机器可读的角色定义与核心约束（含 model_aliases、final_review trigger codes）
- `scripts/install-agents.py` — Agent profile 安装器（含 `--check` 校验模式）
- `scripts/review-artifact.py` — 为 Final Review 生成候选交付物的确定性身份
- `scripts/doctor.py` — 诊断脚本
- `evals/` — 静态与行为评估数据
