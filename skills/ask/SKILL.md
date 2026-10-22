---
name: ask
description: Ask one Chiron seat a question and get one cited take, with that seat's memory of past calls. Use when the user names an advisor (Munger, Naval, Ferriss, Voss, and the rest of the roster) or says "what would X say", "ask the Munger seat", or wants a single lens rather than a council.
---

# Ask one seat

ChatGPT and Codex have no `/chiron` slash commands. This skill is that ask flow.

The plugin root is the directory that contains `skills/` and `scripts/`. Follow `commands/ask.md` there, exactly. Wherever that file says `${CLAUDE_PLUGIN_ROOT}`, use the plugin root. Run each `python3` invocation as its own command. Do not wrap it in a shell substitution or chain it with `;`.

Seat text lives in `skills/<id>/SKILL.md` and that seat's `references/`. Read those files. Do not copy a seat into this skill, and do not invent a seat that is not installed.

User data stays in `~/.chiron` (`CHIRON_HOME` overrides that directory). Logs, benches, and seats Chiron creates go there, through `python3 <plugin-root>/scripts/memory.py` and `python3 <plugin-root>/scripts/benches.py`. Never write under `~/.claude`. A path under `~/.claude` is legacy and read-only. Pass `--home .chiron` only when the host cannot write the home directory (Cowork).
