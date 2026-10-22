<p align="center">
  <img src="assets/chiron-header.png" alt="Chiron: an authored council of real thinkers for Claude Code" width="820">
</p>

<p align="center"><strong>An authored council of real thinkers for Claude Code. Seats, not generated personas.</strong></p>

<p align="center">
  <a href="https://github.com/rmarji/chiron-council/actions/workflows/ci.yml"><img src="https://github.com/rmarji/chiron-council/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
  <img src="https://img.shields.io/badge/version-0.3.0-blue" alt="version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/standard-Agent%20Skills-8A2BE2" alt="standard">
  <img src="https://img.shields.io/badge/seats-19-orange" alt="seats">
</p>

Chiron is a Claude Code plugin that gives you a council of advisors built from what real thinkers actually published: Munger, Naval, Taleb, Voss, Kahneman, and more, nineteen seats in all. Ask one of them, or convene several and get their independent takes, the disagreements they really have on record, and one recommendation with the dissent kept in.

It is for people who make expensive, hard-to-reverse calls (founders, operators, anyone pricing a deal or choosing a strategy) and want pushback instead of a model that agrees with them. Every seat cites its sources, and a linter fails any seat that is thinly sourced or impersonates a living person. [Why it is built this way](docs/why-chiron.md).

## Quickstart (about a minute)

**You need:** Claude Code, and Python 3.9+ on your `PATH` as `python3` (macOS and most Linux already have it). Nothing to `pip install`, no API keys. macOS and Linux only; Windows is not supported.

In Claude Code:

```
/plugin marketplace add rmarji/chiron-council
/plugin install chiron@compound-club
```

`compound-club` is the marketplace this repo publishes; `chiron` is the plugin. Choose a scope when asked, and allow the `python3` scripts when Claude Code asks (they only read seat and bench files). Then check it loaded:

```
/chiron:roster
```

You should see 19 seats grouped by domain, each with `lint:pass`. Now ask for a real answer:

```
/chiron:consult "take the retainer at 15k/mo or walk?"
/chiron:council relationship "we keep having the same fight about money"
```

`relationship` is one of six example benches that work before you set anything up. When you want Chiron tuned to you, run `/chiron:onboard`: it shows the roster, offers to distill you into a private seat, builds starter benches, and ends on a real consult.

Other ways in: [Cowork and seats-only installs](#other-ways-to-install), and the full [installation guide](docs/installation.md).

## See it work

A council does not average its seats into mush. It makes them argue from the record, then keeps the dissent. Below, three seats take a distribution call and hit a real authored disagreement:

<p align="center">
  <img src="demo/council-demo.gif" alt="Chiron convening a council on a distribution decision" width="820">
</p>

```
/chiron:council money "I built something good but almost no one knows. Keep building, or go tell people?"

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

The recording calls its line-up `distribution`, a custom bench name; the bundled `money` bench seats the same three (Munger, Naval, Rayo), so the command above reproduces it. Higher-res recording: [`demo/council-demo.mp4`](demo/council-demo.mp4).

## The roster

Nineteen seats ship today. Eighteen are corpus-mode: built from published work, cited, in the third person, no impersonation. One, Rayo OS, is original-mode.

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
| **Ferriss** (corpus) | time, leverage, lifestyle design, fear-setting | The 4-Hour Workweek; Tools of Titans; The Tim Ferriss Show |
| **Attia** (corpus) | longevity, health, performance | Outlive; The Drive |
| **Deida** (corpus) | polarity, purpose, relationships | The Way of the Superior Man |
| **Terry Real** (corpus) | relational repair, conflict | Us; The New Rules of Marriage |
| **Marcus Aurelius** (corpus) | stoic temperament, adversity | Meditations |
| **Sherlock Holmes** (corpus) | deduction from evidence | the Conan Doyle stories and novels |
| **Dr. House** (corpus) | diagnosis by testing, because everybody lies | House, M.D. episodes |
| **Columbo** (corpus) | finding the one detail that doesn't fit | Columbo episodes |
| **Rayo OS** (original) | execution, shipping, decision-routing | FATE, Ship Gate, MAX THREE (authored) |

**Rayo OS** is Raed Marji's operating system for deciding and shipping, the author's, packaged as a seat anyone can borrow. It cites his frameworks rather than a published corpus, and it sits in three of the example benches. It is not the reader's operating system; that would be a private `me` seat from `/chiron:distill-me`.

Every real-person seat carries roughly 6,000 to 8,500 words of source-attributed reference material and passes the linter. The three detectives show a seat can be distilled from a fictional canon too, cited to the stories and episodes. Add your own with `/chiron:distill`, or put yourself in the room with `/chiron:distill-me`.

## Commands

| Command | Does |
|---|---|
| `/chiron:onboard` | First-run setup: meet the roster, distill yourself, get starter benches |
| `/chiron:consult <q>` | **Auto-routes.** Chiron picks the right expert(s), and decides whether a council is even worth convening |
| `/chiron:coach <q>` | A guided decision session: frames the real call, consults the right seats as evidence, drives you to one committed, logged decision |
| `/chiron:ask <seat> <q>` | One authored lens, cited, with its memory of your past calls |
| `/chiron:council <bench> <q>` | Independent takes gathered in isolation, real disagreements surfaced, one synthesis with dissent preserved |
| `/chiron:bench` | Create and edit benches (your curated line-ups) as plain YAML |
| `/chiron:roster` | See who is available, filter by domain |
| `/chiron:distill <desc>` | Distill a new seat: deep research on the subject's corpus, full cited seat, linted |
| `/chiron:distill-me` | Distill **you** into a private seat, and read out your go-to experts |
| `/chiron:lint` | Validate seats against the SEAT_SPEC standard |
| `/chiron:log <seat>` | Review past consults and the decisions you never closed |

You can also just talk to it: "run this by my money bench," "what would Munger say about this." Full reference: [docs/commands.md](docs/commands.md).

## Benches

A bench is a named line-up you convene with `/chiron:council <name>`. Six ship as examples in [`benches/examples/benches.yaml`](benches/examples/benches.yaml): `money`, `strategy`, `deals`, `relationship`, `shipping`, and `work-design`. They work by name until you have a benches file of your own.

Your first bench replaces those examples. `/chiron:bench create` writes `.chiron/benches.yaml` in the project (or `~/.chiron/benches.yaml` with `--global`), and once either file exists the bundled examples drop out entirely, including any you did not copy. The create command offers to copy the examples into that file first; take the offer, or copy [`benches/examples/benches.yaml`](benches/examples/benches.yaml) in yourself. To get the examples back later, delete the benches file you created. Project shadows global on a name collision. A benches file left over from an older install at `~/.claude/chiron/benches.yaml` is still read, and the next global write copies it into `~/.chiron/benches.yaml`. Chiron does not write the old path.

```yaml
benches:
  money:
    seats: [munger, naval, rayo]
    chairman: neutral          # or a seat id
    default_depth: quick       # quick | full
```

More in [docs/benches.md](docs/benches.md).

## Make it yours

`/chiron:onboard` takes you from install to your first real council in a few minutes. It shows the roster, then offers `/chiron:distill-me`, which distills *you* the same way the roster distills its thinkers: it reads what you point it at (your notes, your instruction files, this conversation), interviews you, and writes a private, original-mode `me` seat holding your mission, values, goals, frameworks, and the experts you already reach for. That `me` seat can chair your councils and be argued with.

Your `me` seat is **private**. It lives in `~/.chiron/seats/me/` (or a project's `.chiron/seats/me/`), never in this repo, never committed, never shipped. Seats you add with `/chiron:distill` go to `~/.chiron/seats/<id>/` (or a project's `.chiron/seats/<id>/`). Chiron's commands find them through the registry. They do not auto-activate as native Claude skills: that directory is `~/.claude/skills/`, and Claude Code refuses writes under `~/.claude`. `npx skills add` still installs the bundled seats there, because that CLI is not the session's Write tool. The registry also still reads `~/.claude/skills/` and an older `~/.claude/chiron/seats/` if you have them. Project shadows `~/.chiron` shadows those, which shadow the bundled roster, so every seat you add shows up in `/chiron:roster` and can sit on a council.

What a seat tells you is kept separately, at `~/.chiron/logs/<id>/log.md` (or under `$CHIRON_HOME` if you set it). That directory is yours. It is created the first time a seat records a consult, `/chiron:log` reads it back, and a plugin update does not touch it. A log left at `~/.claude/chiron/logs/<id>/log.md` is still read, and the next consult copies it into the new path. In Cowork, where the home directory is not writable, the same logs land in the workspace at `.chiron/logs/`.

## Other ways to install

- **Cowork:** download [`chiron.plugin`](https://github.com/rmarji/chiron-council/releases/latest) and accept it in the app. A release file carries what shipped in that release, so it can lag this branch. See [docs/cowork.md](docs/cowork.md).
- **Just the seats, in any agent.** Every seat is a standard Agent Skill, so the [`skills`](https://skills.sh) CLI (needs Node) can drop seats into other harnesses such as Cursor, Codex, and Gemini CLI:

  ```bash
  npx skills add rmarji/chiron-council                                  # choose seats interactively
  npx skills add rmarji/chiron-council -a codex -s munger naval taleb   # one harness, chosen seats
  ```

  Outside the plugin you invoke a seat by talking to it ("what would the Munger corpus say about this?"). The slash commands and live councils need the plugin. The `chiron` skill in this repo is the plugin's router, not a seat; skip it outside the plugin. More in [docs/portability.md](docs/portability.md).

## Documentation

Full guides live in [`docs/`](docs/index.md):

- [Installation](docs/installation.md) - every install path, verifying, updating, uninstalling
- [Quickstart](docs/quickstart.md) - from installed to your first real council
- [Core concepts](docs/concepts.md) - seats, modes, the router, councils, benches, memory
- [Commands](docs/commands.md) - every command, with examples and when to reach for it
- [Distilling seats](docs/distilling.md) - add an advisor, or put yourself in the room
- [Benches](docs/benches.md) - curate the line-ups you convene as a group
- [The seat standard](docs/the-standard.md) - SEAT_SPEC, the anatomy of a seat, and the linter that enforces it
- [Portability](docs/portability.md) - run seats in Cursor, Codex, Gemini, and other agents
- [Chiron in Cowork](docs/cowork.md) - the sandbox model and how seats activate there
- [Getting the most out of Chiron](docs/getting-the-most.md) - power patterns and the routing philosophy
- [Why Chiron](docs/why-chiron.md) - authored vs generated, the seat standard, and corpus mode
- [Troubleshooting](docs/troubleshooting.md) - common fixes and FAQ

Contributing a seat or a fix: [CONTRIBUTING.md](CONTRIBUTING.md). Changes by version: [CHANGELOG.md](CHANGELOG.md).

## License

MIT. Frameworks and ideas are paraphrased and cited from published works (ideas are not copyrightable; expression is, so quotes are short attributed excerpts). Every real-person seat is an independent study aid, not affiliated with or endorsed by its subject. See [LEGAL.md](LEGAL.md).
