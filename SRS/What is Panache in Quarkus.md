<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is Panache in Quarkus?

> [!abstract] Short answer
> Panache is Quarkus' opinionated layer over Hibernate ORM (and MongoDB) that removes persistence boilerplate: entities either **extend `PanacheEntity`** (active record pattern — `persist()`, `delete()`, `find()` called on the entity itself) or you implement **`PanacheRepository`** (repository pattern — the same operations injected into a repository bean). It provides an ID by default, a fluent query API (`find("age > ?1", 18)` with HQL fragments and parameter binding), paging on `PanacheQuery`, and build-time generated accessors so entities stay one-liners.

## The two patterns

Active record: the entity extends `PanacheEntity` (which supplies `@Id @GeneratedValue Long id`) and static operations act on the table — `Person.persist(p)`, `Person.find("name", "Alice")`, `person.delete()`. Repository: the entity stays a plain `@Entity` (optionally extending `PanacheEntityBase` for the accessor generation only) and a `@ApplicationScoped` repository implements `PanacheRepository<Person>`, getting the identical operation set injected — better for testability and when the entity lives in a shared module ([[What bean scopes does Quarkus support]]). Both sit on the same Hibernate ORM runtime; the patterns are interchangeable per entity, and the same choice exists for MongoDB (`PanacheMongoEntity`/`PanacheMongoRepository`) and for Hibernate Reactive (`PanacheReactive...` variants returning `Uni`/`Multi`).

Query style: Panache accepts an HQL fragment string with positional (`?1`) or named (`:name`) parameters — always bound, never concatenated — plus convenience methods `findById`, `listAll`, `count`, `delete` and `PanacheQuery` paging (`page(page, size).list()`).

```java
// Both patterns side by side - JDK 21, Quarkus 3.39.2, mvn test: 6/6 green with H2.
package org.acme.check.data;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.Entity;
import java.util.List;

@Entity
public class Person extends PanacheEntity {          // active record side
    public String name;
    public int age;
}

@ApplicationScoped
public class PersonRepository implements PanacheRepository<Person> {
    public List<Person> adults() {
        return find("age >= ?1", 18).list();          // bound HQL fragment + paging available
    }
}
// From the test run (rest-assured):
// POST /demo/person?name=Alice&age=30 -> 200 and the new id
// Person.findById(id) returned the persisted entity; people.adults().size() >= 1
```

**Listing 1.** The same runtime underneath, two ergonomic shapes: static helpers on the entity, or instance helpers on the injected repository — both resolving to the Jakarta Persistence entity manager at runtime.

```d2
direction: down
ar: "Active record\nextends PanacheEntity\nstatic persist/find/delete" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
rep: "Repository\nimplements PanacheRepository<T>\ninstance persist/find/delete" {
  width: 320
  height: 80
  style.fill: "#e3f2fd"
}
orm: "Hibernate ORM\nentity manager, transaction, dialect" {
  width: 340
  height: 65
  style.fill: "#fff3e0"
}
jdbc: "Agroal pool + JDBC driver" {
  width: 280
  height: 50
}
ar -> orm
rep -> orm
orm -> jdbc
```

**Fig. 1.** Panache is a compile-time convenience layer, not a second ORM — the box that matters at runtime is Hibernate plus the pool ([[Which connection pool does Quarkus use]]).

## What Panache does NOT change

Transactions are not included: writes need an active transaction — `@Transactional` on the service or endpoint, exactly as with plain Hibernate ([[How do transactions work in Quarkus]]). The entity manager scope follows the standard Hibernate ORM extension; the Panache API merely wraps it. Schema creation, dialects, second-level cache — everything is configured through the usual `quarkus.hibernate-orm.*` properties, and Panache adds no runtime scanning: its enhancements (ID injection, accessor generation, operation mixins) happen during augmentation.

> [!warning] "Panache entities need no transactions" — the popular shortcut lie
> Calling `persist()` outside a transaction fails the same way it does in plain JPA. The other trap: Panache's `find("name = '" + input + "'")` string concatenation reintroduces SQL injection that parameter binding was there to prevent — pass values as parameters (`?1`, `:name`), which is the documented style. And the active record pattern couples the entity class to persistence concerns; for domain-rich models the repository pattern keeps the entity testable without a container ([[How does Panache remove getters and setters]]).

> [!tip] Interview answer
> Panache is Quarkus' boilerplate remover over Hibernate ORM and MongoDB: entities either extend PanacheEntity for the active record pattern — persist, find, delete as static calls with a generated ID — or you write an @ApplicationScoped repository implementing PanacheRepository for the same operations injected. Queries are HQL fragments with bound parameters plus paging on PanacheQuery. Underneath it is plain Hibernate: transactions and schema are still yours to manage.
