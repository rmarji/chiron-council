#!/usr/bin/env python3
"""Chiron seat registry — scans one or more seat dirs and emits a roster index.

Usage:
    python3 scripts/registry.py [--seats-dir DIR]... [--json] [--domain TAG]

Multiple --seats-dir may be given, in precedence order (lowest first). A seat
id found in a later dir shadows the same id in an earlier one. This is how
bundled seats, global user seats (~/.claude/chiron/seats), and project seats
(.chiron/seats) merge into one roster. Missing dirs are skipped.

Output (--json): [{id, display_name, mode, domains, lint, path, shadows?}]
Exit codes: 0 = ok, 2 = no seat directory found at all.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_seat import discover_seats, lint_seat, lint_status  # noqa: E402


def build_registry(seats_dirs, level="standard"):
    """Merge seats from dirs in precedence order (later dirs shadow earlier).

    Accepts a single dir string or a list. Returns None only if no dir exists.
    """
    if isinstance(seats_dirs, str):
        seats_dirs = [seats_dirs]

    # Union of every installed id across all scopes, for L9 counterpart checks.
    installed_ids = set()
    for d in seats_dirs:
        for p in discover_seats(d) or []:
            installed_ids.add(os.path.basename(p.rstrip("/")))

    merged = {}   # id -> entry (higher-precedence scope wins)
    order = []    # first-seen order, for stable output
    any_found = False

    for d in seats_dirs:
        paths = discover_seats(d)
        if paths is None:
            continue
        any_found = True

        dir_entries = []
        for path in paths:
            findings, meta = lint_seat(path, level=level, installed_ids=installed_ids)
            dir_entries.append({
                "id": meta["id"],
                "display_name": meta["display_name"],
                "mode": meta["mode"],
                "domains": meta["domains"],
                "lint": lint_status(findings),
                "path": path,
            })

        # L3 within this scope: two folders claiming the same frontmatter id
        # is an ambiguous collision, not intentional shadowing — fail both.
        counts = {}
        for e in dir_entries:
            counts[e["id"]] = counts.get(e["id"], 0) + 1
        for e in dir_entries:
            if counts[e["id"]] > 1:
                e["lint"] = "fail"

        # Cross-scope: a later dir intentionally shadows an earlier same-id seat.
        for e in dir_entries:
            if e["id"] in merged:
                e["shadows"] = merged[e["id"]]["path"]
            else:
                order.append(e["id"])
            merged[e["id"]] = e

    if not any_found:
        return None
    return [merged[i] for i in order]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Chiron seat registry")
    parser.add_argument("--seats-dir", action="append", dest="seats_dirs",
                        help="seat directory (repeatable; precedence low to high)")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--domain", help="filter by domain tag")
    args = parser.parse_args(argv)

    seats_dirs = args.seats_dirs or ["seats"]
    registry = build_registry(seats_dirs)
    if registry is None:
        err = {"error": "no seats directory found; run /chiron:distill or install a pack"}
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
                tag = "  (shadows %s)" % r["shadows"] if r.get("shadows") else ""
                print("  %-14s %-32s %-8s lint:%-5s [%s]%s"
                      % (r["id"], r["display_name"] or "?", r["mode"] or "?",
                         r["lint"], ", ".join(r["domains"]), tag))
    return 0


if __name__ == "__main__":
    sys.exit(main())
