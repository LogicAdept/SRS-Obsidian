<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# How do execute, executeQuery, and executeUpdate differ in JDBC?

> [!abstract] Short answer
> **`executeQuery`** is for a statement that produces **one** `ResultSet` (typically `SELECT`): it **returns that set**, never `null`. **`executeUpdate`** is for DML (`INSERT`/`UPDATE`/`DELETE`) or SQL that returns nothing (DDL): it **returns an `int` row count**, or `0` when there is nothing to count — and **throws** if the SQL produces a `ResultSet`. **`execute`** accepts **any** SQL, including stored procedures or unknown text that may yield **several** result sets and/or update counts: it returns a **`boolean`** (`true` = first result is a `ResultSet`) and you then pull results with `getResultSet` / `getUpdateCount` / `getMoreResults`.

## Three shapes of “run this SQL”

On `java.sql.Statement` (Java SE 26) the `String` overloads are:

| Method | Typical SQL | Return | Wrong kind of SQL |
| --- | --- | --- | --- |
| `executeQuery(sql)` | `SELECT` (a **single** result set) | `ResultSet`, **never `null`** | Anything that is not a single `ResultSet` → `SQLException` |
| `executeUpdate(sql)` | `INSERT` / `UPDATE` / `DELETE`, or DDL that returns nothing | `int`: row count, or `0` if nothing | Produces a `ResultSet` → `SQLException` |
| `execute(sql)` | Any statement; uncommon **multiple** results | `boolean`: `true` if the **first** result is a `ResultSet`; `false` if it is an update count **or** there are no results | Not a “kind” check — you inspect the first result |

`PreparedStatement` / `CallableStatement` expose **no-arg** `executeQuery()`, `executeUpdate()`, and `execute()` for the SQL already prepared. Calling the inherited **`executeQuery(String)` / `executeUpdate(String)` / `execute(String)`** on those types **throws** `SQLException`.

All three **execution** methods **implicitly close** that statement’s current `ResultSet` if one is open. By default only one `ResultSet` per `Statement` may be open ([[How are database query results processed in JDBC]]).

```d2
direction: right
sql: "SQL to run" {
  width: 140
  height: 70
  style.fill: "#eceff1"
}
q: "executeQuery\nResultSet" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
u: "executeUpdate\nint count" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
e: "execute\nboolean then getters" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}

sql -> q
sql -> u
sql -> e
```

**Fig. 1.** Pick the method by what you expect back. `execute` is the general dispatcher; the other two fail fast on the wrong result shape.

## `execute` result walking

After `execute` (or a procedure that returns mixed results), the first result is already “current”:

- `true` → `getResultSet()` once (or `null` if this result is not a set)
- `false` → `getUpdateCount()` once (`-1` means this result is a `ResultSet` **or** there are **no more** results)
- `getMoreResults()` moves on and **closes** the current `ResultSet`

There are no more results when:

```java
!stmt.getMoreResults() && stmt.getUpdateCount() == -1
```

**Listing 1.** Conceptual end test from `Statement.getMoreResults`. Call `getResultSet` / `getUpdateCount` **once per result**.

That pattern is why `execute` exists for stored procedures and dynamic SQL ([[How do you call a stored procedure from Java]], [[How do you call a stored procedure from Java]]). Day-to-day `SELECT` / `UPDATE` should use `executeQuery` / `executeUpdate` instead of decoding the boolean.

`executeUpdate` overloads can also request generated keys (`RETURN_GENERATED_KEYS` or column indexes/names); `getGeneratedKeys()` then returns a `ResultSet` of keys. When the row count may exceed `Integer.MAX_VALUE`, `executeLargeUpdate` (Java 8) returns `long` with the same DML/DDL contract.

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public final class ExecuteDispatch {
    public static int rename(Connection con, int id, String name) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement(
                "UPDATE person SET name = ? WHERE id = ?")) {
            ps.setString(1, name);
            ps.setInt(2, id);
            return ps.executeUpdate();
        }
    }

    public static void listIds(Connection con) throws SQLException {
        try (Statement stmt = con.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT id FROM person")) {
            while (rs.next()) {
                rs.getInt(1);
            }
        }
    }
}
```

**Listing 2.** `executeUpdate` → count; `executeQuery` → set you iterate. Both are the no-arg / `String` forms that match the statement type ([[What JDBC statement types exist]]).

> [!warning] Do not use `executeQuery` for DML or `executeUpdate` for `SELECT`
> `executeQuery` throws if the SQL does not produce a **single** `ResultSet`. `executeUpdate` throws if it **does** produce a `ResultSet`. An empty `SELECT` is still a result set (`next()` is just `false`) — that is `executeQuery`, not a `0` from `executeUpdate`.

> [!warning] `Statement.execute(String)` is illegal on a `PreparedStatement`
> Pass the SQL at `prepareStatement` time, then call **`execute()`** with no arguments. The same split applies to `executeQuery` / `executeUpdate`. Supplying an argument to `PreparedStatement.execute()` also throws.

> [!warning] `execute`’s `false` is not “zero rows updated”
> `false` means the first result is an **update count or no result**. Read `getUpdateCount()`. `-1` is “this is a result set, or we are done,” not a failed update. `executeQuery` **never** returns `null`; do not treat a null check as “no rows.”

> [!tip] Interview answer
> `executeQuery` returns a `ResultSet` and is for queries. `executeUpdate` returns a row count and is for DML or DDL that has no result set. `execute` returns a boolean and is for unknown SQL or multiple results — you then call `getResultSet`, `getUpdateCount`, and `getMoreResults`. On a `PreparedStatement` use the no-arg methods; the `String` overloads throw.

## See also

- [[How do JDBC interface types such as Statement and PreparedStatement differ]]
- [[What JDBC API pieces are used to build and execute database queries]]
- [[How do you execute DDL with JdbcTemplate]]
