# Distilling seats (and yourself)

This page is how you grow the roster. `/chiron:distill` turns a thinker's published work into a new cited seat that auto-activates like the shipped ones. `/chiron:distill-me` turns *you* into a private seat that can chair your own councils. Both run the same depth bar, and both end at a passing lint.

The two commands share one idea: you do not hire a persona, you distill a mind from what it actually produced. A seat that ships with stub references is not a seat, it is a name. See [the depth standard](./the-standard.md) for the full spec these commands enforce.

| Command | Builds | Mode | Ships in the repo? |
|---|---|---|---|
| `/chiron:distill <desc>` | a public advisor seat from a subject's corpus | `corpus` (real or fictional), or `original` | Yes, if you contribute it |
| `/chiron:distill-me` | your private `me` seat from your own history | `original` | Never |

---

## Part 1: `/chiron:distill`, a new seat from a corpus

`/chiron:distill` takes a one-line description of the advisor you want and returns a full, linted, auto-activating seat. You do not move any files by hand. Depth is baked into the command, not offered as an upsell.

```
/chiron:distill "Brad Frost on design systems"
/chiron:distill "a negotiation expert, I'm thinking Chris Voss"
/chiron:distill "W. Edwards Deming on quality and management"
```

### The flow

Four phases. Claude narrates as it goes, because deep research is slow and a silent multi-minute run reads as broken.

**1. A short interview (one round).** Chiron infers what it can from your description and asks only what is missing:

- **Subject**: a real person's published corpus, a fictional character with a canon, or an original advisor you are inventing.
- **Living status**: for real people, this sets the legal lane (see [LEGAL.md](../LEGAL.md)).
- **Mode**: `corpus` is recommended for any real person, and it is the only mode that ships for real people. There is a hard rule here (CH-E8): if you ask for `persona` mode (first-person voice) of a living, unlicensed subject, Chiron refuses, explains the rule in a sentence, and offers you either `corpus` mode or an original-mode archetype alias ("The Offer Architect" instead of the person). It will not build the persona under any rephrasing.
- **Domains**: one to six registry tags, so `/chiron:roster --domain <tag>` and the auto-router can find the seat.
- **Anchor sources**: if you already know the key books, talks, or essays, name three or more and Chiron starts there. If you do not, it discovers them in research.

If your request is vague, Chiron does not interrogate you. It offers two or three concrete candidate readings and lets you pick:

```
▸ By "a design expert" do you mean:
  (a) Brad Frost: design systems, atomic design
  (b) Don Norman: usability, affordances, human-centered design
  (c) someone specific?
```

**2. Deep research (the part that takes real time).** Chiron searches the subject's published corpus in multiple rounds: survey the whole body of work first, then go deep per dimension. Books, talks, podcasts, essays, interviews. It is extracting a mind, not summarizing a Wikipedia page. The targets, straight from the [depth standard](./the-standard.md):

- every named framework, with when-to-use, steps, and source
- every named mental model or concept, defined, with origin
- the full belief catalog, each principle with its rationale
- everything the subject warns against, each anti-pattern with the failure it produces
- operational heuristics in IF/THEN form
- verified short quotes, wording checked against a source, paraphrases marked as paraphrases
- a complete dated bibliography, primary sources first

**3. Author the seat.** Chiron writes the seat as a real, auto-activating Agent Skill. The `<id>/` directory it produces:

```
<id>/
├── SKILL.md              # the mind: frontmatter + Priors, Heuristics, Refusals, Voice (< ~6k tokens)
├── disagreements.md      # authored, cited conflicts with installed seats (omitted if none exist)
├── references/           # the depth: seven files at the depth bar
│   ├── principles.md     ├── mental-models.md   ├── frameworks.md
│   ├── anti-patterns.md  ├── heuristics.md       ├── quotes.md
│   └── sources.md
└── log.md                # created on first consult, gitignored
```

`SKILL.md` carries the frontmatter contract (a `name` matching the folder, a triggering `description`, and an `x-chiron` block with `display_name`, `mode`, `domains`, an `alias` for living subjects, and `provenance` with three or more sources). Its body carries the required `## Priors` (five or more), `## Heuristics` (five or more, in IF/THEN shape), `## Refusals` (two or more), and `## Voice`, plus the narrative sections that give a seat its texture. Real-person seats end with the disclaimer block. The subject's two or three signature mental models get named inline in the body, so the mind is visible without loading the reference files.

`disagreements.md` only appears when there is a real, citable, published conflict between this subject and a seat you already have installed, with both positions sourced. If none exists on the record, Chiron skips the file rather than inventing conflict. A chairman that manufactures disagreement is the exact failure mode Chiron exists to kill.

**4. Lint until it passes.** Chiron runs the linter and fixes findings until the seat is clean:

```bash
python3 scripts/lint_seat.py <path-to-new-seat>
# 0 = pass · 1 = warnings · 2 = errors (load-blocking)
```

Then it reports the seat card (id, display name, mode, domains, source count), the per-file word counts, and how to use it. You can re-run the check yourself any time with [`/chiron:lint`](./commands.md).

Here is roughly what a run looks like end to end:

```
/chiron:distill "Chris Voss on negotiation"

▸ interview
  Subject: Chris Voss (living). Mode: corpus (recommended). Domains:
  [negotiation, persuasion, communication]. Anchor: Never Split the
  Difference (2016). Discovering talks and interviews for the rest.

▸ researching · surveying the corpus
  Never Split the Difference; The Black Swan Group masterclass; TED-style
  talks; podcast appearances. Going deep per dimension now.
  found: tactical empathy · calibrated questions · the accusation audit ·
  mirroring · labeling · "That's right" vs "you're right" · the 7-38-55 rule

▸ authoring skills/voss/  (writing SKILL.md + 7 references + disagreements.md)

▸ lint
  PASS [voss] ~/.claude/skills/voss
  references: principles 1,180w · mental-models 1,020w · frameworks 1,340w ·
  anti-patterns 900w · heuristics 1,110w · quotes 640w · sources 720w

  Seat ready. Try:  /chiron:ask voss "counter a lowball on the retainer"
                    add voss to a bench in ~/.claude/chiron/benches.yaml
```

### Where the finished seat lands

The delivery target depends on your harness, and in both cases the seat becomes usable with no manual move.

- **Claude Code** writes to `~/.claude/skills/<id>/`, so the seat auto-activates in your next turn and every council finds it through the registry. If you want it scoped to one repo instead, it writes `<project>/.claude/skills/<id>/`. It never writes inside the plugin install.
- **Cowork** cannot write to `~/.claude`. It writes `<project>/.chiron/seats/<id>/` in the open workspace (the registry scans that path, so councils find it with no home-directory write). If there is no writable project, it emits a one-advisor `.plugin` into `outputs/` for you to accept in the app. More on this split in [cowork.md](./cowork.md) and [portability.md](./portability.md).

The registry merges seats by precedence: project shadows global shadows bundled. A seat you distill with the same id as a bundled one (say, a richer `munger` of your own) overrides the shipped seat everywhere you use Chiron.

### Fictional and original advisors

You can distill any mind, not only living authors.

- **Fictional characters** distill in `corpus` mode, cited to their canon. The shipped detectives bench proves it: **Sherlock Holmes (corpus)**, **Dr. House (corpus)**, and **Columbo (corpus)** are each sourced to the stories and episodes and pass the same lint as the real-person seats. Point `/chiron:distill` at the canon and treat it as the corpus.
- **Original advisors** you invent from scratch use `original` mode. There is no provenance constraint and no disclaimer, because nothing is being attributed to a real person. Rayo OS is the shipped example. For an original seat, Chiron substitutes your own materials and an interview for web research: the frameworks come from you, not from a published body of work.

### One at a time, never a shallow batch

If you ask for several advisors at once, Chiron distills them sequentially, each with its own full deep-research pass. It will not batch them into a single shallow sweep. Thinness and repetition across seats is the tell of a rushed job, and it is exactly what the depth bar exists to prevent. Expect each real-person seat to carry 6,000 to 10,000 words of cited reference material across the seven files. That takes minutes per seat, and that is the point.

### Tips for a good distill

- **Give it anchor sources.** If you know the two or three foundational works, name them. Chiron starts from primary sources instead of spending a round finding them, and you get a better seat.
- **Let it offer options when you are vague.** "A pricing expert" is a fine way to start. Chiron will hand you a short menu of who it thinks you mean. Pick one, and it confirms before it commits.
- **Name the conflicts you care about.** If you already run a council and want the new seat to argue with a specific existing one, say so during the interview so the authored `disagreements.md` targets that counterpart.
- **Contribute it back.** A seat you author is a standard Agent Skill directory. If it is a real thinker distilled to the bar, it can go in the public roster. Your private `me` seat never does (below).

---

## Part 2: `/chiron:distill-me`, put yourself in the room

`/chiron:distill-me` distills *you* the way `/chiron:distill` distills a thinker. It writes an original-mode seat with id `me`: your own operating system, so your priorities, values, and frameworks can sit in the room, chair your councils, and be argued with. It also reads out the experts you already reach for and turns them into a recommended roster.

```
/chiron:distill-me
/chiron:distill-me ~/notes/how-i-work.md
/chiron:distill-me ~/obsidian/vault
```

The optional argument points it at notes, a vault, a folder, or a document to read as source material.

### Consent first

The `me` seat holds personal data: your mission, your values, your goals, your decisions. Chiron states the privacy rules up front and then honors them. It reads personal sources only with your consent, names each source out loud before reading it, and never transmits any of it anywhere.

### What it gathers

You choose which of these it draws on. It reads only what you approve:

- **This conversation and recent Claude Code history**: the frameworks, phrases, and decisions you actually reach for.
- **Instruction and memory files**: `~/.claude/CLAUDE.md`, a project's `CLAUDE.md` or `AGENTS.md`, and any memory files. These already encode how you operate.
- **Anything you point it at**: a notes vault, a "how I work" doc, a resume, past writing. It reads these as your corpus.
- **An interview** to fill the gaps, run as a conversation rather than an interrogation. It offers concrete suggestions ("a lot of people channel someone like Munger for money calls, who is yours?") instead of a wall of open questions.

### What it extracts

It synthesizes, in your own terms and cited to the source where possible:

- **Mission** and what you are optimizing for, plus your current active priorities.
- **Values and non-negotiables**: the lines you will not cross.
- **Goals**: concrete and time-bound, with relative dates converted to absolute ones.
- **Frameworks and mental models** you operate by, named, each with when it applies.
- **Operating principles and heuristics** in IF/THEN form.
- **Anti-patterns and traps**: how you characteristically fail, and the counter.
- **Voice**: how you think and want to be addressed.
- **Go-to experts**: the thinkers you channel, tagged by domain.

### Where it lives, and why it is private

The `me` seat is written to `~/.claude/chiron/seats/me/` (global) or `<project>/.chiron/seats/me/` (project). In Cowork, which cannot write to `~/.claude`, it uses the project path, which the registry scans. It is **never** written into the Chiron plugin repo, never committed, and never shipped. If it is written into a project, Chiron adds `.chiron/seats/` to that project's `.gitignore`, and offers to do it for you.

It uses the full seat structure: `SKILL.md` with `name: me`, `x-chiron` set to `display_name: "<your name> (you)"`, `mode: original`, and your domains. Original mode needs no provenance and no disclaimer, because it is self-authored. The body carries the same required sections as any seat, where `## Refusals` becomes your own guardrails: the decisions and moves you refuse to make. The seven reference files hold the depth so `SKILL.md` stays lean, and Chiron lints it until it passes.

### How it chairs your councils

After it writes the seat, `/chiron:distill-me` maps your named go-to experts against the installed roster and reads out three groups: experts you already have installed, experts that are available and worth distilling next (it offers to `/chiron:distill` each), and proposed starter [benches](./benches.md) built from your experts by domain. It suggests the `me` seat as the chairman for personal-decision benches, so your own operating system arbitrates the council instead of a neutral chair:

```yaml
benches:
  personal:
    seats: [munger, naval, taleb]
    chairman: me            # your operating system runs the synthesis
    default_depth: full
```

From there, put the new bench to work with a real decision:

```
/chiron:consult "take the retainer at 15k/mo or walk?"
```

---

## See also

- [The depth standard](./the-standard.md): the exact bar `/chiron:distill` writes to, and every lint rule.
- [Commands](./commands.md): `/chiron:lint`, `/chiron:roster`, `/chiron:bench`, and the rest.
- [Benches](./benches.md): turn a distilled roster into named line-ups.
- [Cowork](./cowork.md) and [portability](./portability.md): how delivery differs by harness.
- [SEAT_SPEC.md](../SEAT_SPEC.md) and [LEGAL.md](../LEGAL.md): the seat file format and the provenance policy the persona refusal comes from.
