# Benches

A bench is a curated line-up of seats you convene as a group. This page covers the YAML that defines one, where benches live, how to create and edit them, some line-ups worth stealing, how big to make them, and when a bench actually beats a single [`/chiron:ask`](./commands.md).

## What a bench is

Chiron ships eighteen [seats](./concepts.md), each one mind distilled from a real record. A bench is a named set of those seats you have decided belong in the room together for a class of decision: a money bench, a strategy bench, a relationship bench. When you convene it, Chiron runs the [council state machine](./commands.md#chironcouncil): each seat gives its take in isolation, any authored disagreements between them get surfaced from the record, and a chairman writes one synthesis with the dissent preserved.

Benches are plain YAML. The file is the API. You can create them with [`/chiron:bench`](./commands.md) or open the file in an editor and type. Nothing is hidden behind a database or a server.

## The YAML shape

A bench file has a `benches:` root, and each key under it is a bench name mapped to three fields.

```yaml
benches:
  money:
    seats: [munger, naval, rayo]
    chairman: neutral        # a seat id, or "neutral"
    default_depth: quick     # quick | full
```

| Field | What it is | Values | Default |
|---|---|---|---|
| `seats` | the seat ids in the room | 2 to 8 valid seat ids | required |
| `chairman` | who writes the synthesis | `neutral`, or one of the seat ids | `neutral` |
| `default_depth` | how deep a convene runs unless overridden | `quick` or `full` | `quick` |

Notes on each field:

- **`seats`** are ids, not display names: `munger`, `naval`, `terry-real`, `paul-graham`. Run [`/chiron:roster`](./commands.md) to see every installed id. A `me` in the list refers to your private seat (see [Chairing with your `me` seat](#chairing-with-your-me-seat)).
- **`chairman: neutral`** synthesizes as a plain analyst. Naming a seat id instead makes that seat write the final call in its own voice. A chairman that is also one of the `seats` gives its own take in phase one and then chairs; that is fine and common.
- **`default_depth: quick`** gathers the takes and closes with a micro-synthesis (recommendation, one line of preserved dissent, confidence). `full` adds the authored-conflict pass and a fuller synthesis. Either way you can override per convene with `--depth`.

## Where benches live

Two locations, same shape:

- **Global:** `~/.claude/chiron/benches.yaml`. Available in every project.
- **Project:** `.chiron/benches.yaml`. Scoped to the repo you are in.

On a name collision, **project shadows global**. If you have a global `strategy` bench and a project `strategy` bench, the project one wins inside that repo, and Chiron notes the shadowing once per session when it applies. Removing the project entry falls back to the global one.

The project `.chiron/` directory is gitignored by Chiron's own repo because it also holds your private `me` seat and personal config. In your own project you decide whether to commit `.chiron/benches.yaml`. Commit it to share a team's benches; leave it ignored to keep them personal.

## Creating and editing

### With `/chiron:bench`

```
/chiron:bench create money munger naval rayo
/chiron:bench create strategy rumelt munger naval --depth full
/chiron:bench create deals voss munger rayo --chairman rayo --global
/chiron:bench list
/chiron:bench remove deals
```

What `create` does:

1. Validates the name against `^[a-z0-9-]{2,32}$` (lowercase letters, digits, hyphens; 2 to 32 characters).
2. Validates every seat id against the live registry. An unknown id does not get written: Chiron suggests the closest matches instead.
3. Enforces sizing: 1 seat is refused with "use `/chiron:ask`, a bench of one is a person"; more than 8 is refused outright; 6 or more is allowed but warned (see [Sizing](#sizing-a-bench)).
4. Writes to the project file by default when you are inside a project, or to the global file with `--global` (and always global when you are not in a project). It preserves your existing entries and comments and echoes back the resulting YAML block.

Flags:

| Flag | Effect |
|---|---|
| `--global` | write to `~/.claude/chiron/benches.yaml` instead of the project file |
| `--chairman <id>` | set the chairman to a seat id (default `neutral`) |
| `--depth <quick\|full>` | set `default_depth` (default `quick`) |

`list` reads both files and renders a table of name, seats, chairman, depth, and source (project or global), marking any shadowed globals and flagging any bench that references a seat you no longer have installed. `remove <name>` deletes the entry from the scope where it lives (it asks which if the name exists in both) and shows the diff. Removing a bench never touches seat folders; a bench is just a grouping.

### By hand

Because the file is the API, editing is the same as writing YAML. Open `~/.claude/chiron/benches.yaml` (create it if it does not exist), add a block under `benches:`, save.

```yaml
benches:
  # Money and bets: incentives, leverage, and your own execution laws
  money:
    seats: [munger, naval, rayo]
    chairman: neutral
    default_depth: quick

  # Strategy calls: diagnosis before action, then leverage
  strategy:
    seats: [rumelt, munger, naval]
    chairman: neutral
    default_depth: full
```

Comments survive. Chiron reads the file back and does not strip them. If you fat-finger a seat id, you find out at convene time (a missing seat is named and you are offered the run with the remainder), or immediately if you run `/chiron:bench list`, which flags uninstalled seats inline.

## Convening a bench

Three ways to put a bench in the room:

```
/chiron:council money "take the retainer at 15k/mo or walk?"
/chiron:ask strategy "should we open a second product line?"      # a bench name here becomes a council
/chiron:consult "we keep having the same fight about money"        # auto-routing may pick a named bench that fits
```

`/chiron:council <bench>` is the direct route. `/chiron:ask <bench>` works too: if the first token matches a bench name it runs council semantics at the bench's `default_depth`. Seat ids win ties, so if you ever named a bench the same as a seat, the seat resolves first. `/chiron:consult` routes for you and will reuse a named bench when one fits the domain rather than assembling seats ad hoc.

Override the depth on any convene:

```
/chiron:council money "small copy tweak, which line?" --depth quick
/chiron:council strategy "the whole company bet for the year" --depth full
```

The run header shows the seats, the chairman, the depth, and a token estimate before it spends anything: roughly `seats × 1.5k` tokens for quick and `seats × 4k` for full. A five-seat full council is on the order of 20k tokens. That number is exactly why bench size matters.

## Example benches

Line-ups worth copying. Ship a few of these into your global file and adjust the seats to your roster.

```yaml
benches:
  # Money and bets: incentives, leverage, your own execution laws
  money:
    seats: [munger, naval, rayo]
    chairman: neutral
    default_depth: quick

  # Strategy calls: diagnosis before action, then leverage
  strategy:
    seats: [rumelt, munger, naval]
    chairman: neutral
    default_depth: full

  # Deals and negotiations
  deals:
    seats: [voss, munger, rayo]
    chairman: neutral
    default_depth: quick

  # Relationship decisions: polarity lens plus repair lens (authored opposition)
  relationship:
    seats: [deida, terry-real]
    chairman: neutral
    default_depth: full

  # Diagnosis: three routes to the truth from the detectives bench
  detectives:
    seats: [house, sherlock, columbo]
    chairman: neutral
    default_depth: full
```

Why these hold together:

- **money** pairs incentive and misjudgment analysis (Munger) with leverage and judgment (Naval) and your own execution laws (Rayo). Kept at `quick` because most money calls are frequent and want a fast read.
- **strategy** front-loads diagnosis before action (Rumelt), then pressure-tests it on incentives (Munger) and leverage (Naval). Set to `full` because a strategy call is usually expensive enough to earn the deeper pass.
- **relationship** is deliberately two seats that argue: Deida on polarity and Terry Real on relational repair carry an authored disagreement on the record, so the council surfaces a real tension instead of two voices nodding along. This is the case where a bench of two is exactly right.
- **detectives** is the diagnosis bench: House tests it because everybody lies, Sherlock deduces it from the evidence, Columbo disarms it into the open. Three genuinely different routes to one answer, cited to the canon and the episodes. Point it at a bug, a broken metric, or a story that does not add up.

## Sizing a bench

The workable range is **2 to 8 seats**, and the sweet spot is **2 to 5**.

- **1 seat** is not a bench. Chiron refuses it and sends you to `/chiron:ask`. A bench of one is a person.
- **2 to 5 seats** is where a council does its best work: enough perspectives to hit a real disagreement, few enough that every voice earns its tokens and the synthesis stays sharp. `/chiron:consult` caps its own auto-convened councils at 5 for this reason.
- **6 to 8 seats** works but Chiron warns you: more than five gets noisy, the token cost climbs (a seven-seat full run is near 28k tokens), and past a point you are staging decision theater, a crowd assembled to feel thorough rather than to change the answer. If you reach for a big bench, ask whether two focused benches would serve better.
- **More than 8** is refused (error `CH-E4`). Split it into two benches with distinct jobs.

Adding a seat that shares another seat's domain rarely adds signal; it adds a near-duplicate take and a bill. Prefer seats that cover different ground or that carry an authored disagreement with each other. That disagreement is where a council beats a single answer.

## When a bench earns its keep

A council is not free and it is not always right. Reach for one only when at least one of these is true:

- **The call is expensive or irreversible.** Reversibility is the biggest input. A copy tweak you can change next week does not need three advisors. A pricing change, a hire, an entity decision, a relationship move: that is bench territory.
- **It is genuinely cross-domain.** A question that is part strategy, part psychology, part negotiation cannot be served by one seat's lens. That is what a bench is for.
- **It sits on an authored disagreement.** When two installed seats have a cited conflict that bears on your question, putting both in the room surfaces a real argument from the record. That is the signal generated councils cannot fake.

If none of those hold, a single [`/chiron:ask`](./commands.md) is the honest answer, and often `/chiron:consult` will tell you to skip the council entirely. That "you do not need a bench for this" verdict is a feature, not a failure. Do not convene five seats to launder a decision you could make in your sleep.

## Chairing with your `me` seat

If you have distilled yourself with [`/chiron:distill-me`](./distilling.md), you have a private `me` seat holding your mission, values, and the frameworks you actually run on. Put it in a bench like any other seat, and name it as the `chairman` so the synthesis comes back in your own operating voice, weighing the other seats against your real priorities rather than a neutral analyst's.

```yaml
benches:
  # Founder go-no-go calls: your OS plus the investing and strategy camp
  founder-calls:
    seats: [me, munger, naval, rumelt]
    chairman: me
    default_depth: full

  # Should you build it, and will you actually ship it
  ship-or-stall:
    seats: [me, taleb, rayo]
    chairman: me
    default_depth: quick
```

With `chairman: me`, the flow is: the other seats argue from their records in isolation, then your `me` seat reads the room and makes the call the way you would, keeping the dissent visible so you see exactly what you are overruling. It is the closest thing to sitting at the head of your own table.

Your `me` seat stays private. It lives in `~/.claude/chiron/seats/` or a project's `.chiron/seats/`, is gitignored, and is never shipped. A bench that references it is only usable where that seat is installed, so keep `me`-chaired benches in the same scope (global with a global `me`, project with a project `me`). See [Distilling](./distilling.md) for how the `me` seat is built.

## Related

- [Commands](./commands.md) for `/chiron:bench`, `/chiron:council`, `/chiron:ask`, and `/chiron:consult` in full.
- [Concepts](./concepts.md) for seats, modes, and authored disagreements.
- [Distilling](./distilling.md) for building your `me` seat and new seats.
- [SEAT_SPEC.md](../SEAT_SPEC.md) for the seat standard the linter enforces.
