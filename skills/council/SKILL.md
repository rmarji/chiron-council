---
name: council
description: Convene a Chiron bench. Seats answer independently, only disagreements that are on the record are surfaced, and one recommendation keeps the dissent. Use when the user says "council", "run this by my bench", "convene", or names a bench such as money, strategy, deals, relationship, shipping, or work-design.
---

# Convene a council

ChatGPT and Codex have no `/chiron` slash commands. This skill is that council flow.

The plugin root is the directory that contains `skills/` and `scripts/`. Follow `commands/council.md` there, exactly, including the isolation rule and the sequential fallback when subagents are unavailable. Wherever that file says `${CLAUDE_PLUGIN_ROOT}`, use the plugin root. Run each `python3` invocation as its own command. Do not wrap it in a shell substitution or chain it with `;`.

Seat text lives in `skills/<id>/SKILL.md` and that seat's `references/` and `disagreements.md`. Read those files. Do not copy a seat into this skill, and do not invent a seat that is not installed. With no benches file of the user's own, `python3 <plugin-root>/scripts/benches.py` resolves the bundled examples (`money`, `strategy`, `deals`, `relationship`, `shipping`, `work-design`).

User data stays in `~/.chiron` (`CHIRON_HOME` overrides that directory). Logs, benches, and seats Chiron creates go there, through `python3 <plugin-root>/scripts/memory.py` and `python3 <plugin-root>/scripts/benches.py`. Never write under `~/.claude`. A path under `~/.claude` is legacy and read-only. Pass `--home .chiron` only when the host cannot write the home directory (Cowork).
