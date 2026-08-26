<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is `ResultSetExtractor`?

> [!abstract] Short answer
> **`ResultSetExtractor<T>`** is the `JdbcTemplate.query` callback that receives the **entire `ResultSet`**: **`T extractData(ResultSet rs)`**. **You** navigate with **`rs.next()`**. **Do not close** the set — **`JdbcTemplate` closes it**. Use it for **one aggregate** (an `Order` plus lines, a map of id→rows), not the usual **one object per row**. Everyday lists: **`RowMapper`**. Per-row void work: **`RowCallbackHandler`**.

## Whole cursor, one return value

Javadoc: mainly used **inside** the JDBC framework (`RowMapperResultSetExtractor` wraps a `RowMapper` for `query(RowMapper)`). Simpler choice for row-to-object: **`RowMapper`**. Contrast `RowCallbackHandler`: extractor is **typically stateless and reusable** unless it holds streams/LOB state.

```java
Order order = jdbcTemplate.query(
        "select o.id, i.sku from orders o join items i on i.order_id = o.id where o.id = ?",
        (ResultSet rs) -> {
            Order result = null;
            while (rs.next()) {
                if (result == null) {
                    result = new Order(rs.getLong("id"));
                }
                result.addLine(rs.getString("sku"));
            }
            return result;
        },
        orderId);
```

**Listing 1.** Conceptual — one `Order` graph; **you** loop. Dump cast `(ResultSetExtractor<Order>)` is only needed when Java cannot infer the lambda target. Mapper: [[What is a RowMapper in Spring JDBC]]. Handler: [[What is RowCallbackHandler]]. Diff: [[What is the difference between RowCallbackHandler and ResultSetExtractor]].

```d2
direction: down
rs: "ResultSet (open)" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
ex: "extractData\nwhile (rs.next())" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
t: "T (graph / aggregate)" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}

rs -> ex -> t
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. Fetch styles: [[How can you fetch records with JdbcTemplate]].

> [!warning] Default path is still `RowMapper`
> Do not reach for `ResultSetExtractor` to build `List<Foo>` — that is `query(sql, rowMapper)`.

> [!warning] Do not close the `ResultSet`
> Closing it leaves `JdbcTemplate` cleanup in a bad state. Exception handling stays on the template.

> [!tip] Interview answer
> **`ResultSetExtractor` processes the whole `ResultSet` and returns one `T`.** You call `next()`. `RowMapper` is one object per row into a list. `RowCallbackHandler` is per-row with no mapped return.

## See also

- [[What is a RowMapper in Spring JDBC]]
- [[What is RowCallbackHandler]]
- [[What is the difference between RowCallbackHandler and ResultSetExtractor]]
- [[What is Spring JdbcTemplate]]
- [[How can you fetch records with JdbcTemplate]]
