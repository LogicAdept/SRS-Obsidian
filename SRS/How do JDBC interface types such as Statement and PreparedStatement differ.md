<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# How do JDBC interface types such as Statement and PreparedStatement differ?

> [!abstract] Short answer
> JDBC’s executable SQL objects form a chain: **`Statement`** → **`PreparedStatement`** → **`CallableStatement`**. `Statement` (from `Connection.createStatement`) runs **static** SQL you pass as a `String` on each `execute*` call. `PreparedStatement` (from `prepareStatement`) holds **one** SQL string that may contain **`?` IN placeholders**, binds values with `setXxx`, and is meant to be **reused**. `CallableStatement` (from `prepareCall`) extends that for **stored procedures**, with JDBC call-escape syntax and **OUT** parameters. On a prepared or callable object you must use the **no-arg** `executeQuery` / `executeUpdate` / `execute` — the `String` overloads throw.

## Three interfaces, one hierarchy

```d2
direction: right
stmt: "Statement\nstatic SQL String" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
ps: "PreparedStatement\nprecompiled SQL + ? IN" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
cs: "CallableStatement\nprocedure IN / OUT" {
  width: 250
  height: 80
  style.fill: "#e3f2fd"
}

stmt -> ps -> cs
```

**Fig. 1.** `PreparedStatement extends Statement`. `CallableStatement extends PreparedStatement`. Factory methods: `createStatement`, `prepareStatement`, `prepareCall` ([[What JDBC statement types exist]]).

`Connection.createStatement` is for SQL **without** parameters in the usual case. The same connection text says that if you run the **same** SQL many times, a `PreparedStatement` **may be more efficient**. `prepareStatement` takes SQL that **may** contain one or more `?` IN placeholders — parameterized **or** not. Precompilation is a **driver optimization**: if the driver supports it, `prepareStatement` may send SQL early; if not, send can wait until execute. That changes **which call throws** `SQLException`, not the Java API you write.

`PreparedStatement` is “an object that represents a precompiled SQL statement,” reused with new IN values via setters (`setInt`, `setString`, …). Types should match the SQL parameter type; otherwise `setObject` with a target SQL type. Parameter indexes are **1-based**. `addBatch()` on a prepared statement queues **the current parameter set**; `Statement.addBatch(String)` queues **another SQL string**.

`CallableStatement` is for **stored procedures**. JDBC call escape:

```text
{?= call proc(?, ?)}
{call proc(?, ?)}
```

**Listing 1.** Conceptual JDBC call escapes. A result parameter, if present, is an OUT parameter. IN values use `PreparedStatement` setters. **Every OUT parameter must be registered** with `registerOutParameter` **before** execute; read it with `getXxx` afterward. Process result sets and update counts **before** reading OUT values for portability ([[How do you call a stored procedure from Java]], [[How do you call a stored procedure from Java]]).

## How you run SQL on each type

| | `Statement` | `PreparedStatement` |
| --- | --- | --- |
| Created by | `createStatement()` | `prepareStatement(sql)` |
| SQL text | Argument of `executeQuery(sql)` / `executeUpdate(sql)` / `execute(sql)` | Fixed at prepare; `?` bound with `setXxx` |
| Execute methods | `String` overloads | **No-arg** `executeQuery()` / `executeUpdate()` / `execute()` |
| Typical use | One-off static SQL | Repeated or parameterized SQL |

`CallableStatement` uses the same no-arg execute methods, plus OUT getters. Mixed results still use `execute` + `getResultSet` / `getUpdateCount` / `getMoreResults` ([[How do execute, executeQuery, and executeUpdate differ in JDBC]]).

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public final class StatementVsPrepared {
    public static void staticSelect(Connection con) throws SQLException {
        try (Statement stmt = con.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT id FROM person")) {
            while (rs.next()) {
                rs.getInt(1);
            }
        }
    }

    public static String nameById(Connection con, int id) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement(
                "SELECT name FROM person WHERE id = ?")) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? rs.getString(1) : null;
            }
        }
    }
}
```

**Listing 2.** Static SQL on `Statement` vs a `?` bound with `setInt` on `PreparedStatement`. Do not build `WHERE id = ` + id into the SQL string ([[How does PreparedStatement mitigate SQL injection compared to Statement]]).

> [!warning] `executeQuery(String)` on a `PreparedStatement` throws
> The `String` execute methods **cannot** be called on `PreparedStatement` or `CallableStatement`. Prepare the SQL once, `setXxx`, then `executeQuery()` with **no** argument. Supplying an argument to `PreparedStatement.execute()` also throws.

> [!warning] Placeholders only help if the SQL is fixed
> `?` is an IN parameter, not a hole for identifiers or extra SQL. Concatenating user text into the string you pass to `prepareStatement` is still a `Statement`-style string, just prepared. Bind values with setters; keep table and column names in **your** SQL.

> [!warning] Precompile is not guaranteed
> `prepareStatement` **may** send SQL immediately or wait until execute, depending on the driver. Do not assume a server-side plan exists after `prepareStatement` returns, and do not assume `Statement` is “always slower.” Efficiency is the documented **reason to prefer** a prepared object for repeated SQL, not a hard timing contract.

> [!tip] Interview answer
> `Statement` runs static SQL you pass on each execute. `PreparedStatement` extends it: one SQL string with `?` IN parameters, setters, and no-arg execute methods, intended for reuse. `CallableStatement` extends `PreparedStatement` for stored procedures, with OUT parameters registered before execute. Use prepare-and-bind for values; never glue user input into the SQL text.

## See also

- [[What is the difference between PreparedStatement and Statement in JDBC]]
- [[What is the difference between PreparedStatement and Statement in JDBC]]
- [[How are database query results processed in JDBC]]
- [[How would you explain SQL injection attacks and defenses]]
