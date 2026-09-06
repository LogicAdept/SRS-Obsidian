<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Java/JDBC #SRS

# What are database connection pools for?

> [!abstract] Short answer
> A **connection pool** keeps a set of **already-open** database sessions and **reuses** them. Opening a connection is **expensive** (TCP, auth, and on PostgreSQL a **new backend process**). JDBC: a pooling **`DataSource`** hands out a **logical** `Connection`; `close()` **returns** it, it does not drop the socket. PostgreSQL: **one backend process per connection**; **`max_connections`** defaults to about **100** and **raising it grows shared memory**. Do not “fix” load by exploding that cap — pool in the app and/or put a pooler (PgBouncer **transaction** mode is the usual front) so many clients share few backends.

The dump asked about pooling for Postgres processes. The cue is **what connection pools are for**.

## Why reuse connections

`javax.sql` pooling exists because “creating new connections is very expensive” and pooling “allows a connection to be used and reused.” The app still calls `DataSource.getConnection()` and `Connection.close()`. With a pool, that `Connection` is a **handle** to a `PooledConnection`; the manager puts the physical connection **back in the pool** ([[How does close behave when using a JDBC connection pool]], [[How do you establish a database connection in Java]]). Spring JDBC does **not** implement a pool; it uses a pooling `DataSource` ([[What is connection pooling in Spring JDBC]]).

PostgreSQL is **process-per-connection**: the postmaster **forks a backend** for each client. “The PostgreSQL server can handle multiple concurrent connections… it starts (‘forks’) a new process for each connection.” JDBC is one such client. Those backends are the scarce resource, not Java objects.

`max_connections` is “the maximum number of concurrent connections.” Default is typically **100** (less if the kernel cannot support it at `initdb`). PostgreSQL **sizes resources, including shared memory, from that value**. Increasing it is a server-start parameter, not a free concurrency knob. At most `max_connections` can be active; leftover slots are reserved for superusers.

```d2
direction: down
clients: "Many app threads / HTTP requests" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
pool: "Pool (JDBC DataSource and/or PgBouncer)" {
  width: 320
  height: 55
  style.fill: "#e8f5e9"
}
pg: "Few postgres backends\nmax_connections" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}

clients -> pool -> pg
```

**Fig. 1.** The pool multiplexes chatty clients onto a **small** set of real sessions.

PgBouncer `pool_mode=transaction`: the **server connection is released when the transaction finishes** (session mode waits for client disconnect; statement mode is per query and forbids multi-statement transactions). That is how many clients share few Postgres processes. In transaction mode you **must not rely on session state** (`SET`, temp tables, SQL `PREPARE` without PgBouncer’s prepared-statement tracking) — each transaction may get a **different** backend.

```java
import java.sql.Connection;
import java.sql.SQLException;
import javax.sql.DataSource;

public final class PooledCheckout {
    public static void ping(DataSource ds) throws SQLException {
        try (Connection con = ds.getConnection()) {
            con.isValid(5);
        } // close() returns the handle to the pool
    }
}
```

**Listing 1.** Checkout/return. This is why a pool exists: the next caller skips connect/fork. Nested `REQUIRES_NEW` can still exhaust the pool if each inner TX holds another physical connection ([[Why can REQUIRES_NEW exhaust the connection pool]]).

> [!warning] `max_connections` is not “more users”
> Each slot is a **backend** plus more **shared memory**. Size the **pool** (app + PgBouncer) so backends stay near a measured sweet spot. Raising `max_connections` to match thread count is the dump’s “don’t explode” case.

> [!warning] Transaction pooling is not a session
> PgBouncer transaction mode returns the server at **commit/rollback**. Session features break unless you stay in **session** mode or accept the documented limits. JDBC `Connection.close()` on a pool is still **mandatory**; it is not a no-op.

> [!tip] Interview answer
> Pools exist because connections are expensive: TCP and auth, and on PostgreSQL a whole backend process. JDBC pooling `DataSource`s reuse physical connections; `close()` returns a logical handle. Cap `max_connections` and multiplex with an app pool and/or PgBouncer (often transaction mode) instead of opening one server session per request.

## See also

- [[How does close behave when using a JDBC connection pool]]
- [[What is connection pooling in Spring JDBC]]
- [[How do you establish a database connection in Java]]
- [[Why can REQUIRES_NEW exhaust the connection pool]]
