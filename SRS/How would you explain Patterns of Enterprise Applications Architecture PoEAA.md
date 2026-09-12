<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise #SRS

# How would you explain Patterns of Enterprise Applications Architecture PoEAA

> [!abstract] Short answer
> PoEAA is Martin Fowler's 2002 book "Patterns of Enterprise Application Architecture" and the catalogue it defines: around fifty named patterns for the typical enterprise workload - lots of complex data, business rules, and persistent storage - organized from domain logic and data source mapping up to web presentation, distribution, and session state. Its vocabulary is the ancestor of how Java developers talk about ORM and layering today.

## What the book covers

Fowler scopes enterprise applications explicitly: systems about the display, manipulation, and storage of large amounts of complex data plus automation of business processes - reservation, financial, and supply-chain systems - as opposed to embedded, telecom, or desktop software. The catalogue then splits into:

* **Domain Logic Patterns** - Transaction Script, Domain Model, Table Module, Service Layer: where business rules live.
* **Data Source Architectural Patterns** - Table Data Gateway, Row Data Gateway, Active Record, Data Mapper: how objects meet the database.
* **Object-Relational Behavioral Patterns** - Unit of Work, Identity Map, Lazy Load: how a mapping layer tracks changes and loads graphs.
* **Object-Relational Structural Patterns** - Identity Field, Foreign Key Mapping, Association Table Mapping, Embedded Value, Serialized LOB, and the Single/Class/Concrete Table Inheritance trio.
* **Object-Relational Metadata Mapping** - Metadata Mapping, Query Object, Repository.
* **Web Presentation Patterns** - MVC, Page Controller, Front Controller, Template View, Transform View, Two Step View, Application Controller.
* **Distribution Patterns** - Remote Facade, Data Transfer Object.
* **Offline Concurrency Patterns** - Optimistic Offline Lock, Pessimistic Offline Lock, Coarse-Grained Lock, Implicit Lock.
* **Session State Patterns** - Client, Server, and Database Session State.
* **Base Patterns** - Gateway, Mapper, Layer Supertype, Separated Interface, Registry, Value Object, Money, Special Case, Plugin, Service Stub, Record Set.

```d2
direction: right
dom: "Domain logic\nTransaction Script\nDomain Model\nService Layer" {
  width: 230
  height: 110
  style.fill: "#e3f2fd"
}
src: "Data source\nGateway, Active Record\nData Mapper" {
  width: 240
  height: 110
  style.fill: "#fff3e0"
}
orm: "O-R mapping\nUnit of Work, Identity Map\nLazy Load, Repository" {
  width: 250
  height: 110
  style.fill: "#e8f5e9"
}
web: "Web presentation\nMVC, Page Controller\nFront Controller" {
  width: 240
  height: 110
  style.fill: "#fff3e0"
}
dist: "Distribution\nRemote Facade\nData Transfer Object" {
  width: 230
  height: 110
  style.fill: "#ffebee"
}
base: "Base patterns\nGateway, Registry\nValue Object, Money" {
  width: 230
  height: 110
  style.fill: "#f3e5f5"
}
dom -> src
src -> orm
dom -> web
web -> dist
base -> dom: "support all layers"
```

**Fig. 1.** The catalogue mirrors a layered enterprise application: business logic on top, mapping underneath, presentation and distribution at the edges, with small base patterns reused everywhere.

## Why Java interviews care

Modern Java persistence is a direct implementation of the catalogue: Hibernate and JPA realize Data Mapper with Unit of Work, Identity Map, and Lazy Load, which is the subject of [[How would you explain Hibernate]]. Spring MVC is a Front Controller. The DTO vocabulary comes straight from the Distribution chapter - see [[How would you explain DTO Entity]]. The catalogue also frames the recurring trade-off between simple and rich domain designs: [[What can go wrong with the Active Record pattern]] evaluates the one pattern that blends domain logic with data access, while aggregates in [[What are aggregate aggregate root entity and value object in DDD]] refine the Domain Model side. None of this removes the need for layering discipline - [[What is layered architecture]] is the structural backdrop the book assumes.

> [!warning] PoEAA is not GoF
> GoF catalogues small object-structure patterns for any software; PoEAA catalogues architecture-level patterns for transactional, data-heavy systems. Answering "what is PoEAA" with singleton and factory is an instant credibility loss - the right move is to name the areas: domain logic, data source mapping, web presentation, distribution, offline concurrency, session state.

> [!tip] Interview answer
> PoEAA is Fowler's 2002 catalogue of enterprise application patterns: domain logic styles like Transaction Script and Domain Model, data source patterns like Data Mapper and Active Record, O-R mapping machinery like Unit of Work and Lazy Load, plus web presentation, distribution, and offline concurrency. I use its names daily without noticing - JPA is Data Mapper, Spring MVC is Front Controller, and DTO is its distribution pattern. It matters because it gives precise vocabulary for where business logic lives and how objects meet the database.
