<!--
reps: 0
priority: 0
-->
#Java/JDBC #Databases/Transactions #SRS

# What transaction isolation levels does JDBC support?

> [!abstract] Short answer
> JDBC defines **five** `Connection` constants. **`TRANSACTION_NONE`** means the driver **does not support transactions** (not JDBC-compliant). The other four match SQL isolation, from weakest to strongest: **`TRANSACTION_READ_UNCOMMITTED`**, **`TRANSACTION_READ_COMMITTED`**, **`TRANSACTION_REPEATABLE_READ`**, **`TRANSACTION_SERIALIZABLE`**. They control **dirty reads**, **non-repeatable reads**, and **phantom reads**. Set with **`setTransactionIsolation`**; **`TRANSACTION_NONE` cannot be passed** to that method. A driver **need not** implement every level and **may substitute a stricter** one.

## Five constants, three anomalies

Isolation says what one transaction may **see** of others on the same source. JDBC **adds `TRANSACTION_NONE`** on top of the four SQL99 levels ([[What are SQL transaction isolation levels]]).

| Anomaly | Meaning |
| --- | --- |
| **Dirty read** | T2 reads T1’s **uncommitted** change; if T1 rolls back, T2 used **transient** data. |
| **Non-repeatable read** | T1 reads a row; T2 **changes** it; T1 reads again and gets **different** values. |
| **Phantom read** | T1 reads all rows matching a `WHERE`; T2 **inserts** a matching row; T1 re-evaluates and sees an extra **phantom** row. |

| Level | Dirty | Non-repeatable | Phantom |
| --- | --- | --- | --- |
| **`TRANSACTION_NONE`** | Transactions **unsupported** (driver is not JDBC-compliant). | | |
| **`TRANSACTION_READ_UNCOMMITTED`** | allowed | allowed | allowed |
| **`TRANSACTION_READ_COMMITTED`** | **prevented** | allowed | allowed |
| **`TRANSACTION_REPEATABLE_READ`** | prevented | **prevented** | allowed |
| **`TRANSACTION_SERIALIZABLE`** | prevented | prevented | **prevented** |

Use **`Connection.setTransactionIsolation(int)`** / **`getTransactionIsolation()`**. Allowed arguments to **set** are the four SQL levels — **not** `TRANSACTION_NONE`. When `TRANSACTION_NONE` is in effect, `DatabaseMetaData.supportsTransactions()` is **false** and `commit` is a **no-op**. Configure isolation with the JDBC method, **not** with raw SQL, when a JDBC method exists. Isolation applies inside a **transaction**; default **auto-commit** makes **each statement** its own transaction until you `setAutoCommit(false)` and `commit` / `rollback`. JDBC **`SERIALIZABLE`** is still the **three-anomaly** contract — it does not add “equivalent to some serial schedule.” **`REPEATABLE_READ` is not** JDBC’s name for snapshot isolation ([[What are dirty reads in transaction isolation]], [[What are phantom reads under weak isolation]], [[What are SQL transaction isolation levels]]).

```d2
direction: right
none: "NONE\nno tx" {
  width: 100
  height: 50
}
ru: "READ_\nUNCOMMITTED" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
rc: "READ_\nCOMMITTED" {
  width: 130
  height: 50
  style.fill: "#ffe0b2"
}
rr: "REPEATABLE_\nREAD" {
  width: 130
  height: 50
  style.fill: "#e8f5e9"
}
ser: "SERIALIZABLE" {
  width: 140
  height: 50
  style.fill: "#c8e6c9"
}

none -> ru -> rc -> rr -> ser: "more restrictive"
```

**Fig. 1.** Least to most restrictive. Higher levels typically mean more locking and **less** concurrency.

**Defaults and gaps.** `DatabaseMetaData.getDefaultTransactionIsolation()` is the **database’s** default among the `Connection` constants — JDBC does not pick one default for every driver. A driver **may omit** some of the four SQL levels. If you request an unsupported level, it **may substitute a higher, more restrictive** level; if it cannot, it throws **`SQLException`**. Probe with **`DatabaseMetaData.supportsTransactionIsolationLevel`**. Calling `setTransactionIsolation` **in the middle of a transaction** is **implementation-defined** (spec recommends applying from the **next** transaction, or committing first). `getTransactionIsolation` should show the new level **when the change actually takes effect**.

```java
import java.sql.Connection;
import java.sql.SQLException;

import javax.sql.DataSource;

public final class JdbcIsolation {
    public static void readCommitted(DataSource ds) throws SQLException {
        try (Connection con = ds.getConnection()) {
            con.setAutoCommit(false);
            con.setTransactionIsolation(Connection.TRANSACTION_READ_COMMITTED);
            try {
                // work
                con.commit();
            } catch (SQLException e) {
                con.rollback();
                throw e;
            }
        }
    }
}
```

**Listing 1.** Turn auto-commit off, then set a **settable** level (`READ_COMMITTED`). Do not pass `TRANSACTION_NONE` to `setTransactionIsolation`.

> [!warning] `TRANSACTION_NONE` is not a level you set
> It means “this driver has **no** transactions.” `setTransactionIsolation` **rejects** it. JDBC-compliant drivers support transactions.

> [!warning] The driver may silently go stricter
> Asking for `READ_UNCOMMITTED` can yield `READ_COMMITTED` or higher. Read `getTransactionIsolation` after set, and check `supportsTransactionIsolationLevel` if you must have a specific anomaly profile.

> [!warning] Mid-transaction changes are implementation-defined
> Do not assume the new level applies to the **current** unit of work, and do not assume it **commits**. Set isolation **before** the work, or after a clean `commit` / `rollback`.

> [!tip] Interview answer
> JDBC supports five isolation constants on `Connection`: `NONE` (no transactions) plus the four SQL levels `READ_UNCOMMITTED`, `READ_COMMITTED`, `REPEATABLE_READ`, and `SERIALIZABLE`. They differ by whether dirty, non-repeatable, and phantom reads can happen. You set a level with `setTransactionIsolation`; you cannot pass `NONE`, and the driver may upgrade to a stricter level if it does not support the one you asked for.

## See also

- [[What is database transaction isolation]]
- [[How do you handle transaction isolation anomalies]]
- [[How do you establish a database connection in Java]]
- [[What is JDBC]]
- [[How would you notify a client when a transaction might roll back]]
