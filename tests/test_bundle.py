"""The Cowork bundle is built from the repo and carries version 0.3.0."""

import os
import shutil
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

from build_bundle import EXPECTED_VERSION, build, check  # noqa: E402


class BundleTests(unittest.TestCase):
    def test_bundle_contains_runtime_and_version_0_3_0(self):
        root = tempfile.mkdtemp(prefix="chiron-bundle-")
        self.addCleanup(shutil.rmtree, root)
        dest = os.path.join(root, "chiron.plugin")
        build(dest)
        self.assertEqual(EXPECTED_VERSION, "0.3.0")
        self.assertEqual(check(dest, expected_version="0.3.0"), [])


if __name__ == "__main__":
    unittest.main()
