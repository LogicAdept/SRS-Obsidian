<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is `RowCallbackHandler`?

> [!abstract] Short answer
> **`RowCallbackHandler`** is a **`JdbcTemplate` / `NamedParameterJdbcTemplate`** callback: **`void processRow(ResultSet rs)`** for **each current row**. **Do not call `rs.next()`**. There is **no list of mapped objects** returned to the template — you **stream, log, count, or write** as you go. Javadoc: typically **stateful** (keep results on the handler, inspect later). Prefer **`RowMapper`** when you want **one object per row** collected into a `List`.

## Side effects, not `List<T>`

Javadoc: `SQLException` handled by the template. Trivial impl: count rows. Other: build XML. Example class: **`RowCountCallbackHandler`**.

```java
RowCountCallbackHandler counter = new RowCountCallbackHandler();
jdbcTemplate.query("select id from t_actor", counter);
int rows = counter.getRowCount();
```

**Listing 1.** Conceptual — state lives **on the handler**. Contrast mapper: [[What is a RowMapper in Spring JDBC]]. Whole cursor: [[What is ResultSetExtractor]]. Pair: [[What is the difference between RowCallbackHandler and ResultSetExtractor]].

| Callback | Typical reuse | You `next()`? |
| --- | --- | --- |
| `RowMapper` | **stateless**, reusable | no |
| `RowCallbackHandler` | **stateful** | no |
| `ResultSetExtractor` | **typically stateless** | **yes**, whole `ResultSet` |

```d2
direction: right
rs: "current row" {
  width: 140
  height: 45
  style.fill: "#e3f2fd"
}
cb: "processRow" {
  width: 160
  height: 45
  style.fill: "#fff3e0"
}
st: "handler fields\n(count, stream, …)" {
  width: 220
  height: 55
  style.fill: "#e8f5e9"
}

rs -> cb -> st
```

**Fig. 1.** `JdbcTemplate.query(sql, handler)` return type is **void** at the callback level — nothing to assign as `List`. Template: [[What is Spring JdbcTemplate]].

> [!warning] Do not `next()` in `processRow`
> Same rule as `RowMapper.mapRow`. Walking the cursor here skips rows.

> [!warning] Sharing a stateful handler across threads
> A singleton handler that accumulates counts will race. Create one per call, or use a **stateless `RowMapper`**.

> [!tip] Interview answer
> **`RowCallbackHandler.processRow` runs per row and returns void.** Use it for streaming or counters, not for `List<Entity>`. For objects, `RowMapper`. For one graph over the whole `ResultSet`, `ResultSetExtractor`.

## See also

- [[What is a RowMapper in Spring JDBC]]
- [[What is ResultSetExtractor]]
- [[What is the difference between RowCallbackHandler and ResultSetExtractor]]
- [[What is Spring JdbcTemplate]]
- [[How can you fetch records with JdbcTemplate]]
