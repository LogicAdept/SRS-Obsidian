<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is the difference between `JdbcTemplate` and `NamedParameterJdbcTemplate`?

> [!abstract] Short answer
> **`JdbcTemplate`** binds **JDBC `?` placeholders** in **order**. **`NamedParameterJdbcTemplate` wraps a `JdbcTemplate`** and binds **Spring named parameters** (`:first_name`) from a **`Map`**, **`MapSqlParameterSource`**, or **`BeanPropertySqlParameterSource`**. Same connections, translation, and callbacks underneath. As of **6.1**, **`JdbcClient`** exposes **both** styles on one fluent API.

## Parameter notation, one engine

Docs: named template **differs only in how you write parameters**. **`getJdbcOperations()`** reaches `?`-only methods. Names never go to the driver as names — Spring expands them.

```java
int positional = jdbcTemplate.queryForObject(
        "select count(*) from t_actor where first_name = ?",
        Integer.class, firstName);

int named = namedParameterJdbcTemplate.queryForObject(
        "select count(*) from t_actor where first_name = :first_name",
        new MapSqlParameterSource("first_name", firstName),
        Integer.class);
```

**Listing 1.** Conceptual pair. How-to sources: [[How do you use NamedParameterJdbcTemplate with SqlParameterSource]]. Named class: [[What is NamedParameterJdbcTemplate]]. Fluent: [[What is JdbcClient]].

```d2
direction: down
np: ":name SQL + SqlParameterSource" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
wrap: "NamedParameterJdbcTemplate" {
  width: 260
  height: 45
  style.fill: "#fff3e0"
}
jt: "JdbcTemplate (? binds)" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}

np -> wrap -> jt
```

**Fig. 1.** Central class: [[What is Spring JdbcTemplate]]. Batch named: [[How does JdbcTemplate batchUpdate work]].

> [!warning] Names must still match
> Order no longer matters; **wrong `:token` vs source key** still fails. Bean source keys are **JavaBean property names** (`:firstName` ↔ `getFirstName()`), which may **not** equal SQL column names.

> [!warning] Do not put `:name` on raw `JdbcTemplate`
> Classic template will treat that as literal SQL, not a bind.

> [!tip] Interview answer
> **`JdbcTemplate` uses `?`. `NamedParameterJdbcTemplate` wraps it and uses `:names`.** Same JDBC stack. Long parameter lists are safer with names. `JdbcClient` can do either.

## See also

- [[What is NamedParameterJdbcTemplate]]
- [[What is Spring JdbcTemplate]]
- [[How do you use NamedParameterJdbcTemplate with SqlParameterSource]]
