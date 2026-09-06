<!--
reps: 0
priority: 0
-->
#Java/JDBC #Databases/SQL #SRS

# What are database cursors in JDBC and SQL?

> [!abstract] Short answer
> In **JDBC**, a **cursor** is the **`ResultSet` pointer** to the current row. It starts **before** the first row; **`next()`** advances it. The JDBC tutorial says this **is not a database cursor** — it is a pointer on the Java result table. In **SQL**, a **cursor** is a **named server object**: **`DECLARE … CURSOR FOR query`**, then **`FETCH`**, then **`CLOSE`**. JDBC can **expose** that SQL name via **`ResultSet.getCursorName()`** so **`UPDATE`/`DELETE … WHERE CURRENT OF`** hits the same current row. Default JDBC sets are **forward-only**; SQL cursors default **without hold** (transaction-scoped).

## Two different “cursors”

**JDBC.** `ResultSet` “maintains a cursor pointing to its current row.” `next()` / `previous()` / `absolute()` / `relative()` move it. Default: **forward only**, one pass. Scroll types are `TYPE_SCROLL_INSENSITIVE` / `SENSITIVE` ([[How would you explain ResultSet types scrolling and concurrency modes]], [[How does JDBC ResultSet behave and what configuration options exist]]). Processing SQL with JDBC: you access rows **through a cursor** that is **not** the SQL cursor — it is a pointer on the `ResultSet`.

**SQL.** `DECLARE` creates a cursor “to retrieve a small number of rows at a time out of a larger query.” Rows come with `FETCH`. Position starts **before the first row**; after a fetch it sits on the last row retrieved; running off the end leaves it after last (or before first if fetching backward). PostgreSQL: **no `OPEN`** at the SQL command level — declaring **opens** it (embedded SQL / ECPG still has `OPEN`). `CLOSE` drops it. Default **`WITHOUT HOLD`**: unusable after the creating transaction; must be inside a transaction block. **`WITH HOLD`**: survives **commit** in the same session (abort still drops it) ([[What is a database cursor]]).

`SCROLL` / `NO SCROLL` is SQL’s analog of JDBC scrollability. PostgreSQL: all SQL cursors are **insensitive**; `SENSITIVE` is not available. JDBC `TYPE_SCROLL_SENSITIVE` is a **ResultSet type**, not that SQL keyword.

**The bridge.** In SQL, positioned update/delete names the cursor. JDBC: `getCursorName()` returns “the name of the SQL cursor used by this `ResultSet`.” “The current row of a `ResultSet` object is also the current row of this SQL cursor.” Use `SELECT FOR UPDATE` or positioned updates may fail. The method may throw **`SQLFeatureNotSupportedException`**.

```d2
direction: down
sql: "SQL cursor (named)\nDECLARE / FETCH / CLOSE" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
rs: "ResultSet cursor (Java pointer)\nnext / absolute" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}

sql -> rs: "driver may expose name\ngetCursorName()"
```

**Fig. 1.** Same word, two objects. Only `getCursorName` / `WHERE CURRENT OF` ties them.

```java
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.SQLFeatureNotSupportedException;
import java.sql.Statement;

public final class CursorName {
    public static String sqlName(Statement stmt, String sql) throws SQLException {
        try (ResultSet rs = stmt.executeQuery(sql)) {
            if (!rs.next()) {
                return null;
            }
            try {
                return rs.getCursorName();
            } catch (SQLFeatureNotSupportedException ignored) {
                return null; // ResultSet pointer still works
            }
        }
    }
}
```

**Listing 1.** Walk the JDBC cursor with `next()`. `getCursorName()` is optional. Holdability (`HOLD_CURSORS_OVER_COMMIT`) is a JDBC ResultSet knob; SQL **`WITH HOLD`** is a **DECLARE** option — do not treat them as one flag.

`Types.REF_CURSOR` is a JDBC type code for a **cursor returned from a procedure**, not the ResultSet pointer.

> [!warning] Do not call the ResultSet pointer “the SQL cursor”
> The tutorial draws that line. `next()` does not run SQL `FETCH` unless the driver implements the set that way. `getCursorName` is **not** required.

> [!warning] Default SQL cursors die at transaction end
> PostgreSQL `DECLARE` without `WITH HOLD` **errors outside a transaction block**. JDBC holdability is about **commit** of the Java `ResultSet`, not `DECLARE`. Positioned update wants `FOR UPDATE`.

> [!tip] Interview answer
> JDBC’s cursor is the ResultSet’s current-row pointer; start before row 1 and call `next()`. SQL’s cursor is a named server object you `DECLARE`, `FETCH`, and `CLOSE`, usually inside a transaction. JDBC can expose the SQL cursor name for `WHERE CURRENT OF`. They are related only when the driver supports that name; most Java loops never see it.

## See also

- [[How does JDBC ResultSet behave and what configuration options exist]]
- [[How would you explain ResultSet types scrolling and concurrency modes]]
- [[What is a database cursor]]
- [[How are database query results processed in JDBC]]
