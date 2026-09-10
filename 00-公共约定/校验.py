#!/usr/bin/env python3
"""bingo-figma 文档规范校验。退出码非 0 即失败,可直接挂 CI。

用法:
    python3 00-公共约定/校验.py
    python3 00-公共约定/校验.py --strict   # 检查所有页面的六部分结构(默认同样严格)
"""
import re
import sys
import pathlib
from urllib.parse import unquote, urlsplit

BASE = pathlib.Path(__file__).resolve().parent.parent

TEMPLATES = {
    "活动": ["活动介绍", "运营配置", "参与和领奖规则", "特殊情况", "验收场景", "相关资料"],
    "查询": ["用途", "查询条件", "结果字段", "操作规则", "验收场景", "相关资料"],
    "配置": ["用途", "配置项", "操作规则", "特殊情况", "验收场景", "相关资料"],
    "业务处理": ["用途", "查询与处理信息", "处理规则", "特殊情况", "验收场景", "相关资料"],
}
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
unstarted: list[str] = []   # 索引里有、还没开工的页面(无文件夹),不是错误


def err(msg): errors.append(msg)


def sections(text):
    return [(int(m.group(1)), m.group(2).strip())
            for m in re.finditer(r"^## (\d+)\.\s*(.+)$", text, re.M)]


def section_body(text, title):
    m = re.search(rf"^## \d+\.\s*{re.escape(title)}\s*$(.*?)(?=^## |\Z)",
                  text, re.M | re.S)
    return m.group(1) if m else ""


def table_rows(body, pattern):
    return [l for l in body.splitlines() if re.match(pattern, l.strip())]


# 未解决的合并标记会让同一页同时携带两种状态,在正文检查前拦截。
UNRESOLVED_RULE = re.compile(
    r"待确认|待定|暂定|待评审|待拍板|待决策|待产品确认|待技术评估|待查|"
    r"尚待|尚需明确|规则未明确|未确定的业务|未验证假设|剩余假设|明确假设|"
    r"业务假设|关键参数与假设|枚举未取全|待验证点|尚未定稿|仍需收敛"
)
CONFLICT_MARKER = re.compile(r"^(?:<{7}(?: .*)?|={7}|>{7}(?: .*)?|\|{7}(?: .*)?)$")
for f in sorted(BASE.rglob("*.md")):
    rel = f.relative_to(BASE)
    if any(part in {".git", "node_modules", ".venv", ".gstack"} for part in rel.parts):
        continue
    for line_no, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if UNRESOLVED_RULE.search(line):
            err(f"{rel}:{line_no}: 需求必须给出确定的执行结论")
        if CONFLICT_MARKER.fullmatch(line):
            err(f"{rel}:{line_no}: 含未解决的合并冲突标记")


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
    # 索引里有、文件夹还没建 —— 页面尚未开工的正常状态,不建空占位目录。
    # 页面索引表是页面存在与否的唯一出处;文件夹只在开始写的时候才建。
    unstarted.extend(f"{mod.name} {x}" for x in sorted(listed - exists))
    # 反向必须报错:野文件夹绕过了索引表,规模就统计不到了
    for x in sorted(exists - listed):
        err(f"{mod.name}: 有文件夹 {x} 但 README 未列")

    for banned in BANNED_SECTIONS:
        if re.search(rf"^## .*{banned}", text, re.M):
            err(f"{mod.name}/README.md: 含禁用段落「{banned}」")


# ─────────────────────── 页面级检查 ───────────────────────
pages = sorted(BASE.glob("M[0-9]-*/*/README.md"))
by_template = {name: 0 for name in TEMPLATES}

for f in pages:
    rel = f.relative_to(BASE)
    text = f.read_text(encoding="utf-8")
    # 代码块中的示例不是页面章节;旧链接兼容锚点也不算正文。
    body = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", text, flags=re.M | re.S)
    secs = sections(body)
    titles = [t for _, t in secs]
    nums = [n for n, _ in secs]
    page_no = f.parent.name.split("-")[0]
    if nums != list(range(1, 7)):
        err(f"{rel}: 页面必须恰有连续编号的六部分,实际为 {nums}")
    for m in re.finditer(r"^## (?!\d+\.)(.+)$", body, re.M):
        err(f"{rel}: 二级标题「{m.group(1).strip()}」没有段号")
    if not re.match(r"^# " + re.escape(page_no) + r" · \S[^\n]*\n", text):
        err(f"{rel}: 页面须直接从编号及名称标题开始")
    kind = next((name for name, expected in TEMPLATES.items() if titles == expected), None)
    if kind is None:
        err(f"{rel}: 章节须使用活动、查询、配置或业务处理六部分模板")
        continue
    by_template[kind] += 1
    for title in titles:
        contents = section_body(text, title)
        contents = re.sub(r"<!--.*?-->|<a\s+id=[^>]+></a>", "", contents, flags=re.S)
        contents = re.sub(r"^#{3,6} .*?$", "", contents, flags=re.M)
        if not contents.strip():
            err(f"{rel}: 「{title}」内容为空")
    cases = table_rows(section_body(text, "验收场景"), r"^\|\s*\d+\.\d+-R\d+\s*\|")
    if not cases:
        err(f"{rel}: 验收场景缺少带需求编号的场景")
    listed_ids = set()
    for row in cases:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) != 3 or not all(cells):
            err(f"{rel}: 验收行须为需求编号/场景与操作/预期结果三列且非空")
            continue
        if not re.fullmatch(re.escape(page_no) + r"-R\d+", cells[0]):
            err(f"{rel}: 需求编号 {cells[0]} 与页面编号不符")
        listed_ids.add(cells[0])
    mentioned_ids = set(re.findall(r"(?<![\d.])" + re.escape(page_no) + r"-R\d+\b", body))
    for rid in mentioned_ids - listed_ids:
        err(f"{rel}: {rid} 没有对应验收场景")
    if re.search(r"\*\*(触发条件|可输入数据|功能范围|处理逻辑|错误处理|测试案例)\*\*", body):
        err(f"{rel}: 请将操作、异常和验收分别写入相应章节,不使用旧六栏详述")
    if re.search(r"<页面编号>|<活动名称>|<页面名称>|<查询页面名>", body):
        err(f"{rel}: 正文仍含模板占位符")
    if re.search(r"^\s*\|\s*$|^输入信息：\|", body, re.M):
        err(f"{rel}: 残留不完整表格,请改成完整表格或普通段落")
    if EMOJI.search(body):
        err(f"{rel}: 含emoji")


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


# 检查普通Markdown文件/图片链接的本地目标;不验证远端URL和锚点。
# 去掉代码块和行内代码,避免把文档里的示例路径当作真实引用。
for f in sorted(BASE.rglob("*.md")):
    rel = f.relative_to(BASE)
    if any(part in {".git", "node_modules", ".venv", ".gstack"} for part in rel.parts):
        continue
    body = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", f.read_text(encoding="utf-8"), flags=re.M | re.S)
    body = re.sub(r"`[^`\n]+`", "", body)
    for match in re.finditer(r"\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)", body):
        target = match.group(1).strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        if not (f.parent / unquote(parsed.path)).exists():
            err(f"{rel}: 本地链接不存在 → {target}")

# ─────────────────────── 其他 ───────────────────────
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", ".venv"}
# 空的页面目录是允许的:git 不跟踪空目录,所以它只存在于本地,
# 是「这一页我要开工了」的个人标记,远端与 CI 都看不到。
# 其余位置的空目录仍然报错 —— 那通常是误删或建错的残留。
PAGE_DIR = re.compile(r"^M\d-[^/]+/\d+\.\d+-")
for d in BASE.rglob("*"):
    if not d.is_dir():
        continue
    rel = d.relative_to(BASE)
    if any(p in SKIP_DIRS for p in rel.parts):
        continue
    if not any(d.iterdir()) and not PAGE_DIR.match(rel.as_posix() + "/"):
        err(f"空目录: {rel}")


# ─────────────────────── 输出 ───────────────────────
total = len(pages) + len(unstarted)
print(f"页面 {total} 个(索引口径)· 已有文档 {len(pages)} · 仅登记 {len(unstarted)}")
print("六部分结构: " + " · ".join(f"{name} {count}" for name, count in by_template.items()) + f" · 不符合 {len(pages) - sum(by_template.values())}")
if errors:
    print(f"\n❌ {len(errors)} 个错误\n")
    for e in errors:
        print("  ✗ " + e)
    sys.exit(1)
print("\n✅ 通过")
