<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# How do you fetch auto-generated keys with `JdbcTemplate`?

> [!abstract] Short answer
> Call **`jdbcTemplate.update(PreparedStatementCreator, KeyHolder)`**. Create the statement with **`connection.prepareStatement(sql, new String[] { "id" })`** (or equivalent JDBC 3.0 generated-keys flags), bind values, return the `PreparedStatement`. Pass a **`GeneratedKeyHolder`**. After success, **`keyHolder.getKey()`** holds the key. There is **no single portable** `prepareStatement` shape — the reference example is **Oracle-oriented**.

## JDBC 3.0 keys via `KeyHolder`

Docs: this `update` convenience is **JDBC 3.0** generated keys. The creator exists because drivers differ on how to request keys.

```java
final String INSERT_SQL = "insert into my_test (name) values(?)";
KeyHolder keyHolder = new GeneratedKeyHolder();
jdbcTemplate.update(connection -> {
    PreparedStatement ps = connection.prepareStatement(INSERT_SQL, new String[] { "id" });
    ps.setString(1, name);
    return ps;
}, keyHolder);
Number id = keyHolder.getKey();
```

**Listing 1.** Framework sample. Metadata insert: [[What is SimpleJdbcInsert]] (`usingGeneratedKeyColumns` + `executeAndReturnKey`). Do **not** use **`queryForObject`** after insert unless you have a separate SELECT.

```d2
direction: down
ins: "INSERT PreparedStatement\n(generated keys)" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
kh: "GeneratedKeyHolder" {
  width: 200
  height: 45
  style.fill: "#fff3e0"
}

ins -> kh
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. Batch + keys: `batchUpdate(PreparedStatementCreator, BatchPreparedStatementSetter, KeyHolder)` on `JdbcTemplate`.

> [!warning] Platform-specific `prepareStatement`
> Docs: the Oracle-style `new String[] { "id" }` **may not work** elsewhere. Some drivers want **`Statement.RETURN_GENERATED_KEYS`**. Verify on **your** database.

> [!warning] `getKey()` vs multiple columns
> One numeric key: **`getKey()`**. Several keys or non-numeric: inspect **`keyHolder.getKeyList()`** / maps. `SimpleJdbcInsert.executeAndReturnKey` returns **`Number`** for the same reason.

> [!tip] Interview answer
> **Pass a `PreparedStatementCreator` that requests generated keys and a `GeneratedKeyHolder` into `JdbcTemplate.update`.** Then read `keyHolder.getKey()`. `SimpleJdbcInsert` does the same with metadata.

## See also

- [[What is SimpleJdbcInsert]]
- [[What is Spring JdbcTemplate]]
- [[How can you fetch records with JdbcTemplate]]
