---
name: chiron
description: Route natural-language advisor requests to Chiron seats and benches. Use when the user asks what a named advisor/seat would say ("what would munger say", "ask naval about this"), wants to run a question by a bench or council ("run this by my product bench", "convene the council", "what does my money bench think"), wants to see available advisors ("who can I ask", "show my roster/benches"), or wants to add a new advisor seat ("hire a seat for X"). Covers ask, council, bench, roster, hire, lint, and log flows without slash syntax.
---

# Chiron router

The user invoked Chiron conversationally. Map their intent to the matching command file under `${CLAUDE_PLUGIN_ROOT}/commands/` and follow it exactly — the command files are the source of truth for each flow's contract.

| Intent sounds like | Follow |
|---|---|
| "ask <seat> ...", "what would <seat> say about ..." | `commands/ask.md` |
| "run this by <bench>", "convene ...", "council on ...", "what does my <bench> bench think" | `commands/council.md` |
| "create/show/edit a bench", "my line-up for X" | `commands/bench.md` |
| "who can I ask", "show the roster", "which seats do I have" | `commands/roster.md` |
| "hire/add a seat for X", "I want a <person> advisor" | `commands/hire.md` |
| "check/validate my seats", "lint" | `commands/lint.md` |
| "what did <seat> tell me", "open loops", "past consults" | `commands/log.md` |

Resolution notes:
- Seat and bench names arrive fuzzy ("munger", "the Munger seat", "my pricing people"). Resolve against `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/registry.py --json --seats-dir ${CLAUDE_PLUGIN_ROOT}/seats` and the bench YAMLs (project `.chiron/benches.yaml`, global `~/.claude/chiron/benches.yaml`). Seat wins ties; ask once if genuinely ambiguous.
- A question aimed at one mind → ask. A decision needing multiple lenses or where the user says "they/the bench/the council" → council.
- Never invent a seat that isn't installed — offer `/chiron:hire` instead.
