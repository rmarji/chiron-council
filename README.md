# Chiron

**Authored advisors as lint-enforced files.**

A council is only as good as who's sitting in it. Most "AI advisor" tools ship meetings of generated personas — ask for a board meeting, get five flavors of the same model agreeing with you. Chiron ships **authored people**: one seat per mind, distilled from what that person actually published, with sources cited, disagreements between seats authored from the record, and a linter that enforces all of it. Councils are a feature powered by the seats — not the other way around.

## What you get

- **7 founding seats** — deep, citation-backed distillations: Munger Lens (investing, decision-making), Rumelt (strategy), Voss (negotiation), Naval (wealth, leverage), Deida (polarity, purpose), Terry Real (relational repair), and Rayo OS (execution, shipping).
- **`/chiron:ask`** — one seat, one question, one authored lens. Seats keep a per-seat memory log: they remember what they told you and whether you listened.
- **`/chiron:council`** — independent takes gathered in isolation, real authored disagreements surfaced from the files (never generated conflict), one synthesis that preserves dissent instead of averaging it.
- **Benches** — your curated line-ups ("product", "pricing", "relationships") as plain YAML you can edit by hand.
- **`/chiron:hire`** — add a new seat. Deep research is baked in: the hire flow researches the subject's published corpus and writes the full seat, every claim cited, then lints it.
- **`SEAT_SPEC.md`** — the open seat standard, mechanically enforced by `scripts/lint_seat.py` (stdlib-only Python, runs identically in CI).

## Install (Claude Code)

```
/plugin marketplace add <this-repo>
/plugin install chiron
```

Then:

```
/chiron:roster                                   # see who's available
/chiron:bench create money munger naval rayo     # build a bench
/chiron:ask munger "take the retainer at 15k/mo or walk?"
/chiron:council money "concentrate or diversify a 12-month runway?"
/chiron:log munger --open-loops                  # decisions you never closed
```

## Install (other harnesses)

Seats follow the [Agent Skills](https://agentskills.io) standard: standard `name`/`description` frontmatter plus Chiron extensions under `x-chiron:` that other harnesses safely ignore. Copy any `seats/<id>/` folder into your agent's skills directory and it loads as a plain skill:

```bash
# Codex CLI            Cursor                  Gemini CLI / generic
~/.codex/skills/       ~/.cursor/skills/       ~/.agents/skills/
```

Commands (`/chiron:*`) and councils are Claude Code-specific; the seats themselves are portable.

## Anatomy of a seat

```
seats/munger/
├── SEAT.md              # the mind: priors, heuristics, refusals, voice (< 6k tokens)
├── disagreements.md     # authored conflicts with other seats, positions cited
├── references/          # the depth: complete extraction of the published thinking
│   ├── principles.md    ├── mental-models.md   ├── frameworks.md
│   ├── anti-patterns.md ├── heuristics.md      ├── quotes.md
│   └── sources.md
└── log.md               # append-only consult memory (gitignored)
```

Everything is files. No database, no server, no API keys. Read [SEAT_SPEC.md](SEAT_SPEC.md) for the full standard and depth bar.

## Why corpus-mode, not impersonation

Real-person seats speak in the third person about the corpus ("the Munger corpus would flag...") and cite a source per claim. No first-person cosplay of anyone living — the linter hard-fails it (rule L1). This isn't just legal hygiene ([LEGAL.md](LEGAL.md)): sourced heuristics beat vibes. Every real-person seat is an independent study aid based on published works, not affiliated with or endorsed by its subject.

## Lint

```bash
python3 scripts/lint_seat.py --all                  # exit 0 pass / 1 warns / 2 errors
python3 scripts/lint_seat.py seats/munger --explain
python3 scripts/lint_seat.py --all --format json --level strict
python3 scripts/registry.py --json                  # roster index
```

## Benches

Global: `~/.claude/chiron/benches.yaml` · Project: `.chiron/benches.yaml` (project shadows global on name collision).

```yaml
benches:
  money:
    seats: [munger, naval, rayo]
    chairman: rayo          # or: neutral
    default_depth: quick    # quick | full
```

## Notes

- If you used the `llm-council` skill: `/chiron:council` supersedes it — authored disagreements instead of generated debate. Deprecate the old skill to avoid running two council systems.
- Seat logs (`log.md`) contain **your decisions**; they are gitignored by default. Opt in to committing them if you want the history versioned.

## License

MIT. Seat content: frameworks and ideas are paraphrased and cited from published works (ideas are not copyrightable; expression is — quotes are short attributed excerpts). See [LEGAL.md](LEGAL.md) for the provenance policy and takedown protocol.
