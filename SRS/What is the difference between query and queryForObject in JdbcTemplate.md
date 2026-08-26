<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is the difference between `query` and `queryForObject` in `JdbcTemplate`?

> [!abstract] Short answer
> **`query`** runs a SELECT and maps **zero or more** rows (typically a **`List<T>`** via **`RowMapper`**). **`queryForObject`** maps **exactly one** row to a **single `T`** (scalar `Integer.class` / `String.class`, or a domain type + `RowMapper`). If the result size is not one, **`IncorrectResultSizeDataAccessException`** (no row: usually **`EmptyResultDataAccessException`**). “Maybe missing” → **`query`** and inspect the list, not `queryForObject`.

## Cardinality is the API

Spring examples: `queryForObject("select count(*) …", Integer.class)` for a **one-cell** aggregate; `query(..., rowMapper)` for a **list** of actors; `queryForObject(..., rowMapper, id)` for **one** actor.

```java
int count = jdbcTemplate.queryForObject(
        "select count(*) from t_actor where first_name = ?",
        Integer.class, "Joe");

List<Actor> all = jdbcTemplate.query(
        "select first_name, last_name from t_actor",
        actorRowMapper);

Actor one = jdbcTemplate.queryForObject(
        "select first_name, last_name from t_actor where id = ?",
        actorRowMapper, id);
```

**Listing 1.** Conceptual mix of Framework samples. Mapper: [[What is a RowMapper in Spring JDBC]]. Template: [[What is Spring JdbcTemplate]].

No domain type: **`queryForMap`** (one row → `Map` of columns), **`queryForList`** (many rows → `List<Map>` or `List<T>`). Those still enforce “one row” on the `ForMap` / single-object overloads — [[What is queryForMap in JdbcTemplate]], [[What is queryForList in JdbcTemplate]].

```d2
direction: down
q: "query + RowMapper" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
list: "List<T> (0..n)" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
qo: "queryForObject" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
one: "exactly one T" {
  width: 200
  height: 45
  style.fill: "#fce4ec"
}

q -> list
qo -> one
```

**Fig. 1.** `count(*)` is still **one row**. A `WHERE id = ?` that misses is **not**.

> [!warning] `queryForObject` is not `findById` Optional
> Zero rows throw. Catching that in every DAO is noise — use `query` and `stream().findFirst()` (or handle empty list) when absence is normal.

> [!warning] Two rows also fail `queryForObject`
> Unique constraint missing → **`IncorrectResultSizeDataAccessException`**, not a silent first row.

> [!tip] Interview answer
> **`query` returns a list; `queryForObject` demands exactly one row.** Same `RowMapper` can serve both. Scalars use `queryForObject(sql, Integer.class)`. For optional rows, do not use `queryForObject`.

## See also

- [[What is Spring JdbcTemplate]]
- [[How can you fetch records with JdbcTemplate]]
- [[What is a RowMapper in Spring JDBC]]
- [[What is queryForMap in JdbcTemplate]]
- [[What is queryForList in JdbcTemplate]]
- [[What is the DataAccessException hierarchy]]
