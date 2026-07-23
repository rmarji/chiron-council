# The seat standard (SEAT_SPEC and the linter)

This page is about what makes a seat a seat, and how that is enforced mechanically. You get the anatomy of a seat (the mind in `SKILL.md`, the depth in `references/`, the authored disagreements), the `x-chiron` marker that flags a skill as a seat, every rule the linter checks, and how to write a passing seat by hand. The full normative spec is [`../SEAT_SPEC.md`](../SEAT_SPEC.md); the provenance policy the legal rules come from is [`../LEGAL.md`](../LEGAL.md).

## What a seat is

A seat is an authored mind: one advisor, distilled from a real person's published work, cited per claim, and written to a file format any Agent Skills-compatible harness can load. A seat is a native Agent Skill. It lives at `skills/<id>/SKILL.md` and Claude auto-activates it like any other skill.

What makes it a *seat* and not just a skill is that it passes this standard: cited provenance, explicit refusals, an authored voice, and a full reference set. The `x-chiron` frontmatter block is the marker that flags a skill as a seat. Discovery keys on that marker, so a seat can sit in a shared skills directory next to unrelated skills and the tooling still picks it out (see [The registry](#the-registry-and-x-chiron-discovery) below).

Seats are the unit of value. Councils, benches, and every other feature in the plugin are powered by seats. For how those features use seats at runtime, see [concepts](./concepts.md) and [commands](./commands.md).

## Anatomy of a seat

```
skills/<id>/
├── SKILL.md              # the mind: frontmatter contract + core sections (< 6k tokens)
├── disagreements.md      # authored conflicts with other seats, positions cited
├── references/           # the depth: complete extraction of the subject's thinking
│   ├── principles.md
│   ├── mental-models.md
│   ├── frameworks.md
│   ├── anti-patterns.md
│   ├── heuristics.md
│   ├── quotes.md
│   └── sources.md
└── log.md                # append-only consult memory (created on first use, gitignored)
```

The load contract is progressive disclosure. When a seat is summoned it loads the `SKILL.md` frontmatter, the core sections, and its last 10 `log.md` entries. The `references/` files load on demand. That is why `SKILL.md` must stay under roughly 6k tokens (lint L6) and why the depth lives in `references/`. Real-person seats carry 6,000 to 10,000 words of source-attributed reference material split across those seven files.

## The mind: SKILL.md

### Frontmatter

Standard Agent Skills keys come first, so a non-Claude harness loads the seat as a plain skill. Chiron's extensions live under `x-chiron:`, which those harnesses ignore. Here is the actual frontmatter of the shipped `munger` seat, trimmed:

```yaml
---
name: munger                      # id: ^[a-z0-9-]{2,32}$, unique, matches folder name
description: >                    # triggering description, same rules as any skill
  Applies the reasoning, mental models, and temperament of Charlie Munger...
x-chiron:
  display_name: Munger Lens       # human name; carries a mode suffix for real people
  mode: corpus                    # corpus | persona | original
  domains: [investing, decision-making, incentives, psychology]   # 1 to 6 filter tags
  alias: The Inversion Lens       # archetype fallback name (required for living subjects)
  provenance:                     # required when mode is not original
    subject: Charlie Munger
    living: false
    license: none                 # none | granted | n/a
    sources:                      # 3 to 50 citations; primary sources first
      - "Poor Charlie's Almanack, ed. Peter D. Kaufman (2005)"
      - "The Psychology of Human Misjudgment (Harvard Law School, 1995)"
      - "A Lesson on Elementary, Worldly Wisdom (USC Marshall, 1994)"
---
```

The linter reads every one of these fields. `name` must match `^[a-z0-9-]{2,32}$` and equal the folder name. `description` is required. The `x-chiron` block is required, along with `display_name`, `mode`, and a `domains` list of 1 to 6 tags. When `mode` is not `original`, a `provenance` block is required with `subject`, a boolean `living`, a `license` of `none`, `granted`, or `n/a`, and a `sources` list of 3 to 50 citations. Missing or malformed fields fail as L2.

### Modes

- **corpus**: frameworks and heuristics from the subject's published work, cited, spoken about in the third person ("the Munger corpus would flag..."). This is the default and the only mode that ships for real people.
- **persona**: first-person voice emulation. Never a default. Forbidden for a living subject without a granted license (lint L1, hard fail).
- **original**: an invented or self-authored advisor, with no provenance constraints. The bundled `rayo` seat is original mode, and so is the private `me` seat you write with [`/chiron:distill-me`](./distilling.md).

### Naming rules

For real-person seats, `display_name` carries a mode suffix ("Munger Lens", "Voss (corpus)") so nobody mistakes a study aid for the person. The linter warns (L10) if the subject's surname appears in `display_name` without a suffix like `Lens`, `corpus`, or `study aid`. Every living-subject seat also defines an `alias`, an archetype name like "The Offer Architect", so a takedown request is a rename and not a rebuild (see [`../LEGAL.md`](../LEGAL.md) rule M6).

### Required sections

The `SKILL.md` body must contain these four `##` sections. Headings may carry suffixes, so "## Heuristics and rules of thumb" satisfies "Heuristics". This is lint rule L5.

| Section | Minimum | The bar |
|---|---|---|
| `## Priors` | 5 bullet entries | What the seat believes before hearing your question. Each specific enough to disagree with. "Is smart about investing" fails; "Invert, always invert: state how this decision fails before how it succeeds" passes. |
| `## Heuristics` | 5 bullet entries | Operational decision rules in IF/THEN shape. "Think long-term" fails; "IF the opportunity requires being clever rather than avoiding stupidity THEN pass" passes. L8 warns on entries with no operational shape. |
| `## Refusals` | 2 bullet entries | What this seat declines to opine on, and where it redirects. Refusals are what make a seat a mind instead of a horoscope. |
| `## Voice` | present | The register contract. In corpus mode: third-person analytic, a source per claim, never "I, Charlie". |

Founding seats also carry richer narrative sections (Core principles, how the subject reasons, worked examples, anti-patterns). Keep those, they are the connective tissue, but the four sections above are the contract. Every real-person seat ends with the disclaimer block ([`../LEGAL.md`](../LEGAL.md) rule M4):

> *Independent study aid based on published works. Not affiliated with or endorsed by {subject}.*

## The depth: references/

References are not summaries. Each file is the complete extraction of one dimension of the subject's thinking, the standard a serious student would accept as "this covers what they actually said". Every claim is attributed to a named source: a book plus chapter, a talk plus year, a podcast plus episode. Rough calibration is 600 to 1,500 words per file. Padding to hit a word count is a defect; missing a framework the subject is known for is a bigger one.

| File | Contains |
|---|---|
| `principles.md` | The full catalog of core beliefs, each with rationale and source. |
| `mental-models.md` | Every named model or concept the subject uses, defined, with origin and when it applies. |
| `frameworks.md` | Every named framework with when-to-use, concrete steps, and source. |
| `anti-patterns.md` | Everything the subject warns against, with their reasoning and the failure it produces. |
| `heuristics.md` | The full set of operational rules in IF/THEN form, each attributed. |
| `quotes.md` | Verified short attributed excerpts only, wording checked against the source, paraphrases marked as paraphrases. No chapter dumps. |
| `sources.md` | The complete dated bibliography, primary sources first. This is where `provenance.sources` is drawn from. |

All seven files must exist. Missing files are a warning at the default level and an error under `--level strict` (lint L12). One copyright note that drives the whole design: frameworks and ideas are not copyrightable (17 U.S.C. §102(b)), expression is. So the rule is paraphrase and cite, quote short and attribute.

## Authored disagreements: disagreements.md

This file is what makes council debate authored rather than generated. It records real conflicts between this seat and others, both positions cited from the record. One section per entry:

```markdown
## vs naval: diversification vs concentration

counterpart: naval
topic: diversification vs concentration

**Position (munger):** Wide diversification is "deworsification" for the
competent investor; three wonderful businesses are enough for a lifetime
(Wesco meeting, 1998; Poor Charlie's Almanack).

**Position (naval):** Put all your eggs in one basket you control and watch
that basket; concentrated equity in your own judgment is the path (Almanack
of Naval Ravikant, "Judgment").
```

The `counterpart:` value must name an installed seat id, or be marked `counterpart: external: taleb` when the other party has no seat. The linter warns (L9) on a counterpart that is neither installed nor marked external. Both positions must carry citations. "They disagree about risk" fails the bar. Councils surface only authored disagreements. A chairman that invents conflict is the exact failure mode this product exists to kill. If no real conflict exists for a topic, the seat says so rather than manufacturing one, and a distilled seat skips the file entirely rather than inventing entries. See [benches](./benches.md) for how councils use this at runtime.

## The linter

`scripts/lint_seat.py` enforces the standard mechanically. It is stdlib-only Python by design, so CI and any non-Claude harness run the exact same file and get the exact same result. Anything the linter cannot see is spelled out in [`../SEAT_SPEC.md`](../SEAT_SPEC.md) as a normative requirement.

```bash
python3 scripts/lint_seat.py --all                    # lint every seat under skills/
python3 scripts/lint_seat.py skills/munger --explain  # one seat, print rule descriptions
python3 scripts/lint_seat.py skills/munger --level strict
python3 scripts/lint_seat.py --all --format json      # machine-readable report
```

Exit codes are the contract:

- **0**: pass.
- **1**: warnings only.
- **2**: errors. A seat with an error is load-blocking, it will not load.

Inside the plugin, [`/chiron:lint`](./commands.md) runs the same script against the bundled `skills/` directory, so the standard is identical whether you enforce it from CI, a shell, or a slash command.

### The rules

| # | Level | Rule |
|---|---|---|
| L1 | ERROR | `mode: persona` with a living subject and no granted license. Legal, non-negotiable. |
| L2 | ERROR | Missing or invalid frontmatter field (name, description, x-chiron block, display_name, mode, domains, provenance shape). |
| L3 | ERROR | `id` collides with another seat in the linted set. |
| L4 | ERROR | corpus or persona mode with fewer than 3 provenance sources. |
| L5 | ERROR | A required section is missing or below its minimum entry count. |
| L6 | WARN | Core `SKILL.md` over roughly 6k tokens, which breaks progressive disclosure. |
| L7 | WARN, ERROR at strict | First-person subject voice in a corpus seat (persona leakage). Quoted speech is exempt. |
| L8 | WARN | A heuristic with no operational IF/THEN shape. |
| L9 | WARN | A `disagreements.md` counterpart that is not installed and not marked `external:`. |
| L10 | WARN | The subject's name in `display_name` without a mode suffix. |
| L11 | STRICT | No `evals.md` file (paid packs only). |
| L12 | WARN, ERROR at strict | `references/` missing any of the seven standard files. |

The three load-blocking rules to know are L1 (first-person impersonation of a living person), L4 (fewer than three sources), and L12 under strict (a shallow or missing reference set). Those are what make a seat a seat and not a name.

A couple of the checks are worth understanding because they catch subtle defects. L7 strips double-quoted spans and blockquotes first, then flags patterns like `I always`, `I never`, `I believe`, `I tell`, so a corpus seat that slips into first person outside a quotation gets caught while genuine attributed quotes pass. L8 looks for operational cues (`if/then`, `when`, `never`, `always`, `unless`, `before`, `after`, arrows) in each heuristic and warns on entries that read as vibes rather than rules. Neither of those is fatal on its own at the default level, but they are the difference between a mind and a mood board.

## Writing a seat by hand

The supported path is [`/chiron:distill`](./distilling.md): it interviews you, runs deep research over the subject's corpus, writes the full seat at the depth bar with every claim cited, and lints it. Depth is baked into the standard, not an upsell.

If you would rather author one directly, the loop is short:

1. Create `skills/<id>/` with the id in `^[a-z0-9-]{2,32}$`, matching the folder name.
2. Write `SKILL.md`. Model the frontmatter and body on an installed founding seat, for example `skills/munger/SKILL.md`. Include the `x-chiron` block, and for a real person a `provenance` block with 3 or more sources and an `alias` if they are living. Add the four required sections (`## Priors` with 5+ entries, `## Heuristics` with 5+ IF/THEN entries, `## Refusals` with 2+, `## Voice`), and for a real person the M4 disclaimer blockquote. Keep it under about 6k tokens.
3. Write all seven `references/` files at 600 to 1,500 words each, every claim attributed.
4. Add `disagreements.md` only if there is a real, citable published conflict with an installed seat.
5. Run `python3 scripts/lint_seat.py skills/<id> --explain` and fix until it exits 0.

Mechanical findings (frontmatter, naming, first-person rewrites) are quick fixes. Content gaps (L5 thin sections, L12 missing references) need real authoring at the depth bar, not filler.

Two hard rules the standard enforces no matter how you author. You cannot produce a persona-mode seat for a living, unlicensed subject: use corpus mode or an archetype alias instead. And the private `me` seat you write with [`/chiron:distill-me`](./distilling.md) is never shipped: it holds personal data, lives only in `~/.claude/chiron/seats/` or a project `.chiron/seats/`, is gitignored, and never goes in the plugin repo.

## The registry and x-chiron discovery

`scripts/registry.py` scans one or more seat directories and emits a roster index. Chiron merges seats from several locations in precedence order, and a later scope shadows an earlier one on a shared id:

```bash
python3 scripts/registry.py \
  --seats-dir <bundled>/skills \
  --seats-dir ~/.claude/skills \
  --seats-dir ~/.claude/chiron/seats \
  --seats-dir .claude/skills \
  --seats-dir .chiron/seats \
  --json
```

The order is: bundled roster, global skills (`~/.claude/skills/`, where `/chiron:distill` installs an advisor so it auto-activates everywhere), the private global `me` seat (`~/.claude/chiron/seats/`), then project scopes (`<project>/.claude/skills/` and `<project>/.chiron/seats/`). Missing directories are skipped. A user seat with the same id as a bundled one overrides it, so your own richer `munger` shadows the shipped one. More on this in [portability](./portability.md) and [cowork](./cowork.md).

The mechanism that makes a shared skills directory safe is the `x-chiron` marker. At runtime and for the registry, `discover_seats` returns only directories whose `SKILL.md` carries an `x-chiron` block. So scanning `~/.claude/skills/`, which is full of unrelated skills, picks out exactly the seats and ignores everything else, including Chiron's own conversational router skill (`chiron`), which is a skill but not a seat.

The linter deliberately discovers differently. `lint --all` runs in a permissive mode: it returns every non-hidden directory that contains a `SKILL.md`, except the known non-seat router (`chiron`). This is on purpose. If a bundled seat's `x-chiron` block were missing or malformed, marker-based discovery would silently skip it and hide a broken seat from validation. The permissive lint pass instead sees it, treats it as a candidate seat, and fails it. So the runtime ignores non-seats, and CI cannot be fooled into passing a seat by breaking its marker.

## Where the full spec lives

This page covers the working rules. The complete normative spec, including the load contract, the exact section minimums, the disagreement schema, and the full lint table, is [`../SEAT_SPEC.md`](../SEAT_SPEC.md). The provenance policy behind L1, L10, the disclaimer, and the takedown protocol is [`../LEGAL.md`](../LEGAL.md). The project overview is [`../README.md`](../README.md).
