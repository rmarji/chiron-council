---
description: Create, list, or edit benches — curated seat line-ups
argument-hint: create <name> <seat> <seat> ... [--global] | list | remove <name>
---

# /chiron:bench — manage benches

The user asked: `$ARGUMENTS`

Benches are plain YAML the user can also edit by hand — files are the API. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/benches.py --paths` and use the paths it prints. Write targets:
- **Project:** the `project` path (`.chiron/benches.yaml`). Default write target when inside a project.
- **Global:** the `global` path (`~/.chiron/benches.yaml`, or `$CHIRON_HOME/benches.yaml` when that variable is set). Write here with `--global`, or when not in a project.
- **Legacy (read only):** the `legacy` path (`~/.claude/chiron/benches.yaml`). Never write it. Claude Code refuses writes under `~/.claude`. If that file exists and the global file does not, copy its entries into the new global file before adding the bench.
- On name collision, **project shadows global, which shadows legacy** — mention it once per session when it applies.
- **Bundled examples:** when no user file exists (project, global, or legacy), every command reads the `examples` path instead, so `money`, `strategy`, `deals`, `relationship`, `shipping`, and `work-design` work on a fresh install. They drop out as soon as the user has a benches file of their own.

Resolve what is in effect with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/benches.py --json` (add a name to look up one bench).

File shape:

```yaml
benches:
  product:
    seats: [munger, naval, hormozi]
    chairman: neutral        # a seat id, or "neutral"
    default_depth: quick     # quick | full
```

## create <name> <seats...>

1. Validate the name: `^[a-z0-9-]{2,32}$`.
2. Validate every seat id against `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/registry.py --json --seats-dir ${CLAUDE_PLUGIN_ROOT}/skills --seats-dir ~/.claude/skills --seats-dir ~/.claude/chiron/seats --seats-dir ~/.chiron/seats --seats-dir .claude/skills --seats-dir .chiron/seats`. The `~/.claude/` directories are read only. If `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py seats` prints a directory other than `~/.chiron/seats`, pass that directory in place of `~/.chiron/seats`. Unknown id → suggest the top fuzzy matches, don't write.
3. 2-8 seats required. 1 seat → "use /chiron:ask, a bench of one is a person." More than 8 → refuse (CH-E4). **6+ → warn** about token cost and decision theater but proceed.
4. **Stop and ask before writing anything.** If the user has no benches file yet (the resolver reports `source: example`), say that writing one retires the bundled examples, offer to copy the examples into the new file first so they keep working, and wait for the answer. Do not do step 5 until they reply. If a legacy file exists and you are creating the global file, copy the legacy entries in first (see above) instead of the examples.
5. Read the target YAML (create file + `benches:` root if missing), add the bench with `chairman: neutral` and `default_depth: quick` defaults (honor `--chairman` / `--depth` flags if given), write it back preserving existing entries and comments.
6. **CH-E7:** if the same name exists in the other scope, create anyway and warn which one now shadows which.
7. Confirm with the resulting YAML block and the file it was written to.

## list

Run the resolver. Render a table: name, seats, chairman, depth, source (project|global|legacy|example), and mark shadowed globals. If every row is `example`, say these are the bundled examples and that `/chiron:bench create` starts the user's own file. If a row is `legacy`, say it is still being read from `~/.claude/chiron/benches.yaml` and the next global write copies it to `~/.chiron/benches.yaml` without writing the old path. If a listed bench references a seat that is no longer installed, flag it inline.

## remove <name>

Remove the entry from the scope where it's defined (ask which, if it exists in both). Show the diff. Never touch seat folders — bench deletion never cascades to seats.
