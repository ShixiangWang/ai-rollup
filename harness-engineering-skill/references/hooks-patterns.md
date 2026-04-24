# Hook 模式详解

## 核心概念

**Hooks 是反馈回路的核心实现。**

---

## Hook 类型

| 类型 | 触发时机 | 用途 |
|------|----------|------|
| PreToolUse | 工具执行前 | 验证、阻止 |
| PostToolUse | 工具执行后 | 格式化、lint |
| Stop | 会话结束时 | 审计 |
| PreCompact | 压缩前 | 保存信息 |

---

## PreToolUse 示例

```json
{
  "PreToolUse": [
    {
      "matcher": "tool_input.command matches \"rm -rf\"",
      "hooks": [{ "type": "block", "message": "Dangerous" }]
    }
  ]
}
```

---

## PostToolUse 示例

```json
{
  "PostToolUse": [
    {
      "matcher": "tool_input.file_path matches \"\\.tsx?$\"",
      "hooks": [{ "type": "command", "command": "prettier --write ${file_path}" }]
    }
  ]
}
```

---

## 与反馈回路对应

| 反馈阶段 | Hook 实现 |
|----------|-----------|
| 验证门控 | PreToolUse block |
| 自动修正 | PostToolUse format |
| 质量审计 | Stop scan |

---

## 其他编辑器替代

pre-commit 替代 Hooks：

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: prettier
        entry: prettier --write
```