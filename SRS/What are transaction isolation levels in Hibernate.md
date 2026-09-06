<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate #Java/JDBC #Databases/Transactions #SRS

# What are transaction isolation levels in Hibernate?

> [!abstract] Short answer
> Hibernate does **not** invent isolation levels. Isolation is the **JDBC / database** setting on the physical `Connection`. Hibernate uses JDBC (or JTA) **without extra in-memory locks**; “the isolation level of your database transactions **does not change** when you use Hibernate.” Configure it with **`hibernate.connection.isolation`** using the JDBC names **`READ_UNCOMMITTED`**, **`READ_COMMITTED`**, **`REPEATABLE_READ`**, **`SERIALIZABLE`**. If you **omit** the property, Hibernate **does not** call `setTransactionIsolation`. The **`Session`** still gives **repeatable reads** for **id lookup and entity loads** via the **first-level cache** — that is **not** the same as JDBC `REPEATABLE_READ`.

## Physical isolation is JDBC

`JdbcSettings.ISOLATION` (`hibernate.connection.isolation`) is applied when obtaining connections from a `ConnectionProvider` that **respects** the setting — **every built-in provider except `DataSourceConnectionProvider`**. With a container **`DataSource`**, set isolation on the **pool / DataSource**, not this property.

`java.sql.Connection.setTransactionIsolation` accepts four usable constants (`TRANSACTION_NONE` means transactions are **not supported** and must **not** be passed):

| JDBC constant | Allowed phenomena (JDBC spec) |
| --- | --- |
| **`TRANSACTION_READ_UNCOMMITTED`** | Dirty, non-repeatable, and phantom reads |
| **`TRANSACTION_READ_COMMITTED`** | No dirty read; non-repeatable and phantom **can** occur |
| **`TRANSACTION_REPEATABLE_READ`** | No dirty or non-repeatable; **phantoms can** occur |
| **`TRANSACTION_SERIALIZABLE`** | Dirty, non-repeatable, and phantom reads **prevented** |

A **dirty read** is seeing another transaction’s **uncommitted** row. A **non-repeatable read** is rereading a row and getting **different committed** values. A **phantom** is a **new** row matching the same `WHERE` on a second read. The DBMS may implement a level **stricter** than requested; drivers differ — Hibernate does not paper over that.

```properties
# only if the ConnectionProvider applies it (not a typical DataSource)
hibernate.connection.isolation=READ_COMMITTED
```

**Listing 1.** Conceptual: Hibernate forwards the JDBC isolation name; omitted means “leave the connection as the pool created it.”

## What the Session still does

Hibernate **does not lock objects in memory**. Concurrency is the **database’s** (plus **optimistic `@Version`** or **pessimistic `LockMode` / `SELECT … FOR UPDATE`** when you ask). The `Session` is a **transaction-scoped cache**: a second `find` of the **same id** in the **same** persistence context returns the **same instance** without a second SELECT. Hibernate 5.0 also notes that this repeatable-read behavior applies to **entity queries**, **not** to **scalar / reporting** queries.

That cache-level repeatable read can make **`READ_COMMITTED`** *feel* like repeatable read for **managed entities**, while a native SQL scalar query on the same connection still sees **committed** changes from others. Flush / `refresh` / a **new** session go back to the database.

```d2
direction: right
app: "Session\nL1 identity map" {
  width: 220
  height: 100
  style.fill: "#e3f2fd"
}
jdbc: "JDBC Connection\nisolation level" {
  width: 240
  height: 100
  style.fill: "#fff3e0"
}
db: "RDBMS locks / MVCC" {
  width: 200
  height: 100
  style.fill: "#e8f5e9"
}

app -> jdbc -> db
```

**Fig. 1.** Isolation is enforced at the connection/database; L1 only repeats entity state already loaded in this session.

Keep the **physical** transaction **short** (transactional write-behind): do not hold the JDBC transaction open across user think-time. Isolation + row locks held for a conversation is a **scalability** anti-pattern Hibernate documents explicitly.

> [!warning] `hibernate.connection.isolation` is ignored for a DataSource, and L1 is not SERIALIZABLE
> A Spring/Jakarta **`DataSource`** typically goes through **`DataSourceConnectionProvider`**, which **does not** apply this setting — the pool’s isolation wins. L1 repeatable read does **not** stop phantoms, does **not** apply to scalars, and **does not** see updates done with **plain JDBC** or another JVM. Second-level cache **bypasses** DB isolation on purpose (`CacheConcurrencyStrategy` even flags **`READ_WRITE` / `NONSTRICT_READ_WRITE` as incompatible with serializable isolation**). Pessimistic `LockMode` is **extra SQL locking**, not a fifth isolation level.

> [!tip] Interview answer
> Hibernate isolation levels are the JDBC ones: read uncommitted, read committed, repeatable read, serializable. Hibernate does not add in-memory locks; it uses the connection’s isolation as the database implements it. I set hibernate.connection.isolation only when Hibernate opens the connections itself; with a DataSource I configure the pool. The Session still repeatable-reads entities by id in the first-level cache, which is a persistence-context effect, not JDBC REPEATABLE_READ.

See [[What transaction isolation levels does JDBC support]], [[How does the Hibernate first-level cache work in Spring]], [[What are Hibernate first and second level cache tiers]], and [[What is the difference between optimistic and pessimistic locking in Hibernate]].
