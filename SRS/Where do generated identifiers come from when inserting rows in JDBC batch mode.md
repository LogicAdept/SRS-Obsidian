<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# Where do generated identifiers come from when inserting rows in JDBC batch mode?

> [!abstract] Short answer
> The identifiers come from the **database**, not from JDBC and not from `executeBatch`’s `int[]`. Many DBMS products **generate a unique key on INSERT** (identity / serial / sequence / trigger). JDBC only **retrieves** those values with **`Statement.getGeneratedKeys()`**, after you asked for them with **`Statement.RETURN_GENERATED_KEYS`** (or column names/indexes) on **`prepareStatement`** / **`executeUpdate`**. **`executeBatch` returns update counts**, ordered as `addBatch` — it does **not** return keys. A `getGeneratedKeys` `ResultSet` has **one row per key the statement generated**, or is **empty**. After a **batch**, filling that set is **not a portable JDBC 3.0 batch guarantee** — check the **driver**.

## The database generates; JDBC fetches

JDBC 3.0 §13.6: “Many database systems have a mechanism that automatically generates a unique key field when a row is inserted.” `getGeneratedKeys()` returns a `ResultSet` with **a column for each** such key. If no keys were generated, the set is **empty**. An `INSERT … SELECT` can produce **more than one** key row. The set is **`CONCUR_READ_ONLY`** and `TYPE_FORWARD_ONLY` or `TYPE_SCROLL_INSENSITIVE`.

You must **signal** the driver when the statement is **prepared or executed**, not when `addBatch` runs:

- `Connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)` — typical for a **batched** `PreparedStatement`
- `prepareStatement(sql, columnIndexes)` / `prepareStatement(sql, columnNames)` — name the key columns
- `Statement.executeUpdate(sql, RETURN_GENERATED_KEYS)` (or name/index arrays) — **one** INSERT, not a batch

The flag/array is **ignored** if the SQL is not an `INSERT` **or** another statement the **vendor** lists as able to return generated keys. If you omit column names/indexes, **the driver chooses** which columns “best represent” the keys ([[How do you organize batch inserts for many rows]]).

`DatabaseMetaData.supportsGetGeneratedKeys()` is `true` only if the driver can retrieve keys after a statement executes, and then **at least for INSERT**. JDBC 4.1 `generatedKeyAlwaysReturned()` asks whether a key comes back when named/indexed columns are valid and the statement succeeds — the value **may or may not** be from those columns; **consult the driver**.

```d2
direction: down
db: "DBMS\nidentity / serial / sequence" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
batch: "executeBatch\nint[] update counts" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
keys: "getGeneratedKeys()\nResultSet of DB keys" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}

db -> batch: "INSERTs run"
db -> keys: "if driver supports it"
```

**Fig. 1.** Batch result is counts. Keys, if any, are **DB-generated** values read through `getGeneratedKeys`.

## Batch mode does not return keys in the `int[]`

Chapter 15: `executeBatch` runs commands **in add order** and, on full success, returns an `int[]` of **update counts** (`SUCCESS_NO_INFO` / `EXECUTE_FAILED` on errors). It **closes** the current `ResultSet` and **clears** the batch. Spec advice: **`setAutoCommit(false)`** for batches so you can commit or roll back after a partial failure.

The generated-keys API is wired to **`execute` / `executeUpdate` / `prepareStatement`**, not to `addBatch`. Portable code therefore does **not** treat `getGeneratedKeys` after `executeBatch` as required. Some drivers fill a multi-row key `ResultSet` in batch add-order; others return empty, throw, or (Oracle) give **`ROWID`** when you used the integer flag instead of column names. Oracle’s JDBC guide: values come from **sequences and triggers**; with `RETURN_GENERATED_KEYS` and **no** column list, the “key” is **`ROWID`**.

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import javax.sql.DataSource;

public final class BatchGeneratedKeys {
    public static void insertTitles(DataSource ds, String[] titles)
            throws SQLException {
        try (Connection con = ds.getConnection();
             PreparedStatement ps = con.prepareStatement(
                     "INSERT INTO article (title) VALUES (?)",
                     Statement.RETURN_GENERATED_KEYS)) {
            con.setAutoCommit(false);
            for (String title : titles) {
                ps.setString(1, title);
                ps.addBatch();
            }
            ps.executeBatch();
            try (ResultSet keys = ps.getGeneratedKeys()) {
                while (keys.next()) {
                    keys.getObject(1);
                }
            }
            con.commit();
        }
    }
}
```

**Listing 1.** Keys are requested at **prepare**. After `executeBatch`, `getGeneratedKeys` is the retrieval API — **if** this driver implements it for batches. `getObject(1)` because the driver chose the column. Not portable without a driver check.

> [!warning] `executeBatch` is not `getGeneratedKeys`
> The `int[]` is **row counts**, not identifiers. Reading `updateCounts[i]` as an id is wrong (`SUCCESS_NO_INFO` is `-2`).

> [!warning] No column list → the driver invents the “key”
> Unspecified columns: the implementation picks what “best represent” generated keys. That might be an identity column, a `ROWID`, or something else. Prefer **column names or indexes**. `generatedKeyAlwaysReturned` still allows a key **not** based on those columns.

> [!warning] Batch + generated keys is driver terrain
> JDBC 3.0 batch chapter never promises a key `ResultSet` after `executeBatch`. `supportsGetGeneratedKeys` is about retrieval **after a statement has executed**, and only **INSERT** is required when it is `true`. If the batch path is empty or throws `SQLFeatureNotSupportedException`, insert one row at a time with `executeUpdate` and `getGeneratedKeys`, or read keys with a follow-up query the DBMS documents.

> [!tip] Interview answer
> In batch inserts the identifiers still come from the database’s identity, serial, or sequence — JDBC does not allocate them. You prepare with `RETURN_GENERATED_KEYS` (or named key columns), `addBatch` / `executeBatch` for the counts, then `getGeneratedKeys()` for a `ResultSet` of those DB values. `executeBatch` itself only returns update counts, and filling `getGeneratedKeys` after a batch is not a portable guarantee; it depends on the driver.

## See also

- [[How do you organize batch inserts for many rows]]
- [[How do execute, executeQuery, and executeUpdate differ in JDBC]]
- [[What JDBC statement types exist]]
- [[What is JDBC ResultSet]]
