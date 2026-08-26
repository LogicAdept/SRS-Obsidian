<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# How do you use `NamedParameterJdbcTemplate` with `SqlParameterSource`?

> [!abstract] Short answer
> Put **`:name`** tokens in SQL. Build a **`SqlParameterSource`**: **`MapSqlParameterSource`** (`addValue` / constructor) or **`BeanPropertySqlParameterSource(bean)`** (JavaBean **getters**). Pass SQL + source into **`query` / `queryForObject` / `update`**. A plain **`Map`** also works. Classic **`JdbcTemplate` does not** accept named sources.

## Two source types

Docs: **`MapSqlParameterSource`** is a `Map` adapter. **`BeanPropertySqlParameterSource`** uses **bean property names** as keys — SQL **`:firstName`** matches **`getFirstName()`**, which may differ from the **column** `first_name`.

```java
String sql = "select count(*) from t_actor where first_name = :first_name";
SqlParameterSource namedParameters = new MapSqlParameterSource("first_name", firstName);
return namedParameterJdbcTemplate.queryForObject(sql, namedParameters, Integer.class);

String beanSql = "select count(*) from t_actor where first_name = :firstName and last_name = :lastName";
SqlParameterSource fromBean = new BeanPropertySqlParameterSource(exampleActor);
return namedParameterJdbcTemplate.queryForObject(beanSql, fromBean, Integer.class);
```

**Listing 1.** Framework samples. Class: [[What is NamedParameterJdbcTemplate]]. vs `?`: [[What is the difference between JdbcTemplate and NamedParameterJdbcTemplate]]. Same sources on [[What is SimpleJdbcInsert]].

Batch: **`SqlParameterSourceUtils.createBatch(actors)`** with named **`batchUpdate`**. `?` APIs: **`getJdbcOperations()`**.

```d2
direction: down
sql: ":firstName in SQL" {
  width: 180
  height: 45
  style.fill: "#e3f2fd"
}
src: "SqlParameterSource" {
  width: 200
  height: 45
  style.fill: "#fff3e0"
}
np: "NamedParameterJdbcTemplate" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}

sql -> src -> np
```

**Fig. 1.** Fluent: [[What is JdbcClient]] `.param("firstName", value)`. Template: [[What is Spring JdbcTemplate]].

> [!warning] Bean names ≠ column names
> `:firstName` follows the **Java** property. The map style often uses **`:first_name`** to match SQL columns. Mixing them is a bind miss.

> [!warning] Not a `JdbcTemplate` method
> Positional template has no `SqlParameterSource` overload. Wrap it or use `JdbcClient`.

> [!tip] Interview answer
> **SQL uses `:names`. Values come from `MapSqlParameterSource` or `BeanPropertySqlParameterSource` (or a `Map`).** The named template wraps `JdbcTemplate`. Bean keys are property names, not necessarily columns.

## See also

- [[What is NamedParameterJdbcTemplate]]
- [[What is the difference between JdbcTemplate and NamedParameterJdbcTemplate]]
- [[What is SimpleJdbcInsert]]
