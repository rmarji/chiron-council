---
title: Commands
nav_order: 6
description: "Every Chiron command, with the plain-words version for Codex and ChatGPT."
---

# Commands

Chiron has eleven commands. In Claude (web, Code and Cowork) you can type them as slash commands. Codex and ChatGPT don't have slash commands, so ask in plain words; the right column shows how. Plain words work in Claude too.

| Command | What it does | In plain words |
|---|---|---|
| [`/chiron:consult <question>`](#chironconsult) | Chiron picks who should answer, or says no advisor is needed | Just ask your question |
| [`/chiron:ask <advisor> <question>`](#chironask) | One advisor answers | "Ask Naval: salary or equity?" |
| [`/chiron:council <council> <question>`](#chironcouncil) | Several advisors answer separately, then one recommendation | "Convene the money council: …" |
| [`/chiron:coach <situation>`](#chironcoach) | Works you through a decision until you commit to a next step | "Coach me through this: …" |
| [`/chiron:log <advisor>`](#chironlog) | What you asked an advisor before, and what you decided | "What did Munger tell me before?" |
| [`/chiron:roster`](#chironroster) | Lists your advisors | "Which Chiron advisors do I have?" |
| [`/chiron:bench`](#chironbench) | Save, list or remove councils | "Make me a council called hiring with…" |
| [`/chiron:onboard`](#chirononboard) | A short guided start | "Help me get started with Chiron" |
| [`/chiron:distill <who>`](#chirondistill) | Build a new advisor from someone's published work | "Build a Chiron advisor for Brad Frost" |
| [`/chiron:distill-me`](#chirondistill-me) | Build a private advisor from your own goals and rules | "Build my own Chiron advisor" |
| [`/chiron:lint`](#chironlint) | Check an advisor's files (for people building advisors) | "Check my Chiron advisors" |

Advisor ids are on the [advisors](advisors.md) page. Ready-made councils are on the [councils](benches.md) page.

---

## /chiron:consult

```
/chiron:consult <your question or situation>
```

You don't name anyone. Chiron reads the decision, picks who should answer, and tells you before it starts. Typing a decision without any command does the same thing.

It looks at three things: how expensive or hard to undo the decision is, whether it touches one area or several, and whether it's a judgment call at all. Then it does one of four things:

- **Answers directly** when it's a fact or a technical question. No advisor needed.
- **Asks one advisor** when one clearly owns the topic and the stakes are moderate.
- **Calls a council** of two to five when the decision is expensive, hard to undo, crosses areas, or sits on a recorded disagreement.
- **Asks you one question first** when it can't tell the stakes. Then it goes ahead.

```
/chiron:consult "take the retainer at 15k a month or walk?"

This is a commitment that's hard to undo and touches pricing and your time,
so I'll ask Hormozi, Naval and Munger separately. It takes a minute or two.
```

```
/chiron:consult "is it 'affect' or 'effect' in this sentence?"

That's a grammar question, not a decision, so no advisor is needed.
It's "effect" (the noun).
```

Override it any time: "just ask Naval" or "make it a full council".

---

## /chiron:ask

```
/chiron:ask <advisor-id> <question>
```

One advisor, one question. The first word is the advisor id (`munger`, `terry-real`, `tim-ferriss`) and the rest is the question.

```
/chiron:ask voss "the counteroffer came in 20% under. how do I respond?"

Chris Voss (negotiation) looked at this.

What he'd tell you
  Don't counter the number yet. Name the gap and let them solve it: "It
  sounds like 20% under is the most you can do right now." Then stay quiet.
  (Never Split the Difference, "Calibrated Questions")

What to do
  Send that line today and wait for their answer before naming any number.
  The catch: it feels slower, and a buyer on a deadline may just walk.
  How sure: 4 out of 5. If it's a final offer with a hard deadline, give
  one clear walk-away number instead.

Want me to remember what you decide, so Voss can follow up next time?
```

Advisors based on real people describe what that person published, with a source for each point. They don't pretend to be the person.

If the id is wrong, Chiron suggests the closest matches. Not sure who to ask? Use `/chiron:consult`.

---

## /chiron:council

```
/chiron:council <council-name or a,b,c> <question> [--depth quick|full]
```

Several advisors answer separately, then you get one recommendation. The first word is a saved council (`money`, `deals`, `strategy`, `relationship`, `shipping`, `work-design`, or your own) or a comma-separated list of advisor ids (`munger,naval,rumelt`).

1. Each advisor answers **on its own**, without seeing the others or your conversation.
2. In a full answer, Chiron also checks the advisors' files for **disagreements written down from their books** and shows those that fit your question. If there's none, it says so. It never makes one up. A short answer notes the main disagreement between the takes in one line.
3. You get **one recommendation**, the catch, how sure it is, and what would change it.

`--depth quick` (the usual) gives a short answer. `--depth full` adds the recorded-disagreement check and each advisor's full reasoning. You can also just say "give me the full reasoning".

```
/chiron:council relationship "we keep having the same fight about money" --depth full

Two advisors looked at this: Terry Real (couples therapist) and David Deida
(author on relationships).

What they'd tell you
  Terry Real: The same fight every time means you're both reacting from old
    patterns. Name the pattern, not the numbers, and repair. (Us)
  Deida: The fight is rarely about money. Stop negotiating the budget and
    change how you show up. (The Way of the Superior Man)

Where they disagree
  Real puts repair first; Deida says repair alone leaves you as good
  roommates. Both positions are from their books, not invented.

What to do
  This week, name the pattern out loud before the next money talk.
  The catch: if there's a real budget problem underneath, you'll still need
  the numbers conversation.
  How sure: 4 out of 5.

Want me to remember what you decide, so these advisors can follow up next time?
```

More than eight advisors is refused. If a council names an advisor you don't have, Chiron says which one and offers to go ahead with the rest.

---

## /chiron:coach

```
/chiron:coach <your decision or situation> [--quick]
```

The other commands answer a question. Coach works you through a decision until you've committed to one next step:

1. **Find the real decision** behind the question, and how hard it is to undo.
2. **Get the constraints on the table.** If you've built a `me` advisor, it checks against your own rules.
3. **Ask the right advisors** (the same way `/chiron:consult` picks them) and treats their answers as evidence.
4. **Pick one option.** You say which way you lean; it won't let you split the difference.
5. **Commit** to one dated next action, and offer to remember it.

`--quick` does it in one pass for small decisions.

```
/chiron:coach "I keep saying I'll launch the paid tier but I haven't shipped anything in a month"
```

Use it when you've been circling a decision and want to be pushed to commit.

---

## /chiron:log

```
/chiron:log <advisor-id> [--open-loops]
```

Shows your notes with one advisor, newest first: the date, what you asked, the one-line take, and what you decided.

`--open-loops` shows only decisions you never made, and flags anything older than two weeks. Tell Chiron what you decided and it records it on that note. Reading the log never changes it.

```
/chiron:log munger --open-loops

Decisions you haven't made yet, with Munger:

  12 June 2026 · money council   (41 days ago)
    Move the emergency fund into the index position?

  19 July 2026 · asked directly
    Kill the weak product line, or give it another quarter?

Tell me what you decided on either and I'll note it.
```

Notes are saved only when you ask a question, and your decision only if you share it. Where they're kept: [Your data](your-data.md).

---

## /chiron:roster

```
/chiron:roster [--domain <topic>]
```

Lists your advisors grouped by topic, including ones you built. `--domain strategy` filters to one topic.

```
/chiron:roster --domain strategy

strategy
  rumelt   Richard Rumelt   diagnosis, focus, competitive advantage
  thiel    Peter Thiel      startups, monopoly, contrarian bets
```

If one of your own advisors has a problem, the roster marks it and points you at `/chiron:lint <id> --explain`.

---

## /chiron:bench

```
/chiron:bench create <name> <id> <id> ... [--global] [--chairman <id>] [--depth quick|full]
/chiron:bench list
/chiron:bench remove <name>
```

Saves a council so you can call it by name. Names are lowercase letters, numbers and dashes. A council needs 2 to 8 advisors; Chiron warns above five.

- `--global` saves to `~/.chiron/benches.yaml` (every project). Without it, inside a project it saves to `.chiron/benches.yaml`.
- `--chairman <id>` has that advisor write the final recommendation instead of a neutral summary.
- `--depth full` makes the long answer the default.

Your first saved council replaces the six ready-made ones, so `create` offers to copy them in first. Removing a council never deletes advisors. Full details: [Councils](benches.md).

---

## /chiron:onboard

```
/chiron:onboard
```

A short guided start. It shows who's available, asks a few questions about what you're working on, suggests advisors and councils, and ends by running a real decision of yours. Building your own `me` advisor is offered, never assumed. You only need it once.

---

## /chiron:distill

```
/chiron:distill <who, in a line>
```

Builds a new advisor from someone's published work: a short interview, several minutes of research, writing the files with sources, then a check. It's saved where every Chiron command finds it: `~/.chiron/seats/<id>/`, or `.chiron/seats/<id>/` in a Cowork workspace or a sandboxed Codex project.

```
/chiron:distill "Brad Frost on design systems"
```

It won't build an advisor that speaks *as* a living person. It offers a sourced advisor *about* their work instead, or an invented advisor with its own name. Full guide: [Build an advisor](distilling.md).

---

## /chiron:distill-me

```
/chiron:distill-me [notes file or folder]
```

Builds a private advisor called `me` from your own goals, values and rules, so you can put yourself on a council or let it write the final recommendation. It asks before reading each source, interviews you to fill the gaps, and saves to `~/.chiron/seats/me/`. It never leaves your computer and is never shared. See [your own advisor](distilling.md#your-own-advisor).

---

## /chiron:lint

```
/chiron:lint [advisor-id | --all] [--strict] [--explain]
```

For people building or editing advisors. Checks an advisor's files against [the advisor standard](the-standard.md): enough sources, the required sections, no first-person imitation of a living person, all seven reference files. `--explain` describes each rule. `--strict` treats warnings as errors.

The same check runs from a shell and in this repo's CI:

```bash
python3 scripts/lint_seat.py --all
python3 scripts/lint_seat.py skills/munger --level strict --explain
python3 scripts/lint_seat.py --all --format json
```

Exit codes: `0` pass, `1` warnings, `2` errors (the advisor won't load).
