<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# What is `SimpleJdbcInsert`?

> [!abstract] Short answer
> **`SimpleJdbcInsert`** builds **INSERT** from **JDBC metadata**: you set the **table name**, pass **column → value**, and Spring writes the statement. **Do not subclass it.** Configure once (fluent **`withTableName`**, optional **`usingColumns`**, **`usingGeneratedKeyColumns`**), then **`execute`**. **`JdbcClient` does not replace this** for inserts that need metadata or generated keys.

## Metadata insert, not a query API

Docs: instantiate in the DAO **initialization** path. Map **keys must match table column names**. Alternatives to `Map`: **`MapSqlParameterSource`**, **`BeanPropertySqlParameterSource`**. Generated keys: **`usingGeneratedKeyColumns("id")`** then **`executeAndReturnKey`** → **`Number`** (not a guaranteed concrete numeric type). Multiple / non-numeric keys: **`executeAndReturnKeyHolder`**. Restrict columns with **`usingColumns`**.

```java
public void setDataSource(DataSource dataSource) {
    this.insertActor = new SimpleJdbcInsert(dataSource)
            .withTableName("t_actor")
            .usingGeneratedKeyColumns("id");
}

public void add(Actor actor) {
    Map<String, Object> parameters = new HashMap<>(2);
    parameters.put("first_name", actor.getFirstName());
    parameters.put("last_name", actor.getLastName());
    Number newId = insertActor.executeAndReturnKey(parameters);
    actor.setId(newId.longValue());
}
```

**Listing 1.** Framework sample — no `id` in the map when the column is generated. Template keys: [[How do you fetch auto-generated keys with JdbcTemplate]]. Named sources: [[How do you use NamedParameterJdbcTemplate with SqlParameterSource]].

```d2
direction: down
cfg: "withTableName + metadata" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
exec: "execute(Map / SqlParameterSource)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
sql: "INSERT constructed for you" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

cfg -> exec -> sql
```

**Fig. 1.** Stored procedures: [[What is SimpleJdbcCall]]. Fluent queries: [[What is JdbcClient]]. Template: [[What is Spring JdbcTemplate]].

> [!warning] Column names, not Java properties
> A `Map` is keyed by **database columns**. Bean property names only apply when you pass **`BeanPropertySqlParameterSource`**.

> [!warning] Not a general `JdbcTemplate`
> No SELECT/UPDATE/batch facade here. Wrong tool for queries.

> [!tip] Interview answer
> **`SimpleJdbcInsert` uses table metadata so you skip a hand-written INSERT.** Configure `withTableName`, `execute` a map of columns. Generated keys: `usingGeneratedKeyColumns` + `executeAndReturnKey`.

## See also

- [[What is SimpleJdbcCall]]
- [[How do you fetch auto-generated keys with JdbcTemplate]]
- [[What is JdbcClient]]
