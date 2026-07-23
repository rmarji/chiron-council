# Commands reference

Chiron adds ten slash commands under the `/chiron:` namespace. This page documents each one: its syntax, what it does, a real example, and when to reach for it. If you only remember two, remember `/chiron:consult` (let Chiron route the decision) and `/chiron:ask` (go straight to one seat). Everything below assumes the plugin is installed in Claude Code or Cowork. See [installation](./installation.md) if it is not.

You never have to memorize the exact grammar. Every command has a plain-language equivalent: "run this by my money bench," "what would the Munger corpus say about this," "who do I have for negotiation." Chiron reads that and reaches for the right command. The slash forms are here so you know exactly what happens when it does.

## Quick reference

| Command | What it does | Reach for it when |
|---|---|---|
| [`/chiron:onboard`](#chirononboard) | First-run setup: meet the roster, distill yourself, get starter benches | You just installed and want a guided start |
| [`/chiron:consult <q>`](#chironconsult) | Auto-routes: picks the right seat(s), or decides no council is warranted | You have a decision and do not want to pick who weighs in. The default. |
| [`/chiron:ask <seat> <q>`](#chironask) | One authored lens, cited, with its memory of your past calls | You already know which mind you want |
| [`/chiron:council <bench> <q>`](#chironcouncil) | Independent takes in isolation, authored conflicts surfaced, one synthesis with dissent kept | The call is expensive, irreversible, or cross-domain |
| [`/chiron:bench`](#chironbench) | Create, list, or remove benches (curated seat line-ups) as plain YAML | You keep convening the same group |
| [`/chiron:roster`](#chironroster) | List installed seats, filter by domain | You want to see who is available |
| [`/chiron:distill <desc>`](#chirondistill) | Distill a new seat from a thinker's published work, cited and linted | You want an advisor the box does not ship |
| [`/chiron:distill-me`](#chirondistill-me) | Distill you into a private `me` seat and read out your go-to experts | You want your own operating system in the room |
| [`/chiron:lint`](#chironlint) | Validate seats against the SEAT_SPEC standard | You authored or edited a seat |
| [`/chiron:log <seat>`](#chironlog) | Review a seat's consult memory and open decisions | You want to see what a seat told you and what you decided |

---

## /chiron:onboard

```
/chiron:onboard
```

First-run setup. It orients you in one paragraph (Chiron is a council of authored, cited seats, not generated personas), shows the installed roster grouped by domain, then offers to distill you into a private `me` seat. If you would rather stay fast, it runs a five-question mini version inline (what you are working on, the decision you are chewing on, the thinkers you already reach for, your non-negotiables, and how you want to be talked to). From your answers it recommends seats, builds two or three starter benches, and ends by running your actual decision through `/chiron:consult` so onboarding produces a real answer, not a tour.

**Example**

```
/chiron:onboard

Chiron is a council of authored advisors. Each seat is one mind distilled
from real published work, cited per claim, not a generated persona. You can
ask one seat or convene several, and Chiron can pick the right ones for you.

Here is what is installed:

  investing     munger        Munger Lens          [investing, decision-making, ...]
  wealth        naval         Naval (corpus)       [wealth, leverage, judgment, ...]
  strategy      rumelt        Rumelt (corpus)      [strategy, diagnosis, ...]
  ...

Want me to distill YOU into a private seat so your own frameworks can sit on
the council? (/chiron:distill-me) Or I can run a quick five-question version
right here. Which do you prefer?
```

**Reach for it when** you have just installed Chiron. You only need it once. After that, `/chiron:consult`, `/chiron:ask`, and `/chiron:distill` are the daily tools. Full walkthrough in [quickstart](./quickstart.md).

---

## /chiron:consult

```
/chiron:consult <your question or situation>
```

The orchestrator, and the flagship. You do not name a seat. Chiron reads your decision, picks the right expert or experts, and decides whether a council is even worth convening. A council that convenes when it should not is decision theater and a token tax, so the most valuable routing verdict is often "you do not need the council for this."

It reads your decision on three axes: **stakes** (cheap and reversible, or expensive and irreversible), **breadth** (one domain or several), and **type** (a judgment call, or something factual and trivial that no seat should touch). Then it picks the cheapest verdict that fully serves the decision:

- **SKIP** answers directly or says plainly that no seat has standing, when the question is factual, technical, or outside every seat's competence.
- **ASK** routes to one seat when there is a clear domain owner and the stakes are low to moderate.
- **COUNCIL** convenes two to five seats only when the call is expensive or irreversible, genuinely cross-domain, or sits on an authored disagreement between installed seats.
- **CLARIFY** asks one sharp question first when it genuinely cannot read the stakes, then routes.

It shows its work before executing, so you can override with "just ask Naval" or "make it a full council."

**Example**

```
/chiron:consult "take the retainer at 15k/mo or walk?"

Routing: this is an expensive, hard-to-reverse commitment that touches
pricing, leverage, and your own capacity. Convening a council of three:
Hormozi (offer and price), Naval (leverage and opportunity cost), and Rayo
(will you actually deliver it). Hormozi and Naval carry an authored
disagreement on trading time for money that bears on this. ~6k tokens.
Proceeding.

[council output follows]
```

A contrasting route:

```
/chiron:consult "is it 'affect' or 'effect' in this sentence?"

SKIP. This is a factual language question, not a judgment call. No seat has
standing here. It is "effect" (the noun). No council needed.
```

**Reach for it when** you have a decision and do not want to think about who should weigh in. This is the default entry point. When you already know the mind you want, skip straight to `/chiron:ask`. More on how routing thinks in [concepts](./concepts.md).

---

## /chiron:ask

```
/chiron:ask <seat-or-bench> <question>
```

One seat, one question, one authored lens, with that seat's memory of your past calls. The first token is a seat id (or a bench name), the rest is the question. Seat ids win ties, so `/chiron:ask deals ...` resolves the `deals` bench only if no seat is named `deals`. If the first token resolves to a bench, this becomes a council at the bench's default depth.

The seat responds in its voice contract. Corpus-mode seats speak in the third person and cite a source for each substantive claim ("the Munger corpus would flag..."), never in first person. The shape is fixed: position first (three to six lines), then reasoning, a confidence of 1 to 5, and what would change the seat's mind. One recommendation, not a menu. If your question hits one of the seat's `## Refusals`, it declines that part and redirects rather than opining outside its competence.

After answering, it appends a one-line entry to the seat's `log.md` and asks once whether to record your decision. That is how the seat remembers what it told you and whether you listened.

**Example**

```
/chiron:ask voss "counteroffer came in 20% under. how do I respond?"

Position: do not counter the number yet. Name the gap out loud and make them
solve it. "It sounds like 20% under is the most you can do right now." Then
silence.

Reasoning: the Voss corpus treats a calibrated "how" question and a labeled
obstacle as the move that gets the other side to argue against their own
lowball. A fast counter concedes the frame. (Never Split the Difference,
"Bend Their Reality"; "Calibrated Questions")

Applied heuristics: mirror-then-label; never split the difference.
Confidence: 4/5.
What would change it: if this is a take-it-or-leave-it with a hard deadline,
tactical empathy gives way to a clean walk-away number.

Record your decision? (updates the seat's log)
```

**Errors you may hit.** An unknown id (**CH-E1**) returns the three closest matches and points you at `/chiron:roster`. A seat that fails lint (**CH-E3**) will not load: Chiron prints the lint errors and stops. A lint `warn` still loads, with a one-line note.

**Reach for it when** you already know which mind you want. If you are not sure, use `/chiron:consult` and let it pick.

---

## /chiron:council

```
/chiron:council <bench-or-seat-list> <question> [--depth quick|full]
```

Convene a bench and get a real debate, not consensus theater. The first token is a bench name or an inline comma-separated seat list (`munger,naval,rumelt`), the rest is the question. `--depth` overrides the bench's `default_depth`; the default is `quick`.

This is a four-phase state machine, and the phases are the point:

1. **TAKES.** Each seat is prompted in isolation, one subagent per seat in parallel. A seat's context holds only its own `SKILL.md`, its last ten log entries, and your question. It does not see the other seats, their takes, or the bench composition. Independence is structural, not simulated. If subagents are unavailable in your harness (**CH-E5**), takes are gathered sequentially and the output says so.
2. **CONFLICT.** Chiron reads every participating seat's `disagreements.md` and surfaces only entries where both counterparts are in the room and the topic matches your question, quoting each with its citations. If nothing matches (**CH-E6**), it says "No authored conflicts on record for this topic." It never invents a disagreement. Generated conflict is the exact failure mode Chiron exists to kill.
3. **SYNTHESIS.** One chairman (a named seat or a neutral analyst) delivers one recommendation, the dissent preserved and named, what you lose by taking the pick, a confidence, and what would change it.
4. **RECORD.** One entry is appended to each participating seat's log, and you are asked once whether to record your decision.

At `quick` depth it gathers takes and gives a micro-synthesis (recommendation, one line of preserved dissent, confidence). At `full` depth it runs the whole conflict and synthesis machinery.

**Example**

```
/chiron:council relationship "we keep having the same fight about money"

Convening: deida, terry-real · chairman neutral · depth full · ~8k tokens

Deida (corpus)   confidence 3/5
  The recurring fight is rarely about money; it is about a collapse of
  polarity. Stop negotiating the budget and restore the charge. (The Way of
  the Superior Man, "Purpose")

Terry Real (corpus)   confidence 4/5
  Same fight, every time, means you are both in adaptive child mode. Name the
  pattern, not the numbers, and repair from your wise adult. (Us; The New
  Rules of Marriage)

authored disagreement · Deida vs Terry Real
  Restore polarity vs do the relational repair work. Both cited from the
  record.

Synthesis (neutral chair)
  Run the repair first: the money fight is the surface. Dissent preserved:
  Deida would say repair without restored polarity just makes you good
  roommates. Confidence 4/5. What changes it: if there is a real budget
  crisis underneath, this needs a numbers conversation too.

Record your decision?
```

**Guards.** A bench that names a missing seat (**CH-E2**) is flagged and you are offered the remainder. More than eight seats (**CH-E4**) is refused for token and quality reasons. Any seat failing lint is dropped with a note. Fewer than two seats resolved sends you to `/chiron:ask` instead.

**Reach for it when** the call is expensive, irreversible, or straddles domains, and you want the tension in the open. For a single clean question, `/chiron:ask` is cheaper. To let Chiron decide whether a council is warranted at all, use `/chiron:consult`. Deeper mechanics in [benches](./benches.md).

---

## /chiron:bench

```
/chiron:bench create <name> <seat> <seat> ... [--global] [--chairman <id>] [--depth quick|full]
/chiron:bench list
/chiron:bench remove <name>
```

Manage benches, which are curated seat line-ups you convene by name. Benches are plain YAML, and the files are the API: you can edit them by hand and Chiron reads the same file. They live in two places:

- **Project:** `.chiron/benches.yaml` (the default write target inside a project)
- **Global:** `~/.claude/chiron/benches.yaml` (write here with `--global`, or when not in a project)

On a name collision, the project bench shadows the global one. The file shape:

```yaml
benches:
  product:
    seats: [munger, naval, rayo]
    chairman: neutral        # a seat id, or "neutral"
    default_depth: quick     # quick | full
```

**create** validates the name against `^[a-z0-9-]{2,32}$`, validates every seat id against the registry (an unknown id is not written; you get fuzzy matches instead), and requires two to eight seats. One seat is refused ("use /chiron:ask, a bench of one is a person"). Six or more seats is allowed but warns about token cost and decision theater. If the same name exists in the other scope (**CH-E7**), it creates anyway and tells you which one now shadows which.

**list** reads both files and renders a table of name, seats, chairman, depth, and source, marking shadowed globals and flagging any bench that references an uninstalled seat.

**remove** deletes the entry from the scope where it is defined (asking which, if it exists in both) and shows the diff. It never touches seat folders. Removing a bench never deletes seats.

**Example**

```
/chiron:bench create money munger naval rayo

Wrote to ~/.claude/chiron/benches.yaml:

  money:
    seats: [munger, naval, rayo]
    chairman: neutral
    default_depth: quick

Convene it with: /chiron:council money "<your question>"
```

**Reach for it when** you keep convening the same group. Name it once, then call it by name. You can also just say "make me a bench for pricing decisions with Hormozi, Cialdini, and Voss." Chiron ships a set of starter benches you can copy from `benches/examples/benches.yaml`.

---

## /chiron:roster

```
/chiron:roster [--domain <tag>]
```

List every installed seat: id, display name, mode, domains, and lint status, grouped by primary domain. It merges seats from all scopes (the bundled roster, your global seats, your project seats, and your private `me` seat), so it shows exactly who is available to ask or bench right now. Pass `--domain <tag>` to filter to one area.

**Example**

```
/chiron:roster --domain strategy

strategy:
  rumelt         Rumelt (corpus)     corpus   lint:pass  [strategy, diagnosis, competitive-advantage]
  thiel          Thiel (corpus)      corpus   lint:pass  [strategy, startups, contrarian-thinking, monopoly]

Ask one: /chiron:ask rumelt "<question>"
Bench them: /chiron:bench create strategy rumelt thiel munger
```

If a seat shows `warn`, you get a one-line note. If it shows `fail`, it is marked unloadable and you are pointed at `/chiron:lint <id> --explain`. If no seat directory is found at all (exit code 2), it tells you to run `/chiron:distill` or install a pack.

**Reach for it when** you want to see who is in the room, check a seat's exact id before asking, or confirm a seat you distilled actually installed. Under the hood it runs `scripts/registry.py`; you can run that directly with `--json` to post-process the roster.

---

## /chiron:distill

```
/chiron:distill <one-line description of the advisor you want to distill>
```

Distill a new seat from a thinker's published work. You do not hire a persona; you extract a mind from what it actually published. The flow interviews you briefly (subject, living status, mode, domains, any anchor sources you already know), runs deep research over the subject's corpus with web search, and writes the full seat: `SKILL.md` plus all seven reference files at the [SEAT_SPEC](../SEAT_SPEC.md) depth bar, every claim cited. Then it lints the seat and fixes findings until it passes. Depth is baked into the standard, not an upsell: a seat that ships with stub references is a name, not a seat.

It delivers a real, auto-activating skill, so there is no manual move:

- In **Claude Code**, it writes `~/.claude/skills/<id>/` (or `<project>/.claude/skills/<id>/` if you want it project-scoped). The seat auto-activates next turn and every council finds it.
- In **Cowork** (which cannot write to `~/.claude`), it writes `<project>/.chiron/seats/<id>/` in the open workspace, or emits a one-advisor `.plugin` into `outputs/` for you to accept in-app. See [cowork](./cowork.md).

**Hard rule (CH-E8).** It will not build a first-person persona of a living, unlicensed subject. It explains the legal reason in one paragraph and offers corpus mode (third person, cited) or an original-mode archetype alias ("The Offer Architect" instead of the person) instead. This is non-negotiable; see [LEGAL.md](../LEGAL.md).

**Example**

```
/chiron:distill "a design systems expert, someone like Brad Frost"

Quick check before I research:
  Subject: Brad Frost (Atomic Design), living, so corpus mode (third person,
    cited). Good?
  Domains: [design-systems, frontend, ux], adjust?
  Anchor sources you already have in mind, or should I discover them?

[on confirm: multi-round deep research, then authoring, then]

Linted skills/brad-frost: PASS
  mode corpus · domains [design-systems, frontend, ux] · 8 sources
  references: principles 1,180w · frameworks 1,340w · ... (7 files)
Use it: /chiron:ask brad-frost "how granular should our tokens be?"
```

**Reach for it when** you want an advisor Chiron does not ship. Full authoring guide in [distilling](./distilling.md) and [the standard](./the-standard.md).

---

## /chiron:distill-me

```
/chiron:distill-me [optional: point at notes, a vault, or a folder to read]
```

Distill you the way `/chiron:distill` distills a thinker: a structured breakdown of how you actually operate, written as an original-mode seat with id `me`. Your own operating system can then sit on the council, chair your benches, and be argued with. It also reads out your go-to experts and turns them into a recommended roster.

It is consent-gated. It asks which sources to draw on (this conversation, your instruction and memory files like `~/.claude/CLAUDE.md`, anything you point it at such as an Obsidian vault or a "how I work" doc) and names each source out loud before reading it. It interviews you to fill the gaps (mission, values and non-negotiables, goals, the frameworks you use by name, your anti-patterns, who you channel when stuck, and how you want to be spoken to). Then it writes the full seat and lints it until it passes.

**Your `me` seat is private.** It writes to `~/.claude/chiron/seats/me/` (global) or `<project>/.chiron/seats/me/` (project), never into the Chiron repo, never committed, never shipped. If written into a project it offers to add `.chiron/seats/` to that project's `.gitignore`.

**Example**

```
/chiron:distill-me

Before I read anything: your "me" seat holds your mission, values, and goals.
It is private and local, never committed, never shipped. I will name each
source before I read it.

May I read this conversation, your ~/.claude/CLAUDE.md, and the notes folder
you mentioned? (yes / pick a subset / interview only)

[after gather + interview]

Wrote ~/.claude/chiron/seats/me/  ·  linted: PASS
  display_name: "Rayo (you)" · original · domains [execution, decisions, ...]
Your go-to experts, matched to the roster:
  Munger → installed   Naval → installed   Kapil Gupta → not installed (distill?)
Proposed benches: money (munger, naval, me · chaired by you), ...
Put it to work: /chiron:consult "<a real decision you are facing>"
```

**Reach for it when** you want your own frameworks in the room and better routing (a `me` seat sharpens what `/chiron:consult` recommends). It is offered as part of `/chiron:onboard`.

---

## /chiron:lint

```
/chiron:lint [seat-id | --all] [--strict] [--explain]
```

Validate seats against the [SEAT_SPEC](../SEAT_SPEC.md) standard. The linter is stdlib-only Python and CI runs the same file, so the standard is enforceable by anyone, not just inside Claude. Exit codes are `0` pass, `1` warnings only, and `2` errors (a seat with errors will not load).

Each finding shows the rule id, what it means (`--explain` prints the rule descriptions), and the concrete fix. The load-blocking rules are the ones that make a seat a seat and not a name:

- **L1** persona mode on a living, unlicensed subject. Hard fail. Switch to corpus mode or adopt the archetype alias.
- **L4** fewer than three provenance sources. Add citations drawn from `references/sources.md`.
- **L5** missing or thin required sections (Priors, Heuristics, Refusals, Voice).
- **L7** first-person leakage in a corpus seat. Rewrite to third-person analytic, or put subject speech in quotation marks. This is a warning at standard level and an error under `--strict`.
- **L12** missing reference files. The seat shipped without its depth. Author the missing files at the SEAT_SPEC depth bar.

If you ask it to fix findings, it fixes the mechanical ones (frontmatter, naming, voice rewrites) directly and re-runs until clean. Content gaps (L5, L12) need real authoring, which it offers to do at the depth bar, not with filler.

**Example: the slash command wraps the same script Chiron and CI run.**

```bash
# Lint every bundled seat
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lint_seat.py --all --seats-dir ${CLAUDE_PLUGIN_ROOT}/skills

# One seat, strict, with rule explanations
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lint_seat.py ${CLAUDE_PLUGIN_ROOT}/skills/munger --level strict --explain

# JSON output for tooling
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lint_seat.py --all --format json --seats-dir skills
```

Note the raw script takes `--level strict` where the slash command takes `--strict`, and `--format json` for machine-readable output.

**Reach for it when** you authored or edited a seat, before you rely on it. All eighteen shipped seats pass. Full rule table in [the standard](./the-standard.md) and [SEAT_SPEC.md](../SEAT_SPEC.md) section 7.

---

## /chiron:log

```
/chiron:log <seat-id> [--open-loops]
```

Review a seat's consult memory. Each seat keeps an append-only `log.md` of what it told you and what you decided, and a summoned seat reads its last ten entries so it remembers the thread. This command reads that ledger. Reading never mutates it.

The default view renders entries newest first: date, source (`ask` or `council:<bench>`), the question, a one-line take, and the decision. If no log exists yet, it says so and stops.

**`--open-loops`** filters to entries whose decision is still `open loop` and prominently flags any older than fourteen days. These are calls you consulted on and never closed. If you then supply a decision for one, it updates only that entry's decision line. That is the single permitted mutation; it never rewrites your takes or questions.

**Example**

```
/chiron:log munger --open-loops

Open loops with Munger Lens:

  2026-06-12 · council:money   (41 days, needs closing)
    Q: Move the emergency fund into the index position?
    Decision: open loop

  2026-07-19 · ask
    Q: Kill the underperforming product line, or give it another quarter?
    Decision: open loop

Close a loop by telling me the decision, and I'll record it.
```

If a log passes one hundred entries, it offers once to compress the oldest into a dated `## Archive digest` block, keeping the newest fifty intact. It only does so if you say yes.

**Reach for it when** you want to see the history with a seat, or when you have a habit of consulting and never deciding. The open-loops view is a quiet accountability check.

---

## The natural-language path

You do not have to type slash commands. Chiron listens for intent in ordinary conversation and reaches for the matching command:

- "what would the Munger corpus say about this?" routes to `/chiron:ask munger`
- "run this by my product bench" convenes the `product` bench via `/chiron:council`
- "help me decide whether to take the retainer" behaves like `/chiron:consult`
- "who do I have for negotiation?" is `/chiron:roster --domain negotiation`
- "add Brad Frost as an advisor" starts `/chiron:distill`

When you are clearly mid-decision but have not asked for anything, Chiron offers to route ("want me to run this by the right seats?") rather than hijacking the turn. Fully autonomous, unprompted interjection is deliberately out of scope: you stay in control of when the council convenes.

Outside the plugin (a seat installed on its own into another agent via the `skills` CLI), the slash commands are not present, but the seats still auto-activate, so you invoke them by talking to them. The orchestrator, live councils, benches, and per-seat memory need the plugin, in Claude Code or Cowork. See [portability](./portability.md).

---

## See also

- [Quickstart](./quickstart.md) for your first ten minutes
- [Concepts](./concepts.md) for seats, benches, modes, and routing
- [Benches](./benches.md) for how councils manufacture independence and surface authored conflict
- [Distilling](./distilling.md) and [the standard](./the-standard.md) for authoring your own seats
- [Getting the most](./getting-the-most.md) for daily workflows
- [Troubleshooting](./troubleshooting.md) for the `CH-E*` error codes in context
