# Anti-Patterns — Rayo OS (documented failure modes)

These are not generic productivity warnings; they are his own logged failure modes, each with the reasoning and the specific counter his system prescribes. The catalog matters because the seat coaches by naming: when advising, cite the pattern by name rather than describing it vaguely.

## The front-of-loop trap (the master pattern)

Optimizing the front of the loop — deciding, researching, tooling, framework-building — while starving the back — shipping and telling. The front is comfortable: it is novel, low-stakes, and feels rigorous. The back is where value is realized and where rejection lives. The canonical tell is the sentence "I'll just build a tool/system for X." *Failure produced:* a growing arsenal of deciders and zero told outputs; excellent machinery, no luck surface, no feedback. *Counter:* the Ship Gate fires exactly at this tell — nothing new starts until one thing is told. Most of the patterns below are instances of this one. (Operating manual; ship-gate, 1-decide skill library.)

## Working in stealth

Building in private with no public version. *Reasoning:* Luck = Doing × Telling, so untold work has a luck surface of zero regardless of quality; stealth is expensive because it forfeits inbound, serendipity, and reputation compounding while costing nothing to fix. *Failure produced:* finished work nobody can respond to, hire from, or buy. *Counter:* EXTERNALIZE on offense — for every build, name the public version (write-up, demo, post) as part of the plan, not as an afterthought. (luck-surface, 4-tell skill library.)

## Open loops

Shipping without a feedback loop or a metric actually looked at. *Reasoning:* if it isn't measured, it isn't done — it's motion. An open loop teaches nothing and therefore cannot compound. *Failure produced:* effort that feels productive and accumulates no learning. *Counter:* define the loop before the build ("what's the loop, how fast can we close it, what does it teach?"), and flag any shipped-unmeasured item in review. (Compounding-lens practice.)

## MAX THREE breach and the shiny object

Taking on a fourth active thing, usually by rationalizing a distraction as an opportunity. *Reasoning:* the variety-seeking engine will always generate a plausible story for the new thing; the story is not evidence. *Failure produced:* every active thread gets slower and worse; nothing finishes. *Counter:* name the breach out loud, then run FATE — Fit exists precisely to kill shiny objects. A genuine opportunity displaces a current slot; it does not add one. (Carapace/ShipOS corpus; FATE, 1-decide skill library.)

## Perfecting the easy problem

Polishing the comfortable task to avoid the hard, scoreable one. *Reasoning:* effort is being spent, so it feels like work, but the effort is allocated by comfort rather than by value — Pareto inverted. *Failure produced:* beautiful low-stakes output, untouched decisive work. *Counter:* call it directly, then FRESH START discipline — the hard task first, with full resources. (Operating manual.)

## The system as shiny object (the meta-trap)

Rebuilding the operating system instead of doing the work the system exists to enable. *Reasoning:* this is the most seductive version of perfecting the easy problem, because meta-work masquerades as discipline — a new dashboard reads as commitment to shipping while being its opposite. *Failure produced:* version seven of the productivity system; version zero of the product. *Counter:* the Ship Gate does not exempt system work — a new framework, app, or matrix is deciding, not shipping, and does not open the gate. (ship-gate, 1-decide skill library.)

## Analysis as avoidance

Running another framework when the real block is emotional. *Reasoning:* his documented tell — a matrix is a socially acceptable place to hide from a feeling. The decision stack has a dedicated layer for this (CTFAR) precisely so the other tools don't get abused for it. *Failure produced:* immaculate scoring of a decision that stays unmade. *Counter:* route by stuck-shape; if the shape is "reacting, ruminating, avoiding," it goes to CTFAR, and if CTFAR itself becomes another matrix, name that and stay with the feeling. (route and CTFAR, 1-decide skill library.)

## Rumination on decided things

Re-litigating a call already made and logged, without new information. *Reasoning:* a decided thing has an address in the decision log; reopening it costs attention and settles nothing, because the reopening is driven by anxiety, not evidence. *Failure produced:* the same decision paid for many times. *Counter:* point at the prior logged decision and move; genuine new information reopens a decision, a mood does not. (Decision Log practice.)

## Rigging the matrix

Setting MCDM weights after seeing the scores, or scoring FATE to justify a call already made. *Reasoning:* the frameworks are honesty instruments; used backwards they become laundering instruments — the same gut call, now with false authority. *Failure produced:* confident wrong decisions that are harder to revisit because they look analyzed. *Counter:* weights before scores, criteria before scoring, and the standing rule that the numbers don't decide — they show what you already believe. If the winner feels wrong, fix the weights openly. (MCDM and FATE, 1-decide skill library.)

## Park-as-bury

Treating a parked opportunity as a killed one. *Reasoning:* park is a verdict with a mechanism — a revisit trigger and a date; without the trigger it is a slow no that was never honestly said. *Failure produced:* a graveyard of 6–8 scores nobody ever revisits, and eroded trust in the verdict system. *Counter:* every park gets a named trigger at scoring time. (FATE, 1-decide skill library.)

## Lifestyle inflation on runway

Letting spend drift upward while operating on a defined, finite runway. *Reasoning:* the default answer to a spending question is via negativa — what can be cut — because every recurring cost is a compounding tax on the runway that buys optionality. *Failure produced:* a shorter runway and forced decisions made from weakness. *Counter:* frame every spend as cash, time at the hourly baseline, opportunity cost, payback, and reversibility; push back on inflation by default. (Operating manual, standing money filter.)

## Busy-posting

Confusing volume of public output with luck surface. *Reasoning:* the surface is built from signal and specificity — work that shows how you think — not from posting cadence; and a wide surface with no CTA lets luck land and bounce off. *Failure produced:* noise, no inbound. *Counter:* one or two genuinely shareable items a week, process included, each with a clear way to reach you. (luck-surface, 4-tell skill library.)
