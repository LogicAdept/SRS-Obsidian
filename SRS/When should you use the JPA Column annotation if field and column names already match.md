<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA/Mapping #Java/Annotations #SRS

# When should you use the JPA Column annotation if field and column names already match?

> [!abstract] Short answer
> Whenever you must **change a default that is not the name**. `@Column` is optional; omitted, **`name` is already the field/property name**. You still write `@Column` for **`nullable`**, **`unique`**, **`length`**, **`precision`/`scale`**, **`insertable`/`updatable`**, **`table`**, or **`columnDefinition`**. Matching names are **not** a reason to skip those.

## Name is only one member

If no `@Column` is present, **all** defaults apply: `name` = attribute name, `nullable = true`, `unique = false`, `length = 255`, `insertable`/`updatable = true`, `precision`/`scale = 0` (provider-inferred), primary table. That is why a Java field `email` can map to column `email` with **zero** annotations — [[What is the JPA Column annotation]].

Use `@Column` **without** `name` when the physical name is already right but you need:

- **`nullable = false`** — DDL NOT NULL (schema generation)
- **`length`** — not 255 (`varchar`/`varbinary`)
- **`precision` / `scale`** — portable `decimal`/`numeric` (do not leave `0` if you generate schema)
- **`unique = true`** — single-column unique key (table-level keys still live on `@Table`) — [[What is the JPA Table annotation and its attributes]]
- **`insertable` / `updatable = false`** — omit from `INSERT`/`UPDATE` (derived, DB-default, read-only)
- **`table`** — column lives on a **secondary** table
- **`columnDefinition` / `options` / `check` / `comment` / `secondPrecision`** — DDL extras

`@Id` can sit beside `@Column` when the PK column name already matches but you still want length or nullability rules — [[What is the JPA Id annotation]].

```java
@Column(nullable = false, length = 320, unique = true)
private String email;

@Column(nullable = false, precision = 12, scale = 2, updatable = false)
private BigDecimal listPrice;
```

**Listing 1.** No `name` — the column is still `email` / `listPrice`. Related: [[What is the Java Persistence API JPA]].

```d2
direction: down
match: "Java field == SQL column name" {
  width: 280
  height: 45
}
skip: "omit @Column entirely" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}
keep: "@Column(nullable, length, …)\nno name() needed" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
match -> skip: "all defaults OK"
match -> keep: "override other defaults"
```

**Fig. 1.** Matching names only retire `name`; they do not retire `@Column`.

> [!warning] Defaults are wide open
> Skipping `@Column` because names match yields **nullable VARCHAR(255)** (or provider numeric inference) in generated schema — often wrong for money and emails. `nullable = false` is **not** Bean Validation. `unique = true` is DDL, not a runtime uniqueness check by the `EntityManager`.

> [!tip] Interview answer
> You do not need Column just to repeat the field name; that is already the default. You still use it when you need NOT NULL, a non-default length, decimal precision, uniqueness, or to keep the column out of insert or update. Name matching is irrelevant to those members.
