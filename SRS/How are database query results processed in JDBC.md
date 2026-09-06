<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# How are database query results processed in JDBC?

> [!abstract] Short answer
> A query returns a **`ResultSet`**: a table with a **cursor**. The cursor starts **before** the first row. You call **`next()`** until it returns `false`, and on each current row you pull columns with **`getXxx(index)`** or **`getXxx(label)`**. Default result sets are **forward-only** and **not updatable** — walk them **once**, first to last. Close the `ResultSet` (and its `Statement`); closing or re-executing the statement **closes** the current result set.

## From SQL to a cursor

`Statement.executeQuery(String)` runs a query (typically `SELECT`) and returns a **single** `ResultSet` that is **never `null`**. `PreparedStatement.executeQuery()` does the same for the precompiled SQL already on that statement (do **not** call the inherited `executeQuery(String)` on a `PreparedStatement` — that throws). For statements that can mix result sets and update counts, `execute` plus `getResultSet` / `getUpdateCount` / `getMoreResults` walks the sequence; `getMoreResults` **implicitly closes** the current `ResultSet`.

A default `Connection.createStatement()` produces result sets of type `TYPE_FORWARD_ONLY` and concurrency `CONCUR_READ_ONLY`. Scrollable or updatable sets need the overloaded `createStatement` that takes type and concurrency — [[How would you explain ResultSet types scrolling and concurrency modes]], [[How does JDBC ResultSet behave and what configuration options exist]].

```d2
direction: right
exec: "executeQuery\nnever-null ResultSet" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
before: "cursor\nbefore first row" {
  width: 220
  height: 80
  style.fill: "#eceff1"
}
row: "next() == true\ngetXxx on current row" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
after: "next() == false\ncursor after last row" {
  width: 250
  height: 80
  style.fill: "#e3f2fd"
}

exec -> before -> row -> after
row -> row
```

**Fig. 1.** Query → empty-looking `ResultSet` → `next` makes row 1 current → getters → `next` until `false`. Getters need a current row.

## Walking rows and reading columns

`ResultSet` is a table of the current query ([[What is JDBC ResultSet]]). `next()` moves the cursor **forward one row**. First `next()` makes row 1 current; when `next()` returns `false`, the cursor sits **after the last row**, and any method that needs a current row throws `SQLException`.

On a valid row, getters (`getString`, `getInt`, `getObject`, …) read a column by **1-based index** or by **label** (SQL `AS` alias, or the column name if there is no `AS`). Index is generally more efficient. Column labels are **case-insensitive**; if several columns share a name, the **first** match wins — use `AS` so labels are unique, or use indexes. `findColumn(label)` maps a label to an index. `getMetaData()` returns `ResultSetMetaData` (count, types, properties of columns).

The driver converts the SQL value to the Java type of the getter you called. SQL `NULL` on `getString` / `getObject` is Java `null`. Primitive getters cannot do that: `getInt` returns **`0`**, `getBoolean` returns **`false`**. Call `wasNull()` **after** the getter to see if that last column was SQL `NULL`.

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public final class QueryProcessing {
    public static void printPeople(Connection con) throws SQLException {
        String sql = "SELECT id, name FROM person ORDER BY id";
        try (PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                int id = rs.getInt(1);
                boolean idNull = rs.wasNull();
                String name = rs.getString(2);
                System.out.println((idNull ? "null" : id) + " " + name);
            }
        }
    }
}
```

**Listing 1.** `executeQuery` never returns `null`; an empty table just makes the `while` skip. `wasNull` is required after primitive getters. Try-with-resources closes `ResultSet` then `PreparedStatement` ([[What is try-with-resources]], [[Why must JDBC and IO resources be closed explicitly]]).

By default **only one** `ResultSet` may be open per `Statement`. Every execute method **implicitly closes** that statement’s current `ResultSet`. Closing the `Statement` closes its current `ResultSet`. `ResultSet.close()` is a no-op if already closed; it does **not** free `Blob` / `Clob` / `NClob` objects from that set.

> [!warning] `next()` before every getter
> The cursor starts **before** the first row. `getXxx` without a current row throws `SQLException`. After `next()` returns `false`, getters still throw. On `TYPE_FORWARD_ONLY`, a **further** `next()` after that is vendor-specific (`false` or `SQLException`).

> [!warning] Columns are 1-based; SQL `NULL` is not Java `0`
> Column `1` is the first select list item. `getInt` / `getBoolean` on SQL `NULL` yield `0` / `false` — indistinguishable from a real zero unless you call `wasNull()` immediately after that getter. For portability, read columns **left to right** and **once** per row.

> [!warning] Re-execute or close the statement and the `ResultSet` is gone
> The generating `Statement` auto-closes the current `ResultSet` on `close`, re-execute, or `getMoreResults`. Interleaving two result sets requires **two** statements. Do not keep using `rs` after `stmt.executeQuery(...)` again.

> [!tip] Interview answer
> JDBC gives you a `ResultSet` whose cursor starts before the first row. You loop `while (rs.next())` and read columns with 1-based `getXxx` calls; default sets are forward-only, one pass, and an empty query still returns a non-null set. Close the set and statement — closing the statement closes the set — and call `wasNull()` after primitive getters.

## See also

- [[How do execute, executeQuery, and executeUpdate differ in JDBC]]
- [[What JDBC statement types exist]]
- [[What are common JDBC SQL types and how do they map to Java types]]
