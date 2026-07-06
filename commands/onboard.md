---
description: First-run setup — meet the roster, distill yourself, and get a starter set of benches
argument-hint: [none]
---

# /chiron:onboard — set up Chiron in five minutes

Get a new user from install to their first useful council. Move quickly, do the work for them, and end on a concrete next action. Keep it conversational, not a wizard.

## 1. Orient (brief)

One short paragraph: Chiron is a council of authored advisors ("seats") built from real published work, cited, not generated personas. You ask one seat, or convene several, and it can pick the right ones for you. Then show what's installed:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/registry.py --seats-dir ${CLAUDE_PLUGIN_ROOT}/seats --seats-dir ~/.claude/chiron/seats --seats-dir .chiron/seats
```

Render the roster grouped by domain so they see who's in the box.

## 2. Distill them (the core of onboarding)

Offer `/chiron:distill-me` to build their private `me` seat and read out their go-to experts. If they'd rather keep it fast, run a **five-question mini-version** inline instead:

1. What are you working on right now?
2. What decision are you chewing on today?
3. Which thinkers do you already reach for? (their go-to experts)
4. What do you refuse to do / what are your non-negotiables?
5. How do you want to be talked to — blunt, or cushioned?

Either path yields: their domains, their go-to experts, and their decision style. (The full `distill-me` also writes the `me` seat; the mini-version can defer that.)

## 3. Recommend seats + build starter benches

From their go-to experts and the decision in Q2:

- Map experts to installed seats; offer to `/chiron:distill` any they named that aren't installed yet.
- Create **2-3 starter benches** with `/chiron:bench` from their domains (e.g. a `money` bench, a `strategy` bench, a `decisions` bench), and a personal bench chaired by their `me` seat if they built one. Write them to `~/.claude/chiron/benches.yaml` (global) unless they're in a project.
- Copy `${CLAUDE_PLUGIN_ROOT}/benches/examples/benches.yaml` as a starting point if useful.

## 4. First real consult

End by running their actual Q2 decision through the orchestrator so onboarding produces a real answer, not a tour:

> `/chiron:consult "<their decision from Q2>"`

Then hand them the three things they'll use daily: `/chiron:consult` (let Chiron route), `/chiron:ask <seat>` (one lens), and `/chiron:distill` (add an expert). Note that they can just talk to it naturally too ("run this by my money bench").
