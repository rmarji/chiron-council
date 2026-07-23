# Core concepts

This is the mental model behind Chiron. Read it once and the rest of the docs click: the commands, the standard, the benches, and the way a council argues all follow from a few ideas. Chiron has one unit of value, the **seat**, and everything else is built on it.

## A seat is one authored mind

A seat is one advisor, distilled from what a real person actually published, cited claim by claim. Not a vibe, not a name on a card, not a prompt that says "act like Munger." A seat carries the person's frameworks, mental models, heuristics, anti-patterns, and refusals, each traceable to a book, a talk, or an episode.

A seat is implemented as a **native Agent Skill**. It lives flat at `skills/<id>/` with a `SKILL.md`, and Claude auto-activates it like any other skill. You do not have to summon it. Ask "what would the Munger corpus say about this incentive?" and the `munger` seat loads on its own.

What makes a skill a *seat*, and not just any skill, is that it passes the [seat standard](./the-standard.md): cited provenance, explicit refusals, an authored voice, and a full reference set. The frontmatter carries an `x-chiron:` block that flags the skill as a seat:

```yaml
---
name: munger
description: Applies the reasoning, mental models, and temperament of Charlie Munger...
x-chiron:
  display_name: Munger Lens
  mode: corpus
  domains: [investing, decision-making, incentives]
  provenance:
    subject: Charlie Munger
    living: false
    sources:
      - "Poor Charlie's Almanack (2005)"
      - "The Psychology of Human Misjudgment (1995)"
      - "Wesco Financial annual meeting transcripts (1999-2011)"
---
```

That `x-chiron` marker is load-bearing. The registry and linter find seats by scanning for it, which means Chiron can share a skills directory with unrelated skills and the `chiron` router itself: anything without an `x-chiron` block is ignored, so a folder full of your other skills never gets mistaken for a seat.

The anatomy of a seat, in one glance:

```
skills/munger/
├── SKILL.md            # the mind: priors, heuristics, refusals, voice (< 6k tokens)
├── disagreements.md    # authored conflicts with other seats, both positions cited
├── references/         # the depth: full extraction of the published thinking
│   ├── principles.md   ├── mental-models.md   ├── frameworks.md
│   ├── anti-patterns.md ├── heuristics.md     ├── quotes.md   └── sources.md
└── log.md              # append-only consult memory (gitignored)
```

Everything is files. No database, no server, no API keys. The full contract lives in [SEAT_SPEC.md](../SEAT_SPEC.md), summarized in [the-standard.md](./the-standard.md).

## Three modes

Every seat declares a `mode`. The mode decides how it may speak.

| Mode | For | Voice | Constraints |
|---|---|---|---|
| **corpus** | Real people, built from published work | Third person about the corpus, a source per claim | The default, and the only mode that ships for a real person |
| **original** | Your own operating system, or an invented advisor | First person in its own voice | No provenance constraints (nobody to cite but the author) |
| **persona** | First-person emulation of a subject | Speaks as the subject | Never a default. Forbidden for a living subject without a granted license |

**Corpus mode** is the backbone of the roster. A corpus seat speaks *about* the record, never *as* the person: "the Munger corpus would flag the incentive here (The Psychology of Human Misjudgment, 1995)," not "I, Charlie, would flag this." Fourteen of the fifteen founding seats are corpus mode.

**Original mode** is for a mind that is its own source. Rayo OS is one: an authored execution and decision-routing operating system (FATE, the Ship Gate, MAX THREE) with no external subject to cite. Your own `me` seat is another. When you run [`/chiron:distill-me`](./distilling.md), Chiron reads how you actually operate and writes an original-mode seat holding your mission, values, goals, frameworks, and the experts you already reach for, so your own operating system can chair a council and be argued with. That `me` seat is **private**: it lives in `~/.claude/chiron/seats/` or a project's `.chiron/seats/`, both gitignored, never committed, and never shipped from the plugin repo.

### Why living people are corpus-only

A living person's seat is always corpus mode. This is both a legal line and a quality line.

The legal line: first-person emulation of a living, unlicensed person runs into right-of-publicity and false-endorsement risk. The linter enforces it mechanically. Rule **L1** hard-fails any seat that combines `mode: persona`, `living: true`, and an ungranted license. It is a load-blocking error, not a warning, and [`/chiron:distill`](./distilling.md) will refuse to build such a seat under any phrasing. The full policy is in [LEGAL.md](../LEGAL.md).

The quality line: sourced heuristics beat generated cosplay. A corpus seat that has to cite a page for every claim cannot drift into a plausible-sounding paraphrase of nothing. The constraint that makes the seat legally safe is the same one that makes it trustworthy.

## The depth bar

Seats are not stubs. A name and a one-paragraph description is exactly what Chiron refuses to ship. Every real-person seat carries the seven standard reference files (`principles`, `mental-models`, `frameworks`, `anti-patterns`, `heuristics`, `quotes`, `sources`), each a full extraction of that dimension of the subject's thinking with a named source per claim. In practice that is 6,000 to 10,000 words of cited material per seat.

The linter defends the bar so "a seat" always means the same thing:

- **L4** fails a corpus seat with fewer than three provenance sources.
- **L12** fails a seat that is missing any of the seven reference files.

If a seat skimps on provenance, the build fails. That is what separates a seat from a name, and it is why depth is baked into the hire rather than sold as an upgrade. See [the-standard.md](./the-standard.md) for the whole rule set.

## Memory

Each seat keeps a private `log.md`: an append-only record of what it was asked, what it advised, and what you decided. When a seat loads, it reads its last 10 entries, so it remembers what it told you and whether you listened. Ask the same seat about a call it weighed in on two weeks ago and it can say "this seat advised X on that; the recorded decision was Y."

The log holds *your* decisions, not the seat's thinking, so it is gitignored by default and stays local. [`/chiron:log <seat>`](./commands.md) surfaces the open loops you never closed.

## The router

You do not have to know which expert to ask. [`/chiron:consult`](./commands.md) is the orchestrator: it reads your decision and routes it. It weighs three axes:

- **Stakes.** Cheap and reversible, or expensive and irreversible? Reversibility is the biggest single input. A call you can undo next week does not need a council.
- **Breadth.** One seat's domain, or does it straddle several (a pricing move that is part strategy, part psychology, part negotiation)?
- **Type.** A judgment call a seat should weigh in on, or something factual, technical, or trivial? Seats opine on decisions, not on syntax errors or lookups.

Then it picks the cheapest verdict that fully serves the decision:

- **SKIP.** No seat has standing. Factual, trivial, or outside every seat's competence. Answering "you do not need a council for this" is a feature, not a dodge.
- **ASK one seat.** One clear domain owner and low-to-moderate stakes. Routes to `/chiron:ask`.
- **COUNCIL.** Convened only when the call is expensive or irreversible, genuinely cross-domain, or sits on an authored disagreement between installed seats. Capped at five for a routed council.
- **CLARIFY.** If the stakes truly cannot be read, one sharp question, then route. Never convene to cover for ambiguity.

The router states its verdict before it acts, so you can override it:

```
> This is an irreversible pricing call that touches strategy, psychology, and
> leverage. Convening Munger, Naval, and Rumelt. Munger and Naval carry an
> authored disagreement on concentration that bears directly on this. Proceeding.
```

You can always say "just ask Voss" or "make it a full council" to overrule the route.

## A council

A council is the opposite of one model wearing five hats. It manufactures real independence and surfaces only real conflict, in three phases.

1. **Independent takes, in isolation.** Chiron spawns one subagent per seat, in parallel. Each subagent sees only that seat's `SKILL.md`, that seat's last 10 log entries, and the question. It does not see the other seats, their takes, the bench, or your conversation. The disagreement is structural, produced by giving each mind a different corpus, not by telling one model to "be the contrarian."

2. **Authored disagreement.** Chiron reads the `disagreements.md` of every seat in the room and surfaces only conflicts that are on the record: entries where both counterparts are present and the topic matches the question, quoted with the citations for each side. If there is no authored conflict for this topic, the council says so. It will not generate, infer, or dramatize a disagreement that is not in the files. Manufactured conflict is the exact failure this product exists to kill.

3. **One synthesis, dissent preserved.** A chairman returns a single recommendation, not a menu, and names the dissent instead of averaging it away: which seats disagree, why, what the recommended path costs you, and what would change the call. The chairman is a neutral analyst by default, or a seat you name (your `me` seat can chair its own councils).

Councils never invent a seat, and never invent a fight. Both guardrails are what make the debate worth reading.

## A bench

A bench is a saved line-up of seats with a chairman. It is plain YAML you can edit by hand, because files are the API:

```yaml
benches:
  money:
    seats: [munger, naval, rayo]
    chairman: neutral      # a seat id, or "neutral"
    default_depth: quick   # quick | full
```

Benches live globally at `~/.claude/chiron/benches.yaml` and per project at `.chiron/benches.yaml`, and project shadows global on a name collision. Name a bench where a council expects a seat list and it convenes that line-up. See [benches.md](./benches.md) for the full mechanics.

## Authored versus generated

This is the whole wedge, in one paragraph. The crowded lane of AI advisor tools auto-generates a "mind" from any input in a weekend, then fakes disagreement by handing each generated persona an opposing archetype. Chiron takes the other bet: seats are hand-authored and curated, every substantive claim points at a source, a linter fails the build on seats that skimp on provenance, and a council surfaces only conflicts the real people actually argued, both positions cited. Authored, cited, and real beats generated, vibes, and manufactured. That is the reason a Chiron seat can tell you something you do not want to hear and you have a reason to believe it.
