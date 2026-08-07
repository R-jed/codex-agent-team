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

---

## 十、Release Candidate 对抗性复核与证据校正

> 本节优先级高于前文的 P0/P1/P2 排序。前文保留为第一轮本地审查记录，其中部分结论已被后续代码证据、GitHub Actions 原始日志和真实 Codex 运行界面推翻或重新定级。
>
> 当前目标不是创建 tag 或 GitHub Release。当前目标是把仓库收敛到一个可冻结的 Release Candidate SHA，并让所有 release gate 有可重复证据。

### 10.1 已推翻或重新定级的结论

1. `全部 26 个测试文件仅用 subprocess` 和 `无直接 import 模块的单元测试` 不成立。`tests/test_installer_concurrency.py` 已直接 import installer 并做 fault injection。测试方法应按风险选择，不能把 direct import 比例本身当 release blocker。
2. `scripts/pre-push-ci.sh` 使用 ImageMagick `import` 的结论不成立。当前脚本没有该命令。真正问题是它忽略核心测试并吞掉 pytest 原始退出状态，存在 false green。
3. `没有 conftest.py`、`共享 fixture 不足`、`direct unit test 比例低` 属于维护性问题。除非它们对应一个无法验证的高风险行为，否则不作为 release P0。
4. 用户调用命令已经由真实 Codex 运行界面验证。用户在命令选择器里看到 `Dispatch` 和 `Doctor`，实际用户入口是 `/dispatch` 和 `/doctor`。选择 `/dispatch` 后，Codex 会在 composer 中注入 namespaced prompt，例如 `/subagents-dispatch:dispatch ...`。因此必须区分：

```text
Plugin ID:          subagents-dispatch
Skill identity:     subagents-dispatch:dispatch / subagents-dispatch:doctor
User command:       /dispatch /doctor
Host namespaced use:/subagents-dispatch:dispatch /subagents-dispatch:doctor
```

不要把用户文档里的 `/dispatch`、`/doctor` 改回 `$...`。也不要机械地把 Plugin metadata 内部 namespaced identity 改成短命令。用户文档和 host/internal metadata 是两个 surface。

### 10.2 当前 release gate

当前状态判定：`NO-GO`。在下面的顺序收口完成前，不创建新的 version tag，不创建 GitHub Release。

| ID | 级别 | Gate | 当前判断 |
|----|------|------|----------|
| RC-01 | Blocker | 当前 HEAD GitHub Actions 全绿 | FAIL，最新 HEAD 有 pytest failure |
| RC-02 | Blocker | Marketplace source 与当前 OpenAI Plugin 子目录分发契约一致 | 待修复并重新验证 |
| RC-03 | Blocker | legacy codex-delegate 安装可通过正常升级路径安全收敛 | 未闭环 |
| RC-04 | Blocker | legacy/current installer 在迁移期不会并发修改同一 CODEX_HOME | 未证明 |
| RC-05 | Blocker | version identity 无冲突 | FAIL，GitHub 已存在 `v1.0.0`，其目标 commit 内 Plugin version 为 `2.0.0` |
| RC-06 | High | Doctor 只有一个 managed-profile 健康真相源 | 未满足，`doctor.py` 自己维护了一套较弱校验 |
| RC-07 | High | 本地 pre-push gate 不产生 false green | 未满足 |
| RC-08 | High | README / README_EN / README_AI / Doctor / install doc 使用同一安装契约 | 未满足 |
| RC-09 | Medium | release tree 不包含本地开发环境残留 | `skills-lock.json` 需确认用途 |
| RC-10 | Governance | `main` 的 release candidate 不会绕过 required CI | 当前 branch protection 未建立 |

### 10.3 顺序收口计划

以下顺序有依赖关系。不要并行修改相互拥有同一契约的文件，避免测试和文档跟着错误假设一起变绿。

#### 1. 固定用户命令与内部 Skill identity 的边界

用户面统一为：

```text
/dispatch <task>
/doctor <diagnostic or maintenance request>
```

`/skills` 保留为 Skill picker。

检查并修正 README、README_EN、安装文档等用户可见 surface，避免要求用户手动输入 `/subagents-dispatch:dispatch` 或 `/subagents-dispatch:doctor`。

Plugin manifest、Skill metadata、host 注入 prompt 中的 namespaced identity 不要因为用户入口变短而机械替换。以真实 Codex 安装后的 command picker 和 composer 行为作为 acceptance evidence。

#### 2. 修正 Marketplace 分发 source，并做真实安装 smoke test

重新核对当前 OpenAI Plugin 文档。Plugin 位于 `plugins/subagents-dispatch/` 子目录时，Marketplace source 必须使用当前平台支持的子目录 source contract，并明确 path。不要只验证 JSON syntax。

修改 `.agents/plugins/marketplace.json` 和对应 contract tests。测试必须验证平台语义，避免把实现对象原样复制为 expected JSON。

然后在干净 Codex 环境完成：

```text
add marketplace
install plugin
fresh session
command picker shows Dispatch and Doctor
/dispatch can be selected
/doctor can be selected
```

记录实际命令、Codex version、Plugin version 和结果。

#### 3. 把 legacy migration 接入正常升级流程

当前 `legacy_migration.py` 和 `--migrate-legacy` 只是底层能力。老用户不能依赖知道隐藏参数才能完成升级。

Doctor 的 upgrade/repair flow 必须显式检测 legacy state，并在需要 mutation 时通过 canonical installer migration path 完成迁移。普通 `--check` 继续保持只读，不暗中迁移。

必须覆盖：

```text
legacy only
current only
mixed
legacy modified
corrupt legacy manifest
partial legacy state
migration complete
```

#### 4. 建立跨代 installer 互斥

当前旧版本使用 `.codex-delegate-agents.lock`，新版本使用 `.subagents-dispatch-agents.lock`。仅检测或删除旧 lock 文件不能证明并发安全。

设计明确的 migration lock ordering。迁移期间必须保证旧 installer 和新 installer 不会同时修改同一 `CODEX_HOME/agents`。

新增真实 held-lock contention test。测试必须让另一个进程实际持有 legacy lock，再启动 migration，验证阻塞、失败关闭或其他明确的安全行为。只创建一个 lock 文件不算 contention test。

#### 5. 修正 legacy ownership 测试

`test_modified_legacy_profile_preserved` 当前 fixture 逻辑错误。它在修改 profile 后把修改后的 hash 写回 manifest，因此验证的是“manifest 拥有修改版本，可以删除”。

正确场景应为：

```text
legacy install writes file + manifest hash
user modifies file afterwards
migration sees current hash != ownership hash
modified legacy file is preserved
warning is emitted
current profiles are installed safely
rerun remains idempotent
```

同时补充 corrupt manifest、symlink、partial ownership 和 rollback failure 边界。

#### 6. 删除 Doctor 的第二套 managed-profile 真相源

`doctor.py --check` 不应自己维护一套弱化 profile validator。managed Agent profiles 的 exact health 由 `install-agents.py --check` 拥有。

Doctor 可以组合：

```text
installer exact verifier
legacy migration detector
Codex host / marketplace diagnostics
```

不要再通过只检查 TOML `name` 来声明安装 healthy。model、reasoning effort、sandbox、developer instructions 或 shipped bytes 被修改时，Doctor 必须和 installer 给出一致结论。

#### 7. 重构 pre-push gate，让它与 GitHub CI 同真相源

当前 `scripts/pre-push-ci.sh` 不得忽略 `tests/test_policy.py` 等核心测试，也不得通过 `|| true` 后解析文本来决定 pytest 是否成功。

目标：

```text
pytest nonzero => pre-push nonzero
collection error => pre-push nonzero
validator failure => pre-push nonzero
installer smoke failure => pre-push nonzero
all required checks pass => zero
```

优先让本地 gate 复用和 `.github/workflows/ci.yml` 相同的命令或同一个 repo-level verification script，减少两套 CI 逻辑漂移。

#### 8. 收敛安装与升级文档为一个 canonical contract

当前 README / README_EN / README_AI / Doctor SKILL / `docs/plugin-installation.md` 存在两套安装命令。

建立一个 canonical owner，并让其他文档引用或严格测试该 contract。至少统一：

```text
marketplace add
plugin add
upgrade
fresh session requirement
legacy upgrade handling
user command /dispatch
user command /doctor
/skills picker
```

测试不要只断言几个 substring 同时存在，因为两套相互冲突的命令也能通过这种测试。

#### 9. 清理 release tree 与低风险代码问题

确认 `skills-lock.json` 是否只是本地开发 Skill 管理器自动生成。如果它不是项目构建、测试或 Plugin runtime 的真实依赖，删除并加入适当 ignore，避免把维护者本机环境表达成项目依赖。

同时处理已确认低风险问题：

```text
legacy_migration unlink TOCTOU
corrupt manifest 处理策略
manifest loader 重复或不一致
requirements-dev 可复现性
```

不要为了“函数覆盖率”进行无边界测试重构。只对安全关键状态机和当前无法验证的失败路径增加直接单元测试或 fault injection。

#### 10. 处理版本身份和仓库治理，但不要自动创建 release

GitHub 当前已经存在 `v1.0.0` tag，而该 tag 指向的 commit 内 `.codex-plugin/plugin.json` 声明 `2.0.0`。这是版本身份冲突。

本地 Agent不得静默移动或删除已发布 tag。先输出证据并等待用户决定：

```text
若 v1.0.0 是误创建且从未对外承诺，可在用户明确授权后删除
若已有人使用，保留历史，正式 release 使用与 manifest 一致的新版本，并在 release notes 解释异常
```

同时检查 `main` branch protection / ruleset。Release Candidate 应要求完整 CI 成功后才能进入发布。

#### 11. 冻结 Release Candidate SHA 并重新跑完整证据链

所有代码和文档修改完成后，选一个唯一 candidate SHA。之后不要继续修改该 SHA 的内容。

必须获得：

```text
GitHub Actions on R-jed/subagents-dispatch
Ubuntu Python 3.11 PASS
Ubuntu Python 3.12 PASS
macOS Python 3.11 PASS
Windows Python 3.11 PASS
pinned official OpenAI Plugin validator PASS
full pytest PASS
managed profile lifecycle PASS
legacy migration tests PASS
real Plugin install smoke PASS
/dispatch runtime smoke PASS
/doctor runtime smoke PASS
```

任何一项失败，candidate 作废，修复后生成新的 SHA 重新验证。

#### 12. 重写本报告为 candidate-bound 最终报告

最终 `docs/deep-review-report.md` 不再使用“当前分支”“当前本地状态”作为核心证据。最终报告必须绑定：

```text
candidate commit SHA
Plugin version
GitHub Actions run id / URL
exact test count
OpenAI validator result
marketplace/install smoke evidence
legacy migration acceptance evidence
/dispatch and /doctor runtime evidence
remaining accepted risks
version tag decision
```

只有最终报告结论为 `GO`，并且用户明确要求发布之后，才进入 version tag / GitHub Release 创建阶段。

### 10.4 Release Candidate GO 标准

全部满足才允许进入正式 tag/release：

- HEAD/candidate CI 全绿，没有 skipped-away core failures。
- Marketplace source 与当前 OpenAI 子目录 Plugin 分发契约一致，并通过真实安装验证。
- 用户调用 `/dispatch`、`/doctor` 在真实 Codex command surface 可用。
- legacy-only、mixed、modified、partial、corrupt、rerun、真实 lock contention 都有明确并通过的 acceptance test。
- Doctor 和 installer 对 managed-profile health 没有相互冲突的定义。
- pre-push 与 GitHub CI 不会出现同一 commit 一个 green 一个 red 的结构性差异。
- 所有用户文档只有一个安装和升级 contract。
- version identity 已经解释并收敛，错误历史 tag 未被静默改写。
- release tree 无明显本地开发环境残留。
- candidate SHA 冻结后完整 evidence chain 全绿。

当前结论：`NO-GO`。本节中的顺序收口全部完成并重新对抗性验证后，再把结论更新为 `GO` 或继续保留 `NO-GO`。
