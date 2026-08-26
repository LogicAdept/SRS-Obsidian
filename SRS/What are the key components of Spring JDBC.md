<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# What are the key components of Spring JDBC?

> [!abstract] Short answer
> The pieces that usually appear together: a **`DataSource`** (connections, ideally a **pool**), **`JdbcTemplate`** (SQL execution, resource close, exception translation, `ResultSet` iteration), and often **`NamedParameterJdbcTemplate`** (`:name` binds). Mapping uses **`RowMapper`** (and cousins). As of **6.1**, **`JdbcClient`** is a fluent facade over the templates. **`SimpleJdbcInsert` / `SimpleJdbcCall`** cover insert metadata and stored procedures. **`SimpleJdbcTemplate` is legacy** — not a current starting class.

## Working set

Spring *Data Access with JDBC* + *core classes*:

| Piece | Role |
| --- | --- |
| **`DataSource`** | You configure URL/credentials (or JNDI). Spring opens/closes connections through it |
| **`JdbcTemplate`** | Central delegate: `query` / `update` / `execute` / `batchUpdate` |
| **`NamedParameterJdbcTemplate`** | Wraps a `JdbcTemplate`; `:firstName` instead of `?` |
| **`JdbcClient`** (6.1) | Unified fluent query/update; delegates to the templates |
| **`RowMapper` / `RowCallbackHandler` / `ResultSetExtractor`** | How rows become objects (or side effects) |
| **`SQLExceptionTranslator`** | `SQLException` → `DataAccessException` |
| **`SimpleJdbcInsert` / `SimpleJdbcCall`** | Convenience for inserts / procedures when `JdbcClient` is not enough |

Interview lists that stop at “three classes” omit mappers and translation. Broader “approaches” lists that still name **`SimpleJdbcTemplate`** are **stale**.

```java
@Repository
public class ActorDao {

    private final JdbcTemplate jdbc;
    private final NamedParameterJdbcTemplate named;

    public ActorDao(DataSource dataSource) {
        this.jdbc = new JdbcTemplate(dataSource);
        this.named = new NamedParameterJdbcTemplate(jdbc);
    }
}
```

**Listing 1.** Conceptual — one `DataSource`, template + named wrapper. Central class: [[What is Spring JdbcTemplate]]. Named: [[What is NamedParameterJdbcTemplate]].

```d2
direction: down
ds: "DataSource" {
  width: 180
  height: 45
  style.fill: "#e8f5e9"
}
jt: "JdbcTemplate" {
  width: 180
  height: 45
  style.fill: "#fff3e0"
}
np: "NamedParameterJdbcTemplate" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
map: "RowMapper" {
  width: 160
  height: 45
  style.fill: "#fce4ec"
}

ds -> jt
jt -> np
jt -> map
```

**Fig. 1.** `JdbcClient.create(dataSource)` hides the same stack. Module: [[What is Spring JDBC]]. DAO exceptions: [[What is Spring DAO support]].

> [!warning] `DataSource` is not optional decoration
> A template without a real pool is still JDBC. **`DriverManagerDataSource` is not a pool** — [[What is connection pooling in Spring JDBC]].

> [!warning] Named parameters are Spring SQL, not JDBC `?`
> The driver still sees positional parameters after Spring substitutes. Mixing `:name` on a raw `JdbcTemplate` does not bind names.

> [!tip] Interview answer
> **`DataSource` + `JdbcTemplate` (+ named template or `JdbcClient`) + `RowMapper`.** Spring closes JDBC resources and translates exceptions. `SimpleJdbcInsert`/`SimpleJdbcCall` for metadata-heavy insert/procedure cases. Skip `SimpleJdbcTemplate` on modern lists.

## See also

- [[What is Spring JDBC]]
- [[What is Spring JdbcTemplate]]
- [[What is NamedParameterJdbcTemplate]]
- [[What is JdbcClient]]
- [[What is a RowMapper in Spring JDBC]]
- [[What is SimpleJdbcInsert]]
- [[What is SimpleJdbcCall]]
- [[Which classes are present in the Spring JDBC API]]
