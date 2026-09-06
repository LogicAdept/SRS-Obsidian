<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# What JDBC API pieces are used to build and execute database queries?

> [!abstract] Short answer
> You need a **`Connection`** (from **`DataSource.getConnection`**, preferred, or **`DriverManager`**), then a statement: **`Statement`**, **`PreparedStatement`**, or **`CallableStatement`**. **Queries** that return a table use **`executeQuery`**, which yields a **`ResultSet`**. Parameterized SQL is built on **`PreparedStatement`** with **`?`** and **`setXxx`**. **`executeUpdate`** is for DML/DDL counts, not a query result. Walk the set with **`next()`** and getters.

## The types that build and run a query

Package `java.sql` groups the work as: **connect**, **send SQL**, **retrieve/update results**. Spec overview: `Connection` methods create `Statement` / `PreparedStatement` / `CallableStatement`; those objects **execute SQL and retrieve results**; **`ResultSet` encapsulates a query’s rows** ([[What are the main JDBC steps to work with a database]], [[How are database query results processed in JDBC]]).

| Piece | Role in a query |
| --- | --- |
| **`DataSource`** (preferred) or **`DriverManager`** | Factory for a **`Connection`** — the session in which SQL runs ([[How do you establish a database connection in Java]]). |
| **`Connection`** | `createStatement()`, `prepareStatement(sql)`, `prepareCall(sql)`. Also transaction attributes (`setAutoCommit`, isolation). |
| **`Statement`** | Static SQL **without** `?` markers. `executeQuery(sql)` for a single `ResultSet`. |
| **`PreparedStatement`** | SQL supplied at prepare; **`?` IN parameters** via `setInt` / `setString` / … then **no-arg** `executeQuery()`. Reuse with new binds ([[What is the difference between PreparedStatement and Statement in JDBC]]). |
| **`CallableStatement`** | `prepareCall` — stored procedures; IN/OUT parameters; may still produce a `ResultSet`. |
| **`ResultSet`** | Table of rows. Cursor starts **before** the first row; `next()` + `getXxx`. Default **forward-only**, **read-only** ([[What is JDBC ResultSet]]). |

**Which execute method.** If the SQL is a query returning a `ResultSet`, use **`executeQuery`**. If it is DML/DDL returning a count, use **`executeUpdate`**. If you do not know, use **`execute`**, then `getResultSet` / `getUpdateCount` / `getMoreResults` ([[How do execute, executeQuery, and executeUpdate differ in JDBC]]). `executeQuery` on a non-query throws `SQLException`. On a `PreparedStatement`, the **`String` overloads throw** — use the no-arg methods.

Supporting types you hit while building queries: **`ParameterMetaData`** (prepared IN markers), **`ResultSetMetaData`** (column count/types). **`SQLException`** on access errors. **`Driver`** is required to *reach* the source; you do not call it to compose SQL.

```d2
direction: right
ds: "DataSource /\nDriverManager" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
c: "Connection" {
  width: 140
  height: 50
  style.fill: "#e3f2fd"
}
s: "Statement /\nPreparedStatement" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}
r: "ResultSet" {
  width: 140
  height: 50
  style.fill: "#f3e5f5"
}

ds -> c -> s -> r: "executeQuery"
```

**Fig. 1.** API objects for a SELECT: factory → session → statement → row cursor.

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import javax.sql.DataSource;

public final class JdbcQueryPieces {
    public static String titleById(DataSource ds, int id) throws SQLException {
        try (Connection con = ds.getConnection();
             PreparedStatement ps = con.prepareStatement(
                     "SELECT title FROM article WHERE id = ?")) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? rs.getString(1) : null;
            }
        }
    }
}
```

**Listing 1.** Pieces in one query: `DataSource` → `Connection` → `PreparedStatement` (`?` + `setInt`) → `executeQuery()` → `ResultSet`. Nested try-with-resources (JDBC 4.1 `AutoCloseable`).

`Connection`, `Statement`, and `ResultSet` close in reverse of creation. Closing the statement **closes** its current `ResultSet`. **By default** only **one** `ResultSet` per `Statement` may be open. Re-execute also closes the current set.

> [!warning] `executeQuery` is not `executeUpdate`
> `INSERT` / `UPDATE` / `DELETE` / DDL use `executeUpdate` (a count). `executeQuery` on those throws. A `SELECT` is the `ResultSet` path. Dump “use `execute` for `CREATE TABLE`” is optional — DDL is the documented **`executeUpdate`** case; `execute` is for mixed or unknown shapes. Factories are **`Connection` instance methods**, not `java.sql.createStatement()`.

> [!warning] Do not call `executeQuery(sql)` on a `PreparedStatement`
> The SQL was already given to `prepareStatement`. The `String` execute methods throw `SQLException` on `PreparedStatement` / `CallableStatement`. `setXxx`, then `executeQuery()`.

> [!warning] Getters need `next()` first
> The `ResultSet` cursor starts **before** row 1. `getString` without a successful `next()` throws. After `false`, there is no current row.

> [!tip] Interview answer
> To run a query you obtain a `Connection`, create a `Statement` or more often a `PreparedStatement` with `?` parameters, call `executeQuery`, and walk the `ResultSet` with `next()` and getters. `DataSource.getConnection` is the preferred way to get the session. Updates use `executeUpdate` and do not give you a result set.

## See also

- [[What JDBC statement types exist]]
- [[How do execute, executeQuery, and executeUpdate differ in JDBC]]
- [[What are the main JDBC steps to work with a database]]
- [[What is JDBC ResultSet]]
