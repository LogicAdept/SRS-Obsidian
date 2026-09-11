<!--
reps: 0
priority: 0
-->
#Databases/SQL/DML #Java/JDBC #SRS

# How do you organize batch inserts for many rows?

> [!abstract] Short answer
> For **many similar `INSERT`s**, prepare **one** `PreparedStatement`, **`setXxx` + `addBatch()`** per row, then **`executeBatch()`** (or **`executeLargeBatch()`** if counts may exceed `Integer.MAX_VALUE`). That submits the **list of parameter sets** as a JDBC **batch**. Probe **`DatabaseMetaData.supportsBatchUpdates()`** first. `Statement.addBatch(String)` queues **whole SQL strings** and **cannot** be used on a `PreparedStatement`. A failed command throws **`BatchUpdateException`**; the driver **may or may not** run the rest.

## One prepared `INSERT`, many parameter sets

`PreparedStatement.addBatch()` “adds a **set of parameters** to this `PreparedStatement` object's batch.” `Statement.executeBatch()` then **submits that list** and, if every command succeeds, returns an `int[]` of update counts **in add order** (since JDBC 2 / Java 1.2). Count values:

- **≥ 0** — rows affected
- **`Statement.SUCCESS_NO_INFO`** — succeeded, count **unknown**
- On failure: **`BatchUpdateException`**. Whether later commands still run is **driver/DBMS-fixed** (always continue **or** always stop). If it continues, `getUpdateCounts()` is **as long as the batch** and at least one element is **`Statement.EXECUTE_FAILED`**.

A batch command that tries to **return a `ResultSet`** also fails that way. `executeLargeBatch()` (Java 8) is the same contract with `long[]` when a count may exceed `Integer.MAX_VALUE`.

`Statement.addBatch(String)` is for **plain** `Statement` objects (typically `INSERT`/`UPDATE` text). Calling it on `PreparedStatement` / `CallableStatement` **throws**. For inserts of many rows with bound values, use **no-arg `addBatch()`** ([[How do JDBC interface types such as Statement and PreparedStatement differ]]).

```d2
direction: right
prep: "prepareStatement\nINSERT … VALUES (?, ?)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
row: "setXxx + addBatch()\nper row" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
run: "executeBatch()\nint[] counts" {
  width: 210
  height: 80
  style.fill: "#e8f5e9"
}

prep -> row -> run
row -> row
```

**Fig. 1.** Same SQL, many parameter tuples. `clearBatch()` empties the list without executing.

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.List;

public final class BatchInserts {
    public static int[] insertNames(Connection con, List<String> names)
            throws SQLException {
        if (!con.getMetaData().supportsBatchUpdates()) {
            throw new SQLException("batch updates are not supported");
        }
        String sql = "INSERT INTO person(name) VALUES (?)";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            for (String name : names) {
                ps.setString(1, name);
                ps.addBatch();
            }
            return ps.executeBatch();
        }
    }
}
```

**Listing 1.** Organize “many rows” as **one prepared insert + a batch list**. Nested try-with-resources still **closes** the statement ([[How do you close a database connection properly]]). For huge lists, call `executeBatch()` every N `addBatch` calls, then keep adding — JDBC does not define N; it only defines the **list then submit** API.

Turn **auto-commit off**, `executeBatch`, then **`commit`** (or `rollback` on `BatchUpdateException`) so a failed batch is not left implementation-defined at `close` ([[How do execute, executeQuery, and executeUpdate differ in JDBC]]). Generated keys from a batch are a separate contract ([[Where do generated identifiers come from when inserting rows in JDBC batch mode]]).

Spring `JdbcTemplate.batchUpdate` / `BatchPreparedStatementSetter` is this same JDBC batch with a callback ([[How does JdbcTemplate batchUpdate work]], [[What is BatchPreparedStatementSetter]]).

> [!warning] `addBatch(String)` on a `PreparedStatement` throws
> Queue **parameter sets** with `addBatch()`. Do not concatenate row values into new SQL strings on the prepared object. Check `supportsBatchUpdates()`; if false, `addBatch` / `executeBatch` throw.

> [!warning] `executeBatch` does not mean “all remaining rows ran”
> After `BatchUpdateException`, the driver **either** always continues **or** always stops — you cannot assume both. Read `getUpdateCounts()` / `getLargeUpdateCounts()`. `SUCCESS_NO_INFO` is **not** zero rows.

> [!warning] A batch is not a `SELECT`
> `executeBatch` throws if a command tries to return a **result set**. Keep the batch to DML (`INSERT`/`UPDATE`/`DELETE`) as `addBatch(String)` documents.

> [!tip] Interview answer
> For many inserts, use one `PreparedStatement`, `addBatch()` after each row’s binds, then `executeBatch()`. That is JDBC’s batch list, not a special SQL keyword. Check `supportsBatchUpdates()`, handle `BatchUpdateException` because leftover commands may or may not have run, and wrap the batch in a transaction if auto-commit is off.

