<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# How does close behave when using a JDBC connection pool?

> [!abstract] Short answer
> The application still calls **`Connection.close()`**. With pooling, that object is only a **logical handle** to a **`PooledConnection`** (the **physical** connection). The pool manager is a **`ConnectionEventListener`**: it **deactivates the handle** and **puts the `PooledConnection` back in the pool**. The **socket is recycled, not closed**. The physical connection is closed only when the **manager** calls **`PooledConnection.close()`** (orderly shutdown or a fatal error). Application code **never** calls `PooledConnection` APIs.

## Logical `close` vs physical `close`

`DataSource.getConnection()` still returns a `java.sql.Connection`. If pooling is in use, that `Connection` is a **handle** to a `PooledConnection`. The manager keeps a pool of those physical objects. On checkout it either reuses one or asks `ConnectionPoolDataSource` for a new physical connection.

When the app calls **`Connection.close()`**:

1. The manager is notified (`addConnectionEventListener`).
2. It deactivates the logical handle.
3. It **returns the `PooledConnection` to the pool** for reuse.

So `Connection.close()` does **not** mean “tear down TCP to the database.” It means “this checkout is finished.” JDBC 9 notes the same pattern: the pool caches `PooledConnection`s; the app closes the **logical** `Connection` **before** that physical object goes back to the cache. If the manager wraps the handle, it must call **`endRequest`** or **`close`** on the logical `Connection` when returning it.

`PooledConnection.close()` **closes the physical connection**. The javadoc says an application **never** calls it; the pool module does, typically on server shutdown or when the connection is unusable.

`Connection.close()` itself is still: release that **handle’s** JDBC resources immediately; a second `close()` is a **no-op**; closing with an **active transaction** is **implementation-defined** — commit or roll back first ([[How do you close a database connection properly]]).

```d2
direction: right
app: "app\nConnection.close()" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
mgr: "pool manager\nConnectionEventListener" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
phys: "PooledConnection\nback in the pool" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}

app -> mgr -> phys
```

**Fig. 1.** Application `close` recycles the physical connection. Only the manager’s `PooledConnection.close()` destroys it.

The same listener idea exists for **statement pooling**: app `PreparedStatement.close()` can recycle a pooled prepared statement instead of dropping it (`StatementEventListener`, Java 6).

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import javax.sql.DataSource;

public final class PooledClose {
    public static void insertName(DataSource ds, String name) throws SQLException {
        try (Connection con = ds.getConnection();
             PreparedStatement ps = con.prepareStatement(
                     "INSERT INTO person(name) VALUES (?)")) {
            ps.setString(1, name);
            ps.executeUpdate();
        }
    }
}
```

**Listing 1.** Try-with-resources still **must** run. Here `con.close()` returns the **handle**; it does not shut the pool ([[What are database connection pools for]], [[How do you establish a database connection in Java]]).

> [!warning] Skipping `Connection.close()` leaks the pool
> The manager only recycles when it is notified of logical close. An unclosed handle stays checked out. `isClosed()` after a pooled `close()` means the **handle** is closed, not that the database is down.

> [!warning] Never call `PooledConnection.close()` from application code
> That API is for the **pool manager**. It closes the **physical** connection. You talk only to the `Connection` from `DataSource.getConnection()`.

> [!warning] Transaction + pooled `close` is still implementation-defined
> Commit or roll back **before** returning the handle. A pool may also reset client state; that is manager-specific. JDBC requires `endRequest` or logical `close` when the manager wraps the handle.

> [!tip] Interview answer
> With a JDBC pool, `Connection.close()` closes the logical handle and returns the physical `PooledConnection` to the pool. The real connection stays open for the next checkout. Only the pool manager calls `PooledConnection.close()` to destroy a physical connection. You still have to close every checkout, usually with try-with-resources.

## See also

- [[How do you connect to a database and add logging in a servlet]]
- [[What is connection pooling in Spring JDBC]]
- [[Why can REQUIRES_NEW exhaust the connection pool]]
