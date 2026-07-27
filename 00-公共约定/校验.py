#!/usr/bin/env python3
"""bingo-figma 文档规范校验。退出码非 0 即失败,可直接挂 CI。

用法:
    python3 00-公共约定/校验.py
    python3 00-公共约定/校验.py --strict   # 要求所有页面都已迁移到 v3
"""
import re
import sys
import pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
STRICT = "--strict" in sys.argv

V3_SECTIONS = [
    "背景与目标", "入口", "术语", "关键参数与假设", "字段清单",
    "需求清单", "需求详述", "数据流向与系统串接", "异常与边界",
    "状态清单", "涉及表与职责", "关联页面",
]
# 适用范围必须覆盖的维度(自检案例:本地化 / 用户场景未定义)
SCOPE_KEYS = ["终端", "响应式", "语言", "时区"]
BANNED_SECTIONS = {"待探讨", "页面结构"}

# emoji 与装饰性符号(需求文档靠结构表达轻重,不靠图标)
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF"      # 表情、符号与象形
    "\U00002600-\U000027BF"       # 杂项符号与装饰
    "\U00002B00-\U00002BFF"       # 箭头补充
    "\U0000FE0F"                  # 变体选择符
    "✅❌⬜⚠]"   # 对勾/叉/白块/警告
)

errors: list[str] = []
warns: list[str] = []


def err(msg): errors.append(msg)
def warn(msg): warns.append(msg)


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def sections(text):
    return [(int(m.group(1)), m.group(2).strip())
            for m in re.finditer(r"^## (\d+)\.\s*(.+)$", text, re.M)]


def section_body(text, title):
    m = re.search(rf"^## \d+\.\s*{re.escape(title)}\s*$(.*?)(?=^## |\Z)",
                  text, re.M | re.S)
    return m.group(1) if m else ""


def table_rows(body, pattern):
    return [l for l in body.splitlines() if re.match(pattern, l.strip())]


# ─────────────────────── 模块级检查 ───────────────────────
modules = sorted(p for p in BASE.glob("M[0-9]-*") if p.is_dir())
for mod in modules:
    readme = mod / "README.md"
    if not readme.exists():
        err(f"{mod.name}: 缺 README.md")
        continue
    text = readme.read_text(encoding="utf-8")

    listed = set(re.findall(r"^\| (\d+\.\d+) \|", text, re.M))
    exists = {p.name.split("-")[0] for p in mod.iterdir()
              if p.is_dir() and re.match(r"^\d+\.\d+-", p.name)}
    for x in sorted(listed - exists):
        err(f"{mod.name}: README 列了 {x} 但无文件夹")
    for x in sorted(exists - listed):
        err(f"{mod.name}: 有文件夹 {x} 但 README 未列")

    for banned in BANNED_SECTIONS:
        if re.search(rf"^## .*{banned}", text, re.M):
            err(f"{mod.name}/README.md: 含禁用段落「{banned}」")


# ─────────────────────── 页面级检查 ───────────────────────
pages = sorted(BASE.glob("M[0-9]-*/*/README.md"))
migrated = 0

for f in pages:
    rel = f.relative_to(BASE)
    text = f.read_text(encoding="utf-8")
    fm = frontmatter(text)
    secs = sections(text)
    titles = [t for _, t in secs]
    nums = [n for n, _ in secs]
    # 是否已迁移:由段落结构本身判定,不靠人工标记
    v3 = titles == V3_SECTIONS
    if v3:
        migrated += 1

    # 页面编号从文件夹名推导,不在 frontmatter 重复
    page_no = f.parent.name.split("-")[0]

    # 1) 段落编号连续
    if nums != list(range(1, len(nums) + 1)):
        err(f"{rel}: 段落编号不连续 {nums}")

    # 1b) 不允许无编号的二级标题 —— 会打乱段落结构且不易察觉
    for m in re.finditer(r"^## (?!\d+\.)(.+)$", text, re.M):
        err(f"{rel}: 二级标题「{m.group(1).strip()}」没有段号,"
            f"要么并入某段(降为 ###),要么给它编号")

    # 2) 禁用段落
    for banned in BANNED_SECTIONS:
        if banned in titles:
            err(f"{rel}: 含禁用段落「{banned}」")

    # 3) frontmatter 必填(中文键,仅 6 项)
    for k in ("名称", "路由", "模块", "优先级", "状态", "更新"):
        if k not in fm:
            err(f"{rel}: frontmatter 缺「{k}」")

    body_req = section_body(text, "需求清单")
    rows = table_rows(body_req, r"^\|\s*\d+\.\d+-R\d+\s*\|")

    # 4) 需求编号须与文件夹编号一致
    for r in rows:
        rid = r.strip().strip("|").split("|")[0].strip()
        if not rid.startswith(page_no + "-R"):
            err(f"{rel}: 需求编号 {rid} 与页面编号 {page_no} 不符")

    # 5) 需求详述里展开的编号,必须在需求清单中存在
    listed = {r.strip().strip("|").split("|")[0].strip() for r in rows}
    for m in re.finditer(r"^### (\S+)", section_body(text, "需求详述"), re.M):
        if listed and m.group(1) not in listed:
            err(f"{rel}: 需求详述展开了 {m.group(1)},但需求清单中没有这条")

    # ── v3 专属检查 ──
    if not v3:
        if STRICT:
            err(f"{rel}: 段落结构未迁移到 v3 模板")
        else:
            warn(f"{rel}: 待迁移到 v3")
        continue

    # 5) 段落名与顺序
    if titles != V3_SECTIONS:
        err(f"{rel}: 段落不符 v3 模板\n"
            f"      期望 {V3_SECTIONS}\n      实际 {titles}")

    # 6) 需求表 5 列(ID/需求/触发条件/验收/权限),触发条件必填
    for r in rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if len(cells) != 5:
            err(f"{rel}: 需求行应 5 列"
                f"(ID/需求/触发条件/验收标准/权限码) → {cells[0]}")
            continue
        if not cells[2]:
            err(f"{rel}: {cells[0]} 缺触发条件")

    # 7) 「需求详述」展开的每一条须 6 栏齐全 + 正逆向测试
    detail = section_body(text, "需求详述")
    for m in re.finditer(r"^### (\S+)[^\n]*\n(.*?)(?=^### |\Z)",
                         detail, re.M | re.S):
        rid, blk = m.group(1), m.group(2)
        for col in ("触发条件", "可输入数据", "功能范围",
                    "处理逻辑", "错误处理", "测试案例"):
            if col not in blk:
                err(f"{rel}: {rid} 详述缺栏位「{col}」")
        if "正向" not in blk or "逆向" not in blk:
            err(f"{rel}: {rid} 测试案例须含正向与逆向各至少一例")

    # 8) 异常与边界 ≥ 3 条
    edge = table_rows(section_body(text, "异常与边界"), r"^\|\s*E\d+\s*\|")
    if len(edge) < 3:
        err(f"{rel}: 异常与边界仅 {len(edge)} 条,至少 3 条(正反流程都要想)")

    # 9) 背景与目标须含「不做什么」+ 适用范围各维度
    bg = section_body(text, "背景与目标")
    if "不做什么" not in bg:
        err(f"{rel}: 背景与目标缺「不做什么」边界声明")

    # 9b) 第 1 段面向所有人(含老板),不得出现代码/路径/接口
    for pat, why in (
        (r"\.(ts|tsx|js|py|go|prisma)\b", "文件名"),
        (r"\b\w+/\w+/\w+\.", "文件路径"),
        (r"\b(resolver|GraphQL|SQL|API|endpoint|schema)\b", "技术名词"),
    ):
        m = re.search(pat, bg, re.I)
        if m:
            err(f"{rel}: 背景与目标出现{why}「{m.group()}」— "
                f"第 1 段面向所有人,不写代码细节")
    if "适用范围" not in bg:
        err(f"{rel}: 背景与目标缺「适用范围」")
    else:
        for k in SCOPE_KEYS:
            if k not in bg:
                err(f"{rel}: 适用范围缺「{k}」维度")

    # 10) 数据流向与系统串接
    flow = section_body(text, "数据流向与系统串接")
    if "数据流向" not in flow:
        err(f"{rel}: 第 7 段缺「数据流向」")
    if "系统串接" not in flow:
        err(f"{rel}: 第 7 段缺「系统串接」(无外部系统也要显式声明)")

    # 11) 涉及表与职责
    if "服务端" not in section_body(text, "涉及表与职责"):
        err(f"{rel}: 涉及表与职责缺前后端职责划分")

    # 12) 禁用 emoji
    hits = sorted({m.group() for m in EMOJI.finditer(text)})
    if hits:
        err(f"{rel}: 含 emoji {hits} — 需求文档不使用 emoji")


# ─────────────────────── mermaid 结构检查 ───────────────────────
# 语法错误会在 GitHub 上渲染成红色报错框,比没有图更糟。
# 这里做结构性快检;完整语法解析由 CI 的 mermaid-cli 步骤负责。
MERMAID_TYPES = ("flowchart", "graph", "stateDiagram", "sequenceDiagram",
                 "erDiagram", "mindmap", "classDiagram", "journey",
                 "gantt", "pie", "gitGraph", "timeline")

for f in sorted(BASE.rglob("*.md")):
    if ".git" in f.parts:
        continue
    rel = f.relative_to(BASE)
    lines = f.read_text(encoding="utf-8").splitlines()
    open_at = None
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if open_at is None and s == "```mermaid":
            open_at = i
            head = lines[i].strip() if i < len(lines) else ""
            if not head.startswith(MERMAID_TYPES):
                err(f"{rel}:{i+1}: mermaid 首行不是已知图型 → {head[:40]!r}")
        elif open_at is not None and s == "```":
            open_at = None
    if open_at is not None:
        err(f"{rel}:{open_at}: mermaid 代码块未闭合")


# ─────────────────────── 其他 ───────────────────────
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", ".venv"}
for d in BASE.rglob("*"):
    if not d.is_dir():
        continue
    rel_parts = d.relative_to(BASE).parts
    if any(p in SKIP_DIRS for p in rel_parts):
        continue
    if not any(d.iterdir()):
        err(f"空目录: {d.relative_to(BASE)}")


# ─────────────────────── 人日汇总 ───────────────────────
# 人日的唯一出处是**模块 README 的页面索引表**。
# 页面 README 不写人日 —— 需求文档面向所有读者,排期信息归模块索引。
by_pri: dict[str, float] = {}
for mod in modules:
    mtext = (mod / "README.md").read_text(encoding="utf-8")
    for m in re.finditer(
            r"^\| (\d+\.\d+) \|[^|]*\|[^|]*\|\s*\**(P\d)\**\s*\|[^|]*\|\s*([\d.]+)\s*\|",
            mtext, re.M):
        by_pri[m.group(2)] = by_pri.get(m.group(2), 0) + float(m.group(3))


# ─────────────────────── 输出 ───────────────────────
print(f"页面 {len(pages)} 个 · 已迁移 v3: {migrated} · 待迁移: {len(pages) - migrated}")
if by_pri:
    parts = " · ".join(f"{k} {v:g}" for k, v in sorted(by_pri.items()))
    print(f"人日(由模块索引汇总): {parts} · 合计 {sum(by_pri.values()):g}")
if warns and not STRICT:
    print(f"\n⚠️  {len(warns)} 个页面待迁移(非阻断)")
if errors:
    print(f"\n❌ {len(errors)} 个错误\n")
    for e in errors:
        print("  ✗ " + e)
    sys.exit(1)
print("\n✅ 通过")
