#!/usr/bin/env python3
"""Chiron seat registry — scans seats/ and emits a roster index.

Usage:
    python3 scripts/registry.py [--seats-dir seats] [--json] [--domain TAG]

Output (--json): [{id, display_name, mode, domains, lint, path}]
Exit codes: 0 = ok, 2 = seats directory missing/unreadable.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_seat import discover_seats, lint_seat, lint_status  # noqa: E402


def build_registry(seats_dir, level="standard"):
    paths = discover_seats(seats_dir)
    if paths is None:
        return None
    installed_ids = {os.path.basename(p.rstrip("/")) for p in paths}
    registry = []
    for path in paths:
        findings, meta = lint_seat(path, level=level, installed_ids=installed_ids)
        registry.append({
            "id": meta["id"],
            "display_name": meta["display_name"],
            "mode": meta["mode"],
            "domains": meta["domains"],
            "lint": lint_status(findings),
            "path": path,
        })
    # L3: duplicate frontmatter ids make ask/bench resolution ambiguous —
    # mark every colliding entry as fail so nothing loads by shadowing.
    counts = {}
    for entry in registry:
        counts[entry["id"]] = counts.get(entry["id"], 0) + 1
    for entry in registry:
        if counts[entry["id"]] > 1:
            entry["lint"] = "fail"
    return registry


def main(argv=None):
    parser = argparse.ArgumentParser(description="Chiron seat registry")
    parser.add_argument("--seats-dir", default="seats")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--domain", help="filter by domain tag")
    args = parser.parse_args(argv)

    registry = build_registry(args.seats_dir)
    if registry is None:
        err = {"error": "no seats directory found; run /chiron:hire or install a pack"}
        print(json.dumps(err) if args.json else err["error"], file=sys.stderr)
        return 2

    if args.domain:
        registry = [r for r in registry
                    if args.domain.lower() in [d.lower() for d in r["domains"]]]

    if args.json:
        print(json.dumps(registry, indent=2))
    else:
        by_domain = {}
        for r in registry:
            key = r["domains"][0] if r["domains"] else "(untagged)"
            by_domain.setdefault(key, []).append(r)
        for domain in sorted(by_domain):
            print("%s:" % domain)
            for r in by_domain[domain]:
                print("  %-14s %-32s %-8s lint:%-5s [%s]"
                      % (r["id"], r["display_name"] or "?", r["mode"] or "?",
                         r["lint"], ", ".join(r["domains"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
