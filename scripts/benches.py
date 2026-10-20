#!/usr/bin/env python3
"""Chiron bench resolver — reads the bench YAMLs and emits the benches in effect.

Usage:
    python3 scripts/benches.py [--json] [--project FILE] [--global FILE]
                               [--examples FILE] [NAME]

Scopes, lowest precedence first:
    global    ~/.claude/chiron/benches.yaml
    project   .chiron/benches.yaml            (shadows global on a name collision)

If neither user file exists, the bundled examples
(benches/examples/benches.yaml, next to this script) are used instead, so a
fresh install can convene `money`, `relationship`, etc. straight away. Once the
user has a benches file of their own, the examples drop out entirely.

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
DEFAULT_GLOBAL = os.path.join("~", ".claude", "chiron", "benches.yaml")
DEFAULT_EXAMPLES = os.path.join(REPO, "benches", "examples", "benches.yaml")


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


def resolve_benches(project_file=DEFAULT_PROJECT, global_file=DEFAULT_GLOBAL,
                    examples_file=DEFAULT_EXAMPLES):
    """Merge the bench scopes in precedence order and return a list of entries.

    The bundled examples are used only when no user benches file exists.
    """
    user_scopes = [("global", os.path.expanduser(global_file)),
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
    parser.add_argument("--global", dest="global_file", default=DEFAULT_GLOBAL)
    parser.add_argument("--examples", default=DEFAULT_EXAMPLES)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        benches = resolve_benches(args.project, args.global_file, args.examples)
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
