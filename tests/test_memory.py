"""Seat memory lives in user data, never in the plugin install."""

import os
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
import io

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

from memory import ensure_log, log_path, main, read_log_path, seats_dir  # noqa: E402

PLUGIN = os.path.join(os.path.expanduser("~"), ".claude", "plugins",
                       "cache", "compound-club", "chiron", "0.3.0")


class LogPathTests(unittest.TestCase):
    def test_default_log_is_under_dot_chiron_not_dot_claude(self):
        old = os.environ.pop("CHIRON_HOME", None)
        self.addCleanup(self._restore_env, old)
        path = log_path("munger", plugin_root=PLUGIN)
        root = os.path.abspath(os.path.expanduser(os.path.join("~", ".chiron")))
        claude = os.path.abspath(os.path.expanduser(os.path.join("~", ".claude")))
        self.assertEqual(path, os.path.join(root, "logs", "munger", "log.md"))
        self.assertFalse(path == claude or path.startswith(claude + os.sep))
        self.assertFalse(path.startswith(os.path.abspath(PLUGIN) + os.sep))

    def test_explicit_home_is_honored_even_under_claude(self):
        # An explicit home is not redirected. Claude Code will refuse the write;
        # the script still reports the path the user asked for.
        home = os.path.join(os.path.expanduser("~"), ".claude", "chiron")
        path = log_path("munger", home=home, plugin_root=PLUGIN)
        self.assertEqual(path, os.path.join(os.path.abspath(home), "logs", "munger", "log.md"))

    def test_env_override_is_honored_and_still_outside_the_plugin(self):
        home = tempfile.mkdtemp(prefix="chiron-home-")
        self.addCleanup(shutil.rmtree, home)
        old = os.environ.get("CHIRON_HOME")
        os.environ["CHIRON_HOME"] = home
        self.addCleanup(self._restore_env, old)
        path = log_path("tim-ferriss", plugin_root=PLUGIN)
        self.assertTrue(path.startswith(os.path.abspath(home) + os.sep))
        self.assertFalse(path.startswith(os.path.abspath(PLUGIN) + os.sep))

    def test_refuses_a_home_inside_the_plugin(self):
        plugin = tempfile.mkdtemp(prefix="chiron-plugin-")
        self.addCleanup(shutil.rmtree, plugin)
        with self.assertRaises(ValueError):
            log_path("munger", home=os.path.join(plugin, "data"), plugin_root=plugin)

    def test_cli_prints_the_user_data_path(self):
        home = tempfile.mkdtemp(prefix="chiron-home-")
        self.addCleanup(shutil.rmtree, home)
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(io.StringIO()):
            code = main(["log", "naval", "--home", home, "--plugin-root", PLUGIN, "--ensure"])
        self.assertEqual(code, 0)
        path = out.getvalue().strip()
        self.assertEqual(path, os.path.join(os.path.abspath(home), "logs", "naval", "log.md"))
        self.assertTrue(os.path.isdir(os.path.dirname(path)))
        self.assertFalse(os.path.exists(path))  # the file is created on first write

    def test_read_uses_legacy_when_the_new_log_is_absent(self):
        new_home = tempfile.mkdtemp(prefix="chiron-new-")
        old_home = tempfile.mkdtemp(prefix="chiron-old-")
        self.addCleanup(shutil.rmtree, new_home)
        self.addCleanup(shutil.rmtree, old_home)
        legacy = os.path.join(old_home, "logs", "munger", "log.md")
        os.makedirs(os.path.dirname(legacy))
        with open(legacy, "w", encoding="utf-8") as handle:
            handle.write("# Log — munger\n\n## 2026-01-01 · ask\n")
        found = read_log_path("munger", home=new_home, plugin_root=PLUGIN, legacy_home=old_home)
        self.assertEqual(found, legacy)
        written = ensure_log("munger", home=new_home, plugin_root=PLUGIN, legacy_home=old_home)
        new_log = os.path.join(new_home, "logs", "munger", "log.md")
        self.assertEqual(written, new_log)
        with open(new_log, encoding="utf-8") as handle:
            self.assertIn("2026-01-01", handle.read())
        # A second ensure must not clobber an entry appended after the copy.
        with open(new_log, "a", encoding="utf-8") as handle:
            handle.write("\n## 2026-02-02 · ask\n")
        with open(legacy, "w", encoding="utf-8") as handle:
            handle.write("replaced\n")
        ensure_log("munger", home=new_home, plugin_root=PLUGIN, legacy_home=old_home)
        with open(new_log, encoding="utf-8") as handle:
            text = handle.read()
        self.assertIn("2026-02-02", text)
        self.assertNotIn("replaced", text)
        again = read_log_path("munger", home=new_home, plugin_root=PLUGIN, legacy_home=old_home)
        self.assertEqual(again, new_log)

    def test_explicit_home_does_not_read_legacy(self):
        new_home = tempfile.mkdtemp(prefix="chiron-new-")
        self.addCleanup(shutil.rmtree, new_home)
        found = read_log_path("munger", home=new_home, plugin_root=PLUGIN)
        self.assertEqual(found, os.path.join(new_home, "logs", "munger", "log.md"))
        self.assertFalse(os.path.exists(found))

    def test_cli_read_and_seats(self):
        new_home = tempfile.mkdtemp(prefix="chiron-new-")
        old_home = tempfile.mkdtemp(prefix="chiron-old-")
        self.addCleanup(shutil.rmtree, new_home)
        self.addCleanup(shutil.rmtree, old_home)
        legacy = os.path.join(old_home, "logs", "naval", "log.md")
        os.makedirs(os.path.dirname(legacy))
        with open(legacy, "w", encoding="utf-8") as handle:
            handle.write("legacy entry\n")
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(io.StringIO()):
            code = main(["log", "naval", "--read", "--home", new_home,
                         "--legacy-home", old_home, "--plugin-root", PLUGIN])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), legacy)
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(io.StringIO()):
            code = main(["seats", "--home", new_home, "--plugin-root", PLUGIN, "--ensure"])
        self.assertEqual(code, 0)
        seat_path = out.getvalue().strip()
        self.assertEqual(seat_path, seats_dir(home=new_home, plugin_root=PLUGIN))
        self.assertTrue(os.path.isdir(seat_path))
        self.assertFalse(seat_path.startswith(os.path.abspath(PLUGIN) + os.sep))

    def _restore_env(self, old):
        if old is None:
            os.environ.pop("CHIRON_HOME", None)
        else:
            os.environ["CHIRON_HOME"] = old


class NoPluginLogInstructionTests(unittest.TestCase):
    """No doc or command may tell a seat to write its log inside the plugin."""

    SCAN = ["commands", "docs", "skills/chiron", "README.md", "SEAT_SPEC.md", "CONTRIBUTING.md"]
    WRITE = re.compile(
        r"<seat-dir>/log\.md"
        r"|CLAUDE_PLUGIN_ROOT[^\n]{0,160}log\.md"
        r"|log\.md[^\n]{0,160}CLAUDE_PLUGIN_ROOT"
        r"|skills/<id>/log\.md",
        re.IGNORECASE,
    )
    NEGATION = re.compile(r"\b(never|not|don't|do not|nowhere)\b", re.IGNORECASE)

    def test_nothing_instructs_a_log_write_under_the_plugin(self):
        bad = []
        for rel in self.SCAN:
            path = os.path.join(REPO, rel)
            files = []
            if os.path.isdir(path):
                for dirpath, _, names in os.walk(path):
                    files.extend(os.path.join(dirpath, n) for n in names if n.endswith(".md"))
            else:
                files.append(path)
            for filename in files:
                with open(filename, encoding="utf-8") as handle:
                    for lineno, line in enumerate(handle, 1):
                        if self.WRITE.search(line) and not self.NEGATION.search(line):
                            bad.append("%s:%d: %s" % (
                                os.path.relpath(filename, REPO), lineno, line.strip()))
        self.assertEqual(bad, [], "\n".join(bad))


class NoSensitiveWriteInstructionTests(unittest.TestCase):
    """Commands must not tell the model to write under ~/.claude."""

    SCAN = ["commands", "skills/chiron", "README.md", "SEAT_SPEC.md", "CONTRIBUTING.md", "docs"]
    SENSITIVE = re.compile(r"~/?\.claude/")
    WRITE = re.compile(
        r"\b(write|writes|writing|wrote|append|appends|appending|create the file)\b",
        re.IGNORECASE,
    )
    ALLOW = re.compile(
        r"\b(never|not|don't|do not|cannot|can't|refuses|refused|legacy|read-only|old )\b",
        re.IGNORECASE,
    )

    def test_nothing_instructs_a_write_under_claude_home(self):
        bad = []
        for rel in self.SCAN:
            path = os.path.join(REPO, rel)
            files = []
            if os.path.isdir(path):
                for dirpath, _, names in os.walk(path):
                    files.extend(os.path.join(dirpath, n) for n in names if n.endswith(".md"))
            elif os.path.isfile(path):
                files.append(path)
            for filename in files:
                with open(filename, encoding="utf-8") as handle:
                    for lineno, line in enumerate(handle, 1):
                        if (self.SENSITIVE.search(line) and self.WRITE.search(line)
                                and not self.ALLOW.search(line)):
                            bad.append("%s:%d: %s" % (
                                os.path.relpath(filename, REPO), lineno, line.strip()))
        self.assertEqual(bad, [], "\n".join(bad))


if __name__ == "__main__":
    unittest.main()
