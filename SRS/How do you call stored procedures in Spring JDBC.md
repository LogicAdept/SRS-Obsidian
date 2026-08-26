<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# How do you call stored procedures in Spring JDBC?

> [!abstract] Short answer
> Four documented paths: **`JdbcTemplate.update("call …", args)`** for a **simple CALL** with no OUT map; **`JdbcTemplate.call(CallableStatementCreator, List<SqlParameter>)`** for **OUT/IN** via JDBC callable statements; **`SimpleJdbcCall`** (metadata, **no subclass**); **`StoredProcedure`** (RDBMS object, **you subclass**). **`JdbcClient` does not** cover procedure calls.

## Pick by OUT parameters

Core chapter: simple refresh procedure uses **`update` + `call SCHEMA.NAME(?)`**. *More sophisticated stored procedure support is covered later* — that is **`SimpleJdbcCall`** and **`org.springframework.jdbc.object.StoredProcedure`**.

```java
this.jdbcTemplate.update(
        "call SUPPORT.REFRESH_ACTORS_SUMMARY(?)",
        Long.valueOf(unionId));
```

**Listing 1.** Framework simple CALL. Metadata helper: [[What is SimpleJdbcCall]]. Object wrapper: [[What is the Spring StoredProcedure class]]. Template: [[What is Spring JdbcTemplate]].

`JdbcTemplate.call`: pass a **`CallableStatementCreator`** and **declared `SqlParameter`s**; result is a **`Map` of extracted OUT** values (same idea as `SimpleJdbcCall.execute`).

```d2
direction: down
simple: "update(\"call …\")" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
meta: "SimpleJdbcCall" {
  width: 180
  height: 45
  style.fill: "#e3f2fd"
}
obj: "StoredProcedure subclass" {
  width: 220
  height: 45
  style.fill: "#fff3e0"
}
call: "JdbcTemplate.call" {
  width: 180
  height: 45
  style.fill: "#fce4ec"
}
```

**Fig. 1.** Inserts: [[What is SimpleJdbcInsert]]. Fluent queries: [[What is JdbcClient]].

> [!warning] Interview “exactly three ways”
> Dumps that list only `SimpleJdbcCall` / `execute` / `call` omit **`StoredProcedure`** and treat **`execute` as the CALL API**. Simple CALL is **`update`**. **`execute`** is the **DDL / arbitrary SQL** family.

> [!warning] IN vs `SqlOutParameter`
> On **`SimpleJdbcCall`**, only **`SqlParameter` / `SqlInOutParameter`** supply IN values. **`StoredProcedure`** historically also accepts input for **`SqlOutParameter`**.

> [!tip] Interview answer
> **Simple `CALL`: `JdbcTemplate.update`.** OUT parameters: `SimpleJdbcCall` (preferred) or `JdbcTemplate.call`. Reusable typed wrapper: subclass `StoredProcedure`. Not `JdbcClient`.

## See also

- [[What is SimpleJdbcCall]]
- [[What is the Spring StoredProcedure class]]
- [[How do you execute DDL with JdbcTemplate]]
