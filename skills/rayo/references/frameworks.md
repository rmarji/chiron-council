# Frameworks — Rayo OS

The named, stepwise procedures. Each entry: when to use, concrete steps, and the pitfalls his own docs flag. Attribution is to the framework's home in his skill corpus.

## Decision routing (the dispatcher)

*When to use:* a decision is on the table but the shape is unclear ("help me decide," "I'm stuck on," "should I"). Diagnose the stuck-shape first, then run exactly ONE tool — running several frameworks on one decision is itself a named pitfall.

| Stuck-shape | Route to |
|---|---|
| New opportunity, "should I pursue?" | FATE |
| Many known options, must choose one | MCDM (AHP pairwise for close finalists) |
| Big values-level life decision | OOC-EMR |
| Emotionally stuck, reacting, avoiding | CTFAR |
| About to start something new | Ship Gate |
| Reversible and trivial | kill the matrix, pick at random, move |

Second pitfall: defaulting to a matrix when the real block is emotional — that is CTFAR's job, not MCDM's. (route, 1-decide skill library.)

## FATE scoring (opportunity go/no-go)

*When to use:* any new opportunity, deal, project, or commitment competing for time. Not for choosing among options already committed to (that is MCDM).

*Steps:* score each dimension 1–3, max 12:

- **Fit** — matches skills, identity, and current declared outcomes. This dimension exists to kill shiny objects: exciting-but-adjacent scores a 1.
- **Asymmetry** — capped loss plus uncapped or compounding gain (the Taleb/Naval dimension).
- **Timing** — a specific trigger that makes it viable *now*, not last year, not next year. "Anytime" is a low score.
- **Effort** — true cost in hours, attention, and capital, priced at the defined hourly baseline (GHR) including opportunity cost.

*Verdicts:* **≥9 pursue · 6–8 park · ≤5 kill.** Park means a revisit trigger with a date, not a soft no and not a burial. Any single dimension at 1 is flagged for explicit override rather than auto-killing the whole score. Give one line of why per dimension; the lowest score is the thing to watch.

*Pitfalls:* scoring to justify a call already made (name the criteria before scoring); using a high FATE to skip the Ship Gate (a "pursue" still doesn't permit starting until one thing is told); treating park as kill. (FATE, 1-decide skill library.)

## MCDM (weighted multi-option choice)

*When to use:* choosing among multiple known options — tools, vendors, hires, designs, locations. Not for a single go/no-go (FATE) or a values-level life call (OOC-EMR).

*Steps:* (1) list the options; (2) list the criteria; (3) **set weights BEFORE scoring** — this ordering is the honesty mechanism; (4) score each option per criterion 1–5; (5) weighted sum, rank; (6) sensitivity check: would small weight changes flip the winner? If yes, the race is close — run AHP pairwise comparison on the finalists.

*Governing rule:* the numbers do not decide; they show what you already believe. If the winner feels wrong, the weights are wrong — fix the weights openly rather than fudging scores. *Pitfalls:* setting weights after seeing scores (rigging the matrix); silently overriding the math. (MCDM, 1-decide skill library.)

## OOC-EMR (values-level decisions)

*When to use:* career moves, relationships, where to live — decisions too deep for a scorecard, where the criteria themselves are in question.

*Steps:* **O**utcomes — name what is actually wanted, the real goal underneath the decision; **O**ptions — generate more than the obvious two; **C**onsequences — upside and downside per option, weighted by probability; **E**valuate against the named outcomes; **M**itigate — the step most people skip: blend options to keep the upside and shave the downside, because the answer is rarely pure A vs B; **R**esolve — decide and commit.

*Pitfalls:* forcing a binary by skipping Mitigate (the blend is usually the answer); deciding before naming the real Outcome, which optimizes the wrong thing. (OOC-EMR, 1-decide skill library; framework origin: Tony Robbins' OOC/EMR process, marked as an external influence.)

## CTFAR (the emotional layer)

*When to use:* emotionally stuck, ruminating, reacting, or avoiding — the states where running another matrix is itself the avoidance.

*Steps:* **C**ircumstance — camera-only facts, no adjectives, no interpretation; **T**hought — the story told about the C (the hook lives here); **F**eeling — what the thought produces; **A**ction — what the feeling drives, including inaction; **R**esult — what the action creates, usually proving the thought. Find the T driving the loop, then test it.

*Pitfalls:* writing interpretation into C (camera-only, or the whole chain tilts); using the analysis to dodge the feeling — his own documented tell. If CTFAR is becoming another matrix, name that and stay with the F. Once unstuck, route back to the dispatcher and make the actual call. (CTFAR, 1-decide skill library; framework origin: the CTFAR/self-coaching model, marked as an external influence.)

## Ship Gate (the admission procedure)

*When to use:* at the moment of admitting anything new — a project, build, or thread — especially on the tell "I'll just build a tool for X."

*Steps:* (1) name the candidate; (2) check the gate: any active thread with an untold output? If yes, gate CLOSED — the candidate parks; (3) open the gate by shipping one untold thing, stating who received it and where; (4) log `told: what · who · where · date`; (5) admit the candidate, still subject to FATE and MAX THREE.

*Definition:* told = value reached a human who isn't the builder. Published, sent, demoed. "Saved," "it compiles," "draft done" do not count. *Pitfalls:* counting "built the decider" as shipping (a new framework or matrix is deciding, not shipping); gaming "told" with a throwaway post nobody was meant to receive. (ship-gate, 1-decide skill library.)

## The Compounding Lens (plan review)

*When to use:* every plan or build, before committing effort. Four checks, each with an action: **luck surface** (no public version → add one: write-up, demo, post), **feedback loop** (no metric → define the loop before the build), **compounding test** (tomorrow-harder option loses to tomorrow-easier even when smaller), **reversibility** (match the diligence bar to the bet; unclear reversibility is treated as irreversible). (Compounding-lens practice; luck-surface, 4-tell skill library.)

## Luck Surface (the weekly telling practice)

*When to use:* after a build-heavy stretch where a lot got done and little got told — the Ship-Gate-red weeks.

*Steps:* (1) list the week's untold doing (builds, learnings, decisions); (2) pick the one or two most shareable — the ones that show how you think; (3) tell them publicly, in your own voice, process included; (4) make yourself reachable: a clear CTA on each piece; (5) read what inbound the surface caught.

*Pitfalls:* confusing busy-posting with luck surface (it is signal and specificity, not volume); a wide surface with no CTA (luck lands and bounces off); telling only wins — the process is what compounds trust. (luck-surface, 4-tell skill library.)

## Authorship OS (two loops, two valves)

*When to use:* treadmilling — shipping constantly with no felt renewal — or designing how a productivity system or coach should behave.

*Structure:* a **capability loop** (Declare → Encode → Externalize → Ship) that compounds output, and a **meaning loop** (People → Craft → Renew) that compounds the life. Two valves connect them: the **Ship Gate** on the reinvest path (nothing new starts until one thing is told) and the **Dividend Policy** on the distribute path (a fixed cut of every win is spent on the life the same week it lands, written down, not deferred). Remove either valve and the capability loop becomes a hamster wheel with excellent tooling. The apex is authorship: the machine serves the writing, not the pen. (Authorship OS design session, OS corpus.)
