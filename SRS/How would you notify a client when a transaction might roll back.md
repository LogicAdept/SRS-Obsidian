<!--
reps: 0
priority: 0
-->
#Databases/Transactions #Java/JDBC #SRS

# How would you notify a client when a transaction might roll back?

> [!abstract] Short answer
> JDBC notifies the **Java client** with a **`SQLException`**. When the SQLState **class is `40`** (or a vendor-specific case), drivers throw **`SQLTransactionRollbackException`**: the **current statement was automatically rolled back** (deadlock or serialization failure). It extends **`SQLTransientException`** — retry **without** changing application logic may succeed. Read **`getSQLState()`**, **`getErrorCode()`**, and the **`getNextException()`** chain. There is **no** JDBC `setRollbackOnly`. App-initiated undo is **`Connection.rollback()`** (auto-commit off). Propagate the exception (or a mapped one) to **your** callers.

## How the driver tells the JDBC client

Each `SQLException` carries a message, an XOPEN or SQL:2003 **SQLState** (`DatabaseMetaData.getSQLStateType` says which flavor), a **vendor** code, a **next** exception, and a cause. That bundle **is** the notification ([[What are the main JDBC steps to work with a database]]).

`SQLTransactionRollbackException` (Java 6 / JDBC 4.0) is the typed form of SQLState class **`40`**. It means the database **already rolled back the current statement** because of deadlock or other **transaction serialization** failures. Vendor docs list extra conditions. Catch the subclass when you can; still inspect `getSQLState()` because a driver may throw a plain `SQLException`.

It extends `SQLTransientException`: a previously failed operation **might succeed if retried** with no application-level fix. That is the “might roll back / retry” signal — not a promise the whole transaction is dead on every product.

```d2
direction: down
db: "DBMS rolls back a statement\n(deadlock / serialization)" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}
ex: "SQLTransactionRollbackException\nSQLState class 40\nSQLTransientException" {
  width: 340
  height: 80
  style.fill: "#fff3e0"
}
app: "Catch, log SQLState, rollback if needed, retry or fail the caller" {
  width: 400
  height: 70
  style.fill: "#e8f5e9"
}

db -> ex -> app
```

**Fig. 1.** The client is the JDBC application. The driver notifies by throwing; you decide retry vs fail the next layer.

When **you** abort a unit of work (auto-commit disabled): call **`rollback()`**, which undoes changes since the last commit/rollback and releases locks. **`commit()`** makes them permanent. Both throw if the connection is closed, in auto-commit, or in a distributed transaction. Close only after an explicit commit or rollback — otherwise the outcome is **implementation-defined** ([[How do you close a database connection properly]], [[What transaction isolation levels does JDBC support]]).

JDBC has no `setRollbackOnly`. A container/Spring `TransactionStatus.setRollbackOnly()` is a **different** API; a later commit can surface as `UnexpectedRollbackException` ([[What is UnexpectedRollbackException in Spring REQUIRED propagation]]).

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.SQLTransactionRollbackException;

public final class RollbackNotice {
    public static void run(Connection con) throws SQLException {
        con.setAutoCommit(false);
        try (PreparedStatement ps = con.prepareStatement(
                "UPDATE account SET bal = bal - 1 WHERE id = ?")) {
            ps.setInt(1, 1);
            ps.executeUpdate();
            con.commit();
        } catch (SQLTransactionRollbackException ex) {
            con.rollback();
            throw ex; // SQLState class 40: statement already rolled back; may retry
        } catch (SQLException ex) {
            con.rollback();
            throw ex;
        }
    }
}
```

**Listing 1.** Typed catch is the JDBC notification. Re-throw so **your** client sees the failure. Iterate `ex` / `getNextException()` if you need the full chain.

> [!warning] Class `40` rolled back the **statement**, not always the whole transaction
> Product rules differ (some abort the transaction). After this exception, `commit()` is not “maybe it worked.” `rollback()` when auto-commit is off, then retry only if you treat it as transient.

> [!warning] Do not swallow `SQLException` and then `commit()`
> That is how a caller thinks it committed while the work is gone. JDBC will not call a listener for you; **throwing** is how you notify.

> [!tip] Interview answer
> The JDBC client is notified by `SQLException`. Deadlock and serialization failures are `SQLTransactionRollbackException` (SQLState class `40`), a transient exception you can often retry. For an application abort with auto-commit off, call `Connection.rollback()` and propagate the error. JDBC has no `setRollbackOnly`; that belongs to JTA/Spring, not `java.sql.Connection`.

## See also

- [[What transaction isolation levels does JDBC support]]
- [[How do you close a database connection properly]]
- [[What is UnexpectedRollbackException in Spring REQUIRED propagation]]
- [[What is Spring default rollback policy for Transactional]]
