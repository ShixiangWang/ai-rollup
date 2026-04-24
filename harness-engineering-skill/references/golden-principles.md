# 黄金原则清单

## 核心概念

黄金原则是**带有主观意见的机械规则**，用于保持代码库的可读性和一致性。

---

## 原则清单

### 代码组织原则

| ID | 原则 | 理由 |
|----|------|------|
| GP-001 | 共享实用工具 > 手写辅助函数 | 不变式集中 |
| GP-002 | 类型化 SDK > YOLO 式探测数据 | 防止猜测结构 |
| GP-003 | 文件 < 800 行 | 导航性 |
| GP-004 | 函数 < 50 行 | 可理解性 |
| GP-005 | 嵌套深度 < 4 | 可读性 |

### 错误处理原则

| ID | 原则 | 理由 |
|----|------|------|
| GP-010 | 早返回 > 深嵌套 | 可读性 |
| GP-011 | 明确错误处理 > 隐式忽略 | 可调试性 |
| GP-012 | 错误信息包含修复建议 | 智能体可操作 |
| GP-013 | 边界验证 > 内部信任 | 安全性 |

### 日志原则

| ID | 原则 | 理由 |
|----|------|------|
| GP-020 | 结构化日志 > 自由文本 | 可查询 |
| GP-021 | 日志包含上下文 | 可调试性 |

### 测试原则

| ID | 原则 | 理由 |
|----|------|------|
| GP-030 | 测试覆盖 > 80% | 可靠性 |
| GP-031 | 测试命名描述行为 | 可理解性 |

---

## 原则应用示例

### GP-001: 共享实用工具

```python
# 错误：手写辅助函数
def get_user_name(user):
    return user.get('name', 'Unknown')

# 正确：共享实用工具
# src/utils/user_utils.py
class UserUtils:
    @staticmethod
    def get_name(user: User) -> str:
        return user.name or 'Unknown'
```

### GP-012: 错误信息包含修复建议

```python
# 正确：可操作错误
raise ValueError(
    "Invalid input: email format incorrect\n"
    "Expected: user@example.com\n"
    "Fix: Check src/service/AuthService.py:45"
)
```

---

## 后台清理任务

定期运行检查违规，创建针对性重构 PR。