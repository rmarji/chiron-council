#!/usr/bin/env python3
"""Validate the portable ChatGPT/Codex plugin manifest and repo marketplace.

Mirrors the Agent Plugins 1.0.0 schema at
https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
and the marketplace shape Codex reads from .agents/plugins/marketplace.json.
The check is offline: it does not fetch the schema.

Usage:
    python3 scripts/validate_openai_plugin.py

Exit codes: 0 = ok, 1 = invalid, 2 = usage.
"""

import json
import os
import re
import sys

from lint_seat import NON_SEAT_SKILLS, discover_seats, split_frontmatter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PLUGIN_KEYS = {
    "$schema", "name", "version", "description", "author",
    "homepage", "repository", "license", "keywords", "extensions",
}
AUTHOR_KEYS = {"name", "email", "url"}
NAME_RE = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
FLOW_SKILLS = ("ask", "council", "coach", "log")
INSTALL_POLICIES = {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}
AUTH_POLICIES = {"ON_INSTALL", "ON_USE"}


def check_plugin_manifest(data, claude_version):
    """Return problems for a portable plugin.json object."""
    problems = []
    if not isinstance(data, dict):
        return ["plugin.json must be an object"]
    extra = sorted(set(data) - PLUGIN_KEYS)
    if extra:
        problems.append("plugin.json has unknown keys: %s" % ", ".join(extra))
    if data.get("$schema") != SCHEMA:
        problems.append("plugin.json $schema must be %s" % SCHEMA)
    name = data.get("name")
    if not isinstance(name, str) or not NAME_RE.match(name) or not 1 <= len(name) <= 64:
        problems.append("plugin.json name %r does not match the Agent Plugins pattern" % name)
    elif name != "chiron":
        problems.append("plugin.json name is %r, expected 'chiron'" % name)
    version = data.get("version")
    if version != claude_version:
        problems.append("plugin.json version %r does not match .claude-plugin/plugin.json %r"
                        % (version, claude_version))
    author = data.get("author")
    if author is not None:
        if not isinstance(author, dict):
            problems.append("plugin.json author must be an object")
        else:
            extra_author = sorted(set(author) - AUTHOR_KEYS)
            if extra_author:
                problems.append("plugin.json author has unknown keys: %s" % ", ".join(extra_author))
            if not author.get("name"):
                problems.append("plugin.json author.name is empty")
    keywords = data.get("keywords")
    if keywords is not None and (
            not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords)):
        problems.append("plugin.json keywords must be an array of strings")
    return problems


def plugin_source_path(source):
    """Return the local path string, or None when source is not a local path."""
    if isinstance(source, str):
        return source
    if isinstance(source, dict) and source.get("source") == "local":
        path = source.get("path")
        if isinstance(path, str):
            return path
    return None


def check_marketplace(data):
    """Return problems for .agents/plugins/marketplace.json."""
    problems = []
    if not isinstance(data, dict):
        return ["marketplace.json must be an object"]
    if data.get("name") != "compound-club":
        problems.append("marketplace name is %r, expected 'compound-club'" % data.get("name"))
    interface = data.get("interface") or {}
    if not isinstance(interface, dict) or interface.get("displayName") != "Compound Club":
        problems.append("marketplace interface.displayName must be 'Compound Club'")
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        return problems + ["marketplace must list exactly one plugin"]
    plugin = plugins[0]
    if not isinstance(plugin, dict):
        return problems + ["marketplace plugin entry must be an object"]
    if plugin.get("name") != "chiron":
        problems.append("marketplace plugin name is %r, expected 'chiron'" % plugin.get("name"))
    path = plugin_source_path(plugin.get("source"))
    if path not in (".", "./"):
        problems.append(
            "marketplace source path is %r; it must be './' so the plugin is the repo root "
            "and the seats are not copied" % path)
    policy = plugin.get("policy") or {}
    if not isinstance(policy, dict):
        problems.append("marketplace policy must be an object")
    else:
        if policy.get("installation") not in INSTALL_POLICIES:
            problems.append("marketplace policy.installation must be one of %s"
                            % ", ".join(sorted(INSTALL_POLICIES)))
        if policy.get("authentication") not in AUTH_POLICIES:
            problems.append("marketplace policy.authentication must be one of %s"
                            % ", ".join(sorted(AUTH_POLICIES)))
    if plugin.get("category") != "Productivity":
        problems.append("marketplace category is %r, expected 'Productivity'" % plugin.get("category"))
    return problems


def check_skills(repo):
    """Return problems for skill frontmatter and the shared flow skills."""
    problems = []
    skills_dir = os.path.join(repo, "skills")
    missing = [name for name in FLOW_SKILLS if name not in NON_SEAT_SKILLS]
    if missing:
        problems.append("NON_SEAT_SKILLS is missing flow skills: %s" % ", ".join(missing))
    if "chiron" not in NON_SEAT_SKILLS:
        problems.append("NON_SEAT_SKILLS must include the chiron router")
    seats = discover_seats(skills_dir, for_lint=True)
    if seats is None:
        problems.append("skills/ is missing")
    elif len(seats) != 19:
        names = [os.path.basename(p) for p in seats]
        problems.append("expected 19 seats, found %d: %s" % (len(seats), ", ".join(names)))
    if not os.path.isdir(skills_dir):
        return problems
    for entry in sorted(os.listdir(skills_dir)):
        path = os.path.join(skills_dir, entry)
        skill_md = os.path.join(path, "SKILL.md")
        if not os.path.isdir(path) or not os.path.isfile(skill_md):
            continue
        with open(skill_md, encoding="utf-8") as handle:
            text = handle.read()
        fm, body, err = split_frontmatter(text)
        if err or not fm:
            problems.append("%s: %s" % (entry, err or "no frontmatter"))
            continue
        name = fm.get("name")
        description = fm.get("description")
        if not isinstance(name, str) or not name.strip():
            problems.append("%s: name is empty" % entry)
        elif name != entry:
            problems.append("%s: frontmatter name is %r" % (entry, name))
        if not isinstance(description, str) or not description.strip():
            problems.append("%s: description is empty" % entry)
    for flow in FLOW_SKILLS:
        skill_md = os.path.join(skills_dir, flow, "SKILL.md")
        command = os.path.join(repo, "commands", flow + ".md")
        if not os.path.isfile(skill_md):
            problems.append("missing skills/%s/SKILL.md" % flow)
            continue
        if not os.path.isfile(command):
            problems.append("missing commands/%s.md" % flow)
        with open(skill_md, encoding="utf-8") as handle:
            text = handle.read()
        fm, body, _err = split_frontmatter(text)
        if fm and fm.get("x-chiron"):
            problems.append("skills/%s is a flow skill and must not carry x-chiron" % flow)
        if "commands/%s.md" % flow not in body:
            problems.append("skills/%s must follow commands/%s.md" % (flow, flow))
        if "~/.chiron" not in body:
            problems.append("skills/%s must keep user data in ~/.chiron" % flow)
        if "Never write under `~/.claude`" not in body:
            problems.append("skills/%s must forbid writes under ~/.claude" % flow)
    return problems


def validate(repo=REPO):
    """Return a list of problems. Empty means the OpenAI plugin is valid."""
    problems = []
    plugin_path = os.path.join(repo, "plugin.json")
    claude_path = os.path.join(repo, ".claude-plugin", "plugin.json")
    market_path = os.path.join(repo, ".agents", "plugins", "marketplace.json")
    try:
        with open(plugin_path, encoding="utf-8") as handle:
            plugin = json.load(handle)
    except (OSError, ValueError) as exc:
        return ["plugin.json: %s" % exc]
    try:
        with open(claude_path, encoding="utf-8") as handle:
            claude = json.load(handle)
    except (OSError, ValueError) as exc:
        return problems + [".claude-plugin/plugin.json: %s" % exc]
    try:
        with open(market_path, encoding="utf-8") as handle:
            marketplace = json.load(handle)
    except (OSError, ValueError) as exc:
        return problems + [".agents/plugins/marketplace.json: %s" % exc]
    problems.extend(check_plugin_manifest(plugin, claude.get("version")))
    problems.extend(check_marketplace(marketplace))
    root_plugin = os.path.join(repo, "plugin.json")
    root_skills = os.path.join(repo, "skills")
    if not os.path.isfile(root_plugin) or not os.path.isdir(root_skills):
        problems.append("marketplace source './' must be a repo root with plugin.json and skills/")
    problems.extend(check_skills(repo))
    return problems


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv:
        print("usage: python3 scripts/validate_openai_plugin.py", file=sys.stderr)
        return 2
    problems = validate()
    if problems:
        for problem in problems:
            print("error: %s" % problem, file=sys.stderr)
        return 1
    print("ok plugin.json + .agents/plugins/marketplace.json (chiron@compound-club)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
