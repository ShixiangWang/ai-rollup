# 上下文管理详解

## 核心问题

> **200k 上下文窗口 ≠ 200k 有效空间。**

过度配置后实际可用可能只有 70k。

---

## 上下文消耗分析

| 组件 | 单个消耗 | 管理策略 |
|------|----------|----------|
| MCP Tool | 1-5k tokens | 保持 < 10 个活跃 |
| Plugin | 2-10k tokens | 保持 < 5 个活跃 |
| Rule/Skill | 500-2k tokens | 模块化，按需加载 |

---

## 黄金法则

```
配置：20-30 MCPs + 10-15 Plugins + 20 Rules
激活：< 10 MCPs + < 5 Plugins + 模块化 Rules
```

---

## Rules 模块化

```
rules/
  security.md      # 100 行，始终激活
  coding-style.md  # 100 行，写代码时激活
  testing.md       # 100 行，测试时激活
```

---

## 项目禁用配置

```json
// ~/.claude.json
{
  "projects": {
    "/path/to/project": {
      "disabledMcpServers": ["supabase", "firecrawl"]
    }
  }
}
```

---

## 监控上下文

```
/statusline → 显示上下文剩余百分比

> 50%：健康
30-50%：警告
< 30%：危险
```