<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# What are the main JDBC steps to work with a database?

> [!abstract] Short answer
> JDBC Basics lists **five** steps: **(1) establish a `Connection`**, **(2) create a statement**, **(3) execute**, **(4) process the `ResultSet`** (if any), **(5) close**. A **driver** must be loadable first (JDBC 4.0+ auto-loads from the classpath). Prefer **`DataSource.getConnection`**. Use **try-with-resources**. `executeUpdate` has **no** set — step 4 is then the **count**.

## The five steps

The JDBC introduction is the same work in three verbs: **connect**, **send** SQL, **retrieve and process** results. The processing tutorial names the objects:

1. **Connection** — `DataSource.getConnection()` (preferred) or `DriverManager.getConnection` with `jdbc:subprotocol:subname` ([[How do you establish a database connection in Java]]).
2. **Statement** — `createStatement()`, `prepareStatement(sql)`, or `prepareCall(sql)` ([[What JDBC statement types exist]]).
3. **Execute** — `executeQuery` (one `ResultSet`), `executeUpdate` (count / DDL), or `execute` then `getResultSet` / `getUpdateCount` / `getMoreResults` ([[How do execute, executeQuery, and executeUpdate differ in JDBC]]).
4. **ResultSet** — cursor starts **before** the first row; `while (rs.next())` and `getXxx`. Skip when you got a count ([[How are database query results processed in JDBC]]).
5. **Close** — `ResultSet`, `Statement`, `Connection` (try-with-resources). Closing the statement closes its current set. Pooled `Connection.close()` returns a **logical** handle ([[How do you close a database connection properly]]).

**Driver.** JDBC 4.0+ drivers on the classpath register as `java.sql.Driver` services. Older drivers need an explicit load. Not a per-query `Class.forName` ([[How do you register a JDBC driver]]).

Auto-commit is **on** by default: each statement is its own transaction unless you `setAutoCommit(false)` and `commit` / `rollback`.

```d2
direction: right
c: "1 Connection" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
s: "2 Statement" {
  width: 140
  height: 50
  style.fill: "#e3f2fd"
}
e: "3 execute" {
  width: 130
  height: 50
  style.fill: "#e8f5e9"
}
r: "4 ResultSet" {
  width: 140
  height: 50
  style.fill: "#f3e5f5"
}
x: "5 close" {
  width: 110
  height: 50
}

c -> s -> e -> r -> x
```

**Fig. 1.** Official processing order. Driver availability sits before step 1.

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.sql.DataSource;

public final class JdbcSteps {
    public static String nameById(DataSource ds, int id) throws SQLException {
        try (Connection con = ds.getConnection();
             PreparedStatement ps = con.prepareStatement(
                     "SELECT name FROM person WHERE id = ?")) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? rs.getString(1) : null;
            }
        }
    }
}
```

**Listing 1.** Steps 1–5. Nested `ResultSet` closes before the statement. Bind `?`; do not concatenate.

> [!warning] Step 4 is not always `next()`
> `INSERT`/`UPDATE`/`DELETE`/DDL use `executeUpdate`. `executeQuery` on those throws. Close the whole chain, not only the `Connection`.

> [!warning] Re-execute closes the current `ResultSet`
> One default set per `Statement`. `getMoreResults` also closes the current set.

> [!tip] Interview answer
> Main JDBC steps: get a `Connection`, create a `Statement` or `PreparedStatement`, execute, walk any `ResultSet` with `next()` and getters, then close everything with try-with-resources. JDBC 4.0+ usually loads the driver for you. Updates return a count instead of a result set.

## See also

- [[How do you establish a database connection in Java]]
- [[How are database query results processed in JDBC]]
- [[How do you close a database connection properly]]
- [[How do you integrate a database with a Java application]]
