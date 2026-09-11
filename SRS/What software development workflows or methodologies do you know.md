<!--
reps: 0
priority: 0
-->
#Methodologies #SRS

# What software development workflows or methodologies do you know?

> [!abstract] Short answer
> The map has three layers. Plan-driven families: waterfall/phased delivery and its modern softened forms. Iterative and agile families: Scrum (fixed sprints, roles, backlog), Kanban (flow, WIP limits), XP (engineering discipline - testing, pairing, continuous integration), under the Agile Manifesto's values. And practice-level methodologies that sit inside any process: TDD and BDD for driving work through tests and behavior, DDD for modeling complex domains, Design by Contract for explicit interfaces, BDUF as the plan-driven design pole. Knowing what each one changes - and what it costs - is the interview answer.

## The families, with their actual mechanisms

Waterfall/phased: requirements, design, implementation, verification, maintenance as sequential phases with sign-offs; its strength is contractual clarity, its weakness is learning arriving only at the end. Agile: the 2001 manifesto values individuals and interactions over processes and tools, working software over comprehensive documentation, customer collaboration over contract negotiation, responding to change over following a plan - "while there is value in the items on the right, we value the items on the left more". Scrum turns that into sprints and inspect-and-adapt events; Kanban into visible flow and pull; XP into the engineering practices agile frameworks mostly omit ([[How would you explain Test-Driven Development]]).

```d2
direction: right
plan: "Plan-driven\nwaterfall, phased" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
agile: "Agile umbrella\nScrum | Kanban | XP" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
prac: "Practice-level\nTDD, BDD, DDD, DbC" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
plan -> agile: "iterating replaces freezing"
agile -> prac: "any framework can adopt"
```

**Fig. 1.** Process families and practice-level methodologies are orthogonal axes: a Kanban team can run TDD and DDD; a waterfall program can too.

## The practice-level methodologies worth naming

TDD: tests drive implementation - red, green, refactor ([[How would you explain Test-Driven Development]]). BDD: the same loop at behavior level, with business-readable scenarios ([[How would you explain behavior driven development BDD]]). DDD: model complex domains with bounded contexts and a ubiquitous language ([[What is domain driven design]]). Design by Contract: explicit preconditions, postconditions, invariants between caller and callee ([[How would you explain programming by contract and preconditions]]). BDUF: complete up-front design - the plan-driven pole against which agile positioned itself ([[How would you explain big design up front BDUF]]). SOLID and the clean-code principles are the code-level layer under any of these ([[How would you explain the SOLID design principles as a set]]). The honest meta-answer: teams mix these deliberately - a Scrum team doing TDD inside DDD-modeled services is not a contradiction, it is standard.

> [!warning] Naming methodologies is not knowing them
> The failure mode is reciting labels without the trade: Scrum's fixed cadence buys predictability and costs responsiveness to interrupts; Kanban's flow buys flexibility and hides if there is no WIP discipline; TDD buys design feedback and costs initial velocity. Interviewers probe one level down - "what does Kanban cost you?" - to separate experience from vocabulary. The second trap: treating any of them as religion; every method assumes a context (team size, risk profile, requirement stability) and breaks outside it ([[What is overengineering and how does it affect enterprise software]]).

> [!tip] Interview answer
> I frame it as three layers: plan-driven (waterfall and phased delivery), agile (Scrum's cadence, Kanban's flow, XP's engineering practices - all under the manifesto's values), and practice-level methodologies - TDD, BDD, DDD, Design by Contract - that work inside any process. I always attach the trade-off each one makes, because a methodology name without its cost is just vocabulary.
