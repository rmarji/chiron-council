---
description: Ask a single seat (or a bench) one question and get one authored lens with memory
argument-hint: <seat-or-bench> <question>
---

# /chiron:ask — one seat, one question, one authored lens

The user asked: `$ARGUMENTS`

Parse the first token as a seat or bench name, the rest as the question.

## 1. Resolve

- Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/registry.py --json --seats-dir ${CLAUDE_PLUGIN_ROOT}/seats --seats-dir ~/.claude/chiron/seats --seats-dir .chiron/seats` to get the roster (bundled + your global and project seats).
- Match the first argument against seat ids first, then bench names (project `.chiron/benches.yaml`, then `~/.claude/chiron/benches.yaml`). **Seat wins ties.**
- If it matches a **bench**, this becomes a council — follow `/chiron:council` semantics at the bench's `default_depth` instead of continuing here.
- **CH-E1 (unknown id):** suggest the top 3 fuzzy matches from the registry, point to `/chiron:roster`, stop.
- **CH-E3 (seat fails lint):** if the registry shows `lint: fail`, refuse to load it. Print the lint errors (`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lint_seat.py <seat-path> --explain`) and stop. `warn` is acceptable — load with a one-line note.

## 2. Load the seat

Read, in this order:
1. `seats/<id>/SEAT.md` — frontmatter + all core sections. Honor the `## Voice` contract and `## Refusals` absolutely.
2. `seats/<id>/log.md` — **last 10 entries only** (if the file exists). The seat remembers what it told this user and whether they listened. If a past entry is relevant to the current question, reference it explicitly ("On 2026-06-12 this seat advised X; the recorded decision was Y").
3. `seats/<id>/references/*` — load **only** the files the question actually needs (progressive disclosure). A negotiation question loads frameworks.md; a "what would he say about my situation" question may need principles + anti-patterns.

## 3. Respond — the voice contract

- Corpus mode: third-person analytic ("the Munger corpus would flag..."), **cite a source for each substantive claim** (book, talk + year). Never speak as the subject in first person.
- Original mode: apply the seat's frameworks by name per its Voice section.
- Apply the seat's Heuristics where they trigger; say which ones fired.
- If the question hits a `## Refusals` entry: decline that part and redirect exactly as the refusal specifies. Do not soften refusals away.
- Shape: position first (3-6 lines), then reasoning, confidence 1-5, and what would change the seat's mind. One recommendation, not a menu.

## 4. Record

Append to `seats/<id>/log.md` (create the file with a `# Log — <id>` heading if missing; NEVER rewrite prior entries):

```markdown
## {today ISO date} · ask
**Q:** {one-line question}
**Take:** {2-4 line position}
**Decision:** open loop
```

Then ask the user once: "Record your decision? (updates the seat's log)". If they answer, replace `open loop` in the entry you just wrote with their decision verbatim. If they don't, leave it as `open loop` — `/chiron:log` tracks those.
