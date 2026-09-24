"""文档校验 CLI 的范围与拒绝行为回归测试。"""

import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE = pathlib.Path(__file__).resolve().parent
VALID_PAGE = """# 1.1 · 测试配置

## 1. 用途
保存配置。

## 2. 配置项
名称必填。

## 3. 操作规则
保存后生效。

## 4. 特殊情况
名称为空时拒绝保存。

## 5. 验收场景
| 需求编号 | 场景与操作 | 预期结果 |
| --- | --- | --- |
| 1.1-R1 | 保存完整配置 | 保存成功 |

## 6. 相关资料
内部配置说明。
"""

VALID_PLAYER_PAGE = """# Account · 玩家账户

## 1. 用途
查看并管理玩家账户。

## 2. 查询与处理信息
账户标识与验证状态。

## 3. 处理规则
身份核验失败时仅重试未通过的步骤，见Account-R1。

## 4. 特殊情况
提交超时后先查询原请求结果。

## 5. 验收场景
| 需求编号 | 场景与操作 | 预期结果 |
| --- | --- | --- |
| Account-R1 | 重试未通过的身份验证步骤 | 已通过步骤保留 |

## 6. 相关资料
玩家账户说明。
"""

DEFECTS = {
    "unresolved": ("规则待确认。\n", "需求必须给出确定的执行结论"),
    "link": ("[附件](missing.png)\n", "本地链接不存在"),
    "mermaid": ("```mermaid\ninvalid_chart\n```\n", "mermaid 首行不是已知图型"),
    "conflict": ("<<<<<<< HEAD\n", "含未解决的合并冲突标记"),
}


class ValidationScopeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = pathlib.Path(temporary.name)
        scripts = self.repo / "00-公共约定"
        scripts.mkdir()
        for name in ("校验.py", "doc_scope.py"):
            shutil.copy2(SOURCE / name, scripts / name)
        self.write("README.md", "# 文档入口\n")
        self.write("M1-测试/README.md", "# 测试模块\n\n| 1.1 | 测试配置 |\n")
        self.page = self.write("M1-测试/1.1-测试配置/README.md", VALID_PAGE)

    def write(self, relative, text):
        target = self.repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def run_validator(self, *arguments):
        result = subprocess.run(
            [sys.executable, str(self.repo / "00-公共约定/校验.py"), *arguments],
            cwd=self.repo,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=15,
        )
        self.assertEqual(result.stderr, "", result.stderr)
        return result.returncode, result.stdout

    def add_archive_defects(self):
        for name, (text, _) in DEFECTS.items():
            self.write(f".artifacts/history/{name}.md", text)
        (self.repo / ".artifacts/history/empty").mkdir()

    def test_archive_defects_do_not_block_default_or_strict_checks(self):
        self.add_archive_defects()
        for arguments in ((), ("--strict",)):
            with self.subTest(arguments=arguments):
                code, output = self.run_validator(*arguments)
                self.assertEqual(code, 0, output)

    def test_archive_check_is_available_explicitly(self):
        self.add_archive_defects()
        code, output = self.run_validator("--strict", "--include-artifacts")
        self.assertEqual(code, 1, output)
        for _, expected in DEFECTS.values():
            self.assertIn(expected, output)
        self.assertIn("空目录: .artifacts/history/empty", output)

    def test_same_defects_in_formal_documents_are_rejected(self):
        for directory in ("", "M1-测试"):
            for name, (text, expected) in DEFECTS.items():
                with self.subTest(directory=directory, defect=name):
                    target = self.write(pathlib.Path(directory) / "说明.md", text)
                    try:
                        code, output = self.run_validator("--strict")
                        self.assertEqual(code, 1, output)
                        self.assertIn(expected, output)
                    finally:
                        target.unlink()
            with self.subTest(directory=directory, defect="empty-directory"):
                target = self.repo / directory / "empty"
                target.mkdir()
                try:
                    code, output = self.run_validator("--strict")
                    self.assertEqual(code, 1, output)
                    self.assertIn("空目录:", output)
                finally:
                    target.rmdir()

    def test_formal_page_structure_and_numbering_remain_enforced(self):
        examples = (
            (VALID_PAGE.replace("## 6. 相关资料\n内部配置说明。\n", ""),
             "页面必须恰有连续编号的六部分"),
            (VALID_PAGE.replace("# 1.1 ·", "# 1.2 ·"),
             "页面须直接从编号及名称标题开始"),
            (VALID_PAGE.replace("1.1-R1", "1.2-R1"),
             "需求编号 1.2-R1 与页面编号不符"),
        )
        for text, expected in examples:
            with self.subTest(expected=expected):
                self.page.write_text(text, encoding="utf-8")
                code, output = self.run_validator("--strict")
                self.assertEqual(code, 1, output)
                self.assertIn(expected, output)

    def test_formal_links_to_missing_archive_files_still_fail(self):
        self.add_archive_defects()
        self.write("README.md", "# 文档入口\n\n[历史资料](.artifacts/missing.md)\n")
        code, output = self.run_validator("--strict")
        self.assertEqual(code, 1, output)
        self.assertIn("README.md: 本地链接不存在 → .artifacts/missing.md", output)
        self.assertNotIn("需求必须给出确定的执行结论", output)

    def test_player_page_is_checked_but_navigation_is_not_a_page(self):
        self.write("玩家端/README.md", "# 玩家端\n\n[玩家账户](Account/README.md)\n")
        self.write("玩家端/Account/README.md", VALID_PLAYER_PAGE)
        for arguments in ((), ("--strict",)):
            with self.subTest(arguments=arguments):
                code, output = self.run_validator(*arguments)
                self.assertEqual(code, 0, output)
                self.assertIn("已有文档 2", output)
                self.assertIn("业务处理 1", output)

    def test_player_page_structure_and_acceptance_are_enforced(self):
        examples = (
            (VALID_PLAYER_PAGE.replace("## 6. 相关资料\n玩家账户说明。\n", ""),
             "页面必须恰有连续编号的六部分"),
            (VALID_PLAYER_PAGE.replace("# Account ·", "# Profile ·"),
             "页面须直接从编号及名称标题开始"),
            (VALID_PLAYER_PAGE.replace("## 2. 查询与处理信息", "## 2. 账户信息"),
             "章节须使用活动、查询、配置或业务处理六部分模板"),
            (VALID_PLAYER_PAGE.replace("| Account-R1 |", "| Profile-R1 |"),
             "需求编号 Profile-R1 与页面编号不符"),
            (VALID_PLAYER_PAGE.replace("| Account-R1 |", "| 1.1-R1 |"),
             "需求编号 1.1-R1 与页面编号不符"),
            (VALID_PLAYER_PAGE.replace("见Account-R1", "见Account-R2"),
             "Account-R2 没有对应验收场景"),
            (VALID_PLAYER_PAGE.replace("| Account-R1 | 重试未通过的身份验证步骤 | 已通过步骤保留 |", ""),
             "验收场景缺少带需求编号的场景"),
            (VALID_PLAYER_PAGE.replace("| 已通过步骤保留 |", "| |"),
             "验收行须为需求编号/场景与操作/预期结果三列且非空"),
        )
        for text, expected in examples:
            with self.subTest(expected=expected):
                self.write("玩家端/Account/README.md", text)
                code, output = self.run_validator("--strict")
                self.assertEqual(code, 1, output)
                self.assertIn("玩家端/Account/README.md:", output)
                self.assertIn(expected, output)

    def test_other_player_pages_use_their_own_directory_identifier(self):
        self.write("玩家端/Payment-Methods/README.md",
                   VALID_PLAYER_PAGE.replace("Account", "Payment-Methods"))
        code, output = self.run_validator("--strict")
        self.assertEqual(code, 0, output)
        self.assertIn("业务处理 1", output)

    def test_player_acceptance_ids_do_not_bypass_numbered_page_checks(self):
        self.page.write_text(VALID_PAGE.replace("1.1-R1", "Account-R1"), encoding="utf-8")
        code, output = self.run_validator("--strict")
        self.assertEqual(code, 1, output)
        self.assertIn("需求编号 Account-R1 与页面编号不符", output)


if __name__ == "__main__":
    unittest.main()
