<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# How does `JdbcTemplate.batchUpdate` work?

> [!abstract] Short answer
> **`batchUpdate`** groups **many executions of the same (or listed) SQL** so the driver can send them as a **JDBC batch** and cut round-trips. Classic path: **one SQL** + **`BatchPreparedStatementSetter`**. Alternatives: **`List<Object[]>`** for `?`, **`SqlParameterSource[]`** / **`SqlParameterSourceUtils.createBatch`** on **`NamedParameterJdbcTemplate`**, **`batchUpdate(String... sql)`** for **different** statements, or **chunked** **`Collection` + batch size + `ParameterizedPreparedStatementSetter`**.

## Same statement, many binds

Docs: most drivers perform better when you batch the **same prepared statement**. Returns **`int[]`** affected counts; if unknown, drivers often return **-2**. Chunked overload returns **`int[][]`** (per batch, then per statement).

```java
List<Object[]> batch = new ArrayList<>();
for (Actor actor : actors) {
    batch.add(new Object[] {
            actor.getFirstName(), actor.getLastName(), actor.getId()});
}
return jdbcTemplate.batchUpdate(
        "update t_actor set first_name = ?, last_name = ? where id = ?",
        batch);
```

**Listing 1.** Framework list-of-arrays sample. Setter callback: [[What is BatchPreparedStatementSetter]]. Named list: [[How do you use NamedParameterJdbcTemplate with SqlParameterSource]].

`JdbcClient` docs: **batch inserts typically need `JdbcTemplate` or `SimpleJdbcInsert`**, not the fluent client.

```d2
direction: down
app: "List of parameter sets" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
jt: "batchUpdate" {
  width: 180
  height: 40
  style.fill: "#fff3e0"
}
drv: "PreparedStatement.addBatch" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}

app -> jt -> drv
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. Thread-safe template, **per-call** setter/list — [[Is JdbcTemplate thread-safe]].

> [!warning] `batchUpdate(String... sql)` is not “SQL plus args”
> That overload runs **several SQL strings**. Parameterized batches use **one SQL** plus a setter or `List<Object[]>`.

> [!warning] Nulls and `getParameterType`
> List/map batches may call **`ParameterMetaData.getParameterType`**, which is expensive on some drivers. Prefer explicit types, **`BatchPreparedStatementSetter`**, or **`spring.jdbc.getParameterType.ignore`**. As of **6.1.2**, PostgreSQL and SQL Server skip that lookup by default.

> [!tip] Interview answer
> **`batchUpdate` sends many parameter sets for one SQL as a JDBC batch.** Setter, `List<Object[]>`, or named `createBatch`. Return counts can be `-2`. `JdbcClient` is not the batch API.

## See also

- [[What is BatchPreparedStatementSetter]]
- [[What is Spring JdbcTemplate]]
- [[What is JdbcClient]]
