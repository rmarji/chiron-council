---
description: Ask a council of advisors. Each answers separately, you see where they really disagree, and you get one recommendation
argument-hint: <bench-or-seat-list> <question> [--depth quick|full]
---

# /chiron:council — the council state machine

The user asked: `$ARGUMENTS`

First token = bench name (resolve with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/benches.py --json <name>`: project `.chiron/benches.yaml` shadows global `~/.chiron/benches.yaml`, which shadows the older `~/.claude/chiron/benches.yaml` when that file is still there — note a shadow once; with no user benches file it falls back to the bundled examples, so say "using the bundled example bench") or an inline comma-separated seat list. Rest = the question. `--depth` overrides the bench's `default_depth` (default: quick).

**How to talk to the user:** follow `${CLAUDE_PLUGIN_ROOT}/skills/chiron/VOICE.md` for everything the user reads: the opening, labels, closing, and the memory offer. Internal terms in this file (seat, bench, depth, chairman, open loop) are for you, not for them.

**Why this exists:** generated councils produce consensus theater — five flavors of one model agreeing. This state machine manufactures *structural* independence and surfaces only *authored* conflict. Do not shortcut it.

## CONVENE

1. Resolve the bench. Load the roster via `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/registry.py --json --seats-dir ${CLAUDE_PLUGIN_ROOT}/skills --seats-dir ~/.claude/skills --seats-dir ~/.claude/chiron/seats --seats-dir ~/.chiron/seats --seats-dir .claude/skills --seats-dir .chiron/seats`. The `~/.claude/` directories are read only. If `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py seats` prints a directory other than `~/.chiron/seats`, pass that directory in place of `~/.chiron/seats`. Run it as its own `python3` command. Run every `python3` call as its own command: no `;`, `&&`, pipes, loops or `$(...)` around it, and save log entries with the file-editing tool rather than a shell heredoc. Hosts approve plain `python3` calls; anything else triggers an extra permission prompt.
2. Guards:
   - **CH-E2:** bench references a missing seat → name it, offer to run with the remainder, abort if declined.
   - **CH-E4:** more than 8 seats → refuse; explain the token/quality cost; suggest splitting into two benches.
   - Any seat with `lint: fail` → drop it with a note (same rule as ask CH-E3).
   - Fewer than 2 seats resolved → tell the user to use `/chiron:ask` instead.
3. **Clarify first, then announce.** If the question is too thin to answer well, ask ONE clarifying question now and wait for the answer. Never ask one after the takes have started. Then tell the user in one plain line who you're asking and how long it takes, e.g. "I'll ask Munger, Naval and Hormozi separately. It takes a minute or two, and you'll see me open their notes first." Show the technical run header (seats, chairman, depth, token estimate: quick ≈ seats × 1.5k, full ≈ seats × 4k) only if the user asks for it or passed `--depth`.

## TAKES (phase 1 — isolation is the whole point)

Spawn **one subagent per seat, in parallel** (Task tool). Each subagent's context contains ONLY:
- that seat's `SKILL.md`
- that seat's last 10 consult-log entries, from `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py log <id> --read` (add `--home .chiron` in Cowork). Not from the seat directory, and not from anywhere under `${CLAUDE_PLUGIN_ROOT}`. The file may not exist yet.
- the question

It must NOT see: other seats, other takes, the bench composition, or this conversation. Disagreement must be structural, not simulated.

Each subagent returns: **position** (3-6 lines, in the seat's voice contract), **confidence** (1-5), **applied_heuristics** (which of its heuristics fired), **sources** (citations for corpus seats).

**CH-E5:** if subagents are unavailable in this harness, degrade to sequential prompts — but build each seat's prompt fresh from its files only, and DISCLOSE the degradation in the output ("takes gathered sequentially; isolation is by prompt construction, not process").

In quick depth, after takes are gathered, skip to a micro-synthesis (recommendation + one line of preserved dissent + confidence) and then RECORD.

## CONFLICT (phase 2 — authored only)

1. Read `disagreements.md` of every participating seat.
2. Surface entries where **both** counterpart seats are present AND the topic keyword-matches the question (or the chairman judges it clearly relevant).
3. Quote each surfaced disagreement **with its citations**, then note how each seat's take just now lines up with its authored position.
4. **CH-E6:** if nothing matches, state plainly: "No authored conflicts on record for this topic." **NEVER generate, infer, or dramatize a disagreement that is not in the files.** Generated conflict is the competitor failure mode this product exists to kill.

## SYNTHESIS (phase 3)

Written in the chairman's voice (if the bench names a chairman seat, load its Voice contract; otherwise neutral analyst), inside the answer shape in `skills/chiron/VOICE.md`. The content contract is unchanged; the labels the user sees are plain:

| Contract field | User-facing label |
|---|---|
| Opening (new) | one line: who looked at it, each with a 2-4 word description ("Terry Real (couples therapist)") |
| Takes | **What they'd tell you**: 1-3 sentences per advisor, with the source |
| Authored disagreements surfaced | **Where they disagree**: quote with citations and add "Both positions are from their books, not invented." If none: "They don't have a recorded disagreement on this." |
| Recommendation | **What to do**: one pick, phrased as an action the user can take soon |
| Dissent preserved | inside **Where they disagree** or one line under **What to do**: who would push back, and why. Named, not averaged away |
| What you lose | **The catch:** one line |
| Confidence 1-5 | **How sure:** N out of 5 |
| What would change it | one line after "How sure" |

Keep it under about 250 words by default and offer "Want the full reasoning from each advisor?" A user who asks for the technical format (`--depth full`, or "show me the raw council") gets the original field names.

## RECORD (phase 4)

1. Append one entry to EACH participating seat's consult log (schema below; create the file if missing; never rewrite prior entries). The path to write is whatever `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py log <id> --ensure` prints: `~/.chiron/logs/<id>/log.md` by default, `$CHIRON_HOME/logs/<id>/log.md` when that variable is set, and `.chiron/logs/<id>/log.md` in Cowork (pass `--home .chiron`). `--ensure` copies a log that still lives at `~/.claude/chiron/logs/<id>/log.md` into the new path once. Append only to the printed path. Never write under `~/.claude` or `${CLAUDE_PLUGIN_ROOT}`.

```markdown
## {today ISO date} · council:{bench-name}
**Q:** {one-line question}
**Take:** {that seat's 2-4 line position}
**Decision:** open loop
```

2. End with one plain, optional offer: "Want me to remember what you decide, so these advisors can follow up next time?" If they answer with a decision, update `open loop` in every entry just written. If they decline or ignore it, leave the entries as open loops and don't ask again this session.
3. If the log could not be written to `~/.chiron` (for example a sandbox blocked it) and you used `--home .chiron`, say so in one line: "I saved these notes in this project's `.chiron` folder because I couldn't write to your home folder." Do not mention log paths otherwise.
4. Never mention vaults, notes folders, `me.md`, or a `me` advisor unless the user has set one up (a `me` seat is installed). Missing optional context is silent.
