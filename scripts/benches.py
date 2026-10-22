#!/usr/bin/env python3
"""Chiron bench resolver — reads the bench YAMLs and emits the benches in effect.

Usage:
    python3 scripts/benches.py [--json] [--project FILE] [--global FILE]
                               [--examples FILE] [NAME]

Scopes, lowest precedence first:
    legacy    ~/.claude/chiron/benches.yaml   (read only; older installs)
    global    ~/.chiron/benches.yaml          (or $CHIRON_HOME/benches.yaml)
    project   .chiron/benches.yaml            (shadows global on a name collision)

Writes go to the global or project file, never to the legacy path. Claude Code
refuses writes under ~/.claude. If none of the three user files exists, the
bundled examples (benches/examples/benches.yaml, next to this script) are used
instead, so a fresh install can convene `money`, `relationship`, etc. straight
away. Once the user has a benches file of their own, the examples drop out
entirely.

    python3 scripts/benches.py --paths
prints project, global, legacy, and examples locations as JSON.

Output (--json): [{name, seats, chairman, default_depth, source, path, shadows?}]
With NAME, prints only that bench.
Exit codes: 0 = ok, 1 = NAME not found, 2 = a benches file could not be parsed.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_seat import parse_yaml_block  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PROJECT = os.path.join(".chiron", "benches.yaml")
DEFAULT_GLOBAL = os.path.join("~", ".chiron", "benches.yaml")
DEFAULT_LEGACY = os.path.join("~", ".claude", "chiron", "benches.yaml")
DEFAULT_EXAMPLES = os.path.join(REPO, "benches", "examples", "benches.yaml")


def global_benches_file():
    """Where a new global benches file is written. CHIRON_HOME wins over ~/.chiron."""
    home = os.environ.get("CHIRON_HOME")
    if home:
        return os.path.abspath(os.path.join(os.path.expanduser(home), "benches.yaml"))
    return os.path.abspath(os.path.expanduser(DEFAULT_GLOBAL))


def legacy_benches_file():
    """Older global file. Read, never written."""
    return os.path.abspath(os.path.expanduser(DEFAULT_LEGACY))


def load_benches_file(path):
    """Return {name: {seats, chairman, default_depth}} from one benches YAML."""
    with open(path, encoding="utf-8") as fh:
        # The YAML-subset parser keeps trailing "# ..." in values; bench files
        # document fields with inline comments, so drop them first.
        lines = [re.sub(r"\s+#.*$", "", line) for line in fh.read().split("\n")]
    data = parse_yaml_block(lines)
    benches = data.get("benches") or {}
    if not isinstance(benches, dict):
        raise ValueError("%s: `benches:` must be a mapping" % path)
    out = {}
    for name, spec in benches.items():
        spec = spec if isinstance(spec, dict) else {}
        out[name] = {
            "seats": list(spec.get("seats") or []),
            "chairman": spec.get("chairman") or "neutral",
            "default_depth": spec.get("default_depth") or "quick",
        }
    return out


def resolve_benches(project_file=None, global_file=None,
                    examples_file=None, legacy_file=None):
    """Merge the bench scopes in precedence order and return a list of entries.

    The bundled examples are used only when no user benches file exists,
    including the legacy ~/.claude/chiron file.
    """
    if project_file is None:
        project_file = DEFAULT_PROJECT
    if global_file is None:
        global_file = global_benches_file()
    if examples_file is None:
        examples_file = DEFAULT_EXAMPLES
    if legacy_file is None:
        legacy_file = legacy_benches_file()
    user_scopes = [("legacy", os.path.expanduser(legacy_file)),
                   ("global", os.path.expanduser(global_file)),
                   ("project", project_file)]
    scopes = [(s, p) for s, p in user_scopes if os.path.isfile(p)]
    if not scopes and os.path.isfile(examples_file):
        scopes = [("example", examples_file)]

    merged = {}
    order = []
    for source, path in scopes:
        for name, spec in load_benches_file(path).items():
            entry = dict(spec, name=name, source=source, path=path)
            if name in merged:
                entry["shadows"] = merged[name]["path"]
            else:
                order.append(name)
            merged[name] = entry
    return [merged[n] for n in order]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Chiron bench resolver")
    parser.add_argument("name", nargs="?", help="print only this bench")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--global", dest="global_file", default=None,
                        help="global benches file (default ~/.chiron/benches.yaml or $CHIRON_HOME)")
    parser.add_argument("--legacy", dest="legacy_file", default=None,
                        help="older global file, read only (default ~/.claude/chiron/benches.yaml)")
    parser.add_argument("--examples", default=DEFAULT_EXAMPLES)
    parser.add_argument("--paths", action="store_true",
                        help="print project, global, legacy, and examples paths as JSON")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.paths:
        print(json.dumps({
            "project": args.project,
            "global": os.path.abspath(os.path.expanduser(args.global_file)) if args.global_file
                     else global_benches_file(),
            "legacy": os.path.abspath(os.path.expanduser(args.legacy_file)) if args.legacy_file
                     else legacy_benches_file(),
            "examples": args.examples,
        }, indent=2))
        return 0

    try:
        benches = resolve_benches(args.project, args.global_file, args.examples,
                                  args.legacy_file)
    except (OSError, ValueError) as exc:
        err = {"error": "could not read benches: %s" % exc}
        print(json.dumps(err) if args.json else err["error"], file=sys.stderr)
        return 2

    if args.name:
        benches = [b for b in benches if b["name"] == args.name]
        if not benches:
            err = {"error": "no bench named %r" % args.name}
            print(json.dumps(err) if args.json else err["error"], file=sys.stderr)
            return 1

    if args.json:
        print(json.dumps(benches, indent=2))
    else:
        if benches and all(b["source"] == "example" for b in benches):
            print("(no benches file yet; using the bundled examples)")
        for b in benches:
            tag = "  (shadows %s)" % b["shadows"] if b.get("shadows") else ""
            print("  %-14s %-8s chair:%-10s %-6s [%s]%s"
                  % (b["name"], b["source"], b["chairman"], b["default_depth"],
                     ", ".join(b["seats"]), tag))
    return 0


if __name__ == "__main__":
    sys.exit(main())
