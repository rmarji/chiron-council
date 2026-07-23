# Getting the most out of Chiron

The install works out of the box, but the difference between a novelty and a real advisor is how you route decisions to it, which benches you keep, and whether you close the loops it opens. This page is the power-user layer: when to ask one seat versus convene many, how to build a roster you actually use, how to put yourself in the room, and the honest frame for what any of this buys you.

If you have not installed yet, start with [installation](./installation.md) and [quickstart](./quickstart.md). For the concepts behind the commands, see [concepts](./concepts.md); for the full flag reference, see [commands](./commands.md).

## The one rule: match the machinery to the stakes

Every consult costs tokens and attention. A five-seat council convened for a reversible copy tweak is not diligence, it is a token tax dressed as diligence. The whole skill is spending the machinery where it pays.

Read a decision on three axes before you spend anything:

- **Stakes.** Cheap and reversible, or expensive and irreversible? Reversibility is the single biggest input. A call you can undo next week does not need a council.
- **Breadth.** Does it live in one seat's domain, or straddle several? A pricing move can be part strategy, part psychology, part negotiation.
- **Type.** Is this a judgment call, or is it factual, technical, or trivial? Seats opine on decisions, not on syntax errors or lookups.

Then pick the cheapest path that fully serves the decision:

| Situation | Route | Command |
|---|---|---|
| Factual, technical, trivial, or outside every seat's competence | **Skip.** Answer it directly, no seat has standing | (Chiron says so and stops) |
| Low-to-moderate stakes, cleanly single-domain | **Ask one seat.** The cheapest useful path | `/chiron:ask <seat> <q>` |
| Expensive or irreversible | **Small council** | `/chiron:council <bench> <q>` |
| Genuinely cross-domain | **Small council** | `/chiron:council <bench> <q>` |
| Sits on a real, authored disagreement between installed seats | **Small council** (this is where debate has signal) | `/chiron:council <bench> <q>` |
| You cannot read the stakes | **Clarify one thing, then route** | `/chiron:consult <q>` |

You do not have to make that call yourself. That is what the orchestrator is for.

## Let it route, do not micromanage the roster

`/chiron:consult` reads your decision on those three axes, picks the cheapest verdict, and states it in one line before it spends a thing:

```
/chiron:consult "reword this cold email so it doesn't sound desperate"
▸ Reversible copy tweak, single domain. No council. Routing to Voss alone. Proceeding.

/chiron:consult "take the 15k/mo retainer or walk?"
▸ Irreversible, cross-domain (leverage, incentives, your own execution laws).
  Convening Munger, Naval, Rayo. Naval and Munger carry an authored
  disagreement on concentration that bears on this. ~7k tokens. Proceeding.
```

The default posture is: let it route. It will `SKIP` when no seat has standing rather than force an advisor onto a lookup, `ASK` one owner for a single-domain call, and `COUNCIL` (2 to 5 seats when it routes) only when the call is expensive, cross-domain, or sitting on a cited conflict. The most valuable thing it does is often tell you a council is not worth convening.

You keep the override, always. Say "just ask Munger" to collapse it, or "make it a full council" to force one. Use the override when you already know the domain cold. Reach for `/chiron:consult` when you do not, or when you suspect you are about to talk yourself into something.

For anything cheap and reversible, skip the ceremony entirely and use `/chiron:ask`. The orchestrator earns its keep on the calls you cannot take back.

## Build a small library of benches for the decisions you actually face

A **bench** is a named line-up of seats you convene as a unit. Benches are plain YAML you can edit by hand: global at `~/.claude/chiron/benches.yaml`, project-local at `.chiron/benches.yaml` (project shadows global on a name collision). See [benches](./benches.md) for the full mechanics.

The mistake is building a generic all-star team you admire but never call. Build benches for the decisions you *repeat*. If you price offers every month, keep an offers bench. If money calls are your recurring stress, keep a money bench.

```bash
/chiron:bench create money munger naval rayo          # writes to project, or --global
/chiron:bench create pricing hormozi cialdini rayo
/chiron:bench list
```

A bench takes 2 to 8 seats, a `chairman` (a seat id or `neutral`), and a `default_depth` of `quick` or `full`:

```yaml
benches:
  money:
    seats: [munger, naval, rayo]
    chairman: neutral       # or a seat id
    default_depth: quick    # quick | full
```

Keep them small. Two to five seats is the sweet spot. Six or more starts to read as consensus theater and costs real tokens (a `full` run is roughly seats times 4k tokens; `quick` is roughly seats times 1.5k). The bundled `benches/examples/benches.yaml` is a good starting point to copy and trim. Deleting a bench never touches the seats it names, so prune freely.

Once a bench exists you can convene it by name, or just talk to it: "run this by my money bench."

## Distill the experts you already reach for

The roster ships with 18 seats, but the ones that will change your decisions are the ones you *already* channel when you are stuck. Do not build a museum of famous names. Distill the three or four minds you actually reach for, and put them where the router can find them.

```bash
/chiron:distill "Rory Sutherland on behavioral economics and marketing"
```

`/chiron:distill` interviews you briefly, runs deep research over the subject's published corpus, writes the full seat (SKILL.md plus all seven reference files at the depth bar, every claim cited), lints it, and installs it as a live, auto-activating skill. In Claude Code it writes to `~/.claude/skills/<id>/`, so the seat is available in every session and every council finds it with no manual move. In Cowork, which cannot write to `~/.claude`, it writes a workspace `.chiron/seats/<id>/` or emits a `.plugin` for you to accept in-app; see [cowork](./cowork.md).

Two things worth knowing:

- **One subject per pass.** If you want four advisors, distill them one at a time. Batching them into one shallow sweep produces thin, repetitive seats, which is exactly the failure mode the standard exists to kill. Depth is the point; see [the standard](./the-standard.md).
- **It will refuse first-person impersonation of a living person.** Ask for a persona-mode seat of a living, unlicensed subject and the flow declines, then offers corpus mode or an archetype alias instead. That is a legal guardrail, not a limitation to route around. See [../LEGAL.md](../LEGAL.md).

Full walkthrough in [distilling](./distilling.md).

## Put yourself in the room

The highest-leverage seat you can build is your own. `/chiron:distill-me` distills *you* the way the roster distills its thinkers: it reads what you point it at (your notes, your instruction files, this conversation), interviews you, and writes a private, original-mode `me` seat holding your mission, values, goals, frameworks, and the experts you already reach for.

```bash
/chiron:distill-me
```

That `me` seat does two jobs:

1. **It chairs your councils.** Set `chairman: me` on a personal bench and your own operating system arbitrates the debate instead of a neutral analyst. The council argues, and your own laws break the tie.
2. **Its read-out becomes your roster.** The distill-me flow maps your named go-to experts against what is installed, flags the ones you should distill next, and proposes starter benches built from *your* people, not a generic set.

```yaml
benches:
  personal:
    seats: [me, munger, rayo]
    chairman: me
    default_depth: full
```

Your `me` seat is **private**. It lives in `~/.claude/chiron/seats/me/` (global) or a project's `.chiron/seats/me/`, it is gitignored, never committed, and never shipped in the plugin. Treat it like your own notes, because that is what it is. If you build it inside a project, add `.chiron/seats/` to that project's `.gitignore` (the flow offers to do it for you).

## Use the memory

Every consult appends to the seat's `log.md`, and a summoned seat reads its last ten entries, so it remembers what it told you and whether you listened. That memory is only worth having if you look at it.

```bash
/chiron:log rayo                 # everything this seat has weighed in on, newest first
/chiron:log rayo --open-loops    # decisions you consulted on and never closed
```

The `--open-loops` view is the one to run weekly. It filters to entries where the decision is still `open loop` and flags anything older than 14 days. Those are calls you paid a council to think through and then let drift. Close one by telling Chiron the decision you actually made, and it records it against that entry. Reading a log never changes it; the only mutation is you closing a loop.

This is where the [Rayo](../README.md) seat's discipline earns its place even if you never ask it a question. Rayo's operating system runs on two ideas that apply directly here: **Luck = Doing times Telling** (an unacted decision has a luck surface of zero, regardless of how well you reasoned it), and the **Ship Gate** (nothing new should start while a finished thing sits unshipped). An open loop older than two weeks is exactly that: a decision reasoned and never shipped. The open-loops view is your Ship Gate for judgment. When you record the call, ask yourself whether you followed the advice or overrode it, because the log will tell you your own track record over time, and that is worth more than any single take.

## The honest frame

Chiron will not make you right. One agreeable model already tells you that you are right, near 50% more often than a human would, which is precisely why a single chatbot is a bad advisor for a decision you cannot take back.

What Chiron does is make you **wrong less often**, by a few concrete mechanisms:

- It gathers takes in isolation, so a council surfaces structural disagreement instead of five flavors of one model agreeing with you.
- It surfaces only conflicts that are *authored* from what real people actually argued, both positions cited, and says "no authored conflicts on record" rather than inventing drama. If you want to know where thoughtful people genuinely split, that is where you look.
- It remembers, so you can see whether your past self's advice held up and whether you took it.

None of that guarantees a good outcome. Seats can be wrong together, a cited position can still be the wrong call for your situation, and a synthesis is a recommendation, not a verdict. The value is a lower error rate on the calls that matter, and an advisor that will tell you what you do not want to hear. Treat every output as an argued input to your decision, never as the decision.

## Do and do not

**Do**

- Default to `/chiron:consult` and let it route; reach for it hardest on calls you cannot undo.
- Reserve councils for expensive, irreversible, cross-domain, or genuinely-disagreed calls. Ask one seat for everything else.
- Build benches for the decisions you actually repeat, and keep them to 2 to 5 seats.
- Distill the experts you already channel, one at a time, at full depth.
- Put your `me` seat in the chair for personal decisions.
- Run `/chiron:log <seat> --open-loops` weekly and close the loops.
- Override the route when you already know the domain: "just ask Voss."

**Do not**

- Convene a five-seat council for a reversible tweak. That is decision theater and a token tax.
- Dump the whole roster into one bench, or build a generic all-star bench you will never call.
- Expect the council to make the call for you. It argues from the record; you decide.
- Push a seat past its `## Refusals`. When it declines, that boundary is the mind working, not a bug.
- Read a synthesis as consensus. The preserved dissent is the point; do not average it away in your head.
- Commit or ship your `me` seat. It is private, gitignored, and local by design.

## Where to go next

- [commands](./commands.md) for every flag and error path.
- [benches](./benches.md) for the full bench mechanics and shadowing rules.
- [distilling](./distilling.md) for authoring seats and your `me` seat.
- [the standard](./the-standard.md) and [../SEAT_SPEC.md](../SEAT_SPEC.md) for what makes a seat a seat.
- [troubleshooting](./troubleshooting.md) when a route, lint, or install misbehaves.
