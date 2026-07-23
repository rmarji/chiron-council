# Portability: seats in any agent

Every Chiron seat is a standard Agent Skill, so the roster runs far beyond Claude Code. This page covers what a seat is on disk, how to install seats into any harness that loads Agent Skills (with the `skills` CLI or by hand), and exactly which parts of Chiron are plugin-only versus universal.

## A seat is a standard Agent Skill

A seat is not a Chiron-proprietary format. It is a plain Agent Skill: a directory with a `SKILL.md` whose frontmatter carries the standard `name` and `description` keys that every Agent Skills-compatible harness reads to decide when to activate it. That is the whole compatibility story. Chiron adds a few things on top that non-Chiron harnesses simply ignore.

```yaml
---
name: munger
description: >
  Applies the reasoning, mental models, and temperament of Charlie Munger.
  Reach for this skill when the user is making a high-stakes or irreversible
  decision, evaluating a bet, auditing incentives, or trying to avoid a costly
  mistake. Invert the problem, stay inside the circle of competence, run it
  through a latticework of mental models.
x-chiron:                       # Chiron extension; other harnesses ignore it
  display_name: Munger Lens
  mode: corpus
  domains: [investing, decision-making, incentives]
  provenance:
    subject: Charlie Munger
    living: false
    sources:
      - "Poor Charlie's Almanack (2005)"
      - "The Psychology of Human Misjudgment (1995)"
      - "A Lesson on Elementary, Worldly Wisdom, USC (1994)"
---
```

(Frontmatter trimmed for the example. The real `skills/munger/SKILL.md` carries ten sources and a longer description.)

Three parts are Chiron-specific and safe to carry anywhere:

- **`x-chiron:`** in the frontmatter. It is the marker that tells Chiron's registry and linter "this skill is a seat" (display name, mode, domains, provenance). A generic harness reads `name` and `description`, does not recognize the `x-chiron` key, and moves on. No error, no effect.
- **`disagreements.md`** next to `SKILL.md`. Authored, cited conflicts with other seats. Chiron's councils read it; other harnesses never look for it, so it just sits there.
- **`references/`**, the seven-file deep extraction of the subject's thinking. In Claude, these load on demand through progressive disclosure. In another harness they are extra files the loader does not touch unless you point the model at them.

The important consequence: the mind is baked into `SKILL.md` itself. Priors, heuristics, refusals, the voice contract, and the subject's two or three signature mental models are all inline in the body, not hidden in `references/`. A seat is a working advisor from `SKILL.md` alone, whether or not the harness ever reads the reference files. See [The seat standard](./the-standard.md) for the full anatomy, and [../SEAT_SPEC.md](../SEAT_SPEC.md) for the normative spec.

## Install into other harnesses with the skills CLI

The [`skills`](https://skills.sh) CLI installs any Agent Skill into 70+ harnesses and knows where each one keeps its skills, so you do not manage directories yourself. Point it at the Chiron repo and pick seats:

```bash
npx skills add rmarji/chiron-council                                   # pick seats interactively
npx skills add rmarji/chiron-council --all                             # install the whole roster
npx skills add rmarji/chiron-council -a codex -s munger naval taleb    # target a harness, pick seats
```

- `--all` installs every seat in the roster.
- `-a <agent>` selects the target harness (omit it and the CLI installs into Claude Code, or prompts).
- `-s <seat...>` selects specific seats by id (space-separated). Seat ids are the folder names: `munger`, `naval`, `taleb`, `hormozi`, `voss`, `sherlock`, `house`, `columbo`, and so on. Run [`/chiron:roster`](./commands.md) or `python3 scripts/registry.py` to list them.

Common `-a` targets:

| Harness | `-a` slug | Reads skills from |
|---|---|---|
| Claude Code | (default) | `~/.claude/skills/` |
| Cursor | `cursor` | `~/.cursor/skills/` |
| Codex CLI | `codex` | `~/.codex/skills/` |
| Gemini CLI / generic | `gemini-cli` | `~/.agents/skills/` |

Copilot, Cline, and dozens more are supported. The exact slug list comes from the CLI itself, so run the interactive picker (plain `npx skills add rmarji/chiron-council`) or `npx skills --help` to see every harness rather than guessing a slug. The Agent Skills open standard these all share is documented at [agentskills.io](https://agentskills.io).

## Copy a seat by hand

You do not need the CLI. A seat is a directory, so `cp` it into whatever skills folder your agent scans:

```bash
# Claude Code          Cursor                Codex CLI            Gemini CLI / generic
~/.claude/skills/      ~/.cursor/skills/     ~/.codex/skills/     ~/.agents/skills/

cp -r skills/munger ~/.claude/skills/munger
```

Copy the whole `munger/` directory, not just `SKILL.md`, so `disagreements.md` and `references/` travel with it. The seat auto-activates on the next session, the same as any skill you drop in that folder. To move the full roster, copy each seat directory (skip `skills/chiron/`, which is the router, not a seat, and only matters inside the plugin).

Because Chiron discovers seats by the `x-chiron` marker rather than by owning the directory, dropping a seat into a shared skills root that already holds unrelated skills is safe: Chiron's registry picks out the seats and ignores everything else, and the other harness treats a Chiron seat as an ordinary skill. Nothing collides.

## What is plugin-only versus universal

Draw the line between the seats and the plugin around them.

| Universal (any Agent Skills harness) | Plugin only (Claude Code and Cowork) |
|---|---|
| Seats auto-activate on relevant questions | `/chiron:*` slash commands |
| The mind: priors, heuristics, refusals, voice, cited claims | `/chiron:consult` auto-routing to the right expert |
| Third-person corpus voice with a source per claim | Live councils: independent takes, surfaced disagreements, one synthesis |
| You address a seat directly and it responds | Benches (curated line-ups) and per-seat memory (`log.md`) |

The seats themselves run anywhere Agent Skills load. The orchestration around them, the slash commands, the self-routing consult, live councils, benches, and the memory that logs what a seat told you, lives in the Chiron plugin. The plugin runs in Claude Code and in Cowork, which share the plugin format (see [Installation](./installation.md) and [Cowork](./cowork.md)). Outside those two, you get the seats without the conductor.

Be aware of the memory caveat: `log.md` is written by the plugin's `ask` and `council` flows. In a bare harness the seat activates and advises, but nothing appends to its log, so there is no running memory of your past calls. That is a feature of the plugin, not the seat file.

## Invoke a seat outside the plugin

With no slash commands, you invoke a seat by talking to it. Address the corpus by name and the installed skill activates:

```
What would the Munger corpus say about signing a 15k/mo retainer that
locks me in for a year?
```

The seat answers in its contracted voice, third-person and cited, not first-person cosplay of the person:

```
The Munger corpus would invert first: before asking how this retainer
wins, state how it fails. A year of locked capacity is a circle-of-
competence question, are you sure this is work you understand well
enough to commit a year to, and an incentives question, who benefits
from the lock-in, you or them ("The Psychology of Human Misjudgment,"
1995). If the main appeal is that it feels clever rather than that it
avoids a stupid mistake, the corpus says pass.
```

You can name the subject casually ("what would Munger say...") or the lens explicitly ("run this through the Munger corpus"). Either way the skill triggers on the description and holds its refusals: ask it something outside its lane and it declines and redirects, exactly as it would inside the plugin. What you lose without the plugin is the router choosing the seat for you and the council making several seats argue. What you keep is the seat itself, fully authored and cited.

## Your own distilled seats port too

Seats you create with [`/chiron:distill`](./distilling.md) are ordinary seats and travel the same way. In Claude Code, distill writes the new seat to `~/.claude/skills/<id>/`, a standard skills directory, so it auto-activates in every session and installs into other harnesses with the same `cp` or `npx skills` step.

The one exception is your private `me` seat from `/chiron:distill-me`. It holds personal data, so it lives in `~/.claude/chiron/seats/` (or a project's `.chiron/seats/`), which is a Chiron registry path, not a standard skills directory. It is gitignored and never shipped, and because it is not in a skills folder it does not auto-activate as a global skill in another harness. That is deliberate: your operating system stays local to Chiron. See [Concepts](./concepts.md) for the precedence rules and [../SEAT_SPEC.md](../SEAT_SPEC.md) for where seats live.

## The standard travels with the seats

Portability is not just the files, it is the bar. `scripts/lint_seat.py` is stdlib-only Python with no dependencies, so anyone can validate a seat outside Claude, in CI or on their own machine:

```bash
python3 scripts/lint_seat.py skills/munger --explain
python3 scripts/lint_seat.py --all
```

The linter hard-fails first-person impersonation of a living person, fewer than three sources, and shallow or missing reference sets. That is what keeps a ported seat a seat and not just a famous name in a frontmatter block. More in [The seat standard](./the-standard.md) and the provenance policy in [../LEGAL.md](../LEGAL.md).
