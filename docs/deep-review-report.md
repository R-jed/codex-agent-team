# subagents-dispatch 全库 Deep Review 报告

> 审查时间：2026-08-07
> 审查范围：全库只读审查（源码 + 测试 + 文档 + 安全 + 打包）
> 审查方法：3 并行 agent 分维度审查 + 对抗性验证 agent 交叉检验
> 当前分支：main，与 origin/main 同步（0 ahead, 0 behind）
> 未合并分支：origin/feat/thin-coordination-hardening（+2 commits，已 merge main 但未 push）

---

## 一、项目概况

| 维度 | 数据 |
|------|------|
| 源码文件 | 7 个 Python 脚本，2,378 行 |
| 测试文件 | 26 个，3,312 行 |
| 插件目录 | plugins/subagents-dispatch/（原 codex-delegate 重命名） |
| Skills | dispatch + doctor |
| Evals | routing-cases, coordination-cases, behavioral-workloads, runtime-assurance-cases |
| CI | .github/workflows/ci.yml（pytest + codex 官方 validator） |

---

## 二、源码 Bug 审查

### 已确认的真实问题

| 文件 | 行号 | 严重性 | 问题 | 证据 |
|------|------|--------|------|------|
| `legacy_migration.py` | L217 | Low | `target.unlink()` 无 `missing_ok=True`，TOCTOU 竞态可导致 FileNotFoundError | L208 `if not target.exists()` 与 L217 `target.unlink()` 之间存在竞态窗口 |
| `legacy_migration.py` | L59-60 | Low | `load_legacy_manifest` 静默返回 None，损坏 manifest 被当"无 manifest" | 调用方还有 `legacy_profiles_exist` 二次检测，实际影响有限 |
| `legacy_migration.py` | L99-100 | Low | `detect_legacy_state` 静默跳过损坏的 current manifest | 防御性设计，损坏 manifest 不应被信任，但可能触发不必要的重迁移 |
| `install-agents.py` | L246-247 | Low | `parse_profile_name` 解析失败返回 None，`None in current_roles` 永远为 False | 损坏 TOML 文件的角色名冲突检查被绕过，但后果是覆盖写入正确内容 |

### 被推翻的发现

| 原始发现 | 推翻原因 |
|----------|----------|
| `install-agents.py` L182 `profile_hashes` 默认 `{}` 绕过检查 | `manifest_hashes()` 在 manifest=None 时返回 `{}` 是首次安装的正确行为；`load_manifest` 已有 `isinstance` 校验 |
| `install-agents.py` L443 rollback() 异常处理缺陷 | `Path.unlink()` 和 `Path.rename()` 只抛 `OSError` 及子类，不存在非 OSError 异常吞掉原始异常的情况 |
| `pre-push-ci.sh` curl\|bash 无完整性校验 | **文件定位错误**。该脚本无任何 curl/wget 调用，仅做本地检查 |

---

## 三、测试质量审查

### 3.1 函数级覆盖率

| 源码脚本 | 函数数 | 测试引用数 | 覆盖率 |
|----------|--------|-----------|--------|
| doctor.py | 5 | 1 | 20% |
| install-agents.py | 24 | 7 | 29% |
| legacy_migration.py | 7 | 0 | **0%** |
| review-artifact.py | 14 | 3 | 21% |
| runtime-evidence.py | 22 | 5 | 23% |
| validate_team_ledger.py | 6 | 1 | 17% |
| validate_team_plan.py | 8 | 1 | 12% |

**关键发现**：`legacy_migration.py` 的 359 行测试全部通过 subprocess 调用 CLI，零个函数被直接测试。`sha256_bytes`、`load_legacy_manifest`、`detect_legacy_state`、`collect_legacy_files`、`can_safely_remove_legacy`、`migrate_legacy_to_current`、`format_migration_state` 共 7 个函数 + 2 个类（`LegacyManifest`、`MigrationState`）无任何单元级覆盖。

### 3.2 系统性测试架构问题

| 问题 | 影响范围 | 严重性 |
|------|----------|--------|
| **全部 26 个测试文件仅用 subprocess** | 全库 | Medium |
| **14/26（54%）测试文件零错误路径测试** | 全库 | Medium |
| **无 conftest.py 或共享 fixture** | 全库 | Medium |
| **无直接 import 模块的单元测试** | 全库 | Medium |

subprocess-only 测试模式导致：
- 无法测试内部函数的边界条件
- 测试执行慢（每测试启动新 Python 进程）
- 失败堆栈不透明（困在子进程 stdout/stderr 中）
- 无法做 mock/stub 来隔离依赖

### 3.3 缺少错误路径测试的文件（14/26）

```
test_behavioral_evals.py, test_capability_dedup.py, test_concurrency_policy.py,
test_coordination_policy.py, test_final_review_consent.py, test_installer_safety.py,
test_legacy_migration.py, test_official_plugin_compliance.py, test_plugin_packaging.py,
test_policy.py, test_readme_user_facing.py, test_runtime_truth_policy.py,
test_review_artifact.py, test_runtime_assurance.py
```

---

## 四、安全审查

### 4.1 正面发现

| 安全措施 | 覆盖情况 |
|----------|----------|
| subprocess 使用列表参数（非 shell=True） | ✅ 全部脚本 |
| 文件锁（fcntl/msvcrt） | ✅ install-agents.py |
| 符号链接检查（is_symlink） | ✅ install-agents.py |
| 原子写入（mkstemp + fsync + os.replace） | ✅ install-agents.py |
| 无 eval()/exec() | ✅ 全部脚本 |
| 无硬编码密钥/token | ✅ 全库 |
| 无网络调用 | ✅ 全部脚本 |
| YAML 使用 tomllib（标准库安全解析器） | ✅ |
| JSON 使用 json.loads() | ✅ |
| skills/ 目录无可执行代码 | ✅ |
| SECURITY.md 定义安全关注领域 | ✅ |

### 4.2 需关注项

| 文件 | 严重性 | 问题 |
|------|--------|------|
| `.github/workflows/ci.yml` | Low | `python -m pip install -r requirements-dev.txt` 无 hash 校验，版本范围未锁定 |
| `.github/workflows/ci.yml` | Low | 下载远程 Python 脚本后执行，虽有 SHA pin 但无 post-download hash 校验 |
| `scripts/pre-push-ci.sh` | Low | 使用 ImageMagick `import` 命令（L15），可能与系统工具名冲突 |

---

## 五、架构审查

### 5.1 设计评估

| 维度 | 评价 |
|------|------|
| 关注点分离 | ✅ 良好。脚本职责清晰：install/migrate/validate/doctor/review |
| 数据流 | ✅ 清晰。manifest 文件作为单一事实来源 |
| 安全边界 | ✅ guardrails.md 定义了全面的 mutation authority 分级 |
| 扩展性 | ⚠️ 新增 agent profile 需修改多处（TOML + SKILL.md + openai.yaml） |

### 5.2 代码重复

`legacy_migration.py` 和 `install-agents.py` 都有 manifest 加载逻辑，错误处理策略不一致：
- `install-agents.py:load_manifest` — 损坏 manifest 调用 `fail()` 退出
- `legacy_migration.py:load_legacy_manifest` — 损坏 manifest 静默返回 None

建议统一 manifest 加载行为或提取共享模块。

---

## 六、文档审查

| 维度 | 状态 |
|------|------|
| 三个 README（CN/EN/AI）内容一致性 | ⚠️ 未完全同步 |
| 架构文档 vs 实际代码 | ✅ 一致 |
| plugin.json 路径声明 | ✅ 正确 |
| CI 流程文档 | ⚠️ 无独立文档，仅在 README 简述 |

---

## 七、未合并分支状态

`origin/feat/thin-coordination-hardening`（+2 commits）：
- 已在本地 merge main 并解决冲突，但未 push
- 路径已从 `codex-delegate` 更新为 `subagents-dispatch`
- 包含 6 个协调策略 eval 用例 + 7 个测试函数

---

## 八、优先级排序

### P0 — 需要修复

1. **测试质量系统性重构**：从纯 subprocess 集成测试转向直接 import 单元测试，至少覆盖核心函数的边界条件和错误路径
2. **`legacy_migration.py` 函数级测试**：当前 0% 覆盖率不可接受，7 个函数 + 2 个类无任何单元测试

### P1 — 建议修复

3. **`legacy_migration.py` L217 TOCTOU**：`target.unlink(missing_ok=True)` 一行修复
4. **共享 manifest 加载模块**：统一 install-agents 和 legacy_migration 的 manifest 处理策略
5. **添加 conftest.py**：提取共享 fixture，减少测试代码重复

### P2 — 可选优化

6. **CI pip hash 校验**：对 requirements-dev.txt 添加 hash
7. **README 三版本同步**
8. **push feat/thin-coordination-hardening 分支**

---

## 九、对抗性验证统计

| 类别 | 数量 |
|------|------|
| 原始发现总数 | 10 |
| 确认（CONFIRMED） | 5 |
| 存疑（PLAUSIBLE） | 2 |
| 推翻（DEBUNKED） | 3 |
| 新发现（遗漏） | 3 |

推翻率 30% — 原始审查存在误判，主要集中在对 Python 标准库行为的误解（Path 方法异常类型、首次安装语义）和文件定位错误。
