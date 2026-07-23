---
description: Distill a new seat from a thinker's published work — interview, deep research, full cited seat, linted
argument-hint: <one-line description of the advisor you want to distill>
---

# /chiron:distill — distill a mind into a seat, depth baked in

The user asked for: `$ARGUMENTS`

You do not hire a persona; you distill a mind from what it actually published. A seat that ships with stub references isn't a seat, it's a name. This flow produces the full standard: SKILL.md + all 7 reference files at the SEAT_SPEC §4 depth bar, every claim cited. Read `${CLAUDE_PLUGIN_ROOT}/SEAT_SPEC.md` before authoring.

**Narrate as you go.** Before each phase (research, authoring, lint), say in one line what you are about to do, and while researching, surface what you are finding as you find it. Deep research is slow; a silent multi-minute run reads as broken.

## 1. Interview (short — one round of questions)

Establish, inferring what you can from the request and asking only what's missing:
1. **Subject** — a real person's published corpus, or an original/invented advisor?
2. **Living status** (real persons) — determines the legal lane (LEGAL.md tiers).
3. **Mode** — recommend **corpus** for any real person. **CH-E8, hard rule:** if the user requests persona mode for a living, unlicensed subject, refuse — explain LEGAL.md rule L1 in one paragraph — and offer (a) corpus mode, or (b) an original-mode archetype alias ("The Offer Architect" instead of the person). Do not build the persona under any phrasing.
4. **Domains** — 1-6 registry tags.
5. **Anchor sources** — ask for 3+ if the user knows them; otherwise discover them in research.

If the request is vague or the user is unsure, do not interrogate. Offer 2-3 concrete candidate readings and let them pick ("By 'a design expert' do you mean Brad Frost on design systems, Don Norman on usability, or someone specific?"). Suggest, then confirm.

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

**One subject at a time.** If the user asked for several advisors at once, distill them sequentially, each with its own full deep-research pass. Never batch them into one shallow sweep — thinness and repetition across seats is the tell of a rushed job.

## 3. Author

**Deliver the seat as a real, auto-activating Agent Skill** — this is what makes it usable with no manual move. Pick the target by harness:
- **Claude Code:** write `~/.claude/skills/<id>/` (global; the seat auto-activates next turn and every council finds it via the registry), or `<project>/.claude/skills/<id>/` if the user wants it project-scoped. Never write inside the plugin install.
- **Cowork** (cannot write to `~/.claude`): write `<project>/.chiron/seats/<id>/` in the open workspace (the registry scans it, so councils find it with no home-dir write), or if there is no writable project, emit a one-advisor `.plugin` into `outputs/` for the user to accept in-app.

The `<id>/` directory contains:
- `SKILL.md` — frontmatter per SEAT_SPEC §2 (id, description, x-chiron: display_name with mode suffix, mode, domains, alias for living subjects, provenance with 3+ sources); body with narrative sections (model on an installed founding seat, e.g. `skills/munger/SKILL.md`) plus the required `## Priors` (≥5), `## Heuristics` (≥5, IF/THEN), `## Refusals` (≥2), `## Voice`; M4 disclaimer blockquote for real persons. Name the subject's 2-3 signature mental models inline in the body (in Priors or Heuristics), not only in `references/mental-models.md`, so the mind is visible without loading the reference files. Keep under ~6k tokens.
- `references/` — all 7 standard files at the depth bar.
- `disagreements.md` — check installed seats for real, citable published conflicts with this subject; author each with both positions cited (SEAT_SPEC §5). If none exist on the record, skip the file rather than inventing conflict.

## 4. Lint + report

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lint_seat.py <path-to-new-seat>
```

Fix until pass. Report: the seat card (id, display_name, mode, domains, source count), per-file word counts, and how to use it (`/chiron:ask <id> ...`, add to a bench).
