<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is domain driven design?

> [!abstract] Short answer
> Domain driven design (DDD) is an approach to software design introduced by Eric Evans in 2003 that models code around the business domain itself: teams partition the problem space into [[What is a bounded context and how do you identify one|bounded contexts]], build each model with the business experts' vocabulary ([[What is ubiquitous language and why does it matter|ubiquitous language]]), and implement it with tactical patterns such as entities, value objects, and aggregates ([[What are aggregate aggregate root entity and value object in DDD]]). The point is that the code structure mirrors how the business actually works, so rules live in the model instead of being smeared across service scripts.

## Strategic design vs tactical design

DDD splits into two halves, and interviewers care whether you know both. Strategic design decides where the boundaries are: you analyze the domain, split it into subdomains (core, supporting, generic), assign a bounded context to each, and keep a distinct model and language inside every context. Tactical design is the implementation layer inside one context: entities with identity, immutable value objects, aggregates as consistency boundaries, domain services for operations that do not belong to one entity, repositories for persistence, and domain events for what happened. Microsoft's Azure Architecture Center describes exactly this split: strategic DDD "ensures that your architecture remains focused on business capabilities", while tactical DDD "provides design patterns that you can use to create the domain model".

```d2
direction: right
problem: "Strategic design" {
  width: 250
  height: 110
  style.fill: "#e3f2fd"
}
sol: "Solution space" {
  width: 250
  height: 110
  style.fill: "#fff3e0"
}
code: "Tactical building blocks" {
  width: 250
  height: 110
  style.fill: "#e8f5e9"
}
problem -> sol: "one bounded context per subdomain"
sol -> code: "model each context with"
```

**Fig. 1.** DDD works top-down: strategic boundaries first, then tactical patterns inside each boundary.

## When DDD pays for itself

DDD has real modeling cost, so it is aimed at complex domains with many business rules and evolving vocabulary. The Microsoft guidance is blunt that DDD approaches "should be applied only if you are implementing complex microservices with significant business rules" and that simpler responsibilities like a CRUD service "can be managed with simpler approaches". A CRUD admin panel does not need aggregates; a freight-pricing or claims-processing engine does. Saying when NOT to use DDD is a stronger interview answer than reciting its patterns.

## What DDD is not

DDD is not a framework, not a database design method, and not a synonym for microservices. It predates the microservice wave by a decade: Evans' 2003 book ([[What is the blue DDD book]]) talks about layered architecture, not containers. You can apply DDD inside a modular monolith, and you can deploy a microservice whose inside has zero domain modeling. What ties them is boundary thinking: each bounded context is a natural candidate for a service boundary, which is why the pairing is so common in practice.

> [!warning] "We use DDD" while every rule lives in service classes
> A codebase with anemic data bags and fat transaction scripts is not DDD no matter how many folders are named `domain/`. The tell is where behavior sits: if entities are getters and setters and a "manager" service does all the thinking, you have [[What is an anemic domain model and is it useful|an anemic domain model]]. DDD means the model carries the invariants, not the orchestration layer.

> [!tip] Interview answer
> DDD is Evans' approach for taming complex business domains. Strategically you carve the system into bounded contexts, each with its own ubiquitous language shared with domain experts. Tactically you implement each context with entities, value objects, aggregates, repositories, and domain events so invariants live in the model. I would reach for it when business rules are the hard part of the system, and skip it for plain CRUD.
