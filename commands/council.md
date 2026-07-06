---
description: Convene a bench — independent authored takes, real disagreements, one synthesis with dissent preserved
argument-hint: <bench-or-seat-list> <question> [--depth quick|full]
---

# /chiron:council — the council state machine

The user asked: `$ARGUMENTS`

First token = bench name (resolve project `.chiron/benches.yaml`, then `~/.claude/chiron/benches.yaml`; project shadows global — note it once) or an inline comma-separated seat list. Rest = the question. `--depth` overrides the bench's `default_depth` (default: quick).

**Why this exists:** generated councils produce consensus theater — five flavors of one model agreeing. This state machine manufactures *structural* independence and surfaces only *authored* conflict. Do not shortcut it.

## CONVENE

1. Resolve the bench. Load the roster via `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/registry.py --json --seats-dir ${CLAUDE_PLUGIN_ROOT}/seats --seats-dir ~/.claude/chiron/seats --seats-dir .chiron/seats`.
2. Guards:
   - **CH-E2:** bench references a missing seat → name it, offer to run with the remainder, abort if declined.
   - **CH-E4:** more than 8 seats → refuse; explain the token/quality cost; suggest splitting into two benches.
   - Any seat with `lint: fail` → drop it with a note (same rule as ask CH-E3).
   - Fewer than 2 seats resolved → tell the user to use `/chiron:ask` instead.
3. Print the run header: seats, chairman (bench's `chairman:` seat or "neutral"), depth, and a token estimate (quick ≈ seats × 1.5k, full ≈ seats × 4k).

## TAKES (phase 1 — isolation is the whole point)

Spawn **one subagent per seat, in parallel** (Task tool). Each subagent's context contains ONLY:
- that seat's `SEAT.md`
- that seat's last 10 `log.md` entries
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

Written in the chairman's voice (if the bench names a chairman seat, load its Voice contract; otherwise neutral analyst). Output exactly:

- **Recommendation:** one pick, not a menu.
- **Dissent preserved:** which seats disagree and why — named, not averaged away.
- **What you lose:** 1-2 lines on the cost of the recommended path.
- **Confidence:** 1-5.
- **What would change it:** one line.
- Cite which authored disagreements were surfaced (or that none were on record).

## RECORD (phase 4)

1. Append one entry to EACH participating seat's `log.md` (schema below; create file if missing; never rewrite prior entries):

```markdown
## {today ISO date} · council:{bench-name}
**Q:** {one-line question}
**Take:** {that seat's 2-4 line position}
**Decision:** open loop
```

2. Ask the user once: "Record your decision?" If answered, update `open loop` in every entry just written. Otherwise leave as open loops.
