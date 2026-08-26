<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# What is `SimpleJdbcTemplate`?

> [!abstract] Short answer
> **`SimpleJdbcTemplate`** was a **Java 5 convenience wrapper** around **`JdbcTemplate`** (varargs, autoboxing, a slimmer method set). It was **deprecated in Spring 3.1** because **`JdbcTemplate` and `NamedParameterJdbcTemplate` absorbed that API**. Current Framework **does not ship it**. Start with **`JdbcTemplate`**, **`NamedParameterJdbcTemplate`**, or **`JdbcClient`** (6.1).

## Legacy Java 5 layer

3.1 javadoc: *the `JdbcTemplate` and `NamedParameterJdbcTemplate` now provide all the functionality of the `SimpleJdbcTemplate`*. The old type exposed **`getJdbcOperations()`** / **`getNamedParameterJdbcOperations()`** for callbacks, SQL types, **`RowCallbackHandler`**, **`PreparedStatementSetter` updates**, **stored procedures**, and **batches** — those never lived only on the “simple” wrapper.

Current `org.springframework.jdbc.core.simple` holds **`JdbcClient`**, **`SimpleJdbcInsert`**, and **`SimpleJdbcCall`** — not `SimpleJdbcTemplate`. Interview lists that still name it as a first-class Spring JDBC class are **stale**.

```d2
direction: right
old: "SimpleJdbcTemplate\n(removed)" {
  width: 220
  height: 55
  style.fill: "#ffebee"
}
now: "JdbcTemplate /\nNamedParameterJdbcTemplate /\nJdbcClient" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

old -> now
```

**Fig. 1.** Do not confuse this name with [[What is SimpleJdbcInsert]] or [[What is SimpleJdbcCall]] — those are current metadata helpers. Central class: [[What is Spring JdbcTemplate]]. Fluent: [[What is JdbcClient]].

> [!warning] Name collision on “simple”
> **`SimpleJdbcInsert` / `SimpleJdbcCall` are not replacements for `SimpleJdbcTemplate`.** Insert/call classes use **database metadata**. The old template was a **Java 5 syntax** wrapper.

> [!tip] Interview answer
> **`SimpleJdbcTemplate` is gone.** It was a Java 5 wrapper deprecated in 3.1. Use `JdbcTemplate`, named parameters, or `JdbcClient`. `SimpleJdbcInsert` and `SimpleJdbcCall` are different, still-current types.

## See also

- [[What is Spring JdbcTemplate]]
- [[What is NamedParameterJdbcTemplate]]
- [[Which classes are present in the Spring JDBC API]]
