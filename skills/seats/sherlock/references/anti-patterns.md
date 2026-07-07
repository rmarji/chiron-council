# Anti-patterns — the Holmes method (corpus)

Everything the Sherlock Holmes canon warns against as a reasoning failure, with the canon's stated reasoning and the failure each produces. The subject is fictional; the canon is Arthur Conan Doyle's public-domain Holmes stories (1887-1927). Third-person; quotations short and attributed.

## Theorising before the data

**What it is.** Forming a hypothesis before the facts are gathered, then reading each new fact as confirmation of the hypothesis already held. **The canon's reasoning.** "It is a capital mistake to theorise before one has data. Insensibly one begins to twist facts to suit theories, instead of theories to suit facts" ("A Scandal in Bohemia," 1891). The word to notice is *insensibly* — the corruption is unconscious; the theorist does not feel themselves bending the evidence. **The failure it produces.** A conclusion that looks well-supported but was actually decided first and dressed in facts afterward. Every subsequent observation is filtered through the early theory, so disconfirming evidence is quietly discounted. **Outside crime.** The debugger who "knows" it is the cache and reads every log through that lens; the researcher who selects the studies that fit the thesis.

## Guessing dressed as inference

**What it is.** Producing a conclusion no chain of observation supports, and treating it as reasoning. **The canon's reasoning.** "I never guess. It is a shocking habit—destructive to the logical faculty" (The Sign of the Four, 1890). The objection is not that guesses are often wrong; it is that the *habit* degrades the faculty that produces real inferences. **The failure it produces.** A floating claim that cannot be tested or eliminated because it was never tied to evidence, which then contaminates the rest of the chain — you cannot eliminate what has no anchor. **Outside crime.** "It's probably a race condition" offered before any timing evidence; a confident diagnosis with no observable basis.

## Overlooking the trifles

**What it is.** Skipping the small physical details because they seem beneath notice, and reasoning only from the big, salient facts. **The canon's reasoning.** "It has long been an axiom of mine that the little things are infinitely the most important" ("A Case of Identity," 1891); "the world is full of obvious things which nobody by any chance ever observes" (The Hound of the Baskervilles, 1902). The trifles are unguarded and therefore honest, whereas the big narrative is curated. **The failure it produces.** The decisive fact is present in the scene but never enters the reasoning, because it was too small to be picked up. The case looks unsolvable when the answer was in plain sight. **Outside crime.** The exact byte count nobody checked; the one-character config difference; the timestamp ordering that a summary flattened.

## Mistaking the dramatic for the significant

**What it is.** Being pulled toward the lurid, loud, or bizarre feature and treating it as the key, instead of the *singular* feature that actually constrains the answer. **The canon's reasoning.** "As a rule, the more bizarre a thing is the less mysterious it proves to be" ("The Red-Headed League," 1891). The dramatic detail is often the least informative, and the genuinely puzzling cases are "commonplace, featureless" ones. **The failure it produces.** Attention and effort spent on the theatrical element while the quiet, load-bearing anomaly goes unexamined; sometimes the drama is deliberate misdirection. **Outside crime.** Chasing the scary-looking exception in the stack trace instead of the boring line that set up the state; being swayed by a vivid anecdote over the unglamorous base data.

## Dismissing the improbable too early

**What it is.** Discarding a surviving explanation because it is unlikely, even after elimination has ruled out the alternatives. **The canon's reasoning.** "When you have eliminated the impossible, whatever remains, however improbable, must be the truth" (The Sign of the Four, 1890). Improbability is a property of the answer in a hard case, not a disqualifier — the probable causes were exactly the ones already eliminated. **The failure it produces.** The investigation loops, re-examining ruled-out probable causes because it refuses to accept the improbable survivor, and never closes. **Outside crime.** "That can't be it, it's too weird" — said about the one explanation consistent with all the evidence.

## Trusting the account over the evidence

**What it is.** Building on the client's, witness's, or stakeholder's narrative as if it were the ground, rather than checking it against physical traces. **The canon's reasoning.** The method re-derives every case from observed evidence and treats the account as a claim to be verified — the whole practice of "the observation of trifles" ("The Boscombe Valley Mystery," 1891) exists because the curated story is unreliable while the unguarded detail is not. **The failure it produces.** A conclusion inherited from someone else's framing, complete with their errors and omissions, mistaken for an independent finding. **Outside crime.** Accepting the bug report's description of "what I did" as fact; taking a post-mortem's stated timeline without corroborating it against the logs.

## Certainty ahead of the evidence

**What it is.** Converting a balance of probabilities into a confident verdict the data cannot yet support. **The canon's reasoning.** Inference is "the scientific use of the imagination," valid only when anchored to "some material basis," and where observation is incomplete the method holds conclusions at the balance of probabilities (The Hound of the Baskervilles, 1902). **The failure it produces.** Acting on a provisional ranking as if it were proven, so that the next contradicting fact arrives too late to be admitted. **Outside crime.** Shipping the "obvious" fix before reproducing the failure; announcing a root cause that was the most likely candidate but was never actually confirmed.

## Under-stocking the ordinary

**What it is.** Lacking a broad baseline of commonplace knowledge, so that the singular feature of a case cannot be recognized as singular. **The canon's reasoning.** Singularity is defined only against the ordinary, and the method's edge depends on a well-stocked brain-attic of "furniture that he is likely to use" (The Five Orange Pips, 1891). **The failure it produces.** Anomalies pass unnoticed because everything looks equally unfamiliar; with no baseline, nothing stands out as the clue. **Outside crime.** The reviewer who has not seen enough normal cases to notice the abnormal one; the analyst who cannot tell a routine reading from an outlier.
