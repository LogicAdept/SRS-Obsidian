<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# What is `BatchPreparedStatementSetter`?

> [!abstract] Short answer
> **`BatchPreparedStatementSetter`** is the **`JdbcTemplate.batchUpdate(sql, setter)`** callback. You implement **`getBatchSize()`** and **`setValues(PreparedStatement ps, int i)`** (`i` from **0**). Same SQL, many parameter sets, **one prepared statement batch** — fewer round-trips. You do **not** catch **`SQLException`**; the template translates it.

## Bind index `i` of the batch

Docs: `setValues` is invoked **`getBatchSize()` times**. Stream/file input whose last batch is short: **`InterruptibleBatchPreparedStatementSetter`** + **`isBatchExhausted`**.

```java
return jdbcTemplate.batchUpdate(
        "update t_actor set first_name = ?, last_name = ? where id = ?",
        new BatchPreparedStatementSetter() {
            public void setValues(PreparedStatement ps, int i) throws SQLException {
                Actor actor = actors.get(i);
                ps.setString(1, actor.getFirstName());
                ps.setString(2, actor.getLastName());
                ps.setLong(3, actor.getId().longValue());
            }
            public int getBatchSize() {
                return actors.size();
            }
        });
```

**Listing 1.** Framework *JDBC Batch Operations* sample. Other overloads: [[How does JdbcTemplate batchUpdate work]]. Template: [[What is Spring JdbcTemplate]].

```d2
direction: down
sql: "one SQL string" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
set: "setValues(ps, i)" {
  width: 200
  height: 45
  style.fill: "#fff3e0"
}
db: "driver batch" {
  width: 160
  height: 40
  style.fill: "#e8f5e9"
}

sql -> set -> db
```

**Fig. 1.** List-of-`Object[]` and named **`SqlParameterSourceUtils.createBatch`** skip this interface. Insert helper: [[What is SimpleJdbcInsert]].

> [!warning] `getBatchSize` must match the data
> Returning `actors.size()` while `setValues` reads a shorter list throws. Index **`i` starts at 0**.

> [!warning] Return counts may be `-2`
> JDBC **`SUCCESS_NO_INFO`**. Do not assume every driver reports a real row count.

> [!tip] Interview answer
> **`BatchPreparedStatementSetter` fills parameters for each slot in a `batchUpdate`.** `getBatchSize` + `setValues`. Same SQL, many rows, one batch. There are also list-based overloads without this interface.

## See also

- [[How does JdbcTemplate batchUpdate work]]
- [[What is Spring JdbcTemplate]]
- [[Is JdbcTemplate thread-safe]]
