<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is `NamedParameterJdbcTemplate`?

> [!abstract] Short answer
> **`NamedParameterJdbcTemplate`** wraps a **`JdbcTemplate`** and lets SQL use **named parameters** (`:first_name`) instead of only JDBC **`?`**. You pass a **`SqlParameterSource`** (`MapSqlParameterSource`, **`BeanPropertySqlParameterSource`**) or a **`Map`**. It **delegates** real JDBC work to the wrapped template. Names are a **Spring** feature; the driver still gets positional parameters. As of **6.1**, **`JdbcClient`** can do named or indexed binds on one fluent API.

## Named SQL over the same engine

Spring *Using NamedParameterJdbcTemplate*: this class exists **only** to differ on **how you write parameters**. Access `?`-only APIs via **`getJdbcOperations()`**.

```java
private NamedParameterJdbcTemplate namedParameterJdbcTemplate;

public void setDataSource(DataSource dataSource) {
    this.namedParameterJdbcTemplate = new NamedParameterJdbcTemplate(dataSource);
}

public int countOfActorsByFirstName(String firstName) {
    String sql = "select count(*) from t_actor where first_name = :first_name";
    SqlParameterSource namedParameters = new MapSqlParameterSource("first_name", firstName);
    return this.namedParameterJdbcTemplate.queryForObject(sql, namedParameters, Integer.class);
}
```

**Listing 1.** Framework sample — `:first_name` + `MapSqlParameterSource`. Same count with a `Map`: `Collections.singletonMap("first_name", firstName)`.

JavaBean properties as binds: **`BeanPropertySqlParameterSource`** — SQL names match **bean property names** (`:firstName` with `getFirstName()`). How-to: [[How do you use NamedParameterJdbcTemplate with SqlParameterSource]]. vs `?`: [[What is the difference between JdbcTemplate and NamedParameterJdbcTemplate]].

```d2
direction: right
sql: ":first_name SQL" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
np: "NamedParameterJdbcTemplate" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
jt: "JdbcTemplate\npositional JDBC" {
  width: 200
  height: 55
  style.fill: "#e8f5e9"
}

sql -> np -> jt
```

**Fig. 1.** Reuse one wrapped `JdbcTemplate` (thread-safe once configured) — [[Is JdbcTemplate thread-safe]]. Facade: [[What is JdbcClient]].

> [!warning] Colon names on `JdbcTemplate` do nothing useful
> `jdbcTemplate.update("... where id = :id", id)` treats `:id` as **literal SQL**, not a bind. Use this class or `JdbcClient.sql(...).param("id", ...)`.

> [!warning] Name the property, not the column, for beans
> `BeanPropertySqlParameterSource` uses **JavaBean** names. `:first_name` will not see `firstName` unless you align them.

> [!tip] Interview answer
> **`NamedParameterJdbcTemplate` is `JdbcTemplate` plus `:named` parameters.** Pass a map or `SqlParameterSource`. JDBC still uses `?` under the hood. Prefer it when a statement has many binds; `JdbcClient` (6.1) unifies both styles.

## See also

- [[What is Spring JdbcTemplate]]
- [[What is JdbcClient]]
- [[How do you use NamedParameterJdbcTemplate with SqlParameterSource]]
- [[What is the difference between JdbcTemplate and NamedParameterJdbcTemplate]]
- [[What is BeanPropertyRowMapper]]
- [[What is Spring JDBC]]
