<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is a `RowMapper` in Spring JDBC?

> [!abstract] Short answer
> A **`RowMapper<T>`** maps **one current `ResultSet` row** to a **`T`**. The only method is **`mapRow(ResultSet rs, int rowNum)`**. **`JdbcTemplate`** (and stored-procedure out params) call it **once per row**. **Do not call `rs.next()`** — that is **`ResultSetExtractor`** territory. It is a **`@FunctionalInterface`** (lambda). Typically **stateless and reusable**. Built-ins include **`BeanPropertyRowMapper`**, **`DataClassRowMapper`**, **`SingleColumnRowMapper`**.

## One row, no cursor loop

Javadoc: implementations map the **current** row; **`SQLException` is handled by `JdbcTemplate`**. `mapRow` **must not** call `next()`.

```java
private final RowMapper<Actor> actorRowMapper = (resultSet, rowNum) -> {
    Actor actor = new Actor();
    actor.setFirstName(resultSet.getString("first_name"));
    actor.setLastName(resultSet.getString("last_name"));
    return actor;
};

public List<Actor> findAllActors() {
    return this.jdbcTemplate.query("select first_name, last_name from t_actor", actorRowMapper);
}
```

**Listing 1.** Conceptual Framework sample — same mapper for `query` (list) and `queryForObject` (one row). Template: [[What is Spring JdbcTemplate]]. Bean mapping: [[What is BeanPropertyRowMapper]].

| Callback | Returns | Cursor |
| --- | --- | --- |
| **`RowMapper`** | one object per row | Spring already on the row |
| **`RowCallbackHandler`** | `void` (side effects) | per row, no object list |
| **`ResultSetExtractor`** | one aggregate | **you** may `next()` the whole `ResultSet` |

Contrast: [[What is RowCallbackHandler]], [[What is ResultSetExtractor]], [[What is the difference between RowCallbackHandler and ResultSetExtractor]].

```d2
direction: right
rs: "ResultSet\ncurrent row" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
rm: "RowMapper.mapRow" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
obj: "T" {
  width: 100
  height: 50
  style.fill: "#e8f5e9"
}

rs -> rm -> obj
```

**Fig. 1.** Spring advances the cursor; you copy columns. Stateful mappers with fields are a concurrency hazard on a shared template — [[Is JdbcTemplate thread-safe]].

> [!warning] `mapRow` plus `rs.next()` double-skips rows
> That is the **`ResultSetExtractor`** contract. A `RowMapper` that walks the set corrupts `query`/`queryForObject`.

> [!warning] `queryForObject` still wants exactly one row
> A mapper does not turn zero rows into `Optional`. Zero/many rows → **`IncorrectResultSizeDataAccessException`**.

> [!tip] Interview answer
> **`RowMapper` is `mapRow(ResultSet, rowNum)` — one row to one object, no `next()`.** Pass it to `JdbcTemplate.query` or `queryForObject`. Lambdas are fine. Use `ResultSetExtractor` when you need the whole cursor; `RowCallbackHandler` when you do not want a list.

## See also

- [[What is Spring JdbcTemplate]]
- [[What is BeanPropertyRowMapper]]
- [[What is RowCallbackHandler]]
- [[What is ResultSetExtractor]]
- [[How can you fetch records with JdbcTemplate]]
- [[What is the difference between query and queryForObject in JdbcTemplate]]
