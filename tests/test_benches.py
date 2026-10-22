"""Unit tests for scripts/benches.py — bench resolution and the examples fallback."""

import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

from benches import DEFAULT_EXAMPLES, DEFAULT_GLOBAL, main, resolve_benches  # noqa: E402
from registry import build_registry  # noqa: E402


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


class BenchFallbackTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="chiron-benches-")
        self.project = os.path.join(self.root, "proj", ".chiron", "benches.yaml")
        self.global_ = os.path.join(self.root, "home", ".chiron", "benches.yaml")
        self.legacy = os.path.join(self.root, "legacy", "benches.yaml")

    def tearDown(self):
        shutil.rmtree(self.root)

    def resolve(self):
        return {b["name"]: b for b in resolve_benches(
            self.project, self.global_, DEFAULT_EXAMPLES, self.legacy)}

    def test_fresh_install_falls_back_to_examples(self):
        benches = self.resolve()
        for name in ("money", "strategy", "deals", "relationship",
                     "shipping", "work-design"):
            self.assertIn(name, benches)
            self.assertEqual(benches[name]["source"], "example")
        self.assertEqual(benches["relationship"]["seats"], ["deida", "terry-real"])
        self.assertEqual(benches["shipping"]["chairman"], "neutral")

    def test_user_global_file_replaces_examples(self):
        write(self.global_, "benches:\n  mine:\n    seats: [munger, naval]\n")
        benches = self.resolve()
        self.assertEqual(list(benches), ["mine"])
        self.assertEqual(benches["mine"]["source"], "global")
        self.assertEqual(benches["mine"]["chairman"], "neutral")
        self.assertEqual(benches["mine"]["default_depth"], "quick")

    def test_user_bench_shadows_example_of_same_name(self):
        write(self.project, "benches:\n  money:\n    seats: [hormozi, voss]\n")
        benches = self.resolve()
        self.assertEqual(benches["money"]["source"], "project")
        self.assertEqual(benches["money"]["seats"], ["hormozi", "voss"])

    def test_project_shadows_global(self):
        write(self.global_, "benches:\n  money:\n    seats: [munger, naval]\n")
        write(self.project, "benches:\n  money:\n    seats: [hormozi, voss]\n")
        money = self.resolve()["money"]
        self.assertEqual(money["source"], "project")
        self.assertEqual(money["shadows"], self.global_)

    def test_inline_comments_are_not_values(self):
        write(self.global_,
              "benches:\n"
              "  product:\n"
              "    seats: [munger, naval, rayo]\n"
              "    chairman: neutral        # a seat id, or \"neutral\"\n"
              "    default_depth: full      # quick | full\n")
        product = self.resolve()["product"]
        self.assertEqual(product["chairman"], "neutral")
        self.assertEqual(product["default_depth"], "full")

    def test_legacy_file_replaces_examples(self):
        write(self.legacy, "benches:\n  old:\n    seats: [munger, naval]\n")
        benches = self.resolve()
        self.assertEqual(list(benches), ["old"])
        self.assertEqual(benches["old"]["source"], "legacy")
        self.assertNotIn("relationship", benches)

    def test_global_shadows_legacy_by_name(self):
        write(self.legacy,
              "benches:\n  money:\n    seats: [munger]\n  old:\n    seats: [naval, rayo]\n")
        write(self.global_, "benches:\n  money:\n    seats: [hormozi, voss]\n")
        benches = self.resolve()
        self.assertEqual(benches["money"]["source"], "global")
        self.assertEqual(benches["money"]["seats"], ["hormozi", "voss"])
        self.assertEqual(benches["money"]["shadows"], self.legacy)
        self.assertEqual(benches["old"]["source"], "legacy")
        self.assertNotIn("relationship", benches)

    def test_project_shadows_legacy(self):
        write(self.legacy, "benches:\n  money:\n    seats: [munger, naval]\n")
        write(self.project, "benches:\n  money:\n    seats: [hormozi, voss]\n")
        money = self.resolve()["money"]
        self.assertEqual(money["source"], "project")
        self.assertEqual(money["shadows"], self.legacy)

    def test_default_global_path_is_outside_claude_home(self):
        self.assertTrue(DEFAULT_GLOBAL.endswith(os.path.join(".chiron", "benches.yaml")))
        self.assertNotIn(".claude", DEFAULT_GLOBAL)

    def test_cli_named_lookup(self):
        argv = ["--project", self.project, "--global", self.global_,
                "--legacy", self.legacy, "--json"]
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(main(argv + ["relationship"]), 0)
            self.assertEqual(main(argv + ["distribution"]), 1)

    def test_example_benches_only_name_bundled_seats(self):
        seats = {s["id"] for s in build_registry(os.path.join(REPO, "skills"))}
        for bench in resolve_benches(self.project, self.global_, DEFAULT_EXAMPLES, self.legacy):
            for seat in bench["seats"]:
                self.assertIn(seat, seats, "%s names unknown seat %s"
                              % (bench["name"], seat))


if __name__ == "__main__":
    unittest.main()
