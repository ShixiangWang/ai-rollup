# 分层架构详细实现

## 核心概念

架构约束是智能体高效工作的前提。传统团队在数百名工程师时才引入严格分层，对智能体团队这是**早期先决条件**。

---

## 分层模型

### 单领域分层

```
Types → Config → Repo → Service → Runtime → UI
  ↓       ↓        ↓        ↓         ↓        ↓
数据形状  配置注入  数据访问  业务逻辑   运行时    用户界面
纯类型   环境变量  数据库    API       调度器    组件
Schema  设置     查询      服务      任务      视图
```

**依赖规则**: 只能向前依赖（右侧），不能向后或跳跃。

### 横切关注点

```
Providers（单一接口）
├── AuthProvider     — 认证
├── ConnectorProvider — 外部连接器
├── TelemetryProvider — 遥测
├── FeatureFlagProvider — 功能标志
└── CacheProvider    — 缓存
```

**规则**: 横切关注点通过 Providers 接口进入，不允许其他路径。

---

## 语言特定实现

### TypeScript/JavaScript

```typescript
// 依赖方向验证（自定义 ESLint 规则）
// .eslintrc.js
module.exports = {
  rules: {
    'layer-dependency': 'error', // 自定义规则
  },
};

// 层定义
const LAYER_ORDER = ['types', 'config', 'repo', 'service', 'runtime', 'ui'];

// 层目录结构
src/
├── types/       // Zod schemas, TypeScript types
├── config/      // 环境配置，常量
├── repo/        // 数据访问层
├── service/     // 业务逻辑
├── runtime/     // 调度器，后台任务
├── ui/          // React/Vue 组件
└── providers/   // 横切关注点接口
```

### Python

```python
# 层目录结构
src/
├── types/       # Pydantic models, type hints
├── config/      # settings.py, constants
├── repo/        # database.py, queries
├── service/     # business logic
├── runtime/     # async tasks, schedulers
├── ui/          # API routes, views
└── providers/   # dependency injection

# 验证脚本（pre-commit）
def check_layer_dependency(file_path: str, import_path: str):
    """验证依赖方向"""
    file_layer = get_layer(file_path)
    import_layer = get_layer(import_path)
    if LAYER_ORDER.index(import_layer) < LAYER_ORDER.index(file_layer):
        raise ValueError(f"向后依赖: {file_path} -> {import_path}")
```

### Rust

```rust
// 模块分层
mod types;
mod config;
mod repo;
mod service;
mod runtime;
mod ui;
mod providers;

// 层约束通过模块可见性实现
// 架构验证宏
#[macro_export]
macro_rules! layer_check {
    ($from:expr, $to:expr) => {
        const _: () = {
            let from_idx = LAYER_ORDER.iter().position(|l| l == $from).unwrap();
            let to_idx = LAYER_ORDER.iter().position(|l| l == $to).unwrap();
            assert!(to_idx >= from_idx, "向后依赖禁止");
        };
    };
}
```

---

## 文件大小约束

### 约束定义

```
文件类型          最大行数    最大函数/方法数
─────────────────────────────────────────────
Types/Schemas     200        -
Config            100        -
Repo              400        10
Service           500        15
Runtime           300        8
UI Component      300        -
Test              800        -
```

### 验证实现

```python
# scripts/check_file_size.py
import os
from pathlib import Path

MAX_LINES = {
    'types': 200,
    'config': 100,
    'repo': 400,
    'service': 500,
    'runtime': 300,
    'ui': 300,
}

def check_file_sizes(src_dir: Path):
    violations = []
    for file in src_dir.rglob('*'):
        if file.suffix in ['.ts', '.tsx', '.py', '.rs']:
            layer = get_layer(file)
            lines = len(file.read_text().splitlines())
            if lines > MAX_LINES.get(layer, 800):
                violations.append((file, layer, lines))
    return violations
```

---

## 嵌套深度约束

### 约束定义

```
最大嵌套深度: 4 层

错误示例（5层嵌套）:
if condition_a:
    if condition_b:
        if condition_c:
            if condition_d:
                if condition_e:  # 违规！
                    do_something()

正确示例（早返回）:
if not condition_a:
    return
if not condition_b:
    return
# ... 依次检查
```

---

## 边界验证

### 类型边界验证

```typescript
// 边界处解析数据形状
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
});

function parseUser(input: unknown): User {
  return UserSchema.parse(input);
}

type User = z.infer<typeof UserSchema>;
```

### API 边界规则

```
边界类型              必须验证
────────────────────────────────────
HTTP API 入口         Request body, params
数据库查询结果         Row shape
外部 API 响应          Response shape
配置文件              Config schema
环境变量              Env schema
文件读取              File content schema

内部函数调用           不需要验证（信任内部）
```

---

## CI 集成

```yaml
# .github/workflows/architecture-check.yml
name: Architecture Constraints

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check layer dependencies
        run: python scripts/check_layer_dependency.py src/
      - name: Check file sizes
        run: python scripts/check_file_size.py src/
      - name: Check nesting depth
        run: python scripts/check_nesting.py src/
```

---

## 错误信息设计

**智能体友好的错误信息**：

```
错误: [layer-dependency] src/ui/UserList.tsx 依赖 src/types/User.ts

当前层: ui (index: 5)
依赖层: types (index: 0)

规则: 只能向前依赖

修复建议:
1. 如果 UI 需要类型，通过 providers/ 获取
2. 或将类型移至 ui/ 目录内的本地类型文件
3. 参考 docs/architecture-patterns.md#cross-layer-imports
```