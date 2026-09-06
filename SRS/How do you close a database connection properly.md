<!--
reps: 0
priority: 0
-->
#Java/JDBC #Java/Exceptions/TryCatch/TryWithResources #SRS

# How do you close a database connection properly?

> [!abstract] Short answer
> **`Connection` is `AutoCloseable`.** Put it in **try-with-resources** (with the `Statement` / `PreparedStatement` and `ResultSet` you opened) so `close()` runs on every path. `close()` releases the connection’s database and JDBC resources **immediately**; a second `close()` is a no-op. **Commit or roll back** an open transaction **before** `close` — if a transaction is still active, the outcome is **implementation-defined**. A pooled `Connection.close()` still must be called: it closes the **logical** handle ([[How does close behave when using a JDBC connection pool]]).

## What `close()` actually does

`Connection.close()` “releases this `Connection` object's database and JDBC resources immediately instead of waiting for them to be automatically released.” `Statement.close()` is the same idea for a statement and **also closes** its current `ResultSet`. A `ResultSet` is also closed when its statement is closed, re-executed, or moved to the next result. All three `close()` methods are no-ops if already closed.

`isClosed()` is `true` after `close()` (or some fatal errors). It is **not** a liveness probe: the javadoc says a typical client learns a connection is invalid by **catching exceptions** on the next operation, not by polling `isClosed()`.

```d2
direction: right
work: "use Connection\nStatement · ResultSet" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
tx: "commit or rollback\nif auto-commit is off" {
  width: 250
  height: 80
  style.fill: "#e3f2fd"
}
cls: "close ResultSet, Statement,\nthen Connection" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}

work -> tx -> cls
```

**Fig. 1.** Finish the unit of work, end the transaction, then release JDBC objects. Try-with-resources closes declared resources **in reverse order**, which matches ResultSet → statement → connection ([[What is try-with-resources]], [[How would you explain the AutoCloseable interface in Java]]).

`abort(Executor)` (Java 7) **marks the connection closed** and may keep releasing resources on that executor. That is an administrator-style abort, not the normal application `close()`.

## Try-with-resources is the default pattern

Declare the connection and everything created from it in one `try`, so a failure in `executeQuery` still closes what did open ([[Why must JDBC and IO resources be closed explicitly]], [[What happens if close throws after a try-with-resources body succeeds]]):

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public final class CloseConnectionProperly {
    public static String nameById(Connection con, int id) throws SQLException {
        try (con;
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

**Listing 1.** Java 9+ `try (con; …)` closes the existing `Connection` after the inner resources. If this method should **not** own the connection (Spring/pool checkout in an outer transaction), omit `con` from the `try` and only close the statement and result set.

With auto-commit **off**, commit or roll back **before** that `close()`:

```java
con.setAutoCommit(false);
try (PreparedStatement ps = con.prepareStatement(
        "UPDATE person SET name = ? WHERE id = ?")) {
    ps.setString(1, name);
    ps.setInt(2, id);
    ps.executeUpdate();
    con.commit();
} catch (SQLException e) {
    con.rollback();
    throw e;
}
```

**Listing 2.** Conceptual: `rollback` is only legal with auto-commit disabled. Closing with a transaction still open is implementation-defined.

JDBC 9 connection-pool notes describe the usual manager pattern: the pool caches `PooledConnection` objects, hands the app a **logical** `Connection`, and the app calls **`Connection.close`** before that pooled physical connection goes back to the cache. Application code still **closes**; it does not call `beginRequest` / `endRequest` (those are for pooling managers).

> [!warning] Do not `close()` with an open transaction
> Commit or roll back first when auto-commit is off. If you `close` while a transaction is still active, the result is **implementation-defined** — there is no portable “rollback on close” guarantee.

> [!warning] `isClosed()` is not “is the database up”
> It reports whether **`close` was called** (or a fatal error). A still-open handle can already be dead on the server. `close()` on a closed connection is a no-op; it does not tell you the network is healthy.

> [!warning] Skipping `close` on a pooled connection leaks the pool
> Returning a logical connection without `close()` keeps it checked out. `close()` here is not optional cleanup. What the physical socket does next is the pool’s job ([[How does close behave when using a JDBC connection pool]], [[What are database connection pools for]]).

> [!tip] Interview answer
> Close a JDBC `Connection` with try-with-resources so `close()` always runs; it implements `AutoCloseable`. Commit or roll back first if auto-commit is off, because closing during a transaction is implementation-defined. Close statements and result sets too — closing a statement closes its current result set. On a pool you still call `close()`; that returns the logical connection.

## See also

- [[How does JDBC ResultSet behave and what configuration options exist]]
- [[What happens if a try-with-resources resource is null]]
