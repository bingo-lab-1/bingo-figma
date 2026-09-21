"""本地文档校验与 CI Mermaid 检查共用的文件范围。"""

import os
from pathlib import Path


SKIP_DIRS = {".git", "node_modules", ".venv", ".gstack", "__pycache__"}


def find_documents(base: Path, include_artifacts: bool = False):
    """返回 Markdown 和目录;默认不进入仓库根目录的历史归档。"""
    base = base.resolve()
    documents = []
    directories = []
    for current, names, files in os.walk(base):
        parent = Path(current)
        names[:] = sorted(
            name for name in names
            if name not in SKIP_DIRS
            and (include_artifacts or parent != base or name != ".artifacts")
        )
        directories.extend(parent / name for name in names)
        documents.extend(parent / name for name in files if name.endswith(".md"))
    return sorted(documents), sorted(directories)
