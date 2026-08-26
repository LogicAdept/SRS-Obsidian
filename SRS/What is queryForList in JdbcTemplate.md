<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is `queryForList` in `JdbcTemplate`?

> [!abstract] Short answer
> **`queryForList`** is the **many-row** cousin of map/scalar queries. The generic overload returns **`List<Map<String, Object>>`** — **one map per row**, column name as key (same shape as **`queryForMap`**). Overloads with a **`Class`** return **`List<T>`** of **single-column** values (e.g. `Integer.class`). Domain objects still want **`query` + `RowMapper`**.

## Maps vs typed lists

Spring *Running Queries*: most generic form is a **list of maps**. Example result: `[{name=Bob, id=1}, {name=Mary, id=2}]`. Binds: varargs / `Object[]` overloads. **`queryForMap`** is **one** of those maps with a **single-row** check.

```java
List<Map<String, Object>> rows = jdbcTemplate.queryForList("select * from mytable");

List<Integer> ids = jdbcTemplate.queryForList(
        "select id from t_actor where first_name = ?",
        Integer.class,
        firstName);
```

**Listing 1.** Framework-style map list; second line is the `Class` overload (conceptual mix). One map: [[What is queryForMap in JdbcTemplate]]. `RowMapper` list: [[What is a RowMapper in Spring JDBC]]. Overview: [[How can you fetch records with JdbcTemplate]].

```d2
direction: down
sql: "SELECT many rows" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
list: "List<Map> or List<T>" {
  width: 220
  height: 45
  style.fill: "#fff3e0"
}

sql -> list
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. Do not use this for a **one-object graph** — [[What is ResultSetExtractor]].

> [!warning] Not `query` + `RowMapper`
> `List<Map>` is untyped columns. `query(..., rowMapper)` is `List<Person>`. Mixing them in an interview answer is a common slip.

> [!warning] `Class` overload is one column
> `queryForList(sql, Integer.class)` maps **each row’s single column**, not a bean. Multi-column beans: `RowMapper` or `BeanPropertyRowMapper`.

> [!tip] Interview answer
> **`queryForList` without a domain type returns `List<Map<String,Object>>`.** `queryForMap` is the one-row version. For entities, `query` + `RowMapper`.

## See also

- [[What is queryForMap in JdbcTemplate]]
- [[What is the difference between query and queryForObject in JdbcTemplate]]
- [[How can you fetch records with JdbcTemplate]]
