---
description: Auto-route a decision — Chiron picks the right seat(s) and decides whether a council is even worth it
argument-hint: <your question or situation>
---

# /chiron:consult — the orchestrator

The user asked: `$ARGUMENTS`

They did not name a seat. Your job is to **pick the right expert(s) every time**, and to decide whether this even warrants a council. A council that convenes when it should not is decision theater and a token tax. The most valuable routing decision is often "you do not need the council for this."

This is the flagship of Chiron. Do the routing openly, then execute.

## Step 1 — Load the roster

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/registry.py --json --seats-dir ${CLAUDE_PLUGIN_ROOT}/skills --seats-dir ~/.claude/skills --seats-dir ~/.claude/chiron/seats --seats-dir .claude/skills --seats-dir .chiron/seats
```

Also read the bench YAMLs (`.chiron/benches.yaml`, `~/.claude/chiron/benches.yaml`). You now know every installed seat's `domains`, `description`, `mode`, and lint status, and every named bench.

## Step 2 — Read the decision on three axes

- **Stakes:** cheap and reversible, or expensive and irreversible? (Reversibility is the single biggest input. A call you can undo next week does not need a council.)
- **Breadth:** does it live in one seat's domain, or does it straddle several (e.g. a pricing move that is part strategy, part psychology, part negotiation)?
- **Type:** is this a judgment call a seat should weigh in on, or is it factual, technical, or trivial? Seats opine on decisions, not on syntax errors or lookups.

## Step 3 — Pick a routing verdict

Choose the **cheapest verdict that fully serves the decision**. Bias toward the top of this list; earn your way down.

- **SKIP** — no seat fits. The question is factual, technical, trivial, or outside every installed seat's competence (respect each seat's `## Refusals`). Answer it directly, or say plainly that no seat has standing here. Do not force an advisor onto something it has no business judging. This is the "is it worth it" gate saying no, and that is a feature.
- **ASK (one seat)** — one clear domain owner, and the stakes are low-to-moderate or the question is cleanly single-domain. Name the single best seat and run `commands/ask.md`. Cheapest useful path.
- **COUNCIL (2 to 5 seats)** — convene only when at least one is true: the call is **expensive or irreversible**; it is genuinely **cross-domain**; or the topic sits on an **authored disagreement** between installed seats. Select the smallest set that covers the real tensions, prefer seats that have a cited `disagreements.md` entry on this topic (that is where a debate has real signal, not manufactured conflict), cap at 5 (CH-E4), and run `commands/council.md`.
- **CLARIFY** — if you genuinely cannot read the stakes or what is being asked, ask ONE sharp question, then route. Do not convene to cover for ambiguity.

## Step 4 — Select the seats (which experts)

- Match the question to seat `domains` + `description`. A seat whose `## Refusals` cover this topic is disqualified, not merely deprioritized.
- For a council, actively look for the authored-disagreement seams: if two installed seats have a cited conflict relevant to the question, they belong in the room. That is the product's edge over generated debate.
- If a named bench already fits the domain, use it rather than assembling ad hoc.
- If more than 5 seats look relevant, pick the highest-signal set and say which you dropped and why. Never dump the whole roster.

## Step 5 — Show your work, then execute

Before running anything, state the verdict in one or two lines so the user can override:

> "This is a reversible copy tweak, so no council needed. Routing to Voss alone for the phrasing." 

> "This is an irreversible pricing call that touches strategy, psychology, and leverage. Convening Munger, Naval, and Rumelt (Munger and Naval carry an authored disagreement on concentration that bears directly on this). Estimated ~6k tokens. Proceeding."

Then hand off to the chosen flow (`ask` or `council`) and follow its contract exactly, including the log/RECORD step. The user can always say "just ask X" or "make it a full council" to override your route.

## Proactive routing (scope note)

When the user is clearly mid-decision in normal conversation but has not asked Chiron for anything, **offer** to route ("want me to run this by the right seats?") rather than silently hijacking the turn. An advisor that interrupts uninvited is a worse product than one that waits to be asked. Fully autonomous, unprompted interjection is intentionally out of scope for now; keep the human in the loop on when the council convenes.
