<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is `queryForMap` in `JdbcTemplate`?

> [!abstract] Short answer
> **`queryForMap`** runs a SELECT that must return **exactly one row** and maps that row to **`Map<String, Object>`**: **column name → value**. Use it when you **do not** have a domain type. Otherwise prefer **`queryForObject`** + **`RowMapper`**. Zero or extra rows → **`IncorrectResultSizeDataAccessException`** (empty: typically **`EmptyResultDataAccessException`**).

## One row, untyped columns

Javadoc: *the query is expected to be a single row query*. Many rows: **`queryForList`** (list of maps). Domain objects: **`query` / `queryForObject`**. Column **key case** follows the driver / metadata — do not hard-code `"ID"` vs `"id"`.

```java
Map<String, Object> row = jdbcTemplate.queryForMap(
        "select id, first_name, last_name from t_actor where id = ?",
        actorId);
```

**Listing 1.** Conceptual — one map, binds as varargs. Many maps: [[What is queryForList in JdbcTemplate]]. Cardinality: [[What is the difference between query and queryForObject in JdbcTemplate]]. Fetch overview: [[How can you fetch records with JdbcTemplate]].

```d2
direction: right
sql: "SELECT … one row" {
  width: 180
  height: 45
  style.fill: "#e3f2fd"
}
m: "Map column → value" {
  width: 200
  height: 45
  style.fill: "#fff3e0"
}

sql -> m
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. Mapper path: [[What is a RowMapper in Spring JDBC]].

> [!warning] Same one-row contract as `queryForObject`
> Missing row is an **exception**, not an empty map.

> [!warning] Keys are column names
> Interview examples that print `{ID=1, FIRST_NAME=…}` assume that driver’s labels. Always read **`ResultSetMetaData`** names Spring copied, not a guessed case.

> [!tip] Interview answer
> **`queryForMap` is one row as `Map<String,Object>` keyed by column name.** Many rows: `queryForList`. A real type: `queryForObject` + `RowMapper`. Wrong row count throws.

## See also

- [[What is queryForList in JdbcTemplate]]
- [[What is the difference between query and queryForObject in JdbcTemplate]]
- [[How can you fetch records with JdbcTemplate]]
