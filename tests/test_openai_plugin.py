"""The ChatGPT/Codex manifest and marketplace match the portable plugin format."""

import os
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

from validate_openai_plugin import (  # noqa: E402
    check_marketplace,
    check_plugin_manifest,
    validate,
)


class OpenAIPluginTests(unittest.TestCase):
    def test_repo_manifest_and_marketplace_validate(self):
        self.assertEqual(validate(REPO), [])

    def test_schema_rejects_unknown_keys_and_bad_names(self):
        good = {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": "chiron",
            "version": "0.3.0",
        }
        self.assertEqual(check_plugin_manifest(good, "0.3.0"), [])
        extra = dict(good, commands="./commands")
        problems = check_plugin_manifest(extra, "0.3.0")
        self.assertTrue(any("unknown keys" in p for p in problems))
        bad_name = dict(good, name="Chiron")
        problems = check_plugin_manifest(bad_name, "0.3.0")
        self.assertTrue(any("name" in p for p in problems))

    def test_marketplace_source_must_be_the_repo_root(self):
        good = {
            "name": "compound-club",
            "interface": {"displayName": "Compound Club"},
            "plugins": [{
                "name": "chiron",
                "source": {"source": "local", "path": "./"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Productivity",
            }],
        }
        self.assertEqual(check_marketplace(good), [])
        nested = {
            "name": "compound-club",
            "interface": {"displayName": "Compound Club"},
            "plugins": [{
                "name": "chiron",
                "source": {"source": "local", "path": "./plugins/chiron"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Productivity",
            }],
        }
        problems = check_marketplace(nested)
        self.assertTrue(any("repo root" in p for p in problems))
        string_form = dict(good)
        string_form["plugins"] = [dict(good["plugins"][0], source="./")]
        self.assertEqual(check_marketplace(string_form), [])


if __name__ == "__main__":
    unittest.main()
