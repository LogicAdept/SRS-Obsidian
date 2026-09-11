<!--
reps: 0
priority: 0
-->
#Career/Experience #SystemDesign/Architecture #SRS

# What architecture did you use on past projects

> [!abstract] Short answer
> This behavioral-architecture question is answered by picking one representative project and telling its architecture as decisions: the shape (layered monolith, modular monolith, services), why that shape fit the constraints (team size, domain coupling, scale), what you would change now, and one concrete consequence of the choice. The interviewer is testing whether you can connect architectural choices to their causes and costs — not asking for a diagram recital.

## The narrative structure that works

The 2-minute shape: context (domain, team size, traffic scale — one sentence each), the architecture in one view (a layered monolith with a message bus; three services behind a gateway; modular monolith with domain packages), then two or three decisions told as tradeoffs — "we chose a modular monolith over microservices because the team was five people and the domain boundaries were still moving; the cost was discipline to keep module borders clean ([[What are coupling and cohesion and how do they affect maintainability]]), and the payoff was atomic deploys and one deployable to operate". Each decision gets the same triple: the alternatives considered, the deciding constraint, the consequence observed. The technical texture that makes it credible: how the modules communicated (in-process calls versus events — [[How does an aggregate persist and publish events without a distributed transaction]]'s outbox if used), how state was handled ([[What is the difference between a stateful service and a stateless service]]'s statelessness for the deployable units), where the data lived (one schema with module-owned tables versus per-service stores), and how the boundaries held up over time. [[How have you worked with databases and what are the tradeoffs of each approach]] is the data-layer twin of this answer — keep the two consistent.

```text
2-minute shape:
1 context  : domain | team size | scale (one line each)
2 shape    : "modular monolith: N domain modules, one deployable,
             event bus for cross-module async"
3 decisions: (choice, alternative, deciding constraint) x 2-3
4 consequence: one cost + one win, observed not theorized
5 reflection: what I would change now and why
```

**Listing 1.** The five beats of an architecture experience answer.

## The follow-ups and the traps

Expect depth probes: "why not microservices?" (need the organizational and distribution-cost reasons — [[Which kinds of projects benefit most from CQRS]]-style fit analysis applies to architecture styles too), "how did you keep module boundaries from rotting?" (enforced dependencies, code review against boundaries, architecture tests), "what broke at scale?" (the concrete bottleneck story — a database ceiling, a deployment bottleneck — and the fix), and "how did you test it?" (test pyramid shape per unit). The traps: name-dropping every pattern without a constraint that forced it (architecture tourism — [[What is overengineering and how does it affect enterprise software]] is the cautionary frame the interviewer is probing for); claiming a shape you cannot defend at depth (the follow-ups will find the edge); and blaming predecessors — even a legacy mess should be narrated as constraints and staged improvements ([[How would you briefly describe migrating a project to Java]]'s strangler framing is the constructive version). The preparation discipline mirrors the database question: pick two projects, write the shape, the three decisions, the consequences — rehearse them to two minutes each, and keep one honest failure story ready, because the reflective close is where credibility lands.

> [!warning] An architecture without a "why" is a confession
> Listing what the system looked like without the constraints that produced it signals you inherited it rather than shaped it. Every shape claim must survive one "why this and not the alternative" follow-up — prepare the deciding constraint for each.

> [!tip] Interview answer
> I pick one representative project and tell it as decisions: the shape in one sentence (modular monolith, N modules, event bus), why the constraints produced that shape (team size, moving domain boundaries), two tradeoff decisions with their observed consequences, and one thing I would change now. Specific numbers, honest costs, no pattern name-dropping.
