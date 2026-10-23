---
title: Quickstart
nav_order: 2
description: "From installed to your first useful answer in about five minutes."
---

# Quickstart

This takes you from installed to a real answer on a decision you're facing, in about five minutes. Not installed yet? [Pick your app](installation.md) first; it takes a minute.

Examples use Claude's `/chiron:` commands. In Codex and ChatGPT, type the same request in plain words.

## 1. Ask about something real

Pick a decision you're actually weighing. Just say it:

```
should I raise my retainer from 8k to 15k a month, knowing the client might walk?
```

Or use the command, which does the same thing:

```
/chiron:consult "should I raise my retainer from 8k to 15k a month, knowing the client might walk?"
```

Chiron reads the question and tells you who it picked and why before it starts:

```
This is a pricing call that's hard to undo, so I'll ask three advisors
separately: Hormozi (offers), Voss (negotiation) and Munger (incentives).
It takes a minute or two, and you'll see me open their notes first.
```

For a cheap call you can easily undo, it often picks **one** advisor, or answers directly. That's on purpose: a whole council for a small choice wastes your time.

## 2. Read the answer

You get the same shape every time:

```
What they'd tell you
  Hormozi: If doubling the price scares you, the offer needs more in it.
    Add a named outcome and a guarantee, then raise. ($100M Offers)
  Voss: Don't defend the number. Ask "How am I supposed to make this work
    at 8k given what you now need from me?" (Never Split the Difference)
  Munger: First check what the buyer is personally rewarded for. A price
    that fights their incentives fails. (Poor Charlie's Almanack)

Where they disagree
  Voss says a stuck deal moves when the other side feels understood.
  Munger says fix the incentives first. Both positions are from their
  books, not invented.

What to do
  Raise to 15k this month, framed around the added outcome, and open with
  Voss's question instead of a flat demand.
  The catch: the incentive check takes a week you might not want to spend.
  How sure: 3 out of 5. If this client is most of your income, slow down.

Want me to remember what you decide, so these advisors can follow up next time?
```

What to look for:

- **A source on every point.** If an advisor can't point to where the idea comes from, it doesn't say it.
- **Real disagreement only.** Disagreements come from what the thinkers actually wrote. If there's none on record, Chiron says "They don't have a recorded disagreement on this" instead of inventing one.
- **One recommendation, with the catch.** No menu of options.

Want more detail? Ask "Give me the full reasoning from each advisor."

## 3. Say what you decided (optional)

Answer the last question with what you chose, for example "I'm raising to 15k from March." Next time you ask one of those advisors, it remembers. Ignore the question and nothing more happens. [Your data and memory](your-data.md) explains what's saved.

## 4. Try the other ways in

| You want | Type | In Codex or ChatGPT |
|---|---|---|
| One advisor you already have in mind | `/chiron:ask naval "salary or equity?"` | "Ask Naval: salary or equity?" |
| A saved group | `/chiron:council money "move the savings into index funds?"` | "Convene the money council: …" |
| To be worked through a decision until you commit | `/chiron:coach "I keep putting off the launch"` | "Coach me through this: …" |
| To see what you decided before | `/chiron:log munger --open-loops` | "What did Munger tell me before?" |
| To see who's available | `/chiron:roster` | "Which Chiron advisors do I have?" |

## 5. Make it yours (optional)

`/chiron:onboard` takes about five minutes. It asks a few short questions about what you're working on, builds two or three councils around your answers, and runs one real decision through them. In Codex and ChatGPT, say "set up Chiron for me".

Then:

- [Meet all 19 advisors](advisors.md)
- [Save your own councils](benches.md)
- [Add an advisor who isn't here](distilling.md)
- [Get more out of it day to day](getting-the-most.md)
