# 编辑器适配指南

## 核心概念

**方法论是通用的，配置格式是编辑器特定的。**

---

## 各编辑器入口配置

### Claude Code

```markdown
# CLAUDE.md（项目根目录）

## 项目概览
[一句话描述]

## 架构入口
详见 ARCHITECTURE.md

## 快速命令
npm test / pytest
```

**配置位置**: `~/.claude/rules/`, `~/.claude/skills/`, `~/.claude/hooks.json`

### Cursor

```markdown
# .cursorrules（项目根目录）

## 项目概览
[一句话描述]

## 代码规则
- 文件 < 800 行
- 嵌套 < 4 层
```

### VSCode Copilot

```markdown
# .github/copilot-instructions.md

## 项目概览
[一句话描述]

## 编码规范
[具体规则]
```

### Windsurf / Zed

```markdown
# .windsurf/rules 或 .zed/rules

## 项目概览
[一句话描述]
```

---

## 配置层次对应

| 方法论概念 | Claude Code | Cursor | VSCode |
|------------|-------------|--------|--------|
| 入口地图 | CLAUDE.md | .cursorrules | copilot-instructions.md |
| Rules | rules/ 目录 | .cursor/rules/ | 写入入口 |
| Skills | skills/ 目录 | 无 | 无 |
| Hooks | hooks.json | 无 | pre-commit |

---

## Hooks 替代方案

其他编辑器用 pre-commit 替代：

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: prettier
        entry: prettier --write
        language: node
```