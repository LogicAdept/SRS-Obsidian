<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #SRS

# What is the Pure Fabrication principle in GRASP

> [!abstract] Short answer
> Pure Fabrication is a GRASP principle: when a needed responsibility does not naturally belong to any domain concept, invent a class that does not represent anything in the problem domain - fabricated purely to keep coupling low and cohesion high. Domain-driven design calls such classes services.

## When Expert fails, fabricate

Start from the conflict this principle resolves. Information Expert would put persistence on the sale: the sale holds its own data, so it is the expert on saving itself. But that assignment welds a domain object to JDBC, drags storage details into every domain class, and muddies the model. When the expert-based solution damages low coupling or high cohesion, the remedy is to fabricate a class that exists only in the design, not in the domain vocabulary.

```java
class Sale {
    // domain state and behavior only - no storage knowledge
}

class JdbcSaleRepository {                   // pure fabrication: no domain concept behind it
    private final java.sql.Connection connection;

    JdbcSaleRepository(java.sql.Connection connection) {
        this.connection = connection;
    }

    void save(Sale sale) {
        // INSERT INTO sales ... - the one home persistence logic lives in
    }
}
```

**Listing 1.** The repository represents nothing a business analyst would name in the domain; it exists so the sale stays clean and the persistence job has one focused, replaceable home.

```d2
direction: right
domain: "Domain concepts\nSale, Register, Product" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
fabricated: "Pure fabrications\nJdbcSaleRepository, CheckoutController" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
infra: "Infrastructure\nJDBC, HTTP, message broker" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
fabricated -> domain: speaks domain language
fabricated -> infra: speaks infrastructure language
```

**Fig. 1.** A fabricated class is a translator between two worlds: it is not a domain concept itself, but it keeps the domain concepts from touching infrastructure directly.

## Fabrications you already use every day

Once you see the shape, it is everywhere. Repositories, application-layer controllers, adapters, and message gateways are all fabricated classes, and most Spring stereotype components fit the description - the framework survey in [[What design patterns does the Spring Framework use]] and the stereotype comparison in [[What is the difference between Repository Component Controller and Service annotations]] are essentially a catalogue of pure fabrications. A use case controller is a standard example too: it represents nothing in the domain, yet keeps event coordination out of the domain objects - that double role is drawn in [[What is the Controller principle in GRASP]].

> [!warning] Over-fabrication drains the domain model
> Every job pushed into a fabricated service thins the domain objects; carried to the extreme, domain classes become getter bags and all logic lives in services - the anemic domain model dissected in [[What is an anemic domain model and is it useful]]. Fabricate when the Expert assignment would genuinely break coupling or cohesion, not by default; and when you do, check the result against the instinct of [[What is tell don't ask in object oriented design]] - a fabricated class should coordinate domain objects, not strip them of decisions they could make themselves.

> [!tip] Interview answer
> Pure Fabrication says: when a responsibility fits no domain concept - persistence, notifications, transaction handling - invent a class that exists purely in the design to keep coupling low and cohesion high. A JdbcSaleRepository is the textbook case, and DDD would call it a service. Repositories, controllers, and most Spring components are pure fabrications; the discipline is to fabricate only where Expert's answer would damage the design, otherwise the domain model drains into services.
