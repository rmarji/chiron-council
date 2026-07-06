# SEAT_SPEC v0.1.0 — The Chiron Seat Standard

A **seat** is an authored mind: one advisor, distilled from their actual published thinking into a lint-enforced file format that any Agent Skills-compatible harness can load. Seats are the unit of value in Chiron. Councils, benches, and every other feature are powered by seats.

This document is the open standard. `scripts/lint_seat.py` enforces it mechanically; anything the linter cannot see is spelled out here as a normative requirement.

## 1. Anatomy of a seat

```
seats/<id>/
├── SEAT.md              # the mind: frontmatter contract + core sections (< 6k tokens)
├── disagreements.md     # authored conflicts with other seats, with cited positions
├── references/          # the depth: complete extraction of the subject's thinking
│   ├── principles.md
│   ├── mental-models.md
│   ├── frameworks.md
│   ├── anti-patterns.md
│   ├── heuristics.md
│   ├── quotes.md
│   └── sources.md
└── log.md               # append-only consult memory (created on first use, gitignored)
```

Progressive disclosure is the load contract: a summoned seat loads SEAT.md frontmatter + core sections + its last 10 log entries. References load on demand. This is why SEAT.md must stay under ~6k tokens (lint L6) and why the depth lives in `references/`.

## Where seats live

Chiron merges seats from three locations, in precedence order (a later scope shadows an earlier one on a shared id):

1. **Bundled** — the plugin's `seats/` (the shipped roster). Public, versioned, lint-enforced.
2. **Global user seats** — `~/.claude/chiron/seats/`. Yours across every project; where `/chiron:distill` and `/chiron:distill-me` write by default.
3. **Project seats** — `<project>/.chiron/seats/`. Scoped to one repo; shadows global on a shared id.

The registry scans all three (`registry.py --seats-dir <bundled> --seats-dir ~/.claude/chiron/seats --seats-dir .chiron/seats`); missing dirs are skipped. A user seat with the same id as a bundled one overrides it (e.g. your own richer `munger`).

**The `me` seat.** `/chiron:distill-me` writes an original-mode seat with id `me`: your own operating system (mission, values, goals, frameworks, go-to experts), so you can chair your own councils and be argued with. It is **private** — it holds personal data, lives only in your user or project seat dir, is never committed to the plugin repo, and is never shipped. Gitignore `.chiron/seats/` in any project. Treat the `me` seat like `log.md`: local, personal, yours.

## 2. SEAT.md frontmatter

Standard Agent Skills keys first (so non-Claude harnesses load a seat as a plain skill), Chiron extensions under `x-chiron:` (which those harnesses ignore).

```yaml
---
name: munger                      # id: ^[a-z0-9-]{2,32}$, unique, matches folder name
description: >                    # triggering description, same rules as any skill
  Applies the reasoning, mental models, and temperament of Charlie Munger...
x-chiron:
  display_name: Munger Lens       # human name; see naming rules below
  mode: corpus                    # corpus | persona | original
  domains: [investing, decision-making, incentives]   # 1..6 registry filter tags
  alias: The Inversion Lens       # archetype fallback name (required for living subjects)
  provenance:                     # required when mode != original
    subject: Charlie Munger
    living: false
    license: none                 # none | granted | n/a
    sources:                      # 3..50 citations; primary sources first
      - "Poor Charlie's Almanack (2005)"
      - "USC Gould School of Law commencement address (2007)"
      - "Wesco Financial annual meeting transcripts (1999-2011)"
---
```

### Modes

- **corpus** — frameworks and heuristics from the subject's published work, cited, spoken about in the third person ("the Munger corpus would flag..."). This is the default and the only mode that ships for real people.
- **persona** — first-person voice emulation. Never a default. Forbidden for living subjects without a granted license (lint L1, hard fail, non-negotiable). See LEGAL.md.
- **original** — an invented or self-authored advisor. No provenance constraints.

### Naming rules

For real-person seats, `display_name` carries a mode suffix — "Munger Lens", "Voss (corpus)" — so nobody mistakes a study aid for the person (lint L10). Every living-subject seat also defines an `alias` (an archetype name like "The Offer Architect") so a takedown request is a rename, not a rebuild (LEGAL.md rule M6).

## 3. Required SEAT.md sections

The body must contain these `##` sections (lint L5). Headings may carry suffixes ("## Heuristics and rules of thumb" satisfies "Heuristics").

| Section | Minimum | Bar |
|---|---|---|
| `## Priors` | 5 bullet entries | What the seat believes before hearing your question. Each 1-2 sentences, specific enough to disagree with. "Is smart about investing" fails the bar; "Invert, always invert: state how this decision fails before how it succeeds" passes. |
| `## Heuristics` | 5 bullet entries | Operational decision rules in IF/THEN shape (lint L8 warns on vibes). "Think long-term" fails; "IF the opportunity requires being clever rather than avoiding stupidity THEN pass" passes. |
| `## Refusals` | 2 bullet entries | What this seat declines to opine on, and where it redirects. Refusals are what make a seat a mind instead of a horoscope. |
| `## Voice` | present | The register contract. In corpus mode: third-person analytic, citing a source per claim, never "I, Charlie" (lint L7 flags first-person subject voice outside quotations). |

Seats ported from the founding corpus also carry richer narrative sections (Core principles, How X reasons, Applying the frameworks, Anti-patterns, worked examples). Keep them — they are the connective tissue — but the four sections above are the contract.

Every real-person seat ends with the disclaimer block (LEGAL.md rule M4):

> *Independent study aid based on published works. Not affiliated with or endorsed by {subject}.*

## 4. References: the depth bar

References are not summaries. Each file is the **complete extraction** of that dimension of the subject's thinking — the standard a serious student would accept as "this covers what they actually said." Every claim is attributed to a named source: book plus chapter/section, talk plus year, podcast plus episode, essay plus title.

| File | Contains |
|---|---|
| `principles.md` | The full catalog of core beliefs, each with rationale and source. |
| `mental-models.md` | Every named model or concept the subject uses, defined, with origin and when it applies. |
| `frameworks.md` | Every named framework with when-to-use, concrete steps, and source. |
| `anti-patterns.md` | Everything the subject warns against, with their reasoning and the failure it produces. |
| `heuristics.md` | The full set of operational rules, IF/THEN form, each attributed. |
| `quotes.md` | Verified short attributed excerpts only — no chapter dumps (LEGAL.md rule M5). Wording verified against the source; paraphrases are marked as paraphrases. |
| `sources.md` | Complete bibliography with dates: books, talks, interviews, podcasts, essays. Primary sources first. This is where provenance.sources is drawn from. |

All 7 files must exist (lint L12: warn at standard level, error at strict). Rough calibration: 600-1,500 words per file. Padding to hit a word count is a defect; missing a framework the subject is known for is a bigger one.

Copyright note: frameworks and ideas are not copyrightable (17 U.S.C. §102(b)); expression is. Paraphrase and cite. Quote short and attribute.

## 5. disagreements.md

Authored conflicts between this seat and others — what makes council debate authored rather than generated. One section per entry:

```markdown
## vs naval — diversification vs concentration

counterpart: naval
topic: diversification vs concentration

**Position (munger):** Wide diversification is "deworsification" for the competent
investor; three wonderful businesses are enough for a lifetime (Wesco meeting, 1998;
Poor Charlie's Almanack).

**Position (naval):** Put all your eggs in one basket you control and watch that
basket; concentrated equity in your own judgment is the path (Almanack of Naval
Ravikant, "Judgment").
```

Rules: `counterpart:` must name an installed seat id or be marked `counterpart: external: taleb` (lint L9). Both positions carry source citations. "They disagree about risk" fails the bar. Councils surface **only** authored disagreements — a chairman that invents conflict is the failure mode this product exists to kill.

## 6. log.md

Append-only consult memory, created on first consult, gitignored by default (it contains your decisions, not the seat's). Entry schema:

```markdown
## 2026-07-06 · council:cc-pricing
**Q:** Founding member price — $49 or $99/mo?
**Take:** Corpus indicates anchor high, grandfather early believers.
**Decision:** open loop
```

Never rewrite prior entries. At >100 entries, the oldest are summarized into an `## Archive digest` block. A summoned seat reads its last 10 entries — it remembers what it told you and whether you listened.

## 7. Lint rules

`python3 scripts/lint_seat.py <path>|--all [--format text|json] [--level standard|strict]`
Exit codes: **0** pass · **1** warnings only · **2** errors (load-blocking).

| # | Level | Rule |
|---|---|---|
| L1 | ERROR | `mode: persona` + `living: true` + `license != granted` → hard fail. Legal, non-negotiable. |
| L2 | ERROR | Missing/invalid frontmatter field per §2. |
| L3 | ERROR | `id` collision with installed seat. |
| L4 | ERROR | corpus/persona mode with < 3 provenance sources. |
| L5 | ERROR | Required sections missing or under minimums (§3). |
| L6 | WARN | Core SEAT.md > 6k tokens (breaks progressive disclosure). |
| L7 | WARN → ERROR (strict) | First-person subject voice in a corpus seat (persona leakage). Quoted speech is exempt. |
| L8 | WARN | Heuristic not in operational IF/THEN-ish form. |
| L9 | WARN | disagreements.md counterpart unresolved and not marked external. |
| L10 | WARN | Subject's name in `display_name` without a mode suffix. |
| L11 | STRICT | No evals.md file (paid packs only). |
| L12 | WARN → ERROR (strict) | references/ missing any of the 7 standard files (§4). |

## 8. Authoring a new seat

Use `/chiron:distill`. It interviews you (subject, living status, mode, domains), then runs deep research over the subject's published corpus and writes the full seat — SEAT.md plus all 7 references at the §4 depth bar, every claim cited — and lints it. Depth is baked into the standard, not an upsell: a seat that ships with stub references isn't a seat, it's a name.

Hard rule the distill flow enforces: it will not produce a persona-mode seat for a living, unlicensed subject (CH-E8). It offers corpus mode or an archetype alias instead.

---
*SEAT_SPEC v0.1.0 · part of Chiron · bump major on schema or section-contract changes.*
