<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise #Java/OOP #Java/Serialization #SRS

# How would you explain DTO?

> [!abstract] Short answer
> A **DTO (Data Transfer Object)**, in Java EE usually a **Transfer Object**, is a **serializable data carrier** for a **coarse-grained** call across a **process or network boundary**. You fill it once, pass it **by value**, then read fields locally — instead of many remote getters. It is **not** a domain entity and **not** a DDD value object. Members may be public fields or accessors; setters are optional (immutable copy vs updatable copy). Today the same idea is a JSON body on a REST call. vs entity: [[How would you explain DTO Entity]]. vs value object: [[What is a value object and why should you use one]]. JPA type: [[Can a JPA entity class be abstract]].

## One payload instead of chatty remotes

A remote interface call is expensive. Java methods return **one** value, so you cannot return “all the attributes” as a handful of primitives. A DTO **batches** those attributes into one object that can be serialized across the connection. The server (session bean, facade, resource method) **constructs** the DTO, **copies** values from domain/persistence objects, and returns it. After that, getter calls are **local**.

An **assembler** (or mapping code) sits on the server: domain objects stay behind the boundary; the DTO is the contract of the wire. Serialization can live with the DTO so the rest of the model does not know JSON / Java serialization.

**Shape.** Often a constructor that takes every field ([[What is constructor]]). Attributes **public**, or private with getters; **no setters** if the copy must not change after creation. **Setters** (sometimes with field checks) if the client will send the same type back in a coarse `setData(dto)` update. That is a design choice, not “must be a JavaBean with no logic.”

**Not an entity.** A JPA `@Entity` is a persistent identity with a lifecycle. A DTO is a **snapshot** for transport; mutating it does not update the database until some service **merges** it. Sharing one class as both is how persistence and API churn infect each other.

**Stale copies.** Once transferred, the client’s DTO can lag the server. Concurrent updatable DTOs need a version/timestamp if you merge them back. Immutable snapshots avoid accidental local mutation; they do not avoid staleness.

```d2
direction: down
client: "client / REST caller" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
call: "one remote call\ngetCustomer() / HTTP GET" {
  width: 260
  height: 45
  style.fill: "#fff8e1"
}
dto: "CustomerTO\nserialized snapshot" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
dom: "Customer entity / domain" {
  width: 220
  height: 40
}
client -> call
call -> dto
dto -> dom: "assembler copies values"
```

**Fig. 1.** One coarse call returns a DTO. Domain objects stay on the server.

```java
import java.io.Serializable;

final class CustomerTO implements Serializable {
    public final String id;
    public final String email;

    CustomerTO(String id, String email) {
        this.id = id;
        this.email = email;
    }
}

class Customer {
    String id;
    String email;
    String passwordHash; // not copied onto the wire
}

class CustomerAssembler {
    static CustomerTO toTO(Customer c) {
        return new CustomerTO(c.id, c.email);
    }
}
```

**Listing 1.** Immutable Transfer Object plus an assembler. `passwordHash` never leaves the domain type.

> [!warning] A DTO is for a **boundary**, not every Java layer
> In-process service A calling service B in the same JVM does not need a DTO for “purity.” The pattern exists to **cut remote chatter** and to **isolate serialization**. Mapping everything through DTOs inside one process is extra types without that payoff.

> [!warning] “Only fields and getters, never any logic” is too tight
> Public fields with no methods are allowed. So are getters without setters. Coarse update DTOs **do** have setters, sometimes with checks. What you keep off the DTO is **domain** behavior and persistence.

> [!warning] DTO is not a Value Object
> Sun once used “value object” for this pattern; that name now means something else (equality by value, domain). A DTO is a **transfer** shape. It may be immutable; that does not make it a DDD value object.

> [!tip] Interview answer
> A DTO is a serializable object that carries a bundle of data across a process or network boundary in one call, so the client is not chatty with remote getters. The server copies domain values into it through an assembler; the DTO is not the entity. REST request and response bodies are the same idea over HTTP. Use it at the wire, not as a mandatory extra class between every in-process layer.
