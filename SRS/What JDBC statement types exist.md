<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# What JDBC statement types exist?

> [!abstract] Short answer
> Three interfaces, in an inheritance line: **`Statement`**, **`PreparedStatement` extends `Statement`**, **`CallableStatement` extends `PreparedStatement`**. Create them on a **`Connection`**: **`createStatement()`**, **`prepareStatement(sql)`**, **`prepareCall(sql)`**. `Statement` runs **static SQL** with **no `?` markers**. `PreparedStatement` adds **IN parameters** (`?` + `setXxx`) and a **precompiled** command. `CallableStatement` runs **stored procedures** (`{call …}` / `{?= call …}`), with **IN / OUT / INOUT** and **`registerOutParameter`** before execute.

## Three types, one hierarchy

Package `java.sql` lists them under “sending SQL statements to a database.” Spec chapter 13: `Statement` executes SQL **without parameter markers**; `PreparedStatement` **adds setters** for markers; `CallableStatement` **adds getters** for values **returned from stored procedures** ([[What is the difference between PreparedStatement and Statement in JDBC]]).

| Type | Factory | SQL | Extra contract |
| --- | --- | --- | --- |
| **`Statement`** | `createStatement()` | Full string at `executeQuery(sql)` / `executeUpdate(sql)` / `execute(sql)` | No `?`. JDBC 4.3 `enquoteLiteral` / `enquoteIdentifier` if you must quote text in that string. |
| **`PreparedStatement`** | `prepareStatement(sql)` | SQL at prepare; **`?`** for IN values that vary | `setXxx(index, …)` (index from **1**). No-arg `executeQuery()` / `executeUpdate()`. **`String` execute overloads throw.** Precompile is **driver-optional**. |
| **`CallableStatement`** | `prepareCall(sql)` | JDBC **escape**: `{call name(?,…)}` or `{?= call name(?,…)}` | IN via inherited setters. **Every OUT** must be **`registerOutParameter`** *before* execute; then `getXxx`. INOUT is both. Ordinal **or** parameter **name**. |

All three are **`AutoCloseable`**. Default `ResultSet` from any of them is **`TYPE_FORWARD_ONLY`** + **`CONCUR_READ_ONLY`**. `executeQuery` vs `executeUpdate` vs `execute` is the same three-way choice on each type ([[How do execute, executeQuery, and executeUpdate differ in JDBC]]). There is **no fourth** `java.sql` statement interface.

```d2
direction: down
st: "Statement\ncreateStatement — static SQL" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
ps: "PreparedStatement\nprepareStatement — ? IN params" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
cs: "CallableStatement\nprepareCall — stored procedures" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}

st -> ps: "extends"
ps -> cs: "extends"
```

**Fig. 1.** The only JDBC statement types. Each subtype keeps the parent’s execute/batch rules except the `String` overloads, which throw.

A `CallableStatement` may return **one or several** `ResultSet`s (via `Statement` `getResultSet` / `getMoreResults`). For portability, **process result sets and update counts before reading OUT parameters**.

```java
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Types;

import javax.sql.DataSource;

public final class JdbcStatementTypes {
    public static int countArticles(DataSource ds) throws SQLException {
        try (Connection con = ds.getConnection();
             Statement st = con.createStatement();
             ResultSet rs = st.executeQuery("SELECT COUNT(*) FROM article")) {
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

    public static String callProc(DataSource ds, int id) throws SQLException {
        try (Connection con = ds.getConnection();
             CallableStatement cs = con.prepareCall("{call lookup_title(?, ?)}")) {
            cs.setInt(1, id);
            cs.registerOutParameter(2, Types.VARCHAR);
            cs.execute();
            return cs.getString(2);
        }
    }
}
```

**Listing 1.** One method per type. `lookup_title` is illustrative SQL; OUT parameter **2** is registered **before** `execute()`. Prefer `PreparedStatement` for ordinary parameterized DML/SELECT ([[How do you call a stored procedure from Java]]).

> [!warning] `executeQuery(sql)` on `PreparedStatement` or `CallableStatement` throws
> The `String` execute and `addBatch(sql)` methods are `Statement`-only. Subtypes already have their SQL; use no-arg `executeQuery()` / `execute()` after `setXxx`.

> [!warning] OUT parameters: register first, results before getters (portability)
> Unregistered OUT → execute fails. `wasNull()` after an OUT getter is how you detect SQL `NULL`. Reading OUT **before** draining `ResultSet`s is legal on some drivers and not others — process sets/counts first.

> [!warning] These are not `ResultSet` types
> `TYPE_FORWARD_ONLY` / `TYPE_SCROLL_INSENSITIVE` / `TYPE_SCROLL_SENSITIVE` describe the **cursor**, set on `createStatement` / `prepareStatement` / `prepareCall` overloads. They are not extra statement interfaces.

> [!tip] Interview answer
> JDBC has three statement types: `Statement` for static SQL, `PreparedStatement` for precompiled SQL with `?` input parameters, and `CallableStatement` for stored procedures. They form an extends chain, created with `createStatement`, `prepareStatement`, and `prepareCall`. For a stored procedure, register every OUT parameter before execute, and for portability read result sets before OUT values.

## See also

- [[How do JDBC interface types such as Statement and PreparedStatement differ]]
- [[What is the difference between PreparedStatement and Statement in JDBC]]
- [[How do you call a stored procedure from Java]]
- [[How do execute, executeQuery, and executeUpdate differ in JDBC]]
