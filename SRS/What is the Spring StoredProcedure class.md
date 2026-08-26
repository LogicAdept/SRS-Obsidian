<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# What is the Spring `StoredProcedure` class?

> [!abstract] Short answer
> **`org.springframework.jdbc.object.StoredProcedure`** is an **abstract** RDBMS-operation class: you **subclass** it, set the **procedure name** as **`sql`**, **`declareParameter`** (`SqlParameter`, **`SqlOutParameter`**, **`SqlInOutParameter`**), **`compile()`**, then expose a **typed `execute`** that delegates to **`execute(Map)`**. **`SimpleJdbcCall`** is the **non-subclass**, metadata-driven alternative.

## Object wrapper, not ad-hoc SQL in every DAO

Docs: *many Spring developers* replace other `jdbc.object` types with straight **`JdbcTemplate`**, but **`StoredProcedure` is the exception** they still mention as worth keeping. After **`compile()`** the instance is **thread-safe** if created at DAO init.

```java
private class GetSysdateProcedure extends StoredProcedure {

    public GetSysdateProcedure(DataSource dataSource) {
        setDataSource(dataSource);
        setFunction(true);
        setSql("sysdate");
        declareParameter(new SqlOutParameter("date", Types.DATE));
        compile();
    }

    public Date execute() {
        Map<String, Object> results = execute(new HashMap<String, Object>());
        return (Date) results.get("date");
    }
}
```

**Listing 1.** Framework Oracle `sysdate` function sample (inner class). Modern metadata API: [[What is SimpleJdbcCall]]. Menu of call styles: [[How do you call stored procedures in Spring JDBC]].

OUT **`REF CURSOR`**: `SqlOutParameter` with a **`RowMapper`**. IN map keys are **parameter names** you declared.

```d2
direction: down
sub: "subclass + declareParameter" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
cmp: "compile()" {
  width: 140
  height: 40
  style.fill: "#fff3e0"
}
ex: "execute(Map) → OUT map" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}

sub -> cmp -> ex
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. Mapper: [[What is a RowMapper in Spring JDBC]].

> [!warning] You must subclass
> There is no “new StoredProcedure(ds, name).execute” fluent API like `SimpleJdbcCall`. Inner class is fine for one-off functions.

> [!warning] `sql` is the procedure name
> Inherited **`sql`** property is the **RDBMS object name**, not a `CALL …` string you paste into `JdbcTemplate.update`.

> [!tip] Interview answer
> **`StoredProcedure` is an abstract wrapper: subclass, declare IN/OUT, compile, execute a map.** `SimpleJdbcCall` avoids the subclass when metadata works. Simple `CALL` without OUT can stay on `JdbcTemplate.update`.

## See also

- [[What is SimpleJdbcCall]]
- [[How do you call stored procedures in Spring JDBC]]
- [[What is Spring JdbcTemplate]]
