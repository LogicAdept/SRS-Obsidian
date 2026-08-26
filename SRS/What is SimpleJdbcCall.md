<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# What is `SimpleJdbcCall`?

> [!abstract] Short answer
> **`SimpleJdbcCall`** is a **thread-safe, reusable** helper for a **stored procedure or function**. It reads **parameter metadata** so you often only set **`withProcedureName`** (or function name) and **`execute`** an IN **`SqlParameterSource`**. **No subclass.** The call itself runs through **`JdbcTemplate`**. Compare **`StoredProcedure`**, which **requires a subclass** and explicit **`declareParameter`**.

## Metadata call vs RDBMS object

Docs: configure in DAO init, same idea as **`SimpleJdbcInsert`**. **`execute`** returns a **`Map` of OUT parameters** keyed by procedure parameter names. Match IN names to the procedure; **case may differ** per database — use a case-insensitive lookup or **`JdbcTemplate.setResultsMapCaseInsensitive(true)`**.

Metadata lookup is supported for procedures on **Derby, DB2, MySQL, SQL Server, Oracle, Sybase**; functions on **MySQL, SQL Server, Oracle**. Other databases: **`declareParameters`**. To ignore metadata entirely: **`withoutProcedureColumnMetaDataAccess`**.

**IN values** are taken only from parameters declared as **`SqlParameter`** or **`SqlInOutParameter`**. That differs from **`StoredProcedure`**, which (compatibility) also accepts input for **`SqlOutParameter`**.

```java
public void setDataSource(DataSource dataSource) {
    this.procReadActor = new SimpleJdbcCall(dataSource)
            .withProcedureName("read_actor");
}

public Actor readActor(Long id) {
    SqlParameterSource in = new MapSqlParameterSource()
            .addValue("in_id", id);
    Map out = procReadActor.execute(in);
    Actor actor = new Actor();
    actor.setId(id);
    actor.setFirstName((String) out.get("out_first_name"));
    actor.setLastName((String) out.get("out_last_name"));
    return actor;
}
```

**Listing 1.** Framework sample — IN map in, OUT map out. Other call styles: [[How do you call stored procedures in Spring JDBC]]. Object wrapper: [[What is the Spring StoredProcedure class]].

```d2
direction: down
name: "withProcedureName" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
meta: "DB metadata (or declareParameters)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
jt: "JdbcTemplate.call / CallableStatement" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

name -> meta -> jt
```

**Fig. 1.** Simple `CALL` without OUT params can be **`JdbcTemplate.update("call …")`**. Insert helper: [[What is SimpleJdbcInsert]].

> [!warning] OUT map keys follow the database
> Portable code does a **case-insensitive** get, or sets **`resultsMapCaseInsensitive`** on the template passed into the `SimpleJdbcCall` constructor.

> [!warning] `JdbcClient` is not this
> Procedure calls are listed as **out of scope** for `JdbcClient` — [[What is JdbcClient]].

> [!tip] Interview answer
> **`SimpleJdbcCall` wraps a procedure using metadata.** Name it, `execute` IN values, read OUT from the result map. Unlike `StoredProcedure`, you do not subclass. Simple `CALL` with no OUT can be `JdbcTemplate.update`.

## See also

- [[How do you call stored procedures in Spring JDBC]]
- [[What is the Spring StoredProcedure class]]
- [[What is Spring JdbcTemplate]]
