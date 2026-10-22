#!/usr/bin/env python3
"""Build the Cowork chiron.plugin bundle from this repo.

Usage:
    python3 scripts/build_bundle.py <dest.plugin>
    python3 scripts/build_bundle.py --check <dest.plugin>

The bundle is a zip of the runtime: manifests, commands, scripts, seats,
example benches, and the short docs a command reads (README, SEAT_SPEC,
LEGAL, LICENSE). Demo media and the docs site stay out; they are not needed
to run the plugin and they dominate the install size.

--check reads a bundle and reports whether it carries version 0.3.0, the
coach command, the Ferriss seat, the bench resolver, and all 19 seats.
Exit codes: 0 = ok, 1 = check failed, 2 = usage.
"""

import json
import os
import sys
import zipfile

from lint_seat import NON_SEAT_SKILLS

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INCLUDE_DIRS = [".claude-plugin", "commands", "scripts", "skills", "benches"]
INCLUDE_FILES = ["README.md", "LICENSE", "LEGAL.md", "SEAT_SPEC.md"]
EXPECTED_VERSION = "0.3.0"
SKIP_DIRS = {"__pycache__", ".git"}


def _repo_files():
    paths = []
    for name in INCLUDE_FILES:
        paths.append(name)
    for directory in INCLUDE_DIRS:
        base = os.path.join(REPO, directory)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
            for filename in sorted(filenames):
                if filename.endswith(".pyc"):
                    continue
                full = os.path.join(dirpath, filename)
                paths.append(os.path.relpath(full, REPO).replace(os.sep, "/"))
    return paths


def build(dest):
    """Write the bundle zip. Returns the absolute destination path."""
    dest = os.path.abspath(dest)
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for rel in _repo_files():
            archive.write(os.path.join(REPO, rel), rel)
    return dest


def check(path, expected_version=EXPECTED_VERSION):
    """Return a list of problems. Empty means the bundle is good."""
    problems = []
    if not zipfile.is_zipfile(path):
        return ["%s is not a zip archive" % path]
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        try:
            manifest = json.loads(archive.read(".claude-plugin/plugin.json"))
        except KeyError:
            return ["missing .claude-plugin/plugin.json"]
        version = manifest.get("version")
        if version != expected_version:
            problems.append("plugin.json version is %r, expected %r"
                            % (version, expected_version))
        required = [
            "commands/coach.md",
            "scripts/benches.py",
            "scripts/memory.py",
            "scripts/registry.py",
            "scripts/lint_seat.py",
            "skills/tim-ferriss/SKILL.md",
            "skills/chiron/SKILL.md",
            "skills/ask/SKILL.md",
            "skills/council/SKILL.md",
            "skills/coach/SKILL.md",
            "skills/log/SKILL.md",
            "benches/examples/benches.yaml",
        ]
        for rel in required:
            if rel not in names:
                problems.append("missing %s" % rel)
        seats = sorted({
            parts[1] for parts in (n.split("/") for n in names)
            if len(parts) >= 3 and parts[0] == "skills" and parts[-1] == "SKILL.md"
            and parts[1] not in NON_SEAT_SKILLS
        })
        if len(seats) != 19:
            problems.append("expected 19 seats, found %d: %s" % (len(seats), ", ".join(seats)))
        for banned in ("demo/", "assets/", "docs/", "tests/"):
            leaked = [n for n in names if n.startswith(banned)]
            if leaked:
                problems.append("bundle contains %s (%d files)" % (banned, len(leaked)))
    return problems


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    checking = False
    if argv and argv[0] == "--check":
        checking = True
        argv = argv[1:]
    if len(argv) != 1:
        print("usage: python3 scripts/build_bundle.py [--check] <dest.plugin>",
              file=sys.stderr)
        return 2
    dest = argv[0]
    if not checking:
        build(dest)
        print(dest)
    problems = check(dest)
    if problems:
        for problem in problems:
            print("error: %s" % problem, file=sys.stderr)
        return 1
    if checking:
        print("ok %s (version %s, 19 seats)" % (dest, EXPECTED_VERSION))
    return 0


if __name__ == "__main__":
    sys.exit(main())
