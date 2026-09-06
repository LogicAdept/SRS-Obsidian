<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# What is the difference between PreparedStatement and Statement in JDBC?

> [!abstract] Short answer
> **`Statement`** executes **static SQL** you pass as a **string** on each `executeQuery(sql)` / `executeUpdate(sql)` / `execute(sql)`. **`PreparedStatement` extends `Statement`** and holds a **precompiled** statement (with or without **`?` IN parameters**). You set parameters with **`setInt` / `setString` / …** and call **no-arg** `executeQuery()` / `executeUpdate()`. `Connection.createStatement()` is for SQL **without** parameters; **`prepareStatement(sql)`** is for **parameterized** SQL and for the **same SQL many times**. The `String`-taking execute and `addBatch(sql)` methods **cannot** be called on a `PreparedStatement`.

## Static string vs precompiled parameters

`java.sql.Statement` is “the object used for executing a **static SQL** statement.” `Connection.createStatement()`: “SQL statements **without parameters** are normally executed using `Statement` objects. If the **same SQL** statement is executed **many times**, it may be more efficient to use a `PreparedStatement`.”

`PreparedStatement` is “an object that represents a **precompiled SQL** statement.” `prepareStatement(sql)` creates one “for sending **parameterized** SQL statements.” A statement **with or without** IN parameters can be stored and then executed **multiple times**. Placeholders are **`?`**. Setters must match the SQL type (`INTEGER` → `setInt`); use **`setObject`** when you need a conversion. Indexes are **1-based**. After a getter-style bind, **`setNull(index, sqlType)`** needs an explicit SQL type. **`clearParameters()`** drops the current binds; otherwise values **remain in force** for the next execute ([[How do JDBC interface types such as Statement and PreparedStatement differ]], [[What JDBC statement types exist]]).

**Precompilation is optional.** If the driver supports it, `prepareStatement` may send the SQL to the database then. If not, the SQL may wait until **execute**. That changes **which** methods throw `SQLException`, not the application-facing `?` / setter model.

`CallableStatement` extends `PreparedStatement` and is created with `prepareCall` for stored procedures — a third type, not a substitute for this pair.

```d2
direction: right
stmt: "Statement\ncreateStatement()\nexecuteQuery(sql)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
ps: "PreparedStatement\nprepareStatement(sql)\nsetXxx then executeQuery()" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
cs: "CallableStatement\nprepareCall (stored proc)" {
  width: 250
  height: 70
  style.fill: "#e3f2fd"
}

stmt -> ps: "extends"
ps -> cs: "extends"
```

**Fig. 1.** Inheritance. `String` overloads live on `Statement` and are **illegal** on the subtypes.

## Execute, batch, and quoting

| | `Statement` | `PreparedStatement` |
| --- | --- | --- |
| Factory | `createStatement()` | `prepareStatement(sql)` |
| SQL text | Full command at execute time | Fixed at prepare; `?` for IN values |
| Query / update | `executeQuery(sql)`, `executeUpdate(sql)` | `executeQuery()`, `executeUpdate()` — **no** SQL argument |
| Batch | `addBatch(sql)` — a list of SQL strings | `addBatch()` — a **set of parameters** for the prepared SQL |
| Metadata | `ResultSetMetaData` after execute | Also `getParameterMetaData()` |
| Repeat | New string each time | Rebind and execute again |

Calling `executeQuery(String)`, `executeUpdate(String)`, `execute(String)`, or `addBatch(String)` on a `PreparedStatement` throws **`SQLException`** ([[How do execute, executeQuery, and executeUpdate differ in JDBC]]).

If you must embed a literal in a **static** SQL string, JDBC 4.3 adds `Statement.enquoteLiteral` (single quotes, `'` doubled) and `enquoteIdentifier`. That is still **string SQL**, not a `?` bind ([[How does PreparedStatement mitigate SQL injection compared to Statement]]).

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import javax.sql.DataSource;

public final class StatementVsPrepared {
    public static int countStatic(DataSource ds, String table)
            throws SQLException {
        try (Connection con = ds.getConnection();
             Statement st = con.createStatement();
             ResultSet rs = st.executeQuery(
                     "SELECT COUNT(*) FROM " + st.enquoteIdentifier(table, true))) {
            rs.next();
            return rs.getInt(1);
        }
    }

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

**Listing 1.** `Statement` takes SQL at execute (`enquoteIdentifier` for a name). `PreparedStatement` takes SQL at prepare, binds `?` with `setInt`, then no-arg `executeQuery()`.

> [!warning] `executeQuery(sql)` on a `PreparedStatement` throws
> The `String` overloads are `Statement` methods and “cannot be called on a `PreparedStatement` or `CallableStatement`.” Use the no-arg `executeQuery()` / `executeUpdate()` / `execute()` after `setXxx`. Same trap: `addBatch(sql)` vs `addBatch()`.

> [!warning] Precompile is a driver may, not a guarantee
> `prepareStatement` “is optimized for handling parametric SQL.” Some drivers send SQL immediately; others wait until execute. Do not assume a server-side plan exists just because the type is `PreparedStatement`. Execute with an **unset** `?` throws; leftover `setXxx` values **stay** after a successful execute — rebind what changed, or `clearParameters()`.

> [!warning] Concatenating into the SQL string is still `Statement` semantics
> `prepareStatement("SELECT … WHERE name = '" + name + "'")` has **no** IN parameter. Bind with `?` and `setString`. Identifiers (table/column names) are not `?` values — `enquoteIdentifier` or a fixed identifier list, not user text glued into SQL.

> [!tip] Interview answer
> `Statement` runs static SQL you pass as a string on each execute. `PreparedStatement` extends it: you prepare SQL once, fill `?` with setters, and call no-arg `executeQuery` or `executeUpdate`, which is the path for parameters and for repeating the same SQL. The string-taking execute and `addBatch(sql)` methods throw if you call them on a `PreparedStatement`. Precompilation is optional; the `?` and setter contract is not.

## See also

- [[How do JDBC interface types such as Statement and PreparedStatement differ]]
- [[What JDBC statement types exist]]
- [[How does PreparedStatement mitigate SQL injection compared to Statement]]
- [[How do execute, executeQuery, and executeUpdate differ in JDBC]]
