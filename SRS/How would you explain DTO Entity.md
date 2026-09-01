<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #Patterns/Enterprise #SRS

# How would you explain DTO Entity?

> [!abstract] Short answer
> An **entity** is a **persistent domain object**: `@Entity`, **primary key**, managed in a **persistence context**, mapped to tables, with associations that may be **`LAZY`**. A **DTO / Transfer Object** is a **serializable snapshot** for one **boundary** call (HTTP, remote facade). It has **no** persistence identity and **no** lazy proxy. Do **not** return entities from a REST controller: map to a DTO so the API does not expose the schema, secrets, or unfetched associations. DTO: [[How would you explain DTO]]. Abstract entities: [[Can a JPA entity class be abstract]]. Lazy access after the context ends: [[How would you explain LazyInitializationException]].

## Persistence identity vs a wire snapshot

**Entity.** Lightweight persistent domain object. Must be a non-`final` class (not a record/enum/interface) with a public or protected **no-arg** constructor. Persistent state is fields or JavaBean properties; clients should use methods, not poke fields. **Every entity has a primary key.** Inside a persistence context it is **managed** (identity unique, state synchronized). After commit/close/serialize it is **detached**: state is **no longer** guaranteed to match the database. **Available** detached state is only non-`LAZY` attributes and what was already fetched. Navigating an unfetched lazy association outside the context is unsafe (Hibernate throws `LazyInitializationException`). Hibernate name: [[What is LazyInitializationException]].

**DTO.** Built to **cross a process**: one coarse payload, copied from entities by an assembler. No `EntityManager`, no `@Id` contract, no `LAZY` graph. Public fields or getters; often immutable. Mutating a DTO does not `flush` anything.

**Why map.** Serializing an entity to another tier **is** how you get a detached entity. That still carries mapping (`@Column`, `@OneToMany`), **unfetched** associations, and fields you never wanted on the wire (`passwordHash`). JSON then **is** your table shape. A DTO lists the **API** attributes only. Schema changes stay behind the assembler.

```d2
direction: down
rest: "REST / remote client" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
dto: "CustomerTO\nid, email only" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
ent: "@Entity Customer\nid, email, hash, orders LAZY" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
db: "tables" {
  width: 100
  height: 36
}
rest -> dto
dto -> ent: "assembler (not the entity itself)"
ent -> db
```

**Fig. 1.** The wire speaks DTO. The persistence context speaks entity.

```java
// Conceptual: entity mapping needs jakarta.persistence

@Entity
class Customer {
    @Id
    String id;
    String email;
    String passwordHash;

    @OneToMany(fetch = FetchType.LAZY)
    java.util.List<Order> orders;

    String getId() {
        return id;
    }

    String getEmail() {
        return email;
    }
}

final class CustomerTO {
    public final String id;
    public final String email;

    CustomerTO(String id, String email) {
        this.id = id;
        this.email = email;
    }
}

class CustomerAssembler {
    static CustomerTO toTO(Customer c) {
        return new CustomerTO(c.getId(), c.getEmail());
        // do not touch orders here unless you fetched it on purpose
    }
}
```

**Listing 1.** Conceptual. `CustomerTO` is the HTTP body. `orders` stays in the persistence context unless the assembler loads it.

| | Entity | DTO |
| Role | Persistent domain object | Transfer snapshot |
| Identity | Primary key + persistence context | None (or a copied id **field**, not managed) |
| Lifecycle | new / managed / detached / removed | Created for the call, discarded |
| Associations | `@ManyToOne` / `@OneToMany`, often `LAZY` | Nested TOs you **chose** to copy |
| After the transaction | Detached; lazy may be missing | Plain object; all fields you set are there |

> [!warning] A detached entity is not a DTO
> Passing `@Entity` by value to another tier **detaches** it. Unfetched `LAZY` state is not safely readable. `merge` later is an entity operation, not “update the DTO.” Treat that type as persistence, not as your API model.

> [!warning] Returning `@Entity` from a controller couples JSON to the table
> Column names, bidirectional graphs, and secrets ride along. Jackson walking `orders` can trigger lazy loads or infinite recursion. Map explicitly.

> [!warning] Do not make the entity **extend** the DTO for a public API
> That old “entity inherits transfer object” trick duplicates attributes so the bean can `getData()`. It still binds the persistence type to the wire type. When the JSON shape changes, the table mapping wants to change with it.

> [!tip] Interview answer
> An entity is a JPA persistent object with a primary key, managed in a persistence context, and mapped to the database, including lazy associations. A DTO is a serializable copy of the data you are willing to send across a boundary. Do not return entities from REST: map to a DTO so the API does not expose the schema, lazy graphs, or fields that must stay on the server.
