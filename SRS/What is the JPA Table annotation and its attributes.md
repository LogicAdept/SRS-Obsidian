<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA/Mapping #Java/Annotations #SRS

# What is the JPA Table annotation and its attributes?

> [!abstract] Short answer
> **`jakarta.persistence.Table`** names the entity’s **primary table** (`@Target(TYPE)`). Optional members: **`name`**, **`schema`**, **`catalog`**, **`uniqueConstraints`**, **`indexes`**, plus 3.2 **`check` / `comment` / `options`**. Omit it and **`name` defaults to the entity name** (unqualified class name unless `@Entity(name=…)`). It is **not** `@Entity`’s JPQL name. Illegal on `@MappedSuperclass` or `@Embeddable`. Extra tables use `@SecondaryTable`.

## Primary table mapping

`@Table` is optional. Defaults: empty `name` → **entity name**; catalog/schema → provider/user defaults; no extra unique constraints or indexes.

| Member | Role |
| --- | --- |
| `name` | Physical table name |
| `schema` / `catalog` | Qualify the table |
| `uniqueConstraints` | Extra unique keys at **table** level (`UniqueConstraint`) — schema generation only; on top of `@Column(unique)`, `@JoinColumn`, and the PK |
| `indexes` | Extra indexes (`Index`); PK index is created anyway |
| `check` / `comment` / `options` | DDL extras (3.2), generation only |

`@Column(table = …)` can point a basic attribute at a **secondary** table declared with `@SecondaryTable`, not at `@Table`’s primary table (that is the default) — [[What is the JPA Column annotation]]. PK still lives on the primary table — [[What is the JPA Id annotation]].

```java
@Entity
@Table(
    name = "CUST",
    schema = "RECORDS",
    uniqueConstraints = @UniqueConstraint(columnNames = {"TAX_ID"}),
    indexes = @Index(columnList = "LAST_NAME")
)
public class Customer { /* @Id … */ }
```

**Listing 1.** Physical name + schema; unique/index used when the provider generates DDL. Entity mapping: [[What is the Java Persistence API JPA]].

```d2
direction: down
ent: "@Entity Customer\n(entity name: Customer)" {
  width: 240
  height: 55
}
tab: "@Table(name=\"CUST\", schema=\"RECORDS\")" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
ddl: "RECORDS.CUST" {
  width: 160
  height: 45
}
ent -> tab -> ddl
```

**Fig. 1.** `@Entity` name is for queries; `@Table` name is the SQL table.

> [!warning] `name` is not the JPQL entity name
> `@Table(name = "CUST")` does **not** change `FROM Customer` in JPQL. That is `@Entity(name = …)`. `uniqueConstraints` / `indexes` do **nothing** at runtime if you never generate schema. Do not put `@Table` on a mapped superclass or embeddable.

> [!tip] Interview answer
> Table maps an entity to its primary database table and is optional: the default table name is the entity name. Typical attributes are name, schema, catalog, uniqueConstraints, and indexes. Those constraint and index members affect DDL generation, not runtime SQL by themselves. Extra tables are SecondaryTable, not a second Table annotation on the same class.
