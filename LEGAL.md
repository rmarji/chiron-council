# LEGAL.md — Provenance Policy

Chiron ships **corpus-mode** seats: study aids built from published works, cited, spoken about in the third person. This document encodes the legal design constraints as enforceable rules. It is a policy, not legal advice; one hour of IP counsel reviews it before any paid tier ships.

## Why these rules exist

- **Right of publicity** (state law, ~35 states; e.g. Cal. Civ. Code §3344): commercial use of a person's name or identity without consent is actionable. The on-point fact pattern is *Young v. NeoCortext* (Reface) — celebrity names/likenesses used to sell app subscriptions.
- **Lanham Act §43(a)**: false endorsement where a product implies affiliation.
- **Digital-replica statutes** (TN ELVIS Act, California): target simulated persona and voice.
- **Copyright** (17 U.S.C. §102(b)): frameworks and ideas from books are not copyrightable; expression is. Paraphrase + cite is the safe lane; verbatim reproduction is not.

Market signal: Meta paid roughly $5M per celebrity for consented personas; the Carlin estate settled against an unauthorized AI doppelganger. Consent is the product; imitation is the liability.

## Risk tiers

Encoded in each seat's `provenance` block; the linter reads them.

| Tier | Who | Rule |
|---|---|---|
| T0 | Dead, pre-modern (Aurelius, Seneca) | Any mode. No constraints. |
| T1 | Dead, modern (Munger d. 2023 — CA post-mortem rights ~70 yrs) | corpus-mode. persona only with an estate license. |
| T2 | Living, not monetizing their persona | corpus-mode; L10 naming convention; alias defined. |
| T3 | Living, actively monetizing their persona (Hormozi, Lenny, Huberman, Attia) | corpus-mode ONLY. Never gate paid access on their name (M1). Never in marketing (M2). Priority licensing targets. |

## Hard rules (M-series)

- **M1 — No paid gating on a living person's name.** Sell "Strategy Bench," not "The Hormozi Pack." Lint cannot see your sales page; this lives here and in the release checklist.
- **M2 — No real person's name or photo in ads, sales pages, or social posts** implying endorsement. The repo README may state factual provenance ("heuristics drawn from Rumelt's *Good Strategy Bad Strategy*, cited") — factual attribution is not an endorsement claim — but keep it in-repo, not on the sales page.
- **M3 — Corpus seats speak in third person about the corpus and cite sources.** Enforced mechanically by lint L1/L7.
- **M4 — Every real-person seat carries a visible disclaimer block:**

  > *Independent study aid based on published works. Not affiliated with or endorsed by {subject}.*

- **M5 — Verbatim quotes limited to short attributed excerpts**; frameworks paraphrased. No chapter dumps in `references/`.
- **M6 — Archetype alias toggle.** Every T2/T3 seat defines an `alias` (e.g. a Hormozi-corpus seat aliases to "The Offer Architect") so a takedown request is a rename, not a rebuild.
- **M7 — Takedown protocol.** Requests from subjects (or estates) are honored within 7 days. Path: rename seat id and display_name to the alias, strip the subject's name from provenance-visible surfaces, keep the paraphrased frameworks (ideas are not ownable), note the change in the changelog. M6 makes this cheap by design.

## Why this is strategy, not just defense

Corpus-mode with rigorous citation is what makes seats *better* than persona cosplay — sourced heuristics beat vibes. And the licensed official-seats program (rev-share with living experts) turns the biggest legal risk into the distribution channel: one living expert blessing an official seat brings their audience with them.

## Contact

Takedown or licensing inquiries: open an issue titled `[provenance]` or email the maintainer. Requests from verified subjects are honored per M7.
