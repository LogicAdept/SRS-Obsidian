<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is the difference between `RowCallbackHandler` and `ResultSetExtractor`?

> [!abstract] Short answer
> **`RowCallbackHandler.processRow`** runs **once per current row**, returns **void**, and **must not** call **`rs.next()`**. **`ResultSetExtractor.extractData`** receives the **whole `ResultSet`**, **you** loop with **`next()`**, and you **return one `T`**. Third callback: **`RowMapper`** — one object per row, collected by **`query`**.

## Per-row side effect vs one aggregate

Javadoc: handler is typically **stateful** (count, stream, XML). Extractor is typically **stateless** and used internally as **`RowMapperResultSetExtractor`**. Neither should **close** the `ResultSet`.

| | `RowCallbackHandler` | `ResultSetExtractor` | `RowMapper` |
| --- | --- | --- | --- |
| Signature | `void processRow(ResultSet)` | `T extractData(ResultSet)` | `T mapRow(ResultSet, int)` |
| `next()` | no | **yes** | no |
| Typical result | state on the handler | one graph / aggregate | `List<T>` via `query` |

```java
RowCountCallbackHandler counter = new RowCountCallbackHandler();
jdbcTemplate.query("select id from t_actor", counter);
int n = counter.getRowCount();

Order order = jdbcTemplate.query(sql, (ResultSet rs) -> {
    Order result = null;
    while (rs.next()) {
        if (result == null) {
            result = new Order(rs.getLong("id"));
        }
        result.addLine(rs.getString("sku"));
    }
    return result;
}, orderId);
```

**Listing 1.** Conceptual — void counter vs one `Order`. Handler: [[What is RowCallbackHandler]]. Extractor: [[What is ResultSetExtractor]]. Mapper: [[What is a RowMapper in Spring JDBC]].

```d2
direction: right
h: "processRow\nper row, void" {
  width: 180
  height: 55
  style.fill: "#fff3e0"
}
e: "extractData\nwhole RS → T" {
  width: 180
  height: 55
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. Fetch APIs: [[How can you fetch records with JdbcTemplate]].

> [!warning] Calling `next()` in `processRow`
> Skips rows. Same rule as `mapRow`.

> [!warning] Do not close the `ResultSet`
> `JdbcTemplate` closes it. Closing inside either callback breaks the template.

> [!tip] Interview answer
> **Handler: per-row void, no `next()`. Extractor: you walk the whole `ResultSet` and return one object.** For `List<Entity>`, use `RowMapper`.

## See also

- [[What is RowCallbackHandler]]
- [[What is ResultSetExtractor]]
- [[What is a RowMapper in Spring JDBC]]
