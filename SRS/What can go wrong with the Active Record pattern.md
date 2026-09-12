<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise #Persistence/ORM #Patterns/AntiPatterns #SRS

# What can go wrong with the Active Record pattern

> [!abstract] Short answer
> Active Record puts data access inside the domain object: it wraps a database row, owns its own `save`/`load`/finders, and carries business logic on top. It works well for simple domains, but it couples the domain model to the schema, drags a database dependency into unit tests, and pushes complex logic out into services - which is why many teams treat heavy use of it as an antipattern.

## The mechanics

Fowler defines Active Record as "an object that wraps a row in a database table or view, encapsulates the database access, and adds domain logic on that data". The class typically offers static finders, an instance `save`, and the business methods for that row. Each object knows how to read and write its own data - the most obvious approach, and the reason the pattern is easy to adopt. In DDD vocabulary, a rich row object is doing the job of [[What are aggregate aggregate root entity and value object in DDD]] while also being its own persistence layer.

```java
class Employee {
    private Long id;
    private String name;
    private Money salary;

    static Employee load(Long id) { /* SELECT ... */ }
    void save() { /* INSERT or UPDATE ... */ }

    // domain logic lives next to the persistence calls
    void raiseBy(int percent) {
        salary = salary.plus(salary.times(percent / 100.0));
        save();
    }
}
```

**Listing 1.** Conceptual Active Record shape: row mapping, database access, and a business rule in one class.

```d2
direction: right
ar: "Active Record" {
  width: 230
  height: 70
  style.fill: "#ffebee"
}
ardb: "database" {
  width: 160
  height: 60
  style.fill: "#ffebee"
}
dm: "Domain object" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
mapper: "Data Mapper\nmapper layer" {
  width: 190
  height: 80
  style.fill: "#e8f5e9"
}
dmdb: "database" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
ar -> ardb: "own SQL / ORM calls"
dm -> mapper: "independent of storage"
mapper -> dmdb
```

**Fig. 1.** Active Record binds the domain object straight to the database; Data Mapper keeps the two independent, which is the structural source of most Active Record complaints.

## The failure modes

* **Schema coupling.** The row-shaped object hardcodes the table's current columns; a schema change ripples into domain code, and storage design starts dictating the domain model.
* **Testability.** Because the object makes its own database calls, unit tests need a database, an in-memory substitute, or heavy mocking; there is no seam between logic and storage.
* **Anemic drift.** As logic grows, teams avoid putting it in the already-busy row object and accumulate transaction scripts around it; the domain model hollows out into getters and setters.
* **Complex associations.** The one-object-per-row mapping gets awkward for object graphs, inheritance hierarchies, and many-to-many relations; mapping machinery leaks into callers.
* **Hidden dependencies.** Static finders and self-saves cannot be injected or replaced, so callers are welded to a concrete persistence implementation.

## Where it still fits

Fowler's own framing is that Active Record is a good choice when the business logic is of simple transactional complexity and the mapping to tables is close to one-to-one. CRUD-heavy admin tools, small services, and frameworks built around the pattern get real productivity out of it; the problems above appear as the domain model and the schema drift apart.

> [!warning] "A JPA entity is an Active Record" is a popular lie
> JPA and Hibernate follow the Data Mapper idea: persistence goes through the `EntityManager`, which moves data between objects and the database while keeping them independent, and the entity class itself carries no save or load API. Adding repository-like methods to an entity moves it toward Active Record, but plain JPA entities are not that pattern - see [[How would you explain Hibernate]] for how the mapper layer sits between entities and the database.

The drift shows up downstream in web code: once entities both persist and carry logic, it is tempting to hand them to controllers, which is exactly the trap in [[Should you return JPA entities from a Spring controller]] - and lookups belong behind [[How do you get an entity by id in a Spring Boot REST service]] rather than inside the entity class.

> [!tip] Interview answer
> Active Record wraps one database row in an object that also owns its persistence and its business logic. What goes wrong: the domain model gets welded to the schema, unit tests need a database because there is no seam, and complex logic migrates into services, leaving anemic objects. It is fine for simple, CRUD-shaped domains, which is why it thrives in frameworks built around it. In the Java world JPA and Hibernate are Data Mapper, so I would not describe a JPA entity as Active Record.
