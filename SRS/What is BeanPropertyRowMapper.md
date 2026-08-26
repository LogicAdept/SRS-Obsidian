<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is `BeanPropertyRowMapper`?

> [!abstract] Short answer
> **`BeanPropertyRowMapper<T>`** is a **`RowMapper`** that builds a **`T`** with a **no-arg constructor** and **public setters**, matching **column names** (metadata) to properties — **direct** or **underscore → camelCase** (`first_name` → `setFirstName`). Since **2.5**. Convenient, **not** the fast path: javadoc prefers a **custom `RowMapper`** for performance. **Records / data classes** → **`DataClassRowMapper`**. This is **not** JPA `@Entity` mapping.

## Column names to setters

Javadoc: top-level or **static** nested class; **default / no-arg** constructor. Common JDBC types map to wrappers/primitives/`BigDecimal`/`Date`. Alias in SQL when names disagree: `select fname as first_name`.

```java
List<Actor> actors = jdbcTemplate.query(
        "select first_name, last_name from t_actor",
        new BeanPropertyRowMapper<>(Actor.class));
```

**Listing 1.** Conceptual — same idea as dumps’ `new BeanPropertyRowMapper<>(User.class)`. Factory: `BeanPropertyRowMapper.newInstance(Actor.class)`. Custom `mapRow`: [[What is a RowMapper in Spring JDBC]].

`NULL` → setter `null`. **Primitive** properties then throw **`TypeMismatchException`** unless **`setPrimitivesDefaultedForNullValue(true)`** (then a later UPDATE can persist the primitive default — documented footgun).

`checkFullyPopulated`: default **false** (unmapped properties stay at constructor defaults).

```d2
direction: right
col: "column first_name" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
map: "BeanPropertyRowMapper" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
set: "setFirstName(...)" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}

col -> map -> set
```

**Fig. 1.** Spring JDBC 6.x also documents **`SimplePropertyRowMapper`** as a common replacement (with `JdbcClient`). Template: [[What is Spring JdbcTemplate]].

> [!warning] Not `@Entity`
> No persistence context, no `@Column`. If the setter name and column alias do not match, the property stays empty — write a **`RowMapper`** or alias the column.

> [!warning] Records need `DataClassRowMapper`
> No-arg + setters is the `BeanPropertyRowMapper` contract. A canonical constructor / record component mapping is the other class.

> [!warning] Convenience over speed
> Reflection/setters every row. Hot paths: handwritten `RowMapper`.

> [!tip] Interview answer
> **`BeanPropertyRowMapper` maps each row onto a JavaBean via setters and column names (including `snake_case`).** Pass `new BeanPropertyRowMapper<>(Foo.class)` to `query`. Use `DataClassRowMapper` for records. Prefer a custom mapper if names are messy or you need speed.

## See also

- [[What is a RowMapper in Spring JDBC]]
- [[What is Spring JdbcTemplate]]
- [[How can you fetch records with JdbcTemplate]]
- [[What is JdbcClient]]
- [[What is NamedParameterJdbcTemplate]]
