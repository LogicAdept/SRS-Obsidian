<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Persistence/JPA/Mapping #SRS

# Can you use a Java record as a JPA entity?

> [!abstract] Short answer
> **No.** Jakarta Persistence forbids designating a record as an `@Entity`. An entity must be a non-`final` class with a public or protected no-arg constructor and non-`final` persistent fields. A record is implicitly `final`, its component fields are `final`, it already extends `java.lang.Record`, and it has no default no-arg constructor. Use a class for the entity; use records for embeddables, composite ids, and query projections.

## Why `@Entity` on a record fails the spec

```d2
direction: down
jpa: "JPA entity rules\nnon-final class, no-arg ctor\nnon-final persistent fields" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
rec: "Java record\nimplicitly final, final fields\nextends Record, canonical ctor" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
ok: "record as @Embeddable / id class / query DTO" {
  width: 320
  height: 60
  style.fill: "#e8f5e9"
}
jpa -> rec: "not an entity"
rec -> ok
```

**Fig. 1.** The entity contract and the record contract do not overlap. Other JPA roles for records do.

Jakarta Persistence 3.2 §2.1: the entity class must be a top-level class or static inner class; **an enum, record, or interface may not be designated as an entity**. It must have a public or protected constructor with **no parameters**. It must be **non-final**; every method and persistent instance variable must be non-final. The `@Entity` Javadoc repeats the same three bullets and the record ban.

A record misses those on purpose: [[Are Java record fields final]], [[Can a Java record declare additional constructors]], [[What is the difference between a Java record and a regular class]]. There is no implicit `User()`; extra constructors must `this(...)` into the canonical one. Providers that subclass the entity for lazy proxies cannot subclass a `final` type. Dirty checking that writes fields cannot assign `final` components.

Jakarta Persistence **3.1** already required non-final classes, non-final persistent fields, and a no-arg constructor (it listed only enum/interface as illegal kinds). **3.2** names records in the ban and, in the same chapter, **allows** them as embeddables and as composite primary-key classes.

```java
@Entity
public record User(Long id, String name) {} // not an entity
```

**Listing 1.** Illegal as `@Entity`: record type, `final` class, `final` fields, no no-arg constructor.

```java
@Entity
public class User {
    @Id
    private Long id;
    private String name;

    protected User() {} // provider no-arg constructor
}
```

**Listing 2.** Ordinary entity class: non-final, mutable persistent fields, public or protected no-arg constructor.

## What records *are* for next to JPA

JPA 3.2 §2.7: an embeddable **may be any Java record type** (no-arg constructor not required). §2.4.1: a composite primary-key class **may be any Java record type**. Hibernate 7’s introduction uses the same split: `@Embeddable record Name(...)`, `@Embeddable record BookId(...)` / `@IdClass`, and mapping a query select list into a local `record IsbnTitle(...)`. Those are not entities — no `@Id` lifecycle, no persistence context identity.

A record cannot **extend** a `@MappedSuperclass` or another entity: it has no `extends` clause and its superclass is `Record`. Nothing can extend the record either (`final`), so it cannot sit in an entity inheritance hierarchy.

```java
@Embeddable
public record Name(String first, String last) {}

@Entity
public class Author {
    @Id
    private Long id;
    private Name name;
    protected Author() {}
}
```

**Listing 3.** Legal: record as embeddable state of a class entity.

> [!warning] `@Entity` on a record is a spec violation, not a style choice
> Even if a particular Hibernate version appears to start, portable JPA does not treat a record as an entity. Do not rely on bytecode tricks to invent a no-arg constructor and mutable fields; that is not the record you wrote.

> [!warning] “Record as the JPA entity hierarchy” is a red flag
> Records cannot extend a mapped superclass or entity, and cannot be subclassed. Composite ids and embeddables are the supported record roles — not `@Entity` roots or leaves.

> [!tip] Interview answer
> **No — a Java record cannot be a JPA entity: the spec says so, and records are final with final fields and no no-arg constructor.** Keep `@Entity` on a class. Use records as `@Embeddable` types, composite primary keys, or query DTOs.
