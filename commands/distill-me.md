---
description: Distill YOU into a private seat — your frameworks, mission, values, goals, and go-to experts, from your own history
argument-hint: [optional: point at notes/a vault/a folder to read]
---

# /chiron:distill-me — put yourself on the council

This distills *you* the way `/chiron:distill` distills a thinker: a deep, structured breakdown of how you actually operate, written as an **original-mode seat** so your own operating system can sit in the room, chair your councils, and be argued with. It also reads out your **go-to experts** and turns them into a recommended roster.

Read `${CLAUDE_PLUGIN_ROOT}/SEAT_SPEC.md` first. Model the output on an original-mode seat: `${CLAUDE_PLUGIN_ROOT}/skills/rayo/SKILL.md`.

## Privacy first (state this, then honor it)

The `me` seat holds your mission, values, goals, and decisions. It is **private and local**. Tell the user up front:

- It writes to the directory `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py seats` prints, plus `/me/` (`~/.chiron/seats/me/` unless `CHIRON_HOME` is set), or `<project>/.chiron/seats/me/` if the user wants it in one repo. **Never** write `~/.claude/chiron/seats/me/`, never write into the Chiron plugin repo, never committed, never shipped. Claude Code refuses writes under `~/.claude`. In Cowork (no home-directory write), use the project path `<project>/.chiron/seats/me/`, which the registry scans. If a `me` seat already exists at `~/.claude/chiron/seats/me/`, read it and carry it forward into the new directory; do not write the old path.
- If written into a project, add `.chiron/seats/` to that project's `.gitignore` (offer to do it).
- You will read personal sources only with consent, name each source before reading it, and never transmit any of it anywhere.

## 1. Gather (consent-gated)

Ask which of these to draw on; read only what they approve. Name each source out loud before reading. Run the interview as a conversation, not an interrogation: offer concrete suggestions and options ("a lot of people channel someone like Munger for money calls — who's yours?") rather than a wall of open questions, so the user is never overwhelmed.

- **This conversation and recent Claude Code history** — the frameworks, phrases, and decisions the user actually reaches for.
- **Instruction + memory files** — `~/.claude/CLAUDE.md`, project `CLAUDE.md`/`AGENTS.md`, and any `~/.claude/.../memory/` files. These already encode operating rules.
- **Anything the user points at** via `$ARGUMENTS` or in the interview — a notes vault (e.g. an Obsidian folder), a "how I work" doc, a resume, past writing. Read it as corpus.
- **Interview** to fill the gaps (always do this part): mission and current focus; values and non-negotiables; goals (this quarter, this year); the decision frameworks and mental models they use by name; their anti-patterns and known traps; who they channel when stuck (their go-to experts, by domain); and how they want to be spoken to.

## 2. Extract (the breakdown)

Synthesize, in the user's own terms, cited to the source where possible:

- **Mission / what they're optimizing for** and current active priorities.
- **Values and non-negotiables** — the lines they won't cross.
- **Goals** — concrete, time-bound where known (convert "next month" to an absolute date).
- **Frameworks & mental models** they operate by, named, with when-each-applies.
- **Operating principles and heuristics** in IF/THEN form.
- **Anti-patterns / traps** — how they characteristically fail, and the counter.
- **Voice** — how they think and want to be addressed.
- **Go-to experts** — the thinkers they channel, tagged by domain.

## 3. Author the `me` seat

Write `<seats-dir>/me/` from `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py seats` (or the project path), full SEAT_SPEC structure. Do not write under `~/.claude`:

- `SKILL.md`: frontmatter `name: me`, a description, `x-chiron: { display_name: "<their name> (you)", mode: original, domains: [<their domains>] }` (original mode needs no provenance and no M4 disclaimer — it is self-authored). Body: narrative sections plus the required `## Priors` (≥5), `## Heuristics` (≥5, IF/THEN), `## Refusals` (≥2 — the things they refuse to do or decide, e.g. their own guardrails), `## Voice`. Keep under ~6k tokens.
- `references/`: the 7 standard files, holding the depth (their full framework catalog, mission/values/goals, anti-patterns, the source pointers). Everything from step 2 lives here so `SKILL.md` stays lean.
- Lint it: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lint_seat.py <the me directory you just wrote>`. Fix until pass.

## 4. Read out the go-to experts → recommend a roster

Map the user's named go-to experts against the installed roster (`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/registry.py --json --seats-dir ${CLAUDE_PLUGIN_ROOT}/skills --seats-dir ~/.claude/skills --seats-dir ~/.claude/chiron/seats --seats-dir ~/.chiron/seats --seats-dir .claude/skills --seats-dir .chiron/seats`). If `memory.py seats` printed a directory other than `~/.chiron/seats`, pass that directory in its place:

- **Already installed** → note them.
- **Not yet installed but available/known** → offer to `/chiron:distill` each.
- Propose **starter benches** built from their experts by domain, and suggest the `me` seat as chairman for personal-decision benches (your operating system arbitrates the council).

## 5. Report

Show the seat card (id `me`, display_name, domains, section counts, lint result), where it was written, the privacy note, the matched/ recommended experts, and the proposed benches. Close by pointing to `/chiron:consult "<a real decision>"` so they can immediately put the new bench to work.
