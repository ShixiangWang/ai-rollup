# 知识编码策略

## 核心概念

**不存在于代码库中的，对智能体就不存在。**

智能体无法访问：Google Docs、Slack 讨论、会议记录、人类头脑中的知识

---

## 知识类型与存储

| 知识类型 | 存储位置 | 格式 |
|----------|----------|------|
| 产品原则 | docs/core-beliefs.md | Markdown |
| 架构决策 | docs/design-docs/ADR-*.md | ADR 格式 |
| 技术债务 | docs/tech-debt.md | 追踪表 |
| 执行计划 | docs/exec-plans/*.md | 进度日志 |
| API 参考 | docs/references/*.txt | LLM-friendly |

---

## 文档结构模板

### Core Beliefs 模板

```markdown
# 核心信念

## 产品理念
1. [信念名称]
   - 原因：[为什么]
   - 应用：[如何指导决策]

---
验证状态：[已验证/待更新/已过时]
最后更新：YYYY-MM-DD
```

### ADR 模板

```markdown
# ADR-[编号]: [决策标题]

## 状态
[提议/已接受/已废弃]

## 背景
[问题描述]

## 决策
[决策内容]

## 理由
[选择原因]

---
日期：YYYY-MM-DD
```

### 执行计划模板

```markdown
# 执行计划：[名称]

## 状态
[active/completed/paused]

## 任务列表
- [ ] 任务1 - [状态]
- [x] 任务2 - completed

## 进度日志
| 日期 | 进度 |
|------|------|
| YYYY-MM-DD | [描述] |
```

---

## LLM-friendly 格式特点

```
1. 无废话，直接陈述
2. 结构化，可解析
3. 交叉链接完整
4. 示例代码完整
5. 版本信息明确
```

---

## 渐进式披露

CLAUDE.md 作为地图（< 150 行），指向 docs/ 目录的深层信息。

```markdown
# CLAUDE.md 示例

## 项目概览
[一句话描述]

## 架构入口
详见 [ARCHITECTURE.md](ARCHITECTURE.md)

## 核心信念
详见 [docs/core-beliefs.md](docs/core-beliefs.md)

## 快速命令
npm test / pytest
```

---

## 文档园艺

定期运行的智能体：
- 扫描过时文档
- 检测废弃内容
- 发起修复 PR
- 验证交叉链接

CI 作业验证知识库的更新状况。