<!--
reps: 0
priority: 0
-->
#Java/JDBC #Java/IO #Problems/Persistence #SRS

# Why must JDBC and I/O resources be closed explicitly?

> [!abstract] Short answer
> **They hold OS or database resources (file/socket handles, sessions, cursors) until `close()`, and nothing in the JVM promptly releases them for you.** `AutoCloseable.close` is what try-with-resources calls so that release is **prompt** and you avoid resource-exhaustion failures. `java.io.Closeable` is the I/O subtype: `close()` drops system resources such as open files and is **idempotent**. JDBC `Connection` / `Statement` / `ResultSet` each say `close()` releases database and JDBC resources **immediately instead of waiting** for automatic release. `Statement.close` also closes its current `ResultSet`. Commit or roll back before `Connection.close()` — an open transaction at close is **implementation-defined** ([[How would you explain the AutoCloseable interface in Java]], [[How do you close a database connection properly]]).

## Handles stay until `close`

`AutoCloseable` (Java 1.7): an object **may hold resources until it is closed**. Exiting a try-with-resources header calls `close()` automatically. That is the supported way to get timely release. A subclass may implement `AutoCloseable` without holding a native handle — still close when you know a resource is there ([[What is try-with-resources]], [[What happens if close throws after a try-with-resources body succeeds]]).

`Closeable` (1.5) extends it for streams: `close()` releases **system resources**; a second close is a no-op. `FileInputStream` / `FileOutputStream` wrap a `FileDescriptor`. `FilterOutputStream.close` flushes, then closes `out`. `ByteArrayInputStream.close()` is a documented **no-op** — not every `close` is a file ([[How does Java]], [[What kinds of input and output streams exist in Java]]).

**JDBC.** `Connection.close()`: release DB/JDBC resources now; already-closed is a no-op. `Statement.close()`: same, and **closes the current `ResultSet`**. It is “generally good practice” to release as soon as you finish so you do not **tie up database resources**. `ResultSet.close()`: same immediate release; the statement also auto-closes the result set when the statement is closed, **re-executed**, or moved to the next result. `Blob`/`Clob`/`NClob` from a result set are **not** closed by `ResultSet.close()` — call `free()`. Declare try-with-resources **Connection, then Statement, then ResultSet** so teardown is reverse: result set, statement, connection ([[How does close behave when using a JDBC connection pool]], [[What is a suppressed exception in try-with-resources]]).

```java
import java.io.FileInputStream;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

class CloseBoth {
    static int count(Connection con, String sql) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            return rs.next() ? rs.getInt(1) : 0;
        } // rs then ps; con left to the caller
    }

    static int firstByte(String path) throws IOException {
        try (FileInputStream in = new FileInputStream(path)) {
            return in.read();
        }
    }
}
```

**Listing 1.** Try-with-resources is the explicit close. Leaving `con` open here is only correct if the caller owns it — still close that `Connection` in **its** try.

```d2
direction: down
app: "try-with-resources" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
io: "Closeable\nFileDescriptor / socket" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
jdbc: "Connection / Statement / ResultSet\nsession + cursor" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
app -> io
app -> jdbc
```

**Fig. 1.** Same reason on both stacks: file/socket handles and database sessions stay until `close()`. AutoCloseable’s point is **prompt** release so you do not exhaust those resources.

> [!warning] Automatic JDBC close is not “never call `close`,” and array streams lie
> Waiting for statement/result auto-close still holds the connection and the cursor until then. Re-executing a `Statement` closes the previous `ResultSet`. Do not skip `close` because `ByteArrayInputStream` is a no-op. Do not throw `InterruptedException` from `close` (suppression vs interrupt flag). Close `Connection` after commit/rollback when auto-commit is off.

> [!tip] Interview answer
> File streams and JDBC objects pin OS handles or database sessions until you close them. Try-with-resources calls `AutoCloseable.close` so that happens promptly and you do not leak files or connections. Close result set, statement, and connection — the statement will close its current result set, but you still close the connection yourself.
