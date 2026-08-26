<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# How can you fetch records with `JdbcTemplate`?

> [!abstract] Short answer
> Use **`query`** for **many rows** (`List<T>` + **`RowMapper`**), **`queryForObject`** for **exactly one** row (scalar class or mapper), **`queryForList`** / **`queryForMap`** when you want **maps** instead of a domain type. Walk the whole cursor yourself with **`ResultSetExtractor`**. Per-row void work: **`RowCallbackHandler`**. **`update` is DML**, not a fetch. Bind **`?` arguments in order**.

## Read APIs

Spring *Running Queries* / *Querying (SELECT)*:

```java
int count = jdbcTemplate.queryForObject(
        "select count(*) from mytable", Integer.class);

String name = jdbcTemplate.queryForObject(
        "select name from mytable where id = ?", String.class, id);

List<Actor> actors = jdbcTemplate.query(
        "select first_name, last_name from t_actor",
        actorRowMapper);

Actor one = jdbcTemplate.queryForObject(
        "select first_name, last_name from t_actor where id = ?",
        actorRowMapper, id);
```

**Listing 1.** Conceptual Framework patterns. Cardinality: [[What is the difference between query and queryForObject in JdbcTemplate]]. Mapper: [[What is a RowMapper in Spring JDBC]]. Maps: [[What is queryForMap in JdbcTemplate]], [[What is queryForList in JdbcTemplate]].

Two dump “interfaces” for fetching: **`RowMapper`** (usual) and **`ResultSetExtractor`** (whole `ResultSet`) — [[What is ResultSetExtractor]], [[What is RowCallbackHandler]].

```d2
direction: down
sql: "SELECT + binds" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
jt: "JdbcTemplate.query*" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
out: "List / T / Map" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}

sql -> jt -> out
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. Wrong row count on `queryForObject` → **`IncorrectResultSizeDataAccessException`**.

> [!warning] `update` does not fetch
> INSERT/UPDATE/DELETE return **row counts** (or keys). Reads are `query*`.

> [!warning] `?` order is positional
> Named binds need [[What is NamedParameterJdbcTemplate]] or [[What is JdbcClient]].

> [!tip] Interview answer
> **`query` + `RowMapper` for lists, `queryForObject` for one row, `queryForMap`/`queryForList` for untyped rows.** Extractor if you build a graph. `update` is not a read. `queryForObject` throws if the row count is not one.

## See also

- [[What is Spring JdbcTemplate]]
- [[What is a RowMapper in Spring JDBC]]
- [[What is BeanPropertyRowMapper]]
- [[What is ResultSetExtractor]]
- [[What is the difference between query and queryForObject in JdbcTemplate]]
- [[How do you fetch auto-generated keys with JdbcTemplate]]
