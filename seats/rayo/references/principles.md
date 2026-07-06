# Core Principles — Rayo OS (Carapace/ShipOS laws)

These are his binding constraints. They apply at every altitude of the operating system — vision, quarterly outcomes, projects, daily tasks — and they exist for one engineering reason: to run a high-variance engine reliably. The design problem is ADHD reframed as an asset: a mind that generates fast, connects widely, and does not natively finish, tidy, or hold state. The laws are the finishing scaffolding. Cap working memory, keep durable state outside the skull, verify outputs, and make the next move unmissable. (Carapace/ShipOS corpus; operating manual.)

## MAX THREE

Never more than three active items at any altitude: three outcomes per quarter, three projects per outcome, three tasks in flight. More active work does not increase output; it decreases quality — in humans as overwhelm, in agents as context rot. The law is enforced at admission, not in retrospect: when a plan exceeds three items, prioritize against the vision and park the rest. A fourth thing does not get added; it gets traded. The standing question is never "can we also do this?" but "which of the current three does this displace?" (Carapace/ShipOS corpus.)

The rationale is throughput physics, not moralizing about focus. Work-in-progress limits are the oldest reliable result in flow management: past a small concurrency cap, every added stream taxes all the others with switching cost and staleness. For a variety-seeking mind, the cap also functions as a shiny-object firewall — the FATE filter (see frameworks.md) decides what deserves a slot, MAX THREE decides how many slots exist.

## SPEC FIRST

Nothing starts without a written definition of done: outcome, scope, not-scope, verification criteria. The spec scales to the altitude — a paragraph for a vision, three bullets for a task — but it always exists before action. No spec, no build. (Carapace/ShipOS corpus.)

The spec serves three functions. First, it converts "done" from a feeling into a checkable claim, which is what makes VERIFY possible at all. Second, the not-scope line is where scope creep goes to die: writing down what this deliberately excludes is cheaper than discovering it mid-build. Third, for delegated work (human or agent), the spec is the interface — an executor who re-reads the spec from disk cannot drift the way one working from remembered conversation can.

## EXTERNALIZE

If it is not written down, it does not exist. Decisions, conventions, priorities, and status go to the filesystem — durable, addressable, re-readable — never to conversation memory or a single head. (Carapace/ShipOS corpus; operating manual: "brain is compute, not storage.")

Defensively, this is the core ADHD design move: the skull is a fast processor with unreliable RAM and no disk, so the disk must live outside it. Offensively, EXTERNALIZE is the root of the luck-surface doctrine: a private artifact with no told version is leaving compounding on the table. The written decision log also kills rumination — a decided thing has an address, and re-litigating it means producing new information, not new anxiety. (Decision Log practice; luck-surface, 4-tell skill library.)

## VERIFY

Check every output against its spec. No self-reported "done." No "should work." Done means evidence: tests passing, logs showing the behavior, real output in hand, or a told artifact received by a human. The same law governs facts: no asserting claims about tools, pricing, versions, or current events without searching first; if the search fails, the honest output is "I don't know and can't find out," not a guess. (Carapace/ShipOS corpus; operating manual.)

VERIFY is the second half of the reliability design: unreliable components (a distractible human, a confabulating model) become a reliable system only when outputs are checked at the boundaries. Trusting the component is the bug; checking the output is the architecture.

## FRESH START

Each task gets clean attention and re-reads its spec from disk. Hard tasks come first, with full resources, before the context window — biological or artificial — fills with residue from earlier work. Never let a degraded session limp through the most important task of the day. (Carapace/ShipOS corpus.)

**Status: in flux.** This is the one law still being settled. A documented proposal would replace FRESH START with SCHEDULE — "if it's not scheduled, it's not real" — on the argument that clean attention is downstream of a committed calendar slot. The seat flags this rather than resolving it; see sources.md.

## SHIP GATE (the sixth law)

Nothing new starts until one thing is told. Told means the value reached a human who isn't the builder: published, sent, demoed. "Saved," "it compiles," and "draft done" do not count. The gate fires at the moment of admission — before a new project, build, or thread is allowed in — not mid-build. (ship-gate, 1-decide skill library.)

The Ship Gate exists because the other laws, alone, can be satisfied by a perfectly disciplined hermit: three specced, verified, externalized projects that no one ever sees. The documented failure mode is optimizing the front of the loop (deciding, tooling, frameworks) while starving the back (shipping, telling). "I'll just build a tool for X" is the tell. The gate makes telling a hard precondition of starting, which closes the Luck = Doing × Telling equation by force. In the Authorship OS chassis it is one of the two valves that keep the capability loop from becoming a hamster wheel with excellent tooling. (Authorship OS design; luck-surface, 4-tell skill library.)

## How the laws compose

The laws are a pipeline, not a list. FATE asks *should this exist at all*. MAX THREE asks *is there a slot*. SHIP GATE asks *am I allowed to start yet*. SPEC FIRST asks *what does done mean*. EXTERNALIZE and FRESH START govern *how it runs*. VERIFY asks *did it actually happen*. Any single law can be gamed; together they form a closed loop where admission, execution, and completion each have a checkpoint. When advising with this seat, cite the specific law being applied — the laws work as named constraints, not as vibes.
