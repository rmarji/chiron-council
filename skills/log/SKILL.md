---
name: log
description: Read a Chiron seat's consult log and surface decisions that were never closed. Use when the user asks what a seat told them before, wants open loops, or wants a past decision recorded.
---

# Read a seat's log

ChatGPT and Codex have no `/chiron` slash commands. This skill is that log flow.

The plugin root is the directory that contains `skills/` and `scripts/`. Follow `commands/log.md` there, exactly. Wherever that file says `${CLAUDE_PLUGIN_ROOT}`, use the plugin root. Run each `python3` invocation as its own command. Do not wrap it in a shell substitution or chain it with `;`.

Resolve the file with `python3 <plugin-root>/scripts/memory.py log <id> --read`. That is `~/.chiron/logs/<id>/log.md` unless `CHIRON_HOME` is set. If the printed path does not exist, say "No log file is at that path yet." Do not claim the user never consulted the seat. If `--read` prints a path under `~/.claude`, read it and do not write it. Never write under `~/.claude`. A path under `~/.claude` is legacy and read-only.

Do not read or write a `log.md` inside a seat directory or inside the plugin root. The plugin cache is replaced on update. Seat text stays in `skills/<id>/SKILL.md`; do not copy it here.
