#!/usr/bin/env python3
"""Chiron seat memory — where a seat's consult log lives.

Usage:
    python3 scripts/memory.py log <seat-id> [--home DIR] [--ensure]

The log is user data, never part of the plugin install. The plugin cache
(~/.claude/plugins/cache/...) is wiped by `claude plugin update` and Claude
Code refuses writes there. Logs go to:

    ${CHIRON_HOME:-~/.claude/chiron}/logs/<seat-id>/log.md

Pass --home to override (Cowork cannot write ~/.claude; use --home .chiron).
--ensure creates the parent directory. The file itself is created on first
write by the command that appends.

Prints the absolute path. Exit codes: 0 = ok, 2 = bad id or the path would
land inside the plugin install.
"""

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEAT_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def user_home(home=None):
    """The stable user-data directory. CHIRON_HOME wins, then --home, then default."""
    chosen = home or os.environ.get("CHIRON_HOME") or os.path.join("~", ".claude", "chiron")
    return os.path.abspath(os.path.expanduser(chosen))


def log_path(seat_id, home=None, plugin_root=None):
    """Absolute log path for one seat. Raises ValueError if it is unsafe."""
    if not SEAT_ID.match(seat_id or ""):
        raise ValueError("bad seat id: %r" % seat_id)
    root = user_home(home)
    path = os.path.join(root, "logs", seat_id, "log.md")
    if plugin_root:
        plugin = os.path.abspath(plugin_root)
        if path == plugin or path.startswith(plugin + os.sep):
            raise ValueError("log path %s is inside the plugin install %s" % (path, plugin))
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Chiron seat memory paths")
    sub = parser.add_subparsers(dest="cmd")
    log = sub.add_parser("log", help="print the consult-log path for a seat")
    log.add_argument("seat_id")
    log.add_argument("--home", help="user-data dir (default $CHIRON_HOME or ~/.claude/chiron)")
    log.add_argument("--plugin-root", default=REPO,
                     help="refuse a path inside this directory")
    log.add_argument("--ensure", action="store_true",
                     help="create the parent directory")
    args = parser.parse_args(argv)

    if args.cmd != "log":
        parser.print_help(sys.stderr)
        return 2
    try:
        path = log_path(args.seat_id, home=args.home, plugin_root=args.plugin_root)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    if args.ensure:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
