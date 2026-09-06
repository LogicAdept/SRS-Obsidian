<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA/Mapping #Java/Annotations #SRS

# What is the JPA Column annotation?

> [!abstract] Short answer
> **`jakarta.persistence.Column`** maps a **basic** persistent field or property to a **database column**. It is optional: if you omit it, defaults apply (`name` = field/property name, `nullable = true`, `length = 255`, insertable/updatable). You use it to set **name**, **nullability**, **length** / **precision** / **scale**, uniqueness, insert/update inclusion, or a secondary **table**. It is **not** `@JoinColumn`.

## What it actually configures

`@Column` is `@Target({FIELD, METHOD})` and `@Retention(RUNTIME)`. It does **not** make a class an entity and does **not** map associations. It annotates the **basic** attribute (or its getter). [[What is the Java Persistence API JPA]]

Useful members (all optional):

- **`name`** — column name; default is the attribute name
- **`nullable` / `unique`** — DDL nullability and a single-column unique key (plus table-level constraints)
- **`length`** — for length-parameterized types (`varchar`, `varbinary`); default **255**
- **`precision` / `scale`** — exact numerics (`decimal`/`numeric`); `0` means provider-inferred — portable schema generation should set them
- **`insertable` / `updatable`** — whether the provider includes the column in `INSERT` / `UPDATE`
- **`table`** — non-primary table ([[What is the JPA Table annotation and its attributes]])
- **`columnDefinition`** — native DDL fragment; **not** portable

If the Java name already matches the column, you still add `@Column` for `nullable`, `length`, and so on — [[When should you use the JPA Column annotation if field and column names already match]]. `@Id` is a separate mapping ([[What is the JPA Id annotation]]).

```java
@Column(name = "DESC", nullable = false, length = 512)
private String description;

@Column(name = "ORDER_COST", updatable = false, precision = 12, scale = 2)
private BigDecimal cost;
```

**Listing 1.** Name, nullability, length; read-only money with explicit precision/scale.

```d2
direction: right
attr: "basic field / getter" {
  width: 180
  height: 55
}
col: "@Column\nname nullable length\nprecision insertable" {
  width: 220
  height: 80
}
ddl: "SQL column\n(+ INSERT/UPDATE)" {
  width: 180
  height: 55
}
attr -> col -> ddl
```

**Fig. 1.** `@Column` is the basic-attribute-to-column mapping, not a relationship mapping.

> [!warning] Not the foreign-key annotation
> `@ManyToOne` / `@OneToOne` FKs use **`@JoinColumn`**. Putting `@Column` on an association is the wrong mapping. `nullable = false` is a **column** constraint (and schema generation); it is not automatically Bean Validation. `columnDefinition` locks you to one dialect.

> [!tip] Interview answer
> Column maps a basic entity attribute to a table column and is optional when names already match. You set it for a different column name, nullability, varchar length, decimal precision, or to skip the column on insert or update. Associations use JoinColumn, not Column.
