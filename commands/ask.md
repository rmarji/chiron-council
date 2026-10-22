---
description: Ask a single seat (or a bench) one question and get one authored lens with memory
argument-hint: <seat-or-bench> <question>
---

# /chiron:ask — one seat, one question, one authored lens

The user asked: `$ARGUMENTS`

Parse the first token as a seat or bench name, the rest as the question.

## 1. Resolve

- Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/registry.py --json --seats-dir ${CLAUDE_PLUGIN_ROOT}/skills --seats-dir ~/.claude/skills --seats-dir ~/.claude/chiron/seats --seats-dir ~/.chiron/seats --seats-dir .claude/skills --seats-dir .chiron/seats` to get the roster (bundled + your global and project seats). The `~/.claude/` directories are read only. If `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py seats` prints a directory other than `~/.chiron/seats`, pass that directory in place of `~/.chiron/seats`. Run it as its own `python3` command. Run every `python3` call as its own command: no `;`, `&&`, pipes, loops or `$(...)` around it, and save log entries with the file-editing tool rather than a shell heredoc. Hosts approve plain `python3` calls; anything else triggers an extra permission prompt.
- Match the first argument against seat ids first, then bench names (`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/benches.py --json`: project `.chiron/benches.yaml`, then `~/.chiron/benches.yaml`, then a leftover `~/.claude/chiron/benches.yaml`, or the bundled examples when the user has none of those). **Seat wins ties.**
- If it matches a **bench**, this becomes a council — follow `/chiron:council` semantics at the bench's `default_depth` instead of continuing here.
- **CH-E1 (unknown id):** suggest the top 3 fuzzy matches from the registry, point to `/chiron:roster`, stop.
- **CH-E3 (seat fails lint):** if the registry shows `lint: fail`, refuse to load it. Print the lint errors (`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lint_seat.py <seat-path> --explain`) and stop. `warn` is acceptable — load with a one-line note.

## 2. Load the seat

Read, in this order (the seat's directory is the `path` the registry returned for `<id>` — a bundled seat resolves under `${CLAUDE_PLUGIN_ROOT}/skills/<id>/`, a Chiron seat under `~/.chiron/seats/<id>/`, an `npx skills` install under `~/.claude/skills/<id>/`, or a project's `.chiron/seats/<id>/`):
1. `<seat-dir>/SKILL.md` — frontmatter + all core sections. Honor the `## Voice` contract and `## Refusals` absolutely.
2. The seat's consult log, **last 10 entries only**. Resolve it with `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py log <id> --read` (add `--home .chiron` in Cowork) and read that file (it may not exist yet). Never `<seat-dir>/log.md`, and never anything under `${CLAUDE_PLUGIN_ROOT}`: the plugin cache is wiped on update and Claude Code blocks writes there. The seat remembers what it told this user and whether they listened. If a past entry is relevant, reference it explicitly ("On 2026-06-12 this seat advised X; the recorded decision was Y").
3. `<seat-dir>/references/*` — load **only** the files the question actually needs (progressive disclosure). A negotiation question loads frameworks.md; a "what would he say about my situation" question may need principles + anti-patterns.

## 3. Respond — the voice contract

- Corpus mode: third-person analytic ("the Munger corpus would flag..."), **cite a source for each substantive claim** (book, talk + year). Never speak as the subject in first person.
- Original mode: apply the seat's frameworks by name per its Voice section.
- Apply the seat's Heuristics where they trigger; say which ones fired.
- If the question hits a `## Refusals` entry: decline that part and redirect exactly as the refusal specifies. Do not soften refusals away.
- Shape: position first (3-6 lines), then reasoning, confidence 1-5, and what would change the seat's mind. One recommendation, not a menu.
- Wrap it for the user as `${CLAUDE_PLUGIN_ROOT}/skills/chiron/VOICE.md` describes: a one-line opening, plain labels ("How sure: 3 out of 5"), one next step. No token counts, paths, or lint status.

## 4. Record

Append to the path `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/memory.py log <id> --ensure` prints (create the file with a `# Log — <id>` heading if missing; NEVER rewrite prior entries). That is `~/.chiron/logs/<id>/log.md`, or `$CHIRON_HOME/logs/<id>/log.md` when the variable is set (`--home` overrides the variable). In Cowork, where the home directory is not writable, pass `--home .chiron`. `--ensure` copies a log that still lives at `~/.claude/chiron/logs/<id>/log.md` into the new path once. Append only to the printed path. Never write under `~/.claude` or inside the plugin install:

```markdown
## {today ISO date} · ask
**Q:** {one-line question}
**Take:** {2-4 line position}
**Decision:** open loop
```

Then end with one optional offer: "Want me to remember what you decide, so <advisor> can follow up next time?". If they answer, replace `open loop` in the entry you just wrote with their decision verbatim. If they don't, leave it as `open loop` — `/chiron:log` tracks those.
