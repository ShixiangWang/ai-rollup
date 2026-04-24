# 反馈回路设计详解

## 核心概念

反馈回路是 Harness Engineering 的核心机制。目标：最大化智能体自主性，最小化人工干预。

---

## 回路类型

### 1. 验证回路

```
智能体 → 实现 → 自动测试 → 自动审查 → 反馈处理 → 合并
                    ↓ 失败
                  重试/修复 → 新实现
```

### 2. 审查回路

```
智能体 → 自审查 → 修改 → 再审查 → 循环直到满意 → 合并
```

### 3. 可观测性回路

```
智能体实现 → 应用运行 → 可观测性数据 → 智能体查询 → 推理问题 → 修复 → 重启 → 循环
```

---

## 测试回路实现

### 单元测试

```yaml
# CI 配置
tests:
  unit:
    command: npm test / pytest tests/unit/
    timeout: 5m
    on_failure: retry  # 偶发失败重跑
```

### 测试驱动开发（智能体版）

```
步骤：
1. 智能体读取功能需求
2. 智能体编写测试（先失败）
3. 智能体编写实现
4. 运行测试 → 通过？
   - Yes → 继续
   - No → 智能体分析失败，修改实现，重试
5. 循环直到测试通过
6. 合并
```

---

## 可观测性回路实现

### 本地可观测性堆栈

```yaml
# docker-compose.yml (临时堆栈)
services:
  app:
    build: .
    environment:
      - LOG_LEVEL=debug
      - OTEL_EXPORTER=local

  victoria-metrics:
    image: victoriametrics/victoria-metrics:latest
    ports:
      - "8428:8428"

  victoria-logs:
    image: victoriametrics/victoria-logs:latest
    ports:
      - "9428:9428"

  tempo:
    image: grafana/tempo:latest
    ports:
      - "3200:3200"
```

### 查询示例

```python
# 智能体可执行的查询
def query_logs(query: str, time_range: str = "1h"):
    """LogQL 查询日志"""
    # 示例: {service="api"} |= "error"
    response = requests.get(
        "http://localhost:9428/select/logsql/query",
        params={"query": query, "time_range": time_range}
    )
    return response.json()

def query_metrics(query: str, time_range: str = "1h"):
    """PromQL 查询指标"""
    # 示例: rate(http_requests_total[5m])
    response = requests.get(
        "http://localhost:8428/api/v1/query_range",
        params={"query": query}
    )
    return response.json()

def verify_startup_time(threshold_ms: int = 800):
    """验证服务启动时间"""
    metrics = query_metrics("app_startup_duration_ms")
    if metrics["data"]["result"][0]["value"][1] > threshold_ms:
        return {"success": False, "reason": "startup too slow"}
    return {"success": True}
```

---

## 审查回路实现

### 智能体自审查

```yaml
# .claude/agents/self-review.md
workflow:
  1. 读取变更文件
  2. 检查架构合规性、测试覆盖、文档更新
  3. 生成审查评论
  4. 如果有评论，修改代码
  5. 循环直到无评论或达到迭代上限
```

### 智能体间审查

```yaml
review_agents:
  - name: code-reviewer
    focus: 代码质量
  - name: security-reviewer
    focus: 安全漏洞
  - name: architecture-reviewer
    focus: 架构合规

workflow:
  1. 主智能体完成实现
  2. 并行调用所有审查智能体
  3. 收集审查评论
  4. 主智能体处理评论
  5. 循环直到所有审查通过
  6. 合并
```

---

## 合并策略

### 高吞吐量合并规则

```yaml
merge_policy:
  blocking_gates:
    - architecture_lint: must_pass
    - security_scan: must_pass

  non_blocking_gates:
    - unit_tests: retry_3_times
    - integration_tests: report_but_allow

  auto_merge_conditions:
    - all_blocking_pass
    - no_human_review_requested
    - at_least_one_agent_reviewer_approved
```

### 偶发失败处理

```python
class FlakyTestHandler:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def run_test_with_retry(self, test_name: str) -> bool:
        for attempt in range(self.max_retries):
            result = run_test(test_name)
            if result.passed:
                return True
            if result.is_flaky_pattern():
                continue
            return False
        return False
```

---

## 回路监控

### 回路健康指标

| 指标 | 目标 |
|------|------|
| 回路成功率 | > 95% |
| 平均迭代次数 | < 3 |
| 人工干预率 | < 10% |
| 回路时间 | < 30min |

### 回路断路器

```python
MAX_ITERATIONS = 10
MAX_TIME = 60 * 60  # 1 小时

def circuit_breaker(iteration: int, elapsed_time: int):
    if iteration > MAX_ITERATIONS:
        return "max_iterations_exceeded"
    if elapsed_time > MAX_TIME:
        return "max_time_exceeded"
    return None
```