# Harness Engineering Skill

> 通用 AI 研发骨架。简约、可靠、强大、有品。

核心理念：**代码库是记录系统，智能体是执行者，人类是设计师。**

---

## 适用场景

- 新项目初始化（从零到骨架）
- 现有项目重构（架构适配）
- 科学计算/生信项目（可复现性）
- AI 辅助开发全生命周期

---

## 快速开始

### 初始化新项目

```bash
python scripts/harness.py init my-project --lang python
```

生成结构：
```
my-project/
├── AGENTS.md          # 入口地图（~100行）
├── ARCHITECTURE.md    # 架构设计
├── CONTRACT.md        # 可复现契约
├── src/
│   ├── domain/        # 领域层（纯逻辑）
│   ├── infra/         # 基础设施层（IO）
│   └── entry/         # 入口层（CLI/API）
├── pipelines/         # 处理管道
├── data/              # 数据管理（FAIR）
├── experiments/       # 实验记录
├── docs/              # 文档系统
└── tests/
```

### CLI 命令

```bash
harness init <name> [--lang python|typescript|rust]  # 初始化
harness check [--size] [--nesting] [--deps]           # 架构检查
harness verify [--env] [--data] [--checksum]          # 可复现验证
harness garden [--stale 90]                           # 文档园艺
harness golden [--list] [--check]                     # 黄金原则
harness status                                        # 项目状态
harness experiment start|finish <name>                # 实验记录
```

---

## 多专家视角整合

| 视角 | 核心洞察 |
|------|----------|
| **LLM专家** | 上下文预算：配置20-30，激活<10 |
| **科学计算专家** | 可复现性契约：环境锁定+参数记录+结果签名 |
| **生信专家** | Pipeline模式：阶段定义+checkpoint恢复 |
| **软件匠艺** | 黄金原则：命名揭示意图、结构优于注释 |
| **领域驱动** | 三层架构：domain → infra → entry |
| **FAIR原则** | 数据管理：Findable/Accessible/Interoperable/Reusable |

---

## 黄金原则（17条）

### C系列（上下文）
- C01: MCPs < 10 活跃
- C02: Rules 模块化
- C03: 渐进披露

### G系列（代码）
- G01: 命名揭示意图
- G02: 函数单一职责
- G03: 早返回
- G04: 文件 < 800 行
- G05: 嵌套 < 4 层
- G06: 类型边界验证

### R系列（可复现）
- R01: 环境锁定
- R02: 参数记录
- R03: 结果签名
- R04: FAIR 数据

### D系列（设计）
- D01: 结构优于注释
- D02: 测试即文档
- D03: 决策即记录
- D04: 熵需对抗

---

## 编辑器适配

| 编辑器 | 入口文件 | 说明 |
|--------|----------|------|
| Claude Code | CLAUDE.md | 优先加载 |
| Cursor | .cursorrules | 优先加载 |
| VSCode Copilot | .github/copilot-instructions.md | 优先加载 |
| **通用后备** | **AGENTS.md** | 所有编辑器理解 |

---

## 依赖

**CLI 仅使用 Python 标准库**，无需安装任何依赖。

---

## 文件结构

```
harness-engineering-skill/
├── SKILL.md                 # Skill 定义（核心方法论）
├── README.md                # 本文件
├── scripts/
│   └── harness.py           # Python CLI
└── references/              # 参考文档（按需加载）
```

---

## 来源与灵感

- [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)
- FAIR Principles
- Domain-Driven Design
- Software Craftsmanship
- Snakemake/Nextflow

---

## License

MIT