# Frameworks — the Holmes method (corpus)

The named procedures the Sherlock Holmes canon dramatizes, each with when-to-use, concrete steps, and a story citation, framed so they run on non-crime problems (debugging, research, investigation, reading a situation). The subject is fictional; the canon is Arthur Conan Doyle's public-domain Holmes stories (1887-1927). Third-person; quotations short and attributed.

## Framework 1 — Observe → infer → eliminate (the core procedure)

**Source.** The spine of the method, assembled from "The Science of Deduction" (A Study in Scarlet ch. 2, 1887; The Sign of the Four ch. 1, 1890), the data-before-theory rule ("A Scandal in Bohemia," 1891), and the elimination rule (The Sign of the Four, 1890).

**When to use.** Any case that must be read from evidence rather than taken on report: a bug whose symptom misleads, an investigation resting on an account, a research claim standing on thin data, a decision built on a story you cannot yet trust.

**Steps.**
1. **Observe.** Catalog what is actually observed — including the trifles a summary would drop (the cuff, the timestamp, the one out-of-order line). Physically list them. This is the "you see, but you do not observe" gate: force the data out of the glance.
2. **Quarantine the report.** Separate what was *observed* from what was *reported*. The client's narrative is input to be checked, not the ground to build on. Re-derive the problem from the physical traces.
3. **Withhold theory.** Refuse to form a hypothesis until the observation is reasonably complete — "a capital mistake to theorise before one has data." Notice and resist the pull to declare a cause early.
4. **Enumerate.** List every explanation the data admits, not the favorite. Give the singular and the improbable a seat at the table.
5. **Eliminate by test.** Strike out the impossible ones by disconfirming test, not by taste or convenience. The next test should try to kill the front-runner, not flatter it.
6. **Follow the remainder.** Whatever survives, however improbable, is the answer — commit to it and confirm it against the material basis before acting. Do not discard it for being unlikely; elimination has already earned it.

## Framework 2 — Reasoning backward (analytic reconstruction)

**Source.** A Study in Scarlet (1887, pt. 2, ch. 7): "In solving a problem of this sort, the grand thing is to be able to reason backward… There are fifty who can reason synthetically for one who can reason analytically."

**When to use.** When the outcome is already known and the cause is not — a failure that has happened, an artifact to be explained, a result you must account for. This is the opposite of forecasting.

**Steps.**
1. **Fix the result exactly.** State the outcome precisely, not approximately — the *exact* error, the *exact* end-state. Reasoning backward from a fuzzy result yields a fuzzy cause.
2. **Ask what was necessary.** For this precise result, what antecedent must have been true? Not "what could cause something like this," but "what had to be the case for *this*."
3. **Walk each link to a checkable fact.** Turn every necessary antecedent into a claim you can verify against evidence. Where a link cannot be checked, mark it as an assumption to test, not a conclusion.
4. **Reject forward-story temptation.** Do not narrate a plausible forward story and stop; that is synthetic reasoning wearing the answer's clothes. The analytic chain runs result → cause and must close on facts.

## Framework 3 — The absence audit (the dog that didn't bark)

**Source.** Silver Blaze (1892): the decisive clue is that the stable dog did not bark — "the curious incident of the dog in the night-time" — proving the visitor was known to it.

**When to use.** When a scene appears to offer no clue, when everything present looks consistent, or when an investigation has stalled on positive facts.

**Steps.**
1. **Build the expectation set.** Given the situation, list what you would *expect* to observe if things were normal — the alarm that should fire, the log line that should appear, the step someone should have taken, the reaction a person should have had.
2. **Check for absences.** Compare the expectation set against what is actually there. Each expected-but-missing item is a positive clue.
3. **Reason from the gap.** Ask why the expected fact is absent. In Silver Blaze the silence implies familiarity; generally, an absence implies a specific condition that suppressed the expected event. That condition is often the answer.

## Framework 4 — Singularity triage (where to dig first)

**Source.** "The Boscombe Valley Mystery" (1891, "Singularity is almost invariably a clue") and "The Red-Headed League" (1891, "the more bizarre a thing is the less mysterious it proves to be").

**When to use.** When a case has many features and limited time, and you must choose where to look.

**Steps.**
1. **Baseline the ordinary.** Know what a normal instance of this case looks like — this requires the stock of commonplace knowledge (the brain-attic). Without a baseline, nothing reads as singular.
2. **Find the singular feature.** Identify the one detail that does not fit the baseline, the anomaly the tidy story wants to explain away.
3. **Pursue it first, not last.** Treat the singular feature as the handle. Resist the instinct to filter the anomaly as noise; distinctive features constrain the cause-space and are the fastest way in.
4. **Distrust the featureless.** If a case is suspiciously ordinary and clean, apply *more* suspicion — the commonplace, featureless case is the genuinely hard one, and sometimes an engineered one.

## Framework 5 — Scientific use of the imagination (hypothesize, then anchor)

**Source.** The Hound of the Baskervilles (1902): "we balance probabilities and choose the most likely. It is the scientific use of the imagination, but we have always some material basis on which to start our speculation."

**When to use.** When you must generate candidate explanations (which requires imagination) but cannot yet reach certainty (which requires probability discipline).

**Steps.**
1. **Imagine freely.** Generate the full space of possible explanations without self-censoring for plausibility yet.
2. **Demand a material basis.** For each candidate, name the physical evidence it starts from. Discard any candidate with no evidential anchor — that is fantasy, not hypothesis.
3. **Balance probabilities.** Among anchored candidates, rank by likelihood given the evidence, and choose the most likely — while stating that this is a balance, not a certainty.
4. **Hold provisionally.** Where observation is incomplete, report the probability and the basis, and keep the ranking open to the next fact. Do not convert a balance of probabilities into a confident verdict the data cannot carry.
