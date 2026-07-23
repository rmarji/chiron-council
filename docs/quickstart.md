# Quickstart

This gets you from an installed plugin to a real, sourced answer on a decision you actually face, in about ten minutes. There are two paths: a guided setup that meets the roster and builds around how you work, or a single command that reads your decision and routes it to the right mind.

Both assume the plugin is already installed in Claude Code or Cowork. If it is not, do [installation](./installation.md) first (about a minute), then come back here.

If you just want the fastest possible taste, skip to [Path B](#path-b-run-one-real-decision-about-2-minutes). If you want Chiron shaped around you before you lean on it, start with Path A.

## Path A: run `/chiron:onboard` (about 10 minutes)

`onboard` is the guided first run. It does the setup for you and ends on a real answer, not a tour. Run it:

```
/chiron:onboard
```

It moves through four steps, narrating each one before it acts:

1. **Meet the roster.** It reads which seats are installed and shows them grouped by domain, so you see who is in the box: Munger for incentives, Voss for negotiation, Naval for leverage, Rumelt for strategy, and so on. Eighteen seats ship by default.
2. **Distill you (optional, recommended).** It offers `/chiron:distill-me`, which reads what you point it at (your notes, your instruction files, this conversation), interviews you, and writes a private `me` seat holding your mission, values, goals, frameworks, and the experts you already reach for. If you would rather stay fast, it runs a five-question mini-version inline instead. Your `me` seat is private and local, gitignored, never shipped. See [distilling](./distilling.md) for the full flow.
3. **Starter benches.** From your go-to experts and the decision you named, it maps your experts to installed seats, offers to distill any you named that are not installed yet, and writes two or three starter benches (for example a `money` bench, a `strategy` bench, a `decisions` bench) as plain YAML you can edit by hand. See [benches](./benches.md).
4. **Your first real consult.** It runs the actual decision you gave it through the orchestrator, so onboarding produces a genuine, sourced answer.

By the end you have a roster you understand, benches built around your domains, optionally a `me` seat that can chair your councils, and one real decision already worked. Onboarding hands you the same three daily commands listed at the bottom of this page.

## Path B: run one real decision (about 2 minutes)

The faster path is to skip setup and hand Chiron a decision you are actually chewing on. `/chiron:consult` reads it and routes: it picks the single best seat, convenes a small council, or tells you no seat has standing and answers plainly. You do not name a seat; that is the point.

```
/chiron:consult "a client went quiet after my proposal. how do I phrase the follow-up so they re-engage without me sounding desperate?"
```

Chiron states its routing verdict first, so you can override before it spends anything:

```
Routing: this is a reversible phrasing call in a single domain (negotiation).
Not worth a council. Asking Voss alone.

▸ Voss (corpus)   confidence 4/5
  Do not chase. Send a short "no"-oriented message that gives them
  permission to disengage: "Have you given up on fixing this?" It lowers
  the pressure that is making them avoid you, and a reply defending the
  project is them re-selling themselves. Lead with a label, not a pitch:
  "It seems like the timing may have shifted on your end."
  (Never Split the Difference, 2016, chs. 5-7)

  What would change this: if they never engaged in the first place,
  this is a cold-open problem, not a re-engagement one.

Record your decision? (updates the seat's log)
```

Three things to notice. The verdict is explicit and cheap: a reversible, single-domain call gets one lens, not a summoned debate. The seat speaks in the third person about the corpus and cites a source for its claim. And it offers to remember what you decided, so next time it can reference the call you actually made. That is the "no council needed" gate working, and it is a feature: a council that convenes when it should not is decision theater and a token tax.

### When the same command convenes a council

Hand `consult` something expensive, irreversible, or cross-domain and it routes differently. Here it is a pricing move that is part offers, part negotiation, part incentives:

```
/chiron:consult "should I raise my retainer from 8k to 15k a month, knowing the client might walk?"
```

```
Routing: irreversible pricing call that straddles offers, negotiation,
and incentives. Convening Hormozi, Voss, and Munger (Voss and Munger
carry an authored disagreement on how a negotiation is actually won,
which bears directly on this). Neutral chair. Depth: quick. ~5k tokens.

▸ Hormozi (corpus)   confidence 4/5
  If a 2x price scares you, the offer is underdifferentiated, not
  overpriced. Raise to 15k and stack the value: a named outcome, a
  guarantee, and one or two bonuses that cost you little and are worth
  a lot to them. Price is a function of perceived value, not your costs.
  ($100M Offers, 2021)

▸ Voss (corpus)   confidence 4/5
  Anchor high, then let them talk you to the real number. Do not defend
  15k; ask "how am I supposed to make the economics work at 8k given
  what you now need from me?" and let the calibrated question do the
  work. Deals are decided emotionally and justified after.
  (Never Split the Difference, 2016, chs. 2-5)

▸ Munger Lens   confidence 3/5
  Before touching price, audit the client's incentives: what is the
  buyer personally rewarded for? A rate that fights their incentive
  structure fails no matter how the conversation feels. And do not move
  from need; the big money is in the waiting.
  (Poor Charlie's Almanack, 2005)

▸ authored disagreement · Voss vs Munger
  How a stuck deal is actually moved. Voss: relational, make them feel
  understood first ("tactical empathy... people do not act on their
  interests until they feel understood," Never Split the Difference,
  2016). Munger: structural, fix the payoff matrix first ("show me the
  incentive and I will show you the outcome," Poor Charlie's Almanack,
  2005). Both positions cited from the record.

▸ synthesis (neutral chair)
  Recommendation: raise to 15k, but re-anchor through value and a
  calibrated question rather than a flat demand.
  Dissent preserved: Munger would audit the buyer's incentives before
  naming any number, and would rather wait than move from need.
  What you lose: taking the incentive-first path costs you speed; the
  relational open may leave real money on the table.
  Confidence: 3/5. What would change it: if this client is your only
  runway, the reversibility is worse than it looks and Munger leads.

Record your decision?
```

## What the output actually guarantees

Every council follows the same shape, and each part is load-bearing:

- **Positions gathered in isolation.** Each seat forms its take from only its own files and its own memory, never seeing the others. The independence is structural, not a model told to "play the contrarian."
- **Confidence, one to five, per seat.** A 3 is not padded up to a 4 to look decisive.
- **A source per substantive claim.** Corpus seats trace each claim to a book, talk, or episode. If a seat cannot cite it, it does not say it.
- **Authored disagreement, or none.** Chiron surfaces only conflicts that are written in the seats' files, both positions cited from what the people actually argued. If no authored conflict fits the question, it says "No authored conflicts on record for this topic" rather than inventing one. Manufactured debate is the failure mode this exists to kill.
- **A synthesis that keeps the dissent.** The chair makes one pick, names who disagrees and why, and states what the recommended path costs you. It refuses to average the seats into mush.

More on why it is built this way is in [concepts](./concepts.md), and the depth bar every seat clears is in [the standard](./the-standard.md).

## The three you will use daily

Once you are set up, almost everything runs through these three, plus talking to it in plain language.

| Command | Use it when |
|---|---|
| `/chiron:consult "<decision>"` | You have a call to make and do not want to pick the expert yourself. Let it route: one seat, a small council, or "not worth a council." This is the default. |
| `/chiron:ask <seat> "<question>"` | You already know whose lens you want. One authored take, cited, with its memory of your past calls. Example: `/chiron:ask naval "should I take the salary or the equity?"` |
| `/chiron:distill "<description>"` | The mind you want is not in the room yet. It researches the subject's published corpus, writes a full cited seat, lints it, and drops it in as a live skill you can ask immediately. See [distilling](./distilling.md). |

And you do not have to use a slash command at all. Chiron's seats are native skills, so plain language works:

```
what would Munger say about this contract?
run this by my money bench
poke holes in my plan the way Taleb would
```

Ask for one mind by name and that seat answers. Ask for a bench and it convenes the council. The slash commands and live councils need the plugin (Claude Code or Cowork); the seats themselves auto-activate anywhere they are installed. If a name does not resolve or a council will not convene, [troubleshooting](./troubleshooting.md) covers it.

## Where to go next

- Curate your own line-ups: [benches](./benches.md)
- Add an expert, or put yourself in the room: [distilling](./distilling.md)
- Every command and flag: [commands](./commands.md)
- Running in Cowork specifically: [cowork](./cowork.md)
- Get more out of it day to day: [getting the most](./getting-the-most.md)
