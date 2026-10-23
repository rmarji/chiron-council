---
title: Getting the most
nav_order: 8
description: "Habits that make Chiron useful week after week."
---

# Getting the most out of Chiron

Five habits make the difference between trying Chiron once and using it every week.

## 1. Match the effort to the stakes

| The decision is… | Do this |
|---|---|
| A fact, a lookup, or a technical question | Just ask your AI. No advisor needed, and Chiron will say so. |
| Small and easy to undo | Ask one advisor: `/chiron:ask voss "how do I word this follow-up?"` |
| Expensive or hard to undo | Call a council: `/chiron:council money "…"` |
| Part money, part people, part strategy | Call a council |
| You're not sure | Ask without naming anyone and let Chiron pick |

When you don't name anyone, Chiron tells you who it picked and why before it starts:

```
This is a small wording change you can undo, so I'll ask Voss alone.
```

```
This is a commitment that's hard to undo and touches pricing and incentives,
so I'll ask Hormozi, Munger and Naval separately. It takes a minute or two.
```

You can always override: "just ask Munger" or "make it a full council".

## 2. Save councils for the decisions you repeat

Skip the all-star team you'll never call. If you price work every month, keep a pricing council. If money is the recurring worry, keep a money council.

> Make me a council called pricing with Hormozi, Cialdini and Voss.

Keep it to 2 to 5 advisors who see the problem differently. More on [councils](benches.md).

## 3. Add the thinkers you already quote

The advisors that change your decisions are the ones you already reach for when you're stuck. Build those, one at a time:

```
/chiron:distill "Rory Sutherland on behavioural economics and marketing"
```

One person per run. Building four at once gives you four shallow advisors. See [Build an advisor](distilling.md).

## 4. Put yourself in the room (optional)

`/chiron:distill-me` builds a private advisor from your own goals, values and rules. Put it in the chair of a council and the final recommendation weighs the others against *your* priorities. It's private, stays on your computer, and only reads sources you approve. See [your own advisor](distilling.md#your-own-advisor).

## 5. Close the loop

When an answer ends with "Want me to remember what you decide…?", tell it. Then once a week:

```
/chiron:log munger --open-loops
```

That lists decisions you asked about and never made, and flags anything older than two weeks. Tell Chiron what you decided and it records it. Over time the log shows whether you followed the advice and how it turned out, which is worth more than any single answer.

## What it can and can't do

Chiron won't make you right. What it does is make you wrong less often: the advisors answer separately, so you don't get one model agreeing with itself five times; disagreements come from what the thinkers actually wrote; and the memory shows you your own track record.

Advisors can be wrong together, and a well-sourced position can still be the wrong call for your situation. Treat every answer as a strong argument to weigh. The decision is yours.
