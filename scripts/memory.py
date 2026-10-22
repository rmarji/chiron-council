#!/usr/bin/env python3
"""Chiron seat memory — where a seat's consult log and private seats live.

Usage:
    python3 scripts/memory.py log <seat-id> [--home DIR] [--ensure] [--read]
    python3 scripts/memory.py seats [--home DIR] [--ensure]

User data defaults to ~/.chiron. Claude Code refuses writes under ~/.claude
(it treats that tree as a sensitive file), so nothing Chiron writes goes there.
Pass --home to override. CHIRON_HOME overrides the default, and an explicit
--home overrides CHIRON_HOME (Cowork cannot write the home directory at all,
so those commands pass --home .chiron).

    logs:   <home>/logs/<seat-id>/log.md
    seats:  <home>/seats/

`log` prints the path to write. `--read` prints the path to read: the new file
if it exists, otherwise the same log under the previous default
(~/.claude/chiron) when the user is still on the default home. `--ensure`
creates the parent directory and, on the default home only, copies a legacy
log into the new path once so a later append does not split the history.

Prints the absolute path. Exit codes: 0 = ok, 2 = bad id or the path would
land inside the plugin install.
"""

import argparse
import os
import re
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEAT_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
DEFAULT_HOME = os.path.join("~", ".chiron")
LEGACY_HOME = os.path.join("~", ".claude", "chiron")


def user_home(home=None):
    """User-data directory. --home wins, then CHIRON_HOME, then ~/.chiron."""
    chosen = home or os.environ.get("CHIRON_HOME") or DEFAULT_HOME
    return os.path.abspath(os.path.expanduser(chosen))


def using_default_home(home=None):
    """True when neither --home nor CHIRON_HOME picked the directory."""
    return not home and not os.environ.get("CHIRON_HOME")


def legacy_root(override=None):
    return os.path.abspath(os.path.expanduser(override or LEGACY_HOME))


def _reject_plugin(path, plugin_root):
    if not plugin_root:
        return
    plugin = os.path.abspath(plugin_root)
    if path == plugin or path.startswith(plugin + os.sep):
        raise ValueError("path %s is inside the plugin install %s" % (path, plugin))


def log_path(seat_id, home=None, plugin_root=None):
    """Absolute log path to write. Raises ValueError if it is unsafe."""
    if not SEAT_ID.match(seat_id or ""):
        raise ValueError("bad seat id: %r" % seat_id)
    path = os.path.join(user_home(home), "logs", seat_id, "log.md")
    _reject_plugin(path, plugin_root)
    return path


def _legacy_log(seat_id, legacy_home=None):
    if not SEAT_ID.match(seat_id or ""):
        raise ValueError("bad seat id: %r" % seat_id)
    return os.path.join(legacy_root(legacy_home), "logs", seat_id, "log.md")


def _may_use_legacy(home, legacy_home):
    """Legacy is the old default only. An explicit home does not fall back,
    unless a caller passes legacy_home to point at a specific old tree."""
    return bool(legacy_home) or using_default_home(home)


def read_log_path(seat_id, home=None, plugin_root=None, legacy_home=None):
    """Path to read. New file if it exists, else a legacy file, else the write path."""
    path = log_path(seat_id, home=home, plugin_root=plugin_root)
    if os.path.isfile(path):
        return path
    if _may_use_legacy(home, legacy_home):
        old = _legacy_log(seat_id, legacy_home)
        if os.path.isfile(old):
            return old
    return path


def ensure_log(seat_id, home=None, plugin_root=None, legacy_home=None):
    """Create the log directory and copy a legacy log across once. Returns the write path."""
    path = log_path(seat_id, home=home, plugin_root=plugin_root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.isfile(path) and _may_use_legacy(home, legacy_home):
        old = _legacy_log(seat_id, legacy_home)
        if os.path.isfile(old):
            shutil.copyfile(old, path)
    return path


def seats_dir(home=None, plugin_root=None):
    """Directory Chiron writes distilled seats and the private me seat into."""
    path = os.path.join(user_home(home), "seats")
    _reject_plugin(path, plugin_root)
    return path


def _warn_if_sensitive(path):
    claude = os.path.abspath(os.path.expanduser(os.path.join("~", ".claude")))
    if path == claude or path.startswith(claude + os.sep):
        print("warning: %s is under ~/.claude, which Claude Code refuses to write" % path,
              file=sys.stderr)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Chiron seat memory paths")
    sub = parser.add_subparsers(dest="cmd")

    log = sub.add_parser("log", help="print the consult-log path for a seat")
    log.add_argument("seat_id")
    log.add_argument("--home", help="user-data dir (overrides $CHIRON_HOME; default ~/.chiron)")
    log.add_argument("--plugin-root", default=REPO,
                     help="refuse a path inside this directory")
    log.add_argument("--ensure", action="store_true",
                     help="create the parent directory and copy a legacy log once")
    log.add_argument("--read", action="store_true",
                     help="print the path to read (new file, else the legacy file)")
    log.add_argument("--legacy-home",
                     help="old user-data dir to read (default ~/.claude/chiron)")

    seats = sub.add_parser("seats", help="print the directory Chiron writes seats into")
    seats.add_argument("--home", help="user-data dir (overrides $CHIRON_HOME; default ~/.chiron)")
    seats.add_argument("--plugin-root", default=REPO,
                       help="refuse a path inside this directory")
    seats.add_argument("--ensure", action="store_true",
                       help="create the directory")

    args = parser.parse_args(argv)

    try:
        if args.cmd == "log":
            if args.read and args.ensure:
                print("error: pass only one of --read and --ensure", file=sys.stderr)
                return 2
            if args.read:
                path = read_log_path(args.seat_id, home=args.home,
                                     plugin_root=args.plugin_root,
                                     legacy_home=args.legacy_home)
            elif args.ensure:
                path = ensure_log(args.seat_id, home=args.home,
                                  plugin_root=args.plugin_root,
                                  legacy_home=args.legacy_home)
                _warn_if_sensitive(path)
            else:
                path = log_path(args.seat_id, home=args.home,
                                plugin_root=args.plugin_root)
                _warn_if_sensitive(path)
        elif args.cmd == "seats":
            path = seats_dir(home=args.home, plugin_root=args.plugin_root)
            if args.ensure:
                os.makedirs(path, exist_ok=True)
            _warn_if_sensitive(path)
        else:
            parser.print_help(sys.stderr)
            return 2
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
