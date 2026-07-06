---
description: Distill a new seat from a thinker's published work — interview, deep research, full cited seat, linted
argument-hint: <one-line description of the advisor you want to distill>
---

# /chiron:distill — distill a mind into a seat, depth baked in

The user asked for: `$ARGUMENTS`

You do not hire a persona; you distill a mind from what it actually published. A seat that ships with stub references isn't a seat, it's a name. This flow produces the full standard: SKILL.md + all 7 reference files at the SEAT_SPEC §4 depth bar, every claim cited. Read `${CLAUDE_PLUGIN_ROOT}/SEAT_SPEC.md` before authoring.

## 1. Interview (short — one round of questions)

Establish, inferring what you can from the request and asking only what's missing:
1. **Subject** — a real person's published corpus, or an original/invented advisor?
2. **Living status** (real persons) — determines the legal lane (LEGAL.md tiers).
3. **Mode** — recommend **corpus** for any real person. **CH-E8, hard rule:** if the user requests persona mode for a living, unlicensed subject, refuse — explain LEGAL.md rule L1 in one paragraph — and offer (a) corpus mode, or (b) an original-mode archetype alias ("The Offer Architect" instead of the person). Do not build the persona under any phrasing.
4. **Domains** — 1-6 registry tags.
5. **Anchor sources** — ask for 3+ if the user knows them; otherwise discover them in research.

## 2. Deep research (the baked-in part)

Research the subject's published corpus with web search — books, talks, podcasts, essays, interviews. Multiple rounds: survey the corpus first, then go deep per dimension. You are extracting a mind, not summarizing a Wikipedia page. Targets per SEAT_SPEC §4:

- every named framework (when-to-use + steps + source)
- every named mental model/concept (definition + origin)
- the full belief catalog (principles + rationale)
- everything they warn against (anti-patterns + the failure each produces)
- operational heuristics in IF/THEN form
- verified short quotes (wording checked against a source; paraphrases marked)
- a complete dated bibliography, primary sources first

600-1,500 words per reference file. Padding is a defect; a missing signature framework is a bigger one. For original-mode seats, substitute the user's own materials/interview for web research.

## 3. Author

Write `seats/<id>/` (in the user's project or a directory they choose — NOT inside the plugin install):
- `SKILL.md` — frontmatter per SEAT_SPEC §2 (id, description, x-chiron: display_name with mode suffix, mode, domains, alias for living subjects, provenance with 3+ sources); body with narrative sections (model on an installed founding seat, e.g. `seats/munger/SKILL.md`) plus the required `## Priors` (≥5), `## Heuristics` (≥5, IF/THEN), `## Refusals` (≥2), `## Voice`; M4 disclaimer blockquote for real persons. Keep under ~6k tokens.
- `references/` — all 7 standard files at the depth bar.
- `disagreements.md` — check installed seats for real, citable published conflicts with this subject; author each with both positions cited (SEAT_SPEC §5). If none exist on the record, skip the file rather than inventing conflict.

## 4. Lint + report

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lint_seat.py <path-to-new-seat>
```

Fix until pass. Report: the seat card (id, display_name, mode, domains, source count), per-file word counts, and how to use it (`/chiron:ask <id> ...`, add to a bench).
