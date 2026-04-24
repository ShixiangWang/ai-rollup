# CLI 脚手架实现

## 命令列表

| 命令 | 功能 |
|------|------|
| `harness init` | 初始化新项目 |
| `harness refactor` | 分析现有项目 |
| `harness check` | 运行架构检查 |
| `harness garden` | 文档园艺 |
| `harness golden` | 黄金原则检查 |
| `harness status` | 项目健康报告 |

---

## harness init

```bash
harness init [project-name] --language [typescript/python/rust]

执行步骤：
1. 创建目录结构
2. 生成 CLAUDE.md（地图）
3. 创建 ARCHITECTURE.md
4. 初始化 docs/ 目录
5. 创建 src/ 分层目录
6. 设置 lint 配置
7. 创建 CI 配置
8. 设置 pre-commit hooks
```

---

## harness check

```bash
harness check --layer --size --nesting --fix

检查：
- 层依赖方向
- 文件大小
- 嵌套深度
- 自动修复可修复问题
```

---

## harness garden

```bash
harness garden --check --fix --stale-days 90

检查：
- 过时文档
- 失效链接
- 缺失验证状态
```

---

## harness status

```bash
harness status --detailed

报告：
- 架构合规率
- 文档覆盖率
- 测试覆盖率
- 技术债务统计
- 黄金原则合规率
```

---

## 配置文件

```yaml
# .harness.yaml
architecture:
  layers: [types, config, repo, service, runtime, ui]

limits:
  max_file_lines:
    service: 500
  max_nesting_depth: 4
  min_test_coverage: 80
```

---

## 实现要点

CLI 可用 Python 或 TypeScript 实现，核心功能：
1. 目录结构生成器
2. 架构检查器（自定义 lint）
3. 文档健康检查器
4. 统计聚合器