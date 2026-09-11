<!--
reps: 0
priority: 0
-->
#SystemDesign/Architecture #SRS

# What is layered architecture

> [!abstract] Short answer
> Layered architecture organizes a system into horizontal tiers where each layer serves the layer above and depends only on the layer(s) below — canonically presentation, business/domain, and persistence/data. Each layer has one responsibility and a defined interface, so changes inside a layer do not ripple sideways. It is the default enterprise architecture because it maps to teams and to request flow; its risks are the pass-through trap (layers that only forward calls) and the monolith of the business layer holding all logic.

## The layers and their contracts

The classic separation, described by Fowler in the PoEAA tradition (presentation / domain / data source) and refined by the Azure architecture guidance's layered style: presentation renders and validates input; the business layer holds domain rules and use-case orchestration; the persistence layer talks to the database and maps rows. Two rules make it architecture rather than folder structure. First, dependency direction: layers call downward only — the domain does not know about HTTP or SQL details, which keeps the business logic testable without a web server or a database (the dependency-inversion flavor of [[How would you explain the Dependency Inversion Principle in SOLID]]-style design). Second, separation of concerns: a layer can be replaced or rewritten (swap the presentation framework, move the data source) without the others caring, because the contract is the interface. A request flows presentation → business → persistence and back; each hop translates to the next layer's vocabulary (DTOs, domain objects, rows). [[What is layered architecture]]-style designs range from strict layers (each layer sees only the one below) to relaxed (skip-through allowed, faster but more coupling).

```d2
direction: down
presentation: {
  label: "presentation\nHTTP / UI, input validation"
  width: 230
  height: 70
}
business: {
  label: "business / domain\nrules, use cases, orchestration"
  width: 230
  height: 70
}
persistence: {
  label: "persistence\nrepositories, SQL/ORM mapping"
  width: 230
  height: 70
}
db: {label: "database"; width: 120; height: 50}
presentation -> business: "calls down only"
business -> persistence: "interfaces"
persistence -> db
```

**Fig. 1.** Three canonical layers and the one-way dependency direction.

## Strengths, failure modes, and where it goes next

The strengths explain its ubiquity: it is understandable (a new developer knows where a change goes), it separates concerns by technical role, it maps to cheap organization (layers to teams), and it keeps frameworks at the edges. The documented failure modes are equally specific: the pass-through layer (a service method that only forwards to a repository adds ceremony without value — layers should earn their existence by holding logic), the business-layer junk drawer (every rule gravitating into one god-service — cohesion is a per-layer obligation, [[What are coupling and cohesion and how do they affect maintainability]] measures it), and leaking abstractions (DTOs and entities bleeding across boundaries until every layer knows everything). When the domain grows, layering alone stops scaling organizationally — splitting vertically by feature (modular monolith, then microservices) or separating read/write models (CQRS — [[How would you explain CQRS]]) are the standard next moves; migrating a legacy layered monolith incrementally is the strangler-fig play ([[How would you briefly describe migrating a project to Java]] uses exactly that). [[What is the difference between a stateful service and a stateless service]] intersects at the deployment layer of the same story.

> [!warning] A layer that only forwards is ceremony, not architecture
> If every business method is `return repository.findAll()`, the layer adds call depth and mapping code without owning a single rule. Either the layer holds real logic (validation, orchestration, invariants) or it should be thinned — layering is not free just because folders exist.

> [!tip] Interview answer
> Layered architecture stacks presentation, business and persistence tiers with one-way downward dependencies and per-layer responsibilities, so concerns stay separated and frameworks stay at the edge. It is the understandable default; its traps are pass-through layers, god-services and leaky boundaries — and when the domain outgrows it, I split by feature or adopt CQRS rather than fattening the middle.
