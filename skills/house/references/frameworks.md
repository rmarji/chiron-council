# Frameworks — the House method (corpus)

The named procedures the *House, M.D.* corpus runs, each with when-to-use, concrete steps, and source. These are operational — usable on a non-medical problem (a bug, an outage, a decision built on a shaky story) as readily as on the medical cases the show was written for. Third-person; the character is fictional and the series is the corpus.

## 1. The differential diagnosis loop

*Source:* the structural spine of every episode; taught explicitly in "Three Stories" (S1E21, 2005). A real clinical method the show dramatizes.

*When to use:* Any mystery with multiple candidate causes and incomplete, partly untrustworthy evidence.

*Steps:*
1. **Establish the findings.** Write down what is actually confirmed, and separate it hard from what is merely *reported*. Observed/measured data is evidence; a stated account is a claim (see the lie audit).
2. **Enumerate the differential.** List *every* candidate cause that could produce those findings — the obvious and the unlikely. Completeness is the discipline; the favorite is not privileged.
3. **Argue adversarially.** For each candidate, state what would have to be true for it to be the cause, and which single test would rule it in or (better) out. Run this with a team if you have one; the whiteboard exists so candidates are visible and attackable.
4. **Test to eliminate.** Run the cheapest, most decisive *disconfirming* test first — the one that could kill the front-runner, not the one that would flatter it.
5. **Treat to diagnose if stuck.** If no test is decisive under time pressure, start the therapy for the leading candidate and read the response (Framework 3).
6. **Update or discard.** If a result contradicts the diagnosis, the diagnosis is wrong — re-open the differential. Never edit the findings to preserve the theory.

*Non-medical translation:* a production outage — confirmed findings (error rates, logs, timestamps) vs reported story ("nobody deployed anything"); list every candidate cause; for each, the one query that would exclude it; run the cheapest exclusion first; if undiagnosable live, roll back the leading suspect and watch.

## 2. The lie audit

*Source:* the everybody-lies premise ("Pilot," S1E1, 2004; "Three Stories," S1E21, 2005).

*When to use:* When the account you're given is the main basis for a conclusion.

*Steps:*
1. **Mark claim vs evidence.** Go through the account and label each element: is this observed/corroborated, or asserted?
2. **Assume each claim may be false.** Not maliciously — self-serving, mistaken, or wishful counts. Ask "who benefits from this version, and what would it hide if it were wrong?"
3. **Find corroboration.** For each load-bearing claim, locate the physical evidence that confirms it independently.
4. **Test the uncorroborated.** Where no corroboration exists, treat the claim as unverified and design a test — or withhold the conclusion until one exists.
5. **Audit your own account too.** The most dangerous unverified narrative is usually the analyst's own ("Both Sides Now," S5E24, 2009).

## 3. Treat-to-diagnose (the diagnostic trial)

*Source:* recurring across the series; highest-stakes in "House's Head"/"Wilson's Heart" (S4, 2008). Real-medicine name: therapeutic trial / diagnosis ex juvantibus.

*When to use:* Time-boxed, high-uncertainty problems where no single test is decisive and waiting for certainty is itself costly.

*Steps:*
1. **Rank the differential.** Identify the single leading hypothesis.
2. **Check reversibility.** Confirm the intervention is either reversible or informative enough that its failure is worth the information and tolerable in cost.
3. **Intervene as an experiment.** Apply the treatment for the leading hypothesis, having pre-committed to what a "works" and a "fails" result each mean.
4. **Read the response as data.** Improvement corroborates; no change or worsening eliminates.
5. **Update, don't escalate.** If it fails, the diagnosis was wrong — re-open the differential. Do not add a second treatment for the same disproven diagnosis.

## 4. Occam vs zebra (parsimony with an anomaly-check)

*Source:* "Occam's Razor" (S1E3, 2004) for the razor; Woodward's "horses not zebras" aphorism and "You Don't Want to Know" (S4E8, 2007) for the override.

*When to use:* When a simple, common explanation is on the table.

*Steps:*
1. **Seek the unifying cause.** Find the one explanation (ideally one upstream error) that accounts for the most findings; prefer it to a theory needing several independent causes (Occam).
2. **List the residue.** Name explicitly which confirmed findings the simple answer does *not* explain.
3. **Judge the residue.** If the unexplained findings are real (not reported noise), the simple answer is incomplete — invoke Hickam's dictum (there may be two causes) or follow the anomaly to a rarer unifying one.
4. **Respect the base rate as a prior, not a verdict.** Start with the common cause ("it's never lupus"), but override the base rate when the evidence demands it (the one time it *is* lupus).

## 5. Running the differential on a non-medical problem

*Source:* generalization of the differential method; the corpus's Sherlock-Holmes framing licenses treating any problem as a case.

*When to use:* A bug, a business failure, a stalled project, a decision resting on a suspect story.

*Steps:*
1. **State the symptoms in evidence terms.** What is objectively observed (metrics, artifacts, timestamps) versus what is being reported by people with a stake?
2. **Run the lie audit** on the reported layer before trusting it.
3. **Build the differential** — every candidate root cause, not the convenient one.
4. **Design disconfirming tests** — for each candidate, the cheapest check that would exclude it.
5. **Treat-to-diagnose** where live testing is impossible: change one suspected variable and watch the system respond.
6. **Follow the anomaly** — the finding that no tidy story explains is usually where the real cause is hiding; do not round it away.
7. **Kill the theory, not the data** — when a result contradicts your working diagnosis, discard the diagnosis.
