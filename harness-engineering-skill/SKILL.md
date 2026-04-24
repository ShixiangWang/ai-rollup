---
name: harness-engineering
description: |
  通用 AI 研发骨架。简约、可靠、强大、有品。
  核心理念：代码库是记录系统，智能体是执行者，人类是设计师。
  适用于全新项目或重构项目的全生命周期。
triggers:
  - 新项目
  - 项目骨架
  - 研发流程
  - 可复现性
  - pipeline
  - 分层架构
  - 上下文管理
  - 反馈回路
---

# Harness Engineering: 通用 AI 研发骨架

> "简约是复杂的最终形式。" — Da Vinci

---

## 一句话核心理念

**代码库是记录系统，智能体是执行者，人类是设计师。**

稀缺资源：人类注意力 | 上下文窗口 | 可复现性

---

## 三大原则

### P1: 渐进披露

```
入口地图（100行）→ 索引 → 按需加载详情

错误：1000页说明书 → 挤掉任务上下文
正确：地图 + 指向 → 智能体按需探索
```

### P2: 反馈回路

```
PreToolUse → 验证门控
PostToolUse → 自动修正
Stop → 质量审计
PreCompact → 状态保存

自动化反馈 > 事后人工审查
```

### P3: 可复现性契约

```
环境锁定 → 接触点记录 → 结果签名

每次运行可追溯，每个结果可验证
```

---

## 项目结构（通用）

```
project/
├── AGENTS.md              # 入口地图（~100行）
├── ARCHITECTURE.md        # 架构顶层视图
├── CONTRACT.md            # 可复现性契约
│
├── src/                   # 源代码
│   ├── domain/            # 领域核心（纯逻辑）
│   ├── infra/             # 基础设施（IO/外部）
│   └── entry/             # 入口点（CLI/API）
│
├── pipelines/             # 处理管道（生信/科学计算）
│   ├── stages/            # 阶段定义
│   └── checkpoints/       # 断点恢复
│
├── data/                  # 数据管理
│   ├── raw/               # 原始数据（不变）
│   ├── processed/         # 处理结果
│   └── catalog.json       # 数据目录（FAIR）
│
├── experiments/           # 实验记录
│   ├── exp-001/           # 单次实验
│   │   ├── config.yaml    # 参数配置
│   │   ├── results/       # 结果
│   │   └── checksum.sha256 # 结果签名
│
├── docs/
│   ├── decisions/         # 决策记录（ADR）
│   ├── references/        # LLM-friendly 参考
│   └── garden.log         # 文档园艺日志
│
├── tests/
├── evals/                 # 智能体评估
└── scripts/
```

---

## 入口配置（编辑器适配）

### 优先级逻辑

```
编辑器特定入口 → 优先加载
AGENTS.md      → 通用后备
```

| 编辑器 | 入口文件 | 格式 |
|--------|----------|------|
| Claude Code | CLAUDE.md | Markdown |
| Cursor | .cursorrules | Markdown |
| VSCode Copilot | .github/copilot-instructions.md | Markdown |
| Windsurf/Zed | .windsurf/rules / .zed/rules | Markdown |
| **通用后备** | **AGENTS.md** | Markdown |

### AGENTS.md 模板（~100行）

```markdown
# [项目名]

## 一句话使命
[核心目标]

## 架构入口
详见 ARCHITECTURE.md

## 可复现契约
详见 CONTRACT.md

## 快速命令
```bash
[测试] [lint] [构建] [运行]
```

## 约束
依赖: domain → infra → entry
文件: < 800行 | 嵌套: < 4层
数据: FAIR 原则

## 当前状态
实验: experiments/exp-XXX
债务: docs/decisions/TD-XXX

---
验证: YYYY-MM-DD
```

---

## 上下文预算

> **200k ≠ 200k 有效空间**

### 黄金法则

```
配置上限:
  MCPs:     20-30（定义）
  Plugins:  10-15（定义）
  Rules:    20（模块化）

激活上限:
  MCPs:     < 10
  Plugins: < 5
  Rules:    按场景加载

定期审查:
  状态栏 > 50%: 健康
  状态栏 30-50%: 警告
  状态栏 < 30%: 必须清理
```

---

## 分层架构（领域驱动）

### 核心模式

```
┌─────────────────────────────────────────┐
│  Entry Layer（入口）                     │  ← CLI/API/UI
├─────────────────────────────────────────┤
│  Infra Layer（基础设施）                 │  ← DB/Cache/HTTP/FS
├─────────────────────────────────────────┤
│  Domain Layer（领域）                    │  ← 纯逻辑，无IO
└─────────────────────────────────────────┘

依赖方向: Domain → Infra → Entry（反向禁止）
```

### 层职责

| 层 | 职责 | 特征 |
|----|------|------|
| Domain | 业务逻辑 | 纯函数、无IO、可测试 |
| Infra | 基础设施 | IO操作、外部依赖 |
| Entry | 入口点 | 用户交互、路由 |

### 切分信号

```
何时切分 Domain:
  - 文件 > 800 行
  - 类/模块 > 10 个公开方法
  - 嵌套 > 4 层
  - 测试需要 mock 外部依赖

Domain 切分原则:
  - 按业务概念（不是技术概念）
  - 高内聚、低耦合
  - 单一变更原因
```

---

## Pipeline 模式（科学计算/生信）

### 阶段定义

```yaml
# pipelines/stages/process.yaml
stage: process
input:
  - data/raw/*.fastq
output:
  - data/processed/*.bam
params:
  threads: 8
  quality_threshold: 30

checkpoint: true  # 支持断点恢复
retry: 3          # 容错重试
```

### 并行策略

```
阶段间: 顺序执行
阶段内: 并行处理

信号:
  - 多文件输入 → 并行
  - 单文件依赖链 → 顺序
  - checkpoint → 断点恢复
```

---

## 可复现性契约

### CONTRACT.md 模板

```markdown
# 可复现性契约

## 环境锁定
- 语言版本: [version]
- 依赖锁定: [lockfile path]
- 容器镜像: [Dockerfile/Singularity]

## 数据溯源
- 原始数据: data/raw/
- 处理流程: pipelines/stages/
- 结果签名: checksum.sha256

## 参数记录
- 配置文件: config.yaml
- 随机种子: [seed]

## 运行验证
```bash
python scripts/verify_reproducibility.py
```

## FAIR 状态
- Findable: ✓ catalog.json
- Accessible: ✓ 标准路径
- Interoperable: ✓ 通用格式
- Reusable: ✓ LICENSE + README

---
签名: SHA256:[hash]
日期: YYYY-MM-DD
```

---

## 反馈回路实现

### Hook 配置

```json
{
  "PreToolUse": [
    { "matcher": "Bash && command matches 'rm -rf'",
      "hooks": [{ "type": "block", "message": "破坏性操作需确认" }] },
    { "matcher": "Bash && command matches '(pytest|cargo test|npm test)',
      "hooks": [{ "type": "command", "command": "echo '[tmux 提醒] 长运行测试'" }] }
  ],
  "PostToolUse": [
    { "matcher": "Edit && file matches '\\.tsx?$'",
      "hooks": [{ "type": "command", "command": "prettier --write ${file} && tsc --noEmit" }] },
    { "matcher": "Edit && file matches '\\.py$'",
      "hooks": [{ "type": "command", "command": "ruff check ${file} && ruff format ${file}" }] }
  ],
  "Stop": [
    { "matcher": "*",
      "hooks": [{ "type": "command", "command": "grep -r 'console\\.log|print(' src/ && echo '[警告] 调试语句残留'" }] }
  ]
}
```

---

## 子智能体委托

### 委托时机

| 任务类型 | 委托目标 | 工具限制 |
|----------|----------|----------|
| 实现规划 | planner | Read, Grep, Glob |
| 架构设计 | architect | Read, Grep, Glob |
| 测试驱动 | tdd-guide | Read, Write, Edit, Bash(test) |
| 代码审查 | code-reviewer | Read, Grep, Glob |
| 安全审查 | security-reviewer | Read, Grep, Glob |
| 实验运行 | experiment-runner | Read, Bash, Write(results/) |
| 文档维护 | doc-gardener | Read, Write, Edit(docs/) |

### 委托模式

```
主智能体:
  1. 定义任务范围
  2. 设置工具限制
  3. 启动子智能体
  4. 等待结果/继续其他工作

子智能体完成后:
  5. 主智能体审查结果
  6. 决定合并或继续迭代

收益:
  - 释放主上下文
  - 专注执行
  - 权限隔离
```

---

## 黄金原则（有品）

### 上下文原则

| ID | 原则 | 理由 |
|----|------|------|
| C01 | MCPs < 10 活跃 | 上下文消耗 |
| C02 | Rules 模块化 | 按场景激活 |
| C03 | 渐进披露 | 按需加载 |

### 代码原则

| ID | 原则 | 理由 |
|----|------|------|
| G01 | 命名揭示意图 | 可读性 |
| G02 | 函数单一职责 | 可测试性 |
| G03 | 早返回 | 可读性 |
| G04 | 文件 < 800 行 | 导航性 |
| G05 | 嵌套 < 4 层 | 可理解性 |
| G06 | 类型边界验证 | 可靠性 |

### 可复现原则

| ID | 原则 | 理由 |
|----|------|------|
| R01 | 环境锁定 | 环境一致性 |
| R02 | 参数记录 | 参数追溯 |
| R03 | 结果签名 | 结果验证 |
| R04 | FAIR 数据 | 数据可发现 |

### 设计原则

| ID | 原则 | 理由 |
|----|------|------|
| D01 | 结构优于注释 | 自解释代码 |
| D02 | 测试即文档 | 可执行规范 |
| D03 | 决策即记录 | ADR 可追溯 |
| D04 | 熵需对抗 | 品味维护 |

---

## CLI 命令

```bash
# 初始化新项目
harness init <name> --language python|typescript|rust

# 架构检查
harness check [--size] [--nesting] [--deps]

# 可复现验证
harness verify [--env] [--data] [--checksum]

# 文档园艺
harness garden [--stale-days 90]

# 黄金原则
harness golden [--list] [--check]

# 项目状态
harness status

# 实验记录
harness experiment start <name>
harness experiment finish <name>
```

---

## 全生命周期流程

### Phase 0: 初始化（新项目）

```
1. harness init → 创建骨架
2. 编写 AGENTS.md → 定义入口
3. 编写 CONTRACT.md → 可复现契约
4. 设置分层架构 → domain/infra/entry
5. 配置 Hooks → 反馈回路
6. 初始化 docs/ → 决策记录系统
```

### Phase 0: 适配（重构项目）

```
1. 分析现有架构 → 映射到分层
2. 创建 AGENTS.md → 导航现有代码
3. 建立可复现契约 → 锁定环境
4. 迁移知识到代码库 → 决策记录
5. 设置 Hooks → 渐进式反馈回路
6. 启动文档园艺 → 持续维护
```

### Phase 1-N: 迭代开发

```
每个功能:
  1. 设计决策 → docs/decisions/ADR-XXX.md
  2. 测试先行 → tests/
  3. 实现 → src/domain/
  4. 审查 → code-reviewer 子智能体
  5. 记录 → 更新实验/文档
  6. 验证可复现 → harness verify
```

### Phase Complete: 交付

```
1. harness status → 健康检查
2. harness verify → 可复现验证
3. 文档审计 → garden 最终版
4. 技术债务清算 → docs/tech-debt.md
5. 结果签名 → checksum.sha256
```

---

## 参考文件

按需加载：

- [editor-adapters.md](references/editor-adapters.md)
- [context-management.md](references/context-management.md)
- [hooks-patterns.md](references/hooks-patterns.md)
- [reproducibility.md](references/reproducibility.md) — 可复现性详解
- [pipeline-patterns.md](references/pipeline-patterns.md) — Pipeline 模式
- [domain-driven.md](references/domain-driven.md) — 领域驱动设计
- [golden-principles.md](references/golden-principles.md)

---

## 关键洞察

> "代码库是记录系统，不存在于此的东西对智能体就不存在。"

> "200k 窗口过度配置后实际只有 70k。"

> "给智能体一张地图，不是一本说明书。"

> "可复现性是科学计算的生命线。"

> "Pipeline 是生信的标准形态。"

> "熵是必然的，必须主动对抗。"

> "简约是复杂的最终形式。"