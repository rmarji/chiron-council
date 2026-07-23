#!/usr/bin/env python3
"""Chiron seat linter — validates SKILL.md files against SEAT_SPEC.md.

Usage:
    python3 scripts/lint_seat.py <seat-path> [<seat-path> ...]
    python3 scripts/lint_seat.py --all [--seats-dir seats]
    python3 scripts/lint_seat.py --all --format json --level strict

Exit codes: 0 = pass, 1 = warnings only, 2 = errors (load-blocking).

Stdlib-only by design: CI and non-Claude harnesses run it identically.
"""

import argparse
import json
import os
import re
import sys

RULES = {
    "L1": "persona mode with living subject and no license",
    "L2": "missing or invalid frontmatter field",
    "L3": "id collision with installed seat",
    "L4": "corpus/persona mode with fewer than 3 provenance sources",
    "L5": "required section missing or below minimum entries",
    "L6": "core SKILL.md exceeds 6k tokens",
    "L7": "first-person subject voice in corpus-mode seat (persona leakage)",
    "L8": "heuristic not in operational IF/THEN form",
    "L9": "disagreement counterpart unresolved and not marked external",
    "L10": "real person's name in display_name without mode suffix",
    "L11": "no eval file (strict/paid packs only)",
    "L12": "references/ missing standard reference files",
}

STANDARD_REFERENCES = [
    "principles.md",
    "mental-models.md",
    "frameworks.md",
    "anti-patterns.md",
    "heuristics.md",
    "quotes.md",
    "sources.md",
]

REQUIRED_SECTIONS = {
    # section keyword -> minimum bullet entries (0 = presence only)
    "Priors": 5,
    "Heuristics": 5,
    "Refusals": 2,
    "Voice": 0,
}

ID_PATTERN = re.compile(r"^[a-z0-9-]{2,32}$")
MODES = ("corpus", "persona", "original")
LICENSES = ("none", "granted", "n/a")


class Finding:
    def __init__(self, rule, level, message):
        self.rule = rule
        self.level = level  # "error" | "warn"
        self.message = message

    def as_dict(self):
        return {"rule": self.rule, "level": self.level, "message": self.message}


# ---------------------------------------------------------------------------
# Minimal YAML subset parser (stdlib-only constraint).
# Handles: scalars, quoted strings, inline lists, dash lists,
# nested maps by 2-space indentation. Sufficient for SKILL.md frontmatter.
# ---------------------------------------------------------------------------

def _parse_scalar(value):
    value = value.strip()
    if value == "":
        return None
    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        return value[1:-1]
    if value.startswith("'") and value.endswith("'") and len(value) >= 2:
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(v) for v in _split_inline_list(inner)]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in ("null", "~"):
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _split_inline_list(inner):
    parts, depth, quote, current = [], 0, None, []
    for ch in inner:
        if quote:
            current.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            current.append(ch)
        elif ch == "[":
            depth += 1
            current.append(ch)
        elif ch == "]":
            depth -= 1
            current.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        parts.append("".join(current))
    return [p.strip() for p in parts if p.strip()]


def parse_yaml_block(lines):
    """Parse an indented YAML-subset block into nested dicts/lists."""
    root = {}
    stack = [(-1, root)]  # (indent, container)
    i = 0
    while i < len(lines):
        raw = lines[i]
        i += 1
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise ValueError("bad indentation at: %r" % raw)
        container = stack[-1][1]

        if stripped.startswith("- "):
            if not isinstance(container, list):
                raise ValueError("list item outside list at: %r" % raw)
            container.append(_parse_scalar(stripped[2:]))
            stack.append((stack[-1][0], container))
            continue

        if ":" not in stripped:
            raise ValueError("expected key: value at: %r" % raw)
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()

        if not isinstance(container, dict):
            raise ValueError("mapping inside list not supported at: %r" % raw)

        if value in (">", ">-", "|", "|-"):
            # Folded (>) or literal (|) block scalar: consume the indented block.
            block = []
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() == "":
                    block.append("")
                    i += 1
                    continue
                nxt_indent = len(nxt) - len(nxt.lstrip(" "))
                if nxt_indent <= indent:
                    break
                block.append(nxt.strip())
                i += 1
            joiner = " " if value.startswith(">") else "\n"
            container[key] = joiner.join(b for b in block).strip()
            continue

        if value == "":
            # Nested map or list follows; peek at next meaningful line.
            j = i
            child = {}
            while j < len(lines):
                nxt = lines[j]
                if nxt.strip() and not nxt.lstrip().startswith("#"):
                    nxt_indent = len(nxt) - len(nxt.lstrip(" "))
                    if nxt_indent > indent and nxt.strip().startswith("- "):
                        child = []
                    break
                j += 1
            container[key] = child
            stack.append((indent, child))
        else:
            container[key] = _parse_scalar(value)
    return root


def split_frontmatter(text):
    """Return (frontmatter_dict_or_None, body, error_or_None)."""
    if not text.startswith("---"):
        return None, text, "no frontmatter block"
    lines = text.split("\n")
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return None, text, "unterminated frontmatter block"
    try:
        fm = parse_yaml_block(lines[1:end])
    except ValueError as exc:
        return None, "\n".join(lines[end + 1:]), "frontmatter parse error: %s" % exc
    return fm, "\n".join(lines[end + 1:]), None


# ---------------------------------------------------------------------------
# Section helpers
# ---------------------------------------------------------------------------

def extract_sections(body):
    """Map of section keyword -> list of body lines, keyed by ## heading prefix."""
    sections = {}
    current = None
    for line in body.split("\n"):
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            current = m.group(1).strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return sections


def find_section(sections, keyword):
    for title, content in sections.items():
        if title.lower().startswith(keyword.lower()):
            return title, content
    return None, None


def count_entries(section_lines):
    return sum(
        1
        for ln in section_lines
        if re.match(r"^\s*([-*+]\s+|\d+\.\s+)", ln)
    )


def estimate_tokens(text):
    return len(text) // 4


# ---------------------------------------------------------------------------
# Rule checks
# ---------------------------------------------------------------------------

FIRST_PERSON_PATTERNS = re.compile(
    r"\bI\s+(always|never|tell|say|believe|think|want|know)\b"
)

OPERATIONAL_HINTS = re.compile(
    r"(\bIF\b.*\bTHEN\b|\bif\b.*\bthen\b|^when\b|->|→|\bnever\b|\balways\b|"
    r"\bbefore\b|\bafter\b|\bunless\b|\brefuse\b|\bstop\b|\bask\b)",
    re.IGNORECASE,
)


def _strip_quoted(text):
    """Remove double-quoted spans and markdown blockquotes so quoted subject
    speech does not trigger L7."""
    text = re.sub(r'"[^"\n]*"', "", text)
    text = re.sub(r"[“”][^“”\n]*[“”]", "", text)
    text = "\n".join(
        ln for ln in text.split("\n") if not ln.lstrip().startswith(">")
    )
    return text


def lint_seat(seat_path, level="standard", installed_ids=None):
    """Lint one seat directory. Returns (findings, meta)."""
    findings = []
    seat_path = seat_path.rstrip("/")
    seat_md = os.path.join(seat_path, "SKILL.md")
    meta = {"id": os.path.basename(seat_path), "display_name": None, "mode": None,
            "domains": []}

    if not os.path.isfile(seat_md):
        findings.append(Finding("L2", "error", "SKILL.md not found in %s" % seat_path))
        return findings, meta

    with open(seat_md, encoding="utf-8") as fh:
        text = fh.read()

    fm, body, fm_err = split_frontmatter(text)
    if fm_err:
        findings.append(Finding("L2", "error", fm_err))
        return findings, meta

    # --- frontmatter shape -------------------------------------------------
    name = fm.get("name")
    if not name or not isinstance(name, str) or not ID_PATTERN.match(name):
        findings.append(Finding(
            "L2", "error",
            "name must match ^[a-z0-9-]{2,32}$ (got %r)" % (name,)))
    else:
        meta["id"] = name
        if os.path.basename(seat_path) != name:
            findings.append(Finding(
                "L2", "error",
                "frontmatter name %r does not match folder %r"
                % (name, os.path.basename(seat_path))))

    if not fm.get("description"):
        findings.append(Finding("L2", "error", "description is required"))

    x = fm.get("x-chiron") or {}
    if not isinstance(x, dict) or not x:
        findings.append(Finding("L2", "error", "x-chiron extension block is required"))
        x = {}

    display_name = x.get("display_name")
    if not display_name:
        findings.append(Finding("L2", "error", "x-chiron.display_name is required"))
    meta["display_name"] = display_name

    mode = x.get("mode")
    if mode not in MODES:
        findings.append(Finding(
            "L2", "error", "x-chiron.mode must be one of %s (got %r)" % (MODES, mode)))
    meta["mode"] = mode

    domains = x.get("domains")
    if not isinstance(domains, list) or not (1 <= len(domains) <= 6):
        findings.append(Finding(
            "L2", "error", "x-chiron.domains must be a list of 1..6 tags"))
    else:
        meta["domains"] = domains

    # --- provenance / L1 / L4 / L10 ----------------------------------------
    prov = x.get("provenance") or {}
    if mode in ("corpus", "persona"):
        if not isinstance(prov, dict) or not prov:
            findings.append(Finding(
                "L2", "error", "provenance is required when mode != original"))
            prov = {}
        subject = prov.get("subject")
        living = prov.get("living")
        license_ = prov.get("license", "none")
        sources = prov.get("sources") or []

        if not subject:
            findings.append(Finding("L2", "error", "provenance.subject is required"))
        if not isinstance(living, bool):
            findings.append(Finding(
                "L2", "error", "provenance.living must be true or false"))
        if license_ not in LICENSES:
            findings.append(Finding(
                "L2", "error",
                "provenance.license must be one of %s" % (LICENSES,)))

        if mode == "persona" and living is True and license_ != "granted":
            findings.append(Finding(
                "L1", "error",
                "persona mode for a living subject without a granted license "
                "is forbidden (LEGAL.md). Use corpus mode or an archetype alias."))

        if not isinstance(sources, list) or len(sources) < 3:
            findings.append(Finding(
                "L4", "error",
                "provenance.sources needs at least 3 citations (got %d)"
                % (len(sources) if isinstance(sources, list) else 0)))
        elif len(sources) > 50:
            findings.append(Finding(
                "L2", "error", "provenance.sources exceeds 50 entries"))

        if subject and display_name:
            subj_in_name = subject.split()[-1].lower() in display_name.lower()
            has_suffix = re.search(
                r"(lens|corpus|\(corpus\)|study aid)", display_name, re.IGNORECASE)
            if subj_in_name and not has_suffix:
                findings.append(Finding(
                    "L10", "warn",
                    "display_name contains the subject's name without a mode "
                    "suffix; prefer e.g. '%s Lens' or '%s (corpus)'"
                    % (display_name, display_name)))

    # --- required sections / L5 ---------------------------------------------
    sections = extract_sections(body)
    for keyword, minimum in REQUIRED_SECTIONS.items():
        title, content = find_section(sections, keyword)
        if title is None:
            findings.append(Finding(
                "L5", "error", "required section '## %s' is missing" % keyword))
        elif minimum and count_entries(content) < minimum:
            findings.append(Finding(
                "L5", "error",
                "section '## %s' has %d entries; minimum is %d"
                % (title, count_entries(content), minimum)))

    # --- L6 token budget -----------------------------------------------------
    if estimate_tokens(text) > 6000:
        findings.append(Finding(
            "L6", "warn",
            "core SKILL.md is ~%d tokens (> 6k); move depth into references/"
            % estimate_tokens(text)))

    # --- L7 persona leakage --------------------------------------------------
    if mode == "corpus":
        stripped = _strip_quoted(body)
        leaks = FIRST_PERSON_PATTERNS.findall(stripped)
        if leaks:
            findings.append(Finding(
                "L7",
                "error" if level == "strict" else "warn",
                "first-person subject voice detected in corpus seat "
                "(%d occurrence(s), e.g. 'I %s')" % (len(leaks), leaks[0])))

    # --- L8 heuristics operational form --------------------------------------
    _, heur = find_section(sections, "Heuristics")
    if heur:
        for ln in heur:
            if re.match(r"^\s*([-*+]\s+|\d+\.\s+)", ln):
                entry = re.sub(r"^\s*([-*+]\s+|\d+\.\s+)", "", ln)
                if not OPERATIONAL_HINTS.search(entry):
                    findings.append(Finding(
                        "L8", "warn",
                        "heuristic may not be operational (no IF/THEN shape): %r"
                        % entry[:80]))

    # --- L9 disagreements ----------------------------------------------------
    dis_path = os.path.join(seat_path, "disagreements.md")
    if os.path.isfile(dis_path) and installed_ids is not None:
        with open(dis_path, encoding="utf-8") as fh:
            dis_text = fh.read()
        for m in re.finditer(r"^counterpart:\s*(.+)$", dis_text, re.MULTILINE):
            counterpart = m.group(1).strip()
            if counterpart.startswith("external:"):
                continue
            if counterpart not in installed_ids:
                findings.append(Finding(
                    "L9", "warn",
                    "disagreement counterpart %r is not an installed seat and "
                    "not marked 'external:'" % counterpart))

    # --- L12 standard reference set -------------------------------------------
    refs_dir = os.path.join(seat_path, "references")
    missing = [
        f for f in STANDARD_REFERENCES
        if not os.path.isfile(os.path.join(refs_dir, f))
    ]
    if missing:
        findings.append(Finding(
            "L12",
            "error" if level == "strict" else "warn",
            "references/ is missing standard files: %s" % ", ".join(missing)))

    # --- L11 evals (strict only) ----------------------------------------------
    if level == "strict":
        evals = os.path.join(seat_path, "evals.md")
        if not os.path.isfile(evals):
            findings.append(Finding(
                "L11", "error", "strict level requires an evals.md file"))

    return findings, meta


def lint_status(findings):
    if any(f.level == "error" for f in findings):
        return "fail"
    if findings:
        return "warn"
    return "pass"


# Skills that can share a skills root with seats but are NOT advisor seats
# (the conversational router). lint --all excludes these; everything else with a
# SKILL.md is a candidate seat, so a malformed one is failed, not hidden.
NON_SEAT_SKILLS = frozenset({"chiron"})


def _has_x_chiron(path):
    """True if path/SKILL.md carries an `x-chiron` frontmatter block. The registry
    uses this to pick seats out of a shared skills root (~/.claude/skills, or a
    plugin's flat skills/ dir) full of unrelated skills and the router."""
    skill_md = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill_md):
        return False
    try:
        with open(skill_md, encoding="utf-8") as fh:
            fm, _body, _err = split_frontmatter(fh.read())
    except OSError:
        return False
    return bool(fm and fm.get("x-chiron"))


def discover_seats(seats_dir, for_lint=False):
    """List seat directories under seats_dir.

    Default (registry / runtime): return only dirs whose SKILL.md carries an
    x-chiron block, so scanning a shared skills root picks out seats and ignores
    unrelated skills and the router.

    for_lint=True (lint --all / CI): return every non-hidden dir that contains a
    SKILL.md, except known non-seat skills (NON_SEAT_SKILLS). Deliberately
    permissive so lint SEES a seat whose x-chiron is missing or malformed and
    FAILS it, instead of silently hiding a broken bundled seat from validation.
    """
    if not os.path.isdir(seats_dir):
        return None
    out = []
    for entry in sorted(os.listdir(seats_dir)):
        path = os.path.join(seats_dir, entry)
        if not (os.path.isdir(path) and not entry.startswith(".")):
            continue
        if not os.path.isfile(os.path.join(path, "SKILL.md")):
            continue
        if for_lint:
            if entry not in NON_SEAT_SKILLS:
                out.append(path)
        elif _has_x_chiron(path):
            out.append(path)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description="Lint Chiron seats")
    parser.add_argument("paths", nargs="*", help="seat directories to lint")
    parser.add_argument("--all", action="store_true", help="lint every seat in --seats-dir")
    parser.add_argument("--seats-dir", default="skills")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--level", choices=("standard", "strict"), default="standard")
    parser.add_argument("--explain", action="store_true", help="show rule descriptions")
    args = parser.parse_args(argv)

    if args.all:
        paths = discover_seats(args.seats_dir, for_lint=True)
        if paths is None:
            msg = {"error": "no seats directory found; run /chiron:distill or install a pack"}
            print(json.dumps(msg) if args.format == "json" else msg["error"])
            return 2
    else:
        paths = args.paths
    if not paths:
        parser.error("provide seat paths or --all")

    installed_ids = {os.path.basename(p.rstrip("/")) for p in
                     (discover_seats(args.seats_dir, for_lint=True) or [])}

    reports = []
    worst = 0
    for path in paths:
        findings, meta = lint_seat(path, level=args.level,
                                   installed_ids=installed_ids)
        # L3: id collision across seats (same id claimed by two folders)
        status = lint_status(findings)
        if status == "fail":
            worst = max(worst, 2)
        elif status == "warn":
            worst = max(worst, 1)
        reports.append({
            "id": meta["id"],
            "path": path,
            "lint": status,
            "findings": [f.as_dict() for f in findings],
        })

    # L3 across the linted set
    seen = {}
    for rep in reports:
        if rep["id"] in seen:
            rep["findings"].append(
                Finding("L3", "error",
                        "id %r collides with %s" % (rep["id"], seen[rep["id"]])).as_dict())
            rep["lint"] = "fail"
            worst = 2
        else:
            seen[rep["id"]] = rep["path"]

    if args.format == "json":
        print(json.dumps(reports, indent=2))
    else:
        for rep in reports:
            print("%s [%s] %s" % (rep["lint"].upper().ljust(5), rep["id"], rep["path"]))
            for f in rep["findings"]:
                print("  %s %-4s %s" % ("✗" if f["level"] == "error" else "!",
                                        f["rule"], f["message"]))
                if args.explain:
                    print("        rule: %s" % RULES.get(f["rule"], "?"))
        counts = {"pass": 0, "warn": 0, "fail": 0}
        for rep in reports:
            counts[rep["lint"]] += 1
        print("\n%d seat(s): %d pass, %d warn, %d fail"
              % (len(reports), counts["pass"], counts["warn"], counts["fail"]))

    return worst


if __name__ == "__main__":
    sys.exit(main())
