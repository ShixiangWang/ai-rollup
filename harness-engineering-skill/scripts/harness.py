#!/usr/bin/env python3
"""
Harness Engineering CLI - 通用 AI 研发骨架

简约、可靠、强大、有品。仅使用标准库。

Commands:
    init       初始化项目骨架
    check      架构约束检查
    verify     可复现性验证
    garden     文档园艺
    golden     黄金原则
    status     项目健康
    experiment 实验记录

Usage:
    python harness.py init <name> [--lang python|typescript|rust]
    python harness.py check [--size] [--nesting] [--deps]
    python harness.py verify [--env] [--data] [--checksum]
    python harness.py garden [--stale 90]
    python harness.py golden [--list] [--check]
    python harness.py status
    python harness.py experiment start|finish <name>
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ============================================================================
# 配置
# ============================================================================

PROJECT_DIRS = [
    "src/domain", "src/infra", "src/entry",
    "pipelines/stages", "pipelines/checkpoints",
    "data/raw", "data/processed",
    "experiments",
    "docs/decisions", "docs/references",
    "tests/unit", "tests/integration",
    "evals", "scripts",
]

LAYER_ORDER = ["domain", "infra", "entry"]
MAX_FILE_LINES = {"domain": 600, "infra": 400, "entry": 300, "default": 800}
MAX_NESTING_DEPTH = 4

GOLDEN = {
    "C01": "MCPs < 10 活跃",
    "C02": "Rules 模块化",
    "C03": "渐进披露",
    "G01": "命名揭示意图",
    "G02": "函数单一职责",
    "G03": "早返回",
    "G04": "文件 < 800 行",
    "G05": "嵌套 < 4 层",
    "G06": "类型边界验证",
    "R01": "环境锁定",
    "R02": "参数记录",
    "R03": "结果签名",
    "R04": "FAIR 数据",
    "D01": "结构优于注释",
    "D02": "测试即文档",
    "D03": "决策即记录",
    "D04": "熵需对抗",
}

# ============================================================================
# init 命令
# ============================================================================

def cmd_init(name: str, lang: str = "python"):
    """初始化项目骨架"""
    root = Path.cwd() / name
    if root.exists():
        print(f"✗ 目录 '{name}' 已存在")
        return 1

    root.mkdir(parents=True)
    print(f"创建: {name}")

    for d in PROJECT_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {d}/")

    # AGENTS.md
    (root / "AGENTS.md").write_text(f"""# {name}

## 使命
[一句话描述核心目标]

## 架构入口
详见 [ARCHITECTURE.md](ARCHITECTURE.md)

## 可复现契约
详见 [CONTRACT.md](CONTRACT.md)

## 快速命令
```bash
{test_cmd(lang)}     # 测试
{lint_cmd(lang)}     # lint
{build_cmd(lang)}    # 构建
```

## 约束
依赖: domain → infra → entry
文件: < 800行 | 嵌套: < 4层
数据: FAIR原则

---
验证: {today()} | 状态: ✓
""")
    print("  ✓ AGENTS.md")

    # ARCHITECTURE.md
    (root / "ARCHITECTURE.md").write_text("""# 架构设计

## 分层架构
```
┌─────────────────────────────┐
│  Entry Layer（入口）         │  CLI/API/UI
├─────────────────────────────┤
│  Infra Layer（基础设施）     │  DB/Cache/HTTP/FS
├─────────────────────────────┤
│  Domain Layer（领域）        │  纯逻辑，无IO
└─────────────────────────────┘

依赖方向: domain → infra → entry（反向禁止）
```

## 层职责
| 层 | 职责 | 特征 |
|---|---|---|
| Domain | 业务逻辑 | 纯函数、无IO |
| Infra | 基础设施 | IO、外部依赖 |
| Entry | 入口点 | 用户交互 |

## 切分信号
- 文件 > 800 行
- 类/模块 > 10 公开方法
- 嵌套 > 4 层
""")
    print("  ✓ ARCHITECTURE.md")

    # CONTRACT.md
    (root / "CONTRACT.md").write_text(f"""# 可复现性契约

## 环境锁定
- 语言: {lang} [{version_hint(lang)}]
- 锁定文件: {lockfile(lang)}
- 容器: Dockerfile（可选）

## 数据溯源
- 原始数据: data/raw/
- 处理流程: pipelines/stages/
- 结果签名: checksum.sha256

## FAIR 状态
| 维度 | 状态 | 实现 |
|---|---|---|
| Findable | ✓ | catalog.json |
| Accessible | ✓ | 标准路径 |
| Interoperable | ✓ | 通用格式 |
| Reusable | ✓ | LICENSE |

---
签名: 待生成 | 日期: {today()}
""")
    print("  ✓ CONTRACT.md")

    # data/catalog.json
    (root / "data" / "catalog.json").write_text(json.dumps({
        "version": 1,
        "project": name,
        "datasets": [],
        "updated": today()
    }, indent=2))
    print("  ✓ data/catalog.json")

    # docs/decisions/template
    (root / "docs" / "decisions" / "ADR-template.md").write_text("""# ADR-XXX: [决策标题]

## 状态
[提议|已接受|已废弃]

## 背景
[问题背景]

## 决策
[决策内容]

## 理由
[选择原因]

## 影响
[正面|负面]

---
日期: YYYY-MM-DD
""")
    print("  ✓ docs/decisions/ADR-template.md")

    # .harness.yaml
    (root / ".harness.yaml").write_text(f"""# Harness 配置
version: 1
project:
  name: {name}
  language: {lang}

architecture:
  layers: [domain, infra, entry]

limits:
  max_file_lines: {{domain: 600, infra: 400, entry: 300}}
  max_nesting_depth: 4

reproducibility:
  lock_env: true
  track_params: true
  sign_results: true
""")
    print("  ✓ .harness.yaml")

    print(f"\n完成! 下一步:")
    print("  1. 编辑 AGENTS.md 定义使命")
    print("  2. 编辑 CONTRACT.md 锁定环境")
    print("  3. harness check 验证架构")
    return 0


# ============================================================================
# check 命令
# ============================================================================

def cmd_check(size=True, nesting=True, deps=False):
    """架构约束检查"""
    src = Path.cwd() / "src"
    if not src.exists():
        print("✗ src/ 不存在")
        return 1

    violations = []

    # 文件大小检查
    if size:
        for f in src.rglob("*"):
            if f.suffix in [".py", ".ts", ".tsx", ".rs", ".go"]:
                layer = get_layer(f)
                max_lines = MAX_FILE_LINES.get(layer, 800)
                try:
                    lines = len(f.read_text().splitlines())
                    if lines > max_lines:
                        violations.append(f"G04: {f.relative_to(src)} ({lines}>{max_lines})")
                except: pass

    # 嵌套检查
    if nesting:
        for f in src.rglob("*.py"):
            try:
                content = f.read_text()
                for i, line in enumerate(content.splitlines()):
                    if line.strip():
                        indent = len(line) - len(line.lstrip())
                        depth = indent // 4
                        if depth > MAX_NESTING_DEPTH:
                            violations.append(f"G05: {f.relative_to(src)}:{i+1} (depth={depth})")
            except: pass

    # 依赖检查（简单版）
    if deps:
        for f in src.rglob("*.py"):
            layer = get_layer(f)
            try:
                content = f.read_text()
                # 检查是否反向依赖
                for other in LAYER_ORDER:
                    if LAYER_ORDER.index(other) < LAYER_ORDER.index(layer):
                        if f"from {other}" in content or f"import {other}" in content:
                            violations.append(f"DEP: {f.relative_to(src)} → {other} (反向依赖)")
            except: pass

    print("架构检查:")
    if violations:
        for v in violations[:20]:  # 最多显示20条
            print(f"  ✗ {v}")
        if len(violations) > 20:
            print(f"  ... 共 {len(violations)} 条违规")
    else:
        print("  ✓ 无违规")

    return len(violations)


# ============================================================================
# verify 命令
# ============================================================================

def cmd_verify(env=True, data=True, checksum=False):
    """可复现性验证"""
    issues = []

    # 环境检查
    if env:
        lock = lockfile_path()
        if not lock.exists():
            issues.append(f"R01: 缺少环境锁定文件 {lock.name}")

    # 数据目录检查
    if data:
        catalog = Path.cwd() / "data" / "catalog.json"
        if not catalog.exists():
            issues.append("R04: 缺少 data/catalog.json")

        raw = Path.cwd() / "data" / "raw"
        processed = Path.cwd() / "data" / "processed"
        if raw.exists() and not any(raw.iterdir()):
            issues.append("R02: data/raw/ 为空")

    # checksum 验证
    if checksum:
        checksum_file = Path.cwd() / "checksum.sha256"
        if checksum_file.exists():
            expected = parse_checksums(checksum_file)
            actual = compute_checksums(Path.cwd() / "data" / "processed")
            for path, exp_hash in expected.items():
                if path in actual and actual[path] != exp_hash:
                    issues.append(f"R03: {path} checksum 不匹配")

    print("可复现性验证:")
    if issues:
        for i in issues:
            print(f"  ✗ {i}")
    else:
        print("  ✓ 符合契约")

    return len(issues)


# ============================================================================
# garden 命令
# ============================================================================

def cmd_garden(stale_days=90):
    """文档园艺"""
    docs = Path.cwd() / "docs"
    if not docs.exists():
        print("✗ docs/ 不存在")
        return 1

    issues = []

    for f in docs.rglob("*.md"):
        content = f.read_text()

        # 检查日期
        m = re.search(r"(日期|更新|验证)[：:]\s*(\d{4}-\d{2}-\d{2})", content)
        if m:
            date = datetime.strptime(m.group(2), "%Y-%m-%d")
            age = (datetime.now() - date).days
            if age > stale_days:
                issues.append(f"STALE: {f.relative_to(docs)} ({age}天)")

        # 检查链接
        for link in re.findall(r"\[.*?\]\(([^http#].*?)\)", content):
            target = f.parent / link
            if not target.exists():
                issues.append(f"LINK: {f.relative_to(docs)} → {link}")

    print("文档园艺:")
    if issues:
        for i in issues[:10]:
            print(f"  ⚠ {i}")
        if len(issues) > 10:
            print(f"  ... 共 {len(issues)} 条")
    else:
        print("  ✓ 健康")

    # 更新 garden.log
    log = docs / "garden.log"
    entry = f"{today()} | {len(issues)} issues\n"
    log.write_text(log.read_text() + entry if log.exists() else entry)

    return len(issues)


# ============================================================================
# golden 命令
# ============================================================================

def cmd_golden(list_only=False, check=False):
    """黄金原则"""
    if list_only:
        print("黄金原则:")
        for cat in ["C", "G", "R", "D"]:
            print(f"\n{cat} 系列:")
            for id, desc in GOLDEN.items():
                if id.startswith(cat):
                    print(f"  {id}: {desc}")
        return 0

    if check:
        violations = cmd_check(size=True, nesting=True)
        verify_issues = cmd_verify(env=True, data=True)
        total = violations + verify_issues
        print(f"\n黄金违规: {total}")
        return total


# ============================================================================
# status 命令
# ============================================================================

def cmd_status():
    """项目健康报告"""
    print("项目状态:")
    print("=" * 40)

    # 源文件
    src = Path.cwd() / "src"
    if src.exists():
        files = list(src.rglob("*.py"))
        print(f"源文件: {len(files)} ({sum(len(f.read_text().splitlines()) for f in files)} 行)")

    # 文档
    docs = Path.cwd() / "docs"
    if docs.exists():
        print(f"文档: {len(list(docs.rglob('*.md')))} 个")

    # ADR
    decisions = docs / "decisions"
    if decisions.exists():
        adrs = len(list(decisions.glob("ADR-*.md")))
        print(f"决策记录: {adrs}")

    # 数据
    data = Path.cwd() / "data"
    if data.exists():
        catalog = data / "catalog.json"
        if catalog.exists():
            cat = json.loads(catalog.read_text())
            print(f"数据集: {len(cat.get('datasets', []))}")

    # 实验
    exps = Path.cwd() / "experiments"
    if exps.exists():
        print(f"实验: {len(list(exps.iterdir()))} 个")

    # 可复现
    contract = Path.cwd() / "CONTRACT.md"
    if contract.exists():
        print("可复现契约: ✓")

    # 违规数
    violations = cmd_check(size=True, nesting=False)
    print(f"架构违规: {violations}")


# ============================================================================
# experiment 命令
# ============================================================================

def cmd_experiment(action: str, name: str):
    """实验记录"""
    exps = Path.cwd() / "experiments"
    if not exps.exists():
        print("✗ experiments/ 不存在")
        return 1

    exp_dir = exps / name

    if action == "start":
        if exp_dir.exists():
            print(f"✗ 实验 {name} 已存在")
            return 1

        exp_dir.mkdir()
        (exp_dir / "config.yaml").write_text(f"""# 实验配置
name: {name}
date: {today()}
seed: {hashlib.sha256(name.encode()).hexdigest()[:8]}

params:
  # [填写参数]
""")
        (exp_dir / "results").mkdir()
        print(f"✓ 实验 {name} 已启动")
        print("  编辑 config.yaml 设置参数")
        return 0

    if action == "finish":
        if not exp_dir.exists():
            print(f"✗ 实验 {name} 不存在")
            return 1

        # 生成 checksum
        results = exp_dir / "results"
        if results.exists() and any(results.iterdir()):
            checksums = compute_checksums(results)
            sha_file = exp_dir / "checksum.sha256"
            sha_file.write_text(format_checksums(checksums))
            print(f"✓ 结果签名已生成")

        print(f"✓ 实验 {name} 已完成")
        return 0


# ============================================================================
# 辅助函数
# ============================================================================

def get_layer(f: Path) -> str:
    """获取文件所属层"""
    for layer in LAYER_ORDER:
        if layer in f.parts:
            return layer
    return "default"

def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def test_cmd(lang: str) -> str:
    return {"python": "pytest", "typescript": "npm test", "rust": "cargo test"}.get(lang, "pytest")

def lint_cmd(lang: str) -> str:
    return {"python": "ruff check", "typescript": "npm run lint", "rust": "cargo clippy"}.get(lang, "ruff")

def build_cmd(lang: str) -> str:
    return {"python": "python -m build", "typescript": "npm run build", "rust": "cargo build"}.get(lang, "build")

def version_hint(lang: str) -> str:
    return {"python": "3.11+", "typescript": "5.0+", "rust": "1.70+"}.get(lang, "")

def lockfile(lang: str) -> str:
    return {"python": "pyproject.toml", "typescript": "package-lock.json", "rust": "Cargo.lock"}.get(lang, "lock")

def lockfile_path() -> Path:
    lang = detect_lang()
    return Path.cwd() / lockfile(lang)

def detect_lang() -> str:
    """检测项目语言"""
    cwd = Path.cwd()
    if (cwd / "pyproject.toml").exists() or (cwd / "setup.py").exists():
        return "python"
    if (cwd / "package.json").exists():
        return "typescript"
    if (cwd / "Cargo.toml").exists():
        return "rust"
    return "python"

def compute_checksums(directory: Path) -> dict:
    """计算目录 checksum"""
    result = {}
    for f in directory.rglob("*"):
        if f.is_file():
            sha = hashlib.sha256(f.read_bytes()).hexdigest()
            result[str(f.relative_to(directory))] = sha
    return result

def parse_checksums(file: Path) -> dict:
    """解析 checksum 文件"""
    result = {}
    for line in file.read_text().splitlines():
        if "  " in line:
            sha, path = line.split("  ", 1)
            result[path] = sha
    return result

def format_checksums(checksums: dict) -> str:
    """格式化 checksum"""
    lines = [f"{sha}  {path}" for path, sha in checksums.items()]
    return "\n".join(lines) + "\n"


# ============================================================================
# 主入口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Harness CLI - 通用 AI 研发骨架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", help="命令")

    # init
    init_p = sub.add_parser("init", help="初始化项目")
    init_p.add_argument("name", help="项目名")
    init_p.add_argument("--lang", "-l", default="python",
                        choices=["python", "typescript", "rust"], help="语言")

    # check
    check_p = sub.add_parser("check", help="架构检查")
    check_p.add_argument("--size", action="store_true", help="文件大小")
    check_p.add_argument("--nesting", action="store_true", help="嵌套深度")
    check_p.add_argument("--deps", action="store_true", help="依赖方向")

    # verify
    verify_p = sub.add_parser("verify", help="可复现验证")
    verify_p.add_argument("--env", action="store_true", help="环境锁定")
    verify_p.add_argument("--data", action="store_true", help="数据目录")
    verify_p.add_argument("--checksum", action="store_true", help="结果签名")

    # garden
    garden_p = sub.add_parser("garden", help="文档园艺")
    garden_p.add_argument("--stale", type=int, default=90, help="过时天数")

    # golden
    golden_p = sub.add_parser("golden", help="黄金原则")
    golden_p.add_argument("--list", action="store_true", help="列出原则")
    golden_p.add_argument("--check", action="store_true", help="检查违规")

    # status
    sub.add_parser("status", help="项目状态")

    # experiment
    exp_p = sub.add_parser("experiment", help="实验记录")
    exp_p.add_argument("action", choices=["start", "finish"])
    exp_p.add_argument("name", help="实验名")

    args = parser.parse_args()

    if args.cmd == "init":
        return cmd_init(args.name, args.lang)
    elif args.cmd == "check":
        size = args.size or not (args.nesting or args.deps)
        nesting = args.nesting or not (args.size or args.deps)
        return cmd_check(size, nesting, args.deps)
    elif args.cmd == "verify":
        env = args.env or not (args.data or args.checksum)
        data = args.data or not (args.env or args.checksum)
        return cmd_verify(env, data, args.checksum)
    elif args.cmd == "garden":
        return cmd_garden(args.stale)
    elif args.cmd == "golden":
        return cmd_golden(args.list, args.check)
    elif args.cmd == "status":
        cmd_status()
        return 0
    elif args.cmd == "experiment":
        return cmd_experiment(args.action, args.name)
    else:
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main())