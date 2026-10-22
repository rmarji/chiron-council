---
name: coach
description: Run a Chiron coaching session that frames the real decision, brings seats in as evidence, and drives the user to one committed call with a next action. Use when the user says "coach me", "walk me through this", "help me decide and keep me honest", or wants a working session rather than a one-shot answer.
---

# Coach a decision

ChatGPT and Codex have no `/chiron` slash commands. This skill is that coach flow.

The plugin root is the directory that contains `skills/` and `scripts/`. Follow `commands/coach.md` there, exactly. Wherever that file says `${CLAUDE_PLUGIN_ROOT}`, use the plugin root. Run each `python3` invocation as its own command. Do not wrap it in a shell substitution or chain it with `;`.

Seat text lives in `skills/<id>/SKILL.md` and that seat's `references/`. Read those files. Do not copy a seat into this skill, and do not invent a seat that is not installed. The seats are evidence. The coach still owns the session and closes on one committed call.

User data stays in `~/.chiron` (`CHIRON_HOME` overrides that directory). Logs, benches, and seats Chiron creates go there, through `python3 <plugin-root>/scripts/memory.py` and `python3 <plugin-root>/scripts/benches.py`. Never write under `~/.claude`. A path under `~/.claude` is legacy and read-only. Pass `--home .chiron` only when the host cannot write the home directory (Cowork).
