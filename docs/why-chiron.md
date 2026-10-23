---
title: Why Chiron
nav_order: 14
description: "Why sourced advisors beat generated personas."
---

# Why Chiron

This page is the long-form case for Chiron: why it exists, how it differs from a stock AI council, and why the advisor standard matters. To get it running, start with the [quick start](quickstart.md).

## The problem

**Most "AI advisor" tools are one model wearing name tags. Chiron is the opposite.**

You make expensive, irreversible calls alone, and a single model tends to agree with you. Across 11 leading models, one study found AI affirmed users' actions 49% more often than humans did, including when the user described deception or harm ([Cheng et al., "Sycophantic AI decreases prosocial intentions and promotes dependence," *Science*, 2026](https://doi.org/10.1126/science.aec8352)). That makes an agreeable chatbot a poor advisor for a decision you cannot take back. Bolting a "board of advisors" onto that rarely helps: it is five voices of one model nodding along, or celebrity labels with nothing behind them.

Chiron is authored the other way. Each **seat** is one mind, built only from what that person actually published, cited claim by claim, and held to it by a linter that fails the build on thin sourcing or any seat that impersonates a living person. Seats carry **authored disagreements** taken from the record, so convening a council surfaces real conflict instead of polite agreement. It is the board you cannot otherwise afford, and it will tell you what you do not want to hear.

## Why Chiron, not a stock council

The AI-council space is crowded, and almost all of it fails the same few ways. Chiron is built as the answer to each.

- **Authored, not generated.** Many tools generate a "mind" from any input over a weekend. Chiron seats are hand-authored and curated: quality and trust over quantity and speed.
- **Cited, not vibes.** Every substantive claim points at a source, and `scripts/lint_seat.py` fails the build on any seat that skimps on provenance. The lint is the standard, not a suggestion.
- **Real disagreement, not manufactured.** Many tools fake conflict by assigning opposing archetypes ("you be the contrarian"). Chiron surfaces only conflicts authored from what the people actually argued, both positions cited. If none exist for your topic, the council says so instead of inventing one.
- **It routes itself.** `/chiron:consult` reads your decision and picks the right expert, convenes the right few, or tells you it is not worth a council at all. No hunting through a roster, no summoning a debate for a call you could make in your sleep.
- **Memory.** Seats keep a private log. They remember what they told you, and whether you listened.

## The standard is the point

`scripts/lint_seat.py` is stdlib-only Python, and this repo's CI ([`.github/workflows/ci.yml`](https://github.com/rmarji/chiron-council/blob/main/.github/workflows/ci.yml)) runs the same file on every push and pull request, so the seat standard is enforceable by anyone, not just inside one app.

```bash
python3 scripts/lint_seat.py --all                  # exit 0 pass / 1 warns / 2 errors
python3 scripts/lint_seat.py skills/munger --explain
python3 scripts/registry.py --json                  # roster index
```

It hard-fails first-person impersonation of anyone living (L1), fewer than three sources (L4), and shallow or missing reference sets (L12). That is what makes a seat a seat and not a name. The full rule table and the anatomy of a seat are in [the standard](the-standard.md).

## On corpus mode and provenance

Real-person seats speak in the third person about the corpus ("the Munger corpus would flag...") and cite a source per claim. There is no first-person imitation of anyone living; the linter hard-fails it. This is not only legal hygiene, it is the reason sourced rules of thumb beat a generated imitation. Every real-person seat is an independent study aid based on published works, not affiliated with or endorsed by its subject. See [LEGAL.md](https://github.com/rmarji/chiron-council/blob/main/LEGAL.md) for the provenance policy and takedown protocol.
