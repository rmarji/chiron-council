---
title: Councils
nav_order: 5
description: "Ask a saved group of advisors the same question. Six come ready to use."
---

# Councils

A council is a saved group of advisors you ask together. Each advisor answers separately, without seeing the others, then you get one recommendation with the disagreement kept in. (In the files and commands, a saved council is called a *bench*.)

## Ready-made councils

Six work as soon as you install:

| Name | Who sits on it | Use it for |
|---|---|---|
| `money` | Munger, Naval, Hormozi | Pricing, savings, bets with real money |
| `deals` | Voss, Munger, Cialdini | Negotiations, counteroffers, contracts |
| `strategy` | Rumelt, Munger, Naval | Where to focus, what to stop, big plans |
| `relationship` | Deida, Terry Real | Recurring fights, hard conversations |
| `work-design` | Ferriss, Hormozi, Naval | How you spend your time and build your week |
| `shipping` | Rayo OS, Naval, Rumelt | Should you build this, and will you finish it |

Call one:

```
/chiron:council money "should I move my emergency fund into index funds?"
```

In Codex and ChatGPT: *Convene the money council: should I move my emergency fund into index funds?*

Some of these pairs disagree on record (Voss and Munger on how a stuck deal moves, Ferriss and Hormozi on how hard to work, Deida and Terry Real on repair). That's where a council is most useful.

## Make your own

The easy way is to ask:

> Make me a council called hiring with Munger, Voss and Kahneman.

Or use the command:

```
/chiron:bench create hiring munger voss kahneman
/chiron:bench list
/chiron:bench remove hiring
```

Add `--global` to make it available in every project. Add `--depth full` for a longer answer by default.

**Your first saved council replaces the ready-made six.** Chiron offers to copy them into your file first, so you keep them. To get the originals back later, delete your file.

A good size is **2 to 5 advisors**. One advisor isn't a council (use `/chiron:ask`). Six to eight works but gets noisy. More than eight is refused.

Pick advisors who see the problem differently. Two advisors from the same area mostly repeat each other.

## A few worth trying

```
/chiron:bench create detectives house sherlock columbo --depth full
/chiron:bench create risk taleb kahneman munger
/chiron:bench create launch paul-graham hormozi thiel
```

- **detectives** for a bug, a broken number, or a story that doesn't add up. Three different ways to find what's wrong.
- **risk** before a bet that's hard to undo.
- **launch** for what to build and how to sell it.

## When to use a council, and when not to

Use a council when the decision is **expensive or hard to undo**, touches **several areas at once** (part money, part people), or sits on a **known disagreement** between advisors.

For anything smaller, one advisor is faster and usually just as good. If you're not sure, ask without naming anyone and Chiron decides. It often says a council isn't needed, which saves you a couple of minutes.

## The file

Councils are plain YAML. You can edit the file directly; Chiron reads the same file.

```yaml
benches:
  hiring:
    seats: [munger, voss, kahneman]   # advisor ids, 2 to 8
    chairman: neutral                 # who writes the recommendation: "neutral" or an advisor id
    default_depth: quick              # quick (short answer) or full
```

| Where | Scope |
|---|---|
| `~/.chiron/benches.yaml` | Every project |
| `.chiron/benches.yaml` in a project | Just that project. Wins if the same name exists in both |
| `~/.chiron/benches.yaml` doesn't exist yet | The ready-made six from the plugin are used |

An older file at `~/.claude/chiron/benches.yaml` is still read, and the next save copies it into `~/.chiron/`. In Cowork the file lives in the workspace's `.chiron/` folder; see [Cowork](cowork.md).

Advisor ids are listed on [the advisors](advisors.md) page.

## Chair it yourself

If you've built your own `me` advisor with `/chiron:distill-me`, you can put it on a council and let it write the final recommendation, weighing the others against your own priorities:

```yaml
benches:
  founder-calls:
    seats: [me, munger, naval, rumelt]
    chairman: me
    default_depth: full
```

The other advisors still answer separately, and their disagreement stays visible, so you see exactly what you're overruling. See [Build an advisor](distilling.md#your-own-advisor).
