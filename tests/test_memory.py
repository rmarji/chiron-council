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

from memory import log_path, main  # noqa: E402

PLUGIN = os.path.join(os.path.expanduser("~"), ".claude", "plugins",
                       "cache", "compound-club", "chiron", "0.3.0")


class LogPathTests(unittest.TestCase):
    def test_log_is_outside_the_plugin_and_inside_user_data(self):
        home = os.path.join(os.path.expanduser("~"), ".claude", "chiron")
        path = log_path("munger", home=home, plugin_root=PLUGIN)
        home_abs = os.path.abspath(home)
        plugin_abs = os.path.abspath(PLUGIN)
        self.assertTrue(path.startswith(home_abs + os.sep))
        self.assertFalse(path.startswith(plugin_abs + os.sep))
        self.assertEqual(path, os.path.join(home_abs, "logs", "munger", "log.md"))

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


if __name__ == "__main__":
    unittest.main()
