<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# Which classes are present in the Spring JDBC API?

> [!abstract] Short answer
> Core: **`JdbcTemplate`**, **`NamedParameterJdbcTemplate`**, callbacks (**`RowMapper`**, **`RowCallbackHandler`**, **`ResultSetExtractor`**, **`BatchPreparedStatementSetter`**). **6.1:** **`JdbcClient`**. Metadata helpers: **`SimpleJdbcInsert`**, **`SimpleJdbcCall`**. RDBMS objects: **`StoredProcedure`** (and `SqlQuery` / `SqlUpdate`). Support: **`JdbcDaoSupport`** (deprecated **7.0**). **`SimpleJdbcTemplate` is not current** — removed after **3.1** deprecation.

## Packages you actually start with

Spring *Data Access with JDBC* + *core* / *simple* / *object*:

| Area | Types |
| --- | --- |
| Execution | `JdbcTemplate`, `NamedParameterJdbcTemplate`, `JdbcClient` |
| Mapping | `RowMapper`, `BeanPropertyRowMapper`, `RowCallbackHandler`, `ResultSetExtractor` |
| Insert / call | `SimpleJdbcInsert`, `SimpleJdbcCall` |
| Batch | `BatchPreparedStatementSetter` |
| Procedures (object) | `StoredProcedure` |
| Connections | `DataSource` you configure; `DriverManagerDataSource` (tests) |

Interview lists that stop at five names and still include **`SimpleJdbcTemplate`** are **stale**. `JdbcClient` is the missing modern name on those lists.

```d2
direction: down
jt: "JdbcTemplate" {
  width: 180
  height: 40
  style.fill: "#fff3e0"
}
np: "NamedParameterJdbcTemplate" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
cl: "JdbcClient" {
  width: 160
  height: 40
  style.fill: "#e8f5e9"
}

jt -> np
jt -> cl
np -> cl
```

**Fig. 1.** Central class: [[What is Spring JdbcTemplate]]. Legacy wrapper: [[What is SimpleJdbcTemplate]]. Components: [[What are the key components of Spring JDBC]].

> [!warning] `SimpleJdbcTemplate` vs `SimpleJdbcInsert`
> Different types. Insert/call classes **remain**. The Java 5 template **does not**.

> [!warning] `jdbc.object` is optional
> Docs: most operations are simpler as **direct `JdbcTemplate` methods**. **`StoredProcedure`** is the one they still single out.

> [!tip] Interview answer
> **Start with `JdbcTemplate` (and named template or `JdbcClient`).** Add `RowMapper`, `SimpleJdbcInsert` / `SimpleJdbcCall` as needed. Do not list `SimpleJdbcTemplate` as current API.

## See also

- [[What is Spring JdbcTemplate]]
- [[What is JdbcClient]]
- [[What is SimpleJdbcTemplate]]
- [[What are the key components of Spring JDBC]]
