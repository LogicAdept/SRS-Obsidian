<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# When should you not use domain driven design?

> [!abstract] Short answer
> Full DDD pays off when the domain is genuinely complex, evolving, and central to the business - a rich core subdomain with rules that change. It is a poor spend for simple CRUD systems, short-lived utilities, and generic subdomains the industry has already solved; there the modeling ceremony costs more than it returns. The honest middle path: apply the tactical parts that always help - value objects, aggregate thinking, ubiquitous language - without the full strategic machinery.

## The cost side of the ledger

DDD is an investment with running costs: workshops with domain experts to crunch the model, a maintained ubiquitous language, aggregate and context discipline, and the ongoing alignment of code with a shifting business picture. For a domain where "complexity" means a table with ten columns and a status flag, that machinery buys nothing - the rules fit in a page, and a straightforward transaction-script-plus-ORM stack ships faster and stays readable. The classification tool for deciding is the subdomain types themselves ([[What are the types of subdomains in DDD]]): build deep models for core, keep supporting light, buy or adopt for generic. A CRUD admin panel is generic; the industry sells it - modeling it is paying for differentiation you do not own.

```java
enum SubdomainType { CORE, SUPPORTING, GENERIC }

static String strategy(SubdomainType type) {
    return switch (type) {
        case CORE       -> "build with the best team, deep model, protect it";
        case SUPPORTING -> "build minimally, accept a lighter model";
        case GENERIC    -> "buy or adopt an off-the-shelf solution";
    };
}
```

**Listing 1.** Verified on JDK 21.0.12.1: the classification collapses to a decision - `strategy(GENERIC)` returns buy, which for most CRUD-shaped systems is the honest verdict, while `strategy(CORE)` justifies the DDD investment.

```d2
direction: down
q: "Is the domain complex, evolving,\nand differentiating?" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
full: "Core subdomain\nfull DDD: contexts, aggregates,\nubiquitous language, experts" {
  width: 320
  height: 100
  style.fill: "#e8f5e9"
}
tactical: "Simple or supporting\npick tactical pieces:\nvalue objects, aggregate thinking" {
  width: 320
  height: 100
  style.fill: "#e3f2fd"
}
none: "Generic subdomain\nbuy or adopt; no modeling" {
  width: 320
  height: 100
  style.fill: "#ffebee"
}
q -> full: "yes, central"
q -> tactical: "moderate"
q -> none: "no"
```

**Fig. 1.** The decision is graduated, not binary: full DDD for the core, tactical pieces where the domain is simple, and nothing at all where a product exists.

## The pieces that stay useful everywhere

Declining full DDD does not mean declining the vocabulary. Value objects are correct in any codebase - immutability and equality-by-value prevent whole bug classes regardless of domain complexity. Aggregate thinking - one transaction, one consistency boundary - prevents contention bugs in the plainest CRUD app. Ubiquitous language costs only agreeing on names. What a simple domain does not need is the strategic apparatus: context maps, multiple bounded contexts, event-driven inter-context integration, a modeling phase before every feature. The reverse mistake is as common: teams adopt "DDD" as a label, keep the layered-monolith structure, and call every service class a domain service - spending the vocabulary without buying the discipline, which produces neither speed nor model ([[What is an anemic domain model and is it useful]] is the usual endpoint). DDD also does not mean microservices: one bounded context can live happily in a modular monolith, and microservice sprawl without context discipline is just distributed entropy ([[What is domain driven design]] is the practice; the deployment style is a separate decision).

> [!warning] "DDD is always right" is the failure mode
> The dogma costs real projects: months of modeling for a system whose complexity was in the pipeline, not the domain; a context map for three screens and a table. The decision test cuts both ways - model the core deeply, and equally, do not run a five-person CRUD product through strategic design. And if the team cannot get regular access to domain experts, the central DDD activity - crunching the model together - cannot run at all; the ceremony without the collaboration is just slower code.

> [!tip] Interview answer
> I would not run full DDD where the domain is simple or already solved: CRUD admin tools, generic billing or identity - buy those, and keep only the tactical hygiene like value objects and aggregate boundaries. Full DDD - contexts, ubiquitous language, expert crunching - earns its cost on complex, evolving core domains. And DDD is not a synonym for microservices; the modeling discipline works in a modular monolith too.

