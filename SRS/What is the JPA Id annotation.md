<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA/Mapping #Java/Annotations #SRS

# What is the JPA Id annotation?

> [!abstract] Short answer
> **`jakarta.persistence.Id`** is a **marker** on a field or getter that **is the entity’s primary key** (or one piece of a composite key with `@IdClass`). Every entity hierarchy must declare a PK **exactly once**, on the **root** entity or a **mapped superclass**. `@Id` does **not** generate values — pair **`@GeneratedValue`** for that. It is not `@EmbeddedId`.

## Identity, not a column DSL

`@Id` is `@Target({FIELD, METHOD})`, `@Retention(RUNTIME)`, and has **no elements**. The PK uniquely identifies the instance in the persistence context and to `EntityManager`. Legal simple types: primitives and wrappers, `String`, `UUID`, `LocalDate` / `java.util.Date` / `java.sql.Date`, `BigDecimal` / `BigInteger`. (`java.util.Date` still needs `@Temporal(DATE)`.) Provider-generated keys are portable only for `int`/`long` (and wrappers), `UUID`, and `String`.

The PK column is the primary key of the **primary table**. Omit `@Column` and the column name is the attribute name — [[What is the JPA Column annotation]].

**Composite keys:** several `@Id` fields plus `@IdClass`, **or** one `@EmbeddedId` embeddable — not both. `@GeneratedValue` is required only for **simple** generated keys, not derived/composite keys.

Do **not** change the PK after `persist`. Behavior is undefined.

```java
@Entity
public class Customer {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "CUST_SEQ")
    @Column(name = "CUST_ID")
    private Long id;
}
```

**Listing 1.** Marker `@Id` plus optional `@GeneratedValue` and `@Column`. Related: [[What is the Java Persistence API JPA]].

```d2
direction: down
e: "@Entity root" {
  width: 160
  height: 45
}
id: "@Id  (marker)" {
  width: 160
  height: 45
  style.fill: "#e8f5e9"
}
pk: "primary table PK column" {
  width: 200
  height: 45
}
e -> id -> pk
```

**Fig. 1.** `@Id` names the identity attribute; generation and column name are other annotations.

> [!warning] `@Id` does not auto-increment
> Without `@GeneratedValue`, you **assign** the key. `@Id` on a **subclass** when the root already has one is illegal (one PK per hierarchy). Do not put `@Id` and `@EmbeddedId` on the same entity. Mutating `id` after persist is undefined, not a portable “update the PK.”

> [!tip] Interview answer
> Id marks the primary-key attribute of an entity. It is a marker annotation: no members. Every entity needs exactly one identity, declared on the hierarchy root or a mapped superclass. GeneratedValue is what asks the provider to fill a simple key; composite keys use IdClass with several Id fields or a single EmbeddedId.
