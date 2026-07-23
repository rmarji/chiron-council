<p align="center">
  <img src="assets/chiron-header.png" alt="Chiron: an authored council of real thinkers for Claude Code" width="820">
</p>

<p align="center"><strong>An authored council of real thinkers for Claude Code. Seats, not generated personas.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.2.0-blue" alt="version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/standard-Agent%20Skills-8A2BE2" alt="standard">
  <img src="https://img.shields.io/badge/seats-18-orange" alt="seats">
  <img src="https://img.shields.io/badge/lint-18%2F18%20passing-brightgreen" alt="lint">
</p>

**Most "AI advisor" tools are one model wearing name tags. Chiron is the opposite.**

You make expensive, irreversible calls alone, and a single model just agrees with you. Recent research puts AI sycophancy near 50% more affirming than a human would be, which makes an agreeable chatbot a poor advisor for a decision you cannot take back. Bolting a "board of advisors" onto that rarely helps: it is five voices of one model nodding along, or celebrity labels with nothing behind them.

Chiron is authored the other way. Each **seat** is one mind, built only from what that person actually published, cited claim by claim, and held to it by a linter that fails the build on thin sourcing or any seat that impersonates a living person. Seats carry **authored disagreements** taken from the record, so convening a council surfaces real conflict instead of consensus theater. It is the board you cannot otherwise afford, and it will tell you what you do not want to hear.

## See it work

A council does not average its seats into mush. It makes them argue from the record, then keeps the dissent. Below, three seats take a real distribution call and hit a real authored disagreement:

<p align="center">
  <img src="demo/council-demo.gif" alt="Chiron convening a council on a distribution decision" width="820">
</p>

```
/chiron:council distribution "I built something good but almost no one knows. Keep building, or go tell people?"

▸ Naval (corpus)   confidence 5/5
  Build your luck surface. Specific knowledge plus permissionless
  leverage, code and media, is how luck starts finding you. Ship the
  work as media; it compounds while you sleep. (How to Get Rich, 2018)

▸ Rayo OS   confidence 5/5
  Luck = Doing × Telling. Untold work has a luck surface of zero,
  regardless of quality. Stop building. Go tell. (Ship Gate; luck surface)

▸ Munger Lens   confidence 3/5
  The big money is in the waiting; most activity is a tax dressed as
  diligence. (Poor Charlie's Almanack, 2005)

▸ authored disagreement · Rayo vs Munger
  Telling-now vs patience. Both positions cited from the record.

▸ synthesis (neutral chair)
  Tell the finished thing, loudly, now. Dissent preserved: if it isn't
  truly done, Munger is right and you're hiding in noise.
```

That combination is the point: sourced positions, a conflict pulled from what the authors really argued, and a synthesis that refuses to split the difference. Higher-res recording: [`demo/council-demo.mp4`](demo/council-demo.mp4).

## Install

There are two ways in, depending on how much you want.

**Full experience: the plugin** (the orchestrator, live councils, benches, seat memory). Works in **Claude Code** and **Cowork**, which share the plugin format:

- **Claude Code:** `/plugin marketplace add rmarji/chiron-council` then `/plugin install chiron`
- **Cowork:** download [`chiron.plugin`](https://github.com/rmarji/chiron-council/releases/latest) and accept it in the app

Then run `/chiron:onboard`, or jump straight in:

```
/chiron:consult "take the retainer at 15k/mo or walk?"
/chiron:council relationship "we keep having the same fight about money"
```

**Just the seats, in any agent.** Every seat is a standard Agent Skill, so the [`skills`](https://skills.sh) CLI drops the roster into 70+ harnesses (Claude Code, Cursor, Codex, Gemini CLI, Copilot, Cline, and more):

```bash
npx skills add rmarji/chiron-council                                   # choose seats interactively
npx skills add rmarji/chiron-council --all                            # install the whole roster
npx skills add rmarji/chiron-council -a codex -s munger naval taleb   # Codex (or -a cursor, gemini-cli, ...)
```

Outside the plugin you invoke a seat by talking to it ("what would the Munger corpus say about this?"). The slash commands and live councils need the plugin, in Claude Code or Cowork.

## Documentation

Full guides live in [`docs/`](docs/):

- [Installation](docs/installation.md) - every install path, verifying, updating, uninstalling
- [Quickstart](docs/quickstart.md) - from installed to your first real council in about ten minutes
- [Core concepts](docs/concepts.md) - seats, modes, the router, councils, benches, memory
- [Commands](docs/commands.md) - every command, with examples and when to reach for it
- [Distilling seats](docs/distilling.md) - add an advisor, or put yourself in the room
- [Benches](docs/benches.md) - curate the line-ups you convene as a group
- [The seat standard](docs/the-standard.md) - SEAT_SPEC and the linter that enforces it
- [Portability](docs/portability.md) - run seats in Cursor, Codex, Gemini, and 70+ agents
- [Chiron in Cowork](docs/cowork.md) - the sandbox model and how seats activate there
- [Getting the most out of Chiron](docs/getting-the-most.md) - power patterns and the routing philosophy
- [Troubleshooting](docs/troubleshooting.md) - common fixes and FAQ

## The roster

Eighteen seats ship today. Fifteen make up the founding council: fourteen corpus-mode seats (built from published work, cited, third person, no impersonation) and Rayo, an original-mode operating system.

| Seat | Pressure-tests | Built from (cited) |
|---|---|---|
| **Munger Lens** | inversion, incentives, avoiding stupidity | Poor Charlie's Almanack; The Psychology of Human Misjudgment |
| **Rumelt** (corpus) | strategy: diagnosis before action | Good Strategy Bad Strategy; The Crux |
| **Thiel** (corpus) | contrarian strategy, monopoly | Zero to One; CS183 lecture notes |
| **Paul Graham** (corpus) | startups, founders, growth | paulgraham.com essays; Hackers & Painters |
| **Hormozi** (corpus) | offers, pricing, sales | $100M Offers; $100M Leads |
| **Voss** (corpus) | negotiation, tactical empathy | Never Split the Difference |
| **Cialdini** (corpus) | persuasion, influence | Influence; Pre-Suasion |
| **Naval** (corpus) | leverage, judgment, wealth | The Almanack of Naval Ravikant; How to Get Rich |
| **Taleb** (corpus) | risk, antifragility, uncertainty | The Black Swan; Antifragile; Skin in the Game |
| **Kahneman** (corpus) | decisions, cognitive bias | Thinking, Fast and Slow; Noise |
| **Attia** (corpus) | longevity, health, performance | Outlive; The Drive |
| **Deida** (corpus) | polarity, purpose, relationships | The Way of the Superior Man |
| **Terry Real** (corpus) | relational repair, conflict | Us; The New Rules of Marriage |
| **Marcus Aurelius** (corpus) | stoic temperament, adversity | Meditations |
| **Rayo OS** (original) | execution, shipping, decision-routing | FATE, Ship Gate, MAX THREE (authored) |

Every real-person seat carries 6,000 to 10,000 words of source-attributed reference material and passes the linter. The "Built from" column is the hard part: each claim traces to a page, a talk, or an episode. Add your own with `/chiron:distill`, or put yourself in the room with `/chiron:distill-me`.

Because a seat can be distilled from any mind, real or fictional, three more round out the eighteen: a **detectives bench** for when the problem is not a decision but a mystery. **Sherlock Holmes** deduces it from the evidence. **Dr. House** tests it, because everybody lies. **Columbo** disarms his way to the confession. Three routes to the truth, each cited to the canon and the episodes, each lint-enforced like the rest.

## Why Chiron, not a stock council

The AI-council space is crowded, and almost all of it fails the same few ways. Chiron is built as the answer to each.

- **Authored, not generated.** The persona wave auto-generates a "mind" from any input over a weekend. Chiron seats are hand-authored and curated: quality and trust over quantity and speed.
- **Cited, not vibes.** Every substantive claim points at a source, and `scripts/lint_seat.py` fails the build on any seat that skimps on provenance. The lint is the standard, not a suggestion.
- **Real disagreement, not manufactured.** Competitors fake conflict by assigning opposing archetypes ("you be the contrarian"). Chiron surfaces only conflicts authored from what the people actually argued, both positions cited. If none exist for your topic, the council says so instead of inventing one.
- **It routes itself.** `/chiron:consult` reads your decision and picks the right expert, convenes the right few, or tells you it is not worth a council at all. No hunting through a roster, no summoning a debate for a call you could make in your sleep.
- **Memory.** Seats keep a private log. They remember what they told you, and whether you listened.

## Commands

| Command | Does |
|---|---|
| `/chiron:onboard` | First-run setup: meet the roster, distill yourself, get starter benches |
| `/chiron:consult <q>` | **Auto-routes.** Chiron picks the right expert(s), and decides whether a council is even worth convening |
| `/chiron:ask <seat> <q>` | One authored lens, cited, with its memory of your past calls |
| `/chiron:council <bench> <q>` | Independent takes gathered in isolation, real disagreements surfaced, one synthesis with dissent preserved |
| `/chiron:bench` | Create and edit benches (your curated line-ups) as plain YAML |
| `/chiron:roster` | See who is available, filter by domain |
| `/chiron:distill <desc>` | Distill a new seat: deep research on the subject's corpus, full cited seat, linted |
| `/chiron:distill-me` | Distill **you** into a private seat, and read out your go-to experts |
| `/chiron:lint` | Validate seats against the SEAT_SPEC standard |
| `/chiron:log <seat>` | Review past consults and the decisions you never closed |

You can also just talk to it: "run this by my product bench," "what would Munger say about this."

## Make it yours

`/chiron:onboard` takes you from install to your first real council in a few minutes. It shows the roster, then offers `/chiron:distill-me`, which distills *you* the same way the roster distills its thinkers: it reads what you point it at (your notes, your instruction files, this conversation), interviews you, and writes a private, original-mode `me` seat holding your mission, values, goals, frameworks, and the experts you already reach for. That `me` seat can chair your councils and be argued with, and its read-out of your go-to experts becomes a recommended roster.

Your `me` seat is **private**. It lives in `~/.claude/chiron/seats/` (or a project's `.chiron/seats/`), never in this repo, never committed, never shipped. Your own seats and the bundled roster merge automatically (project shadows global shadows bundled), so a seat you distill is available everywhere you use Chiron.

## Anatomy of a seat

```
skills/munger/
├── SKILL.md              # the mind: priors, heuristics, refusals, voice (< 6k tokens)
├── disagreements.md     # authored conflicts with other seats, positions cited
├── references/          # the depth: complete extraction of the published thinking
│   ├── principles.md    ├── mental-models.md   ├── frameworks.md
│   ├── anti-patterns.md ├── heuristics.md      ├── quotes.md
│   └── sources.md
└── log.md               # append-only consult memory (gitignored)
```

Everything is files. No database, no server, no API keys. The full standard and depth bar live in [SEAT_SPEC.md](SEAT_SPEC.md).

## Portability

A seat is a real, drop-in Agent Skill that auto-activates like any other skill. It follows the [Agent Skills](https://agentskills.io) open standard (standard `name`/`description` frontmatter), plus Chiron's own extras (`x-chiron:`, `disagreements.md`, `references/`) that other harnesses harmlessly ignore. Beyond the `npx skills` installer above, you can copy one by hand into any agent's skills directory:

```bash
# Claude Code          Cursor                Codex CLI            Gemini CLI / generic
~/.claude/skills/      ~/.cursor/skills/     ~/.codex/skills/     ~/.agents/skills/

cp -r skills/munger ~/.claude/skills/munger
```

The slash commands, orchestrator, and live councils are specific to Claude Code. The seats themselves run anywhere.

## The standard is the point

`scripts/lint_seat.py` is stdlib-only Python and runs identically in CI, so the seat standard is enforceable by anyone, not just inside Claude.

```bash
python3 scripts/lint_seat.py --all                  # exit 0 pass / 1 warns / 2 errors
python3 scripts/lint_seat.py skills/munger --explain
python3 scripts/registry.py --json                  # roster index
```

It hard-fails first-person impersonation of anyone living (L1), fewer than three sources (L4), and shallow or missing reference sets (L12). That is what makes a seat a seat and not a name.

## Benches

Global: `~/.claude/chiron/benches.yaml`. Project: `.chiron/benches.yaml` (project shadows global on a name collision). Plain YAML you edit by hand.

```yaml
benches:
  money:
    seats: [munger, naval, rayo]
    chairman: neutral          # or a seat id
    default_depth: quick       # quick | full
```

## On corpus-mode and provenance

Real-person seats speak in the third person about the corpus ("the Munger corpus would flag...") and cite a source per claim. There is no first-person cosplay of anyone living; the linter hard-fails it. This is not only legal hygiene, it is the reason sourced heuristics beat generated vibes. Every real-person seat is an independent study aid based on published works, not affiliated with or endorsed by its subject. See [LEGAL.md](LEGAL.md) for the provenance policy and takedown protocol.

## License

MIT. Frameworks and ideas are paraphrased and cited from published works (ideas are not copyrightable; expression is, so quotes are short attributed excerpts). See [LEGAL.md](LEGAL.md).