<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is Spring `JdbcTemplate`?

> [!abstract] Short answer
> **`JdbcTemplate`** is the **central class** in Spring’s JDBC core package. You supply **SQL** (and extract results); it runs the **JDBC workflow**: open statement, execute, iterate the **`ResultSet`**, **close** resources, and translate **`SQLException`** into **`org.springframework.dao.DataAccessException`**. Once configured it is **thread-safe** (holds a **`DataSource`**, not conversational state). As of Framework **6.1**, **`JdbcClient`** is a fluent facade **on top of** it — not a replacement for batches or stored procedures.

## What you write vs what it owns

Javadoc: *central delegate*; *simplifies JDBC and helps avoid common errors*. Docs: avoid forgetting to **close the connection**. Callbacks: **`PreparedStatementCreator`**, **`CallableStatementCreator`**, **`RowMapper`** / **`RowCallbackHandler`**.

| Method family | Typical use |
| --- | --- |
| **`query` / `queryForObject` / `queryForList` / `queryForMap`** | SELECT; object mapping via `RowMapper` |
| **`update`** | INSERT / UPDATE / DELETE; simple `CALL …` |
| **`batchUpdate`** | Many DML statements |
| **`execute`** | Arbitrary SQL — **often DDL**; also `ConnectionCallback` / `StatementCallback` |

```java
@Repository
public class JdbcCorporateEventDao implements CorporateEventDao {

    private final JdbcTemplate jdbcTemplate;

    public JdbcCorporateEventDao(DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
    }

    public Actor findActor(long id) {
        return jdbcTemplate.queryForObject(
                "select first_name, last_name from t_actor where id = ?",
                (rs, rowNum) -> {
                    Actor actor = new Actor();
                    actor.setFirstName(rs.getString("first_name"));
                    actor.setLastName(rs.getString("last_name"));
                    return actor;
                },
                id);
    }
}
```

**Listing 1.** Conceptual Framework sample — constructor `JdbcTemplate(DataSource)`, `queryForObject` + `RowMapper`. Mapper type: [[What is a RowMapper in Spring JDBC]]. Bean-style mapping: [[What is BeanPropertyRowMapper]].

`queryForObject` requires **exactly one row**. Otherwise **`IncorrectResultSizeDataAccessException`** (zero rows: typically **`EmptyResultDataAccessException`**). Prefer `query` + handle an empty list when “maybe missing” is normal — [[What is the difference between query and queryForObject in JdbcTemplate]].

```d2
direction: down
app: "DAO: SQL + RowMapper" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
jt: "JdbcTemplate\nstatement · ResultSet · close" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ds: "DataSource\n(pool)" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}

app -> jt -> ds
```

**Fig. 1.** One configured template is shared across DAOs — [[Is JdbcTemplate thread-safe]]. Exception path: [[How does Spring JDBC translate SQLException]]. Module: [[What is Spring JDBC]].

`execute("create table …")` is the documented DDL path. **`update`** is the DML path (`insert`/`update`/`delete`). A simple stored-procedure **`CALL`** in the docs uses **`update`**, not `execute`. Richer procedures: [[What is SimpleJdbcCall]], [[How do you call stored procedures in Spring JDBC]].

Fluent query/update (positional **or** named parameters): **`JdbcClient`** (6.1), which **delegates** to `JdbcTemplate` / `NamedParameterJdbcTemplate`. Batches and procedures still want the template or **`SimpleJdbcInsert` / `SimpleJdbcCall`**. **`SimpleJdbcTemplate`** is a **legacy** Java 5 wrapper — do not start there; use `JdbcTemplate` or `JdbcClient`. Named parameters: [[What is NamedParameterJdbcTemplate]]. vs JPA: [[What is the difference between Spring JDBC and Spring Data JPA]].

> [!warning] `queryForObject` is not `Optional`
> No row is an **exception**, not `null`. `SQL NULL` in a single column can still return Java `null` for `Class` overloads.

> [!warning] `execute` is not the default DML API
> Use **`update`** for insert/update/delete. `execute` is for arbitrary SQL (DDL, callbacks).

> [!warning] One template per `DataSource`
> Multiple databases → multiple `DataSource` beans and templates. Do not share one template across catalogs by swapping connections yourself.

> [!tip] Interview answer
> **`JdbcTemplate` runs JDBC for you: SQL in, resources and `SQLException` translation out.** Share one configured instance; it is thread-safe. `query`/`queryForObject` for reads, `update` for DML, `execute` often for DDL. `JdbcClient` (6.1) is a fluent facade on the same engine.

## See also

- [[What is Spring JDBC]]
- [[Is JdbcTemplate thread-safe]]
- [[What is a RowMapper in Spring JDBC]]
- [[What is BeanPropertyRowMapper]]
- [[What is NamedParameterJdbcTemplate]]
- [[What is JdbcClient]]
- [[How does Spring JDBC translate SQLException]]
- [[What is the DataAccessException hierarchy]]
- [[How do you configure JdbcTemplate as a bean]]
- [[What is the difference between Spring JDBC and Spring Data JPA]]
