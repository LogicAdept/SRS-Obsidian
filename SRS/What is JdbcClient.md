<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is `JdbcClient`?

> [!abstract] Short answer
> **`JdbcClient`** (Framework **6.1**) is a **fluent facade** for common JDBC **query** and **update** work. One API covers **positional `?`** and **named `:id`** binds. It **delegates** to **`JdbcTemplate`** / **`NamedParameterJdbcTemplate`**. **Batches** and **stored procedures** stay on those templates or on **`SimpleJdbcInsert` / `SimpleJdbcCall`**.

## Unified client, same engine

Javadoc: *convenient unified facade for `PreparedStatement` execution*. Start with **`sql(String)`**, then **`param`**, then **`query(Class)`** / **`update()`**. Factory methods: **`JdbcClient.create(DataSource)`**, **`create(JdbcOperations)`**, **`create(NamedParameterJdbcOperations)`**. As of **7.0**, **`create(namedTemplate, ConversionService)`** for mapped-class conversion.

```java
private final JdbcClient jdbcClient = JdbcClient.create(dataSource);

public Optional<Integer> ageOf(long id) {
    return jdbcClient.sql("SELECT AGE FROM CUSTOMER WHERE ID = :id")
            .param("id", id)
            .query(Integer.class)
            .optional();
}

public int countByFirstName(String firstName) {
    return jdbcClient.sql("select count(*) from t_actor where first_name = ?")
            .param(firstName)
            .query(Integer.class)
            .single();
}
```

**Listing 1.** Framework samples — named `:id` + `optional()`, positional `?` + `single()`. Template it wraps: [[What is Spring JdbcTemplate]]. Named wrapper: [[What is NamedParameterJdbcTemplate]].

Spring Boot auto-configures a `JdbcClient` when a **`NamedParameterJdbcTemplate`** is present. `spring.jdbc.template.*` on the auto-configured template applies to the client as well.

```d2
direction: down
app: "sql().param().query()" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
client: "JdbcClient" {
  width: 180
  height: 45
  style.fill: "#fff3e0"
}
tpl: "JdbcTemplate /\nNamedParameterJdbcTemplate" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}

app -> client -> tpl
```

**Fig. 1.** Inserts/procedures: [[What is SimpleJdbcInsert]], [[What is SimpleJdbcCall]]. Batch path: [[How does JdbcTemplate batchUpdate work]].

> [!warning] Not a full replacement
> Docs: batch inserts and stored-procedure calls typically need **`SimpleJdbc*`** or **`JdbcTemplate`**. Do not assume `JdbcClient` has `batchUpdate` / `call`.

> [!warning] `single()` is still one row
> Like `queryForObject`, a missing or extra row is an exception. Use **`optional()`** when zero rows is normal.

> [!tip] Interview answer
> **`JdbcClient` is the 6.1 fluent API over `JdbcTemplate`.** Same SQL, positional or named binds. For batches and stored procedures, drop down to the template or `SimpleJdbcInsert` / `SimpleJdbcCall`.

## See also

- [[What is Spring JdbcTemplate]]
- [[What is NamedParameterJdbcTemplate]]
- [[What are the key components of Spring JDBC]]
