---
name: chiron
description: Route advisor requests to Chiron seats, and auto-orchestrate decisions to the right expert(s). Use when the user asks what a named advisor/seat would say ("what would munger say", "ask naval about this"), describes a decision without naming anyone ("should I take this deal", "help me think through this", "I'm stuck on pricing"), wants to run a question by a bench or council ("run this by my product bench", "convene the council"), wants to see available advisors ("who can I ask"), or wants to add a seat ("distill a seat for X", "add an advisor"), wants to get set up ("onboard me", "get me started"), or wants to distill themselves into a seat ("distill me", "build my seat", "put me on the council"). Covers consult (auto-routing), ask, council, bench, roster, distill, distill-me, onboard, lint, and log without slash syntax.
---

# Chiron router

The user invoked Chiron conversationally. Map their intent to the matching command file under `${CLAUDE_PLUGIN_ROOT}/commands/` and follow it exactly. The command files are the source of truth for each flow's contract.

**Default to orchestration.** When the user describes a decision or a situation but does NOT name a specific seat or bench, do not guess or grab the whole roster. Follow `commands/consult.md`: it decides whether to skip, ask one seat, or convene a council, and picks the right experts. That routing decision is the point of the product.

| Intent sounds like | Follow |
|---|---|
| a decision/situation with no seat named ("should I...", "I'm torn on...", "help me decide...") | `commands/consult.md` (auto-route) |
| "get started", "set me up", "onboard me" (first run) | `commands/onboard.md` |
| "distill me", "build my seat", "put me on the council" | `commands/distill-me.md` |
| "ask <seat> ...", "what would <seat> say about ..." | `commands/ask.md` |
| "run this by <bench>", "convene ...", "council on ...", "what does my <bench> bench think" | `commands/council.md` |
| "create/show/edit a bench", "my line-up for X" | `commands/bench.md` |
| "who can I ask", "show the roster", "which seats do I have" | `commands/roster.md` |
| "distill/add a seat for X", "I want a <person> advisor" | `commands/distill.md` |
| "check/validate my seats", "lint" | `commands/lint.md` |
| "what did <seat> tell me", "open loops", "past consults" | `commands/log.md` |

Resolution notes:
- Seat and bench names arrive fuzzy ("munger", "the Munger seat", "my pricing people"). Resolve against `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/registry.py --json --seats-dir ${CLAUDE_PLUGIN_ROOT}/seats --seats-dir ~/.claude/chiron/seats --seats-dir .chiron/seats` and the bench YAMLs (project `.chiron/benches.yaml`, global `~/.claude/chiron/benches.yaml`). Seat wins ties; ask once if genuinely ambiguous.
- Explicit beats inferred: if the user names a seat, honor it (ask); if they say "they/the bench/the council" or name a bench, go to council. Only auto-route (consult) when they leave the choice open.
- When the user is mid-decision but has not asked Chiron for anything, offer to route rather than hijacking the turn.
- Never invent a seat that isn't installed. Offer `/chiron:distill` instead.
