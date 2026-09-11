<!--
reps: 0
priority: 0
-->
#Methodologies/BDUF #SRS

# How would you explain big design up front BDUF?

> [!abstract] Short answer
> BDUF means committing to a detailed, comprehensive design of the whole system before implementation starts: interfaces, data models, module boundaries and interaction flows are fully specified, reviewed, and frozen, and construction then follows the blueprint. It is the classical phased (waterfall-style) approach to design. Modern practice treats it as a trade-off: it buys early error detection and contractual clarity when requirements are genuinely stable, and it wastes effort - and locks in wrong decisions - when they are not.

## The mechanism and its logic

The reasoning behind BDUF is real: changes cost more later, so find problems on paper. In a phased process, requirements are signed off, architects produce a complete design (often with formal documents and review gates), and construction implements the plan. The benefit case is strongest where the problem is well understood, requirements are contractually fixed, integration points are external and hard to change (hardware, safety-critical systems, regulated interfaces), and the cost of a wrong runtime decision is catastrophic. Formal design review in that setting catches inconsistencies before they are cast in code.

```d2
direction: right
req: "Requirements\nsigned off" {
  width: 230
  height: 70
  style.fill: "#e3f2fd"
}
des: "Full design\nspecified and reviewed" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
imp: "Implementation\nfollows the blueprint" {
  width: 250
  height: 70
  style.fill: "#e8f5e9"
}
req -> des -> imp
```

**Fig. 1.** BDUF as a pipeline: knowledge is fixed in the design phase, and construction is expected not to alter it.

## Why agile practice rejects the full-strength version

Software discovery is unavoidable: teams learn what the system should be by watching parts of it work - users react to real software, not documents. BDUF defers that learning until after the largest decisions are locked, so speculative design gets built (and paid for) for features that never ship, and late requirement changes hit a design optimized for a different problem. XP's incremental design and the agile manifesto's "responding to change over following a plan" are the direct counters: design continuously, let the architecture evolve with evidence ([[What is overengineering and how does it affect enterprise software]]). A historical nuance worth quoting: even Winston Royce's 1970 paper - often cited as the waterfall source - argued for iterating the design against a first implementation, i.e. even the "original" waterfalls knew pure one-pass BDUF was risky.

> [!warning] "BDUF = any design before coding" is a strawman
> Nobody serious advocates zero design: every team sketches the architecture, picks boundaries, and thinks before typing. The debate is about completeness and freezing - whether the whole system must be fully specified before construction starts. Pretending the choice is "BDUF vs no design" is how discussions get stupid; the honest position is continuum, decided by requirement stability, cost of reversal, and how fast the team can get real feedback ([[What software development workflows or methodologies do you know]]).

> [!tip] Interview answer
> BDUF is the fully-specified, reviewed-and-frozen design phase before implementation - classic waterfall. I acknowledge where it wins: stable requirements, safety-critical or hardware-coupled systems where wrong decisions are unrecoverable. For most product software I prefer incremental design, because real learning starts when users touch working software, and BDUF optimizes for a requirements snapshot that will not survive contact with it.
