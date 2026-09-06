<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# How do you integrate a database with a Java application?

> [!abstract] Short answer
> Use **JDBC**: obtain a **`Connection`** (session) from a **`DataSource`** (preferred) or **`DriverManager`**, create a **`Statement` / `PreparedStatement` / `CallableStatement`**, **`executeQuery` / `executeUpdate` / `execute`**, walk any **`ResultSet`**, then **`close()`** everything (try-with-resources). SQL and drivers are **outside** the JDK; your app talks only to `java.sql` / `javax.sql`. Commit or roll back if auto-commit is off.

## The integration stack

A `Connection` is a **session** with one database ([[How do you establish a database connection in Java]]). JDBC’s preferred factory is **`DataSource`**: a vendor object, typically in **JNDI**, that can be basic, **pooling**, or XA ([[What are database connection pools for]]). `DriverManager.getConnection(jdbc:subprotocol:subname, …)` is the basic alternative; its javadoc tells you to prefer `DataSource` ([[How do you establish a database connection in Java]], [[What parts make up a JDBC URL]]).

Drivers appear via the `jdbc.drivers` property, `java.sql.Driver` **service providers**, or `registerDriver` ([[How do you register a JDBC driver]], [[Why must you load a JDBC database driver]]). Application code does not talk to the vendor protocol; it uses the interfaces.

From the session you create statements ([[How do JDBC interface types such as Statement and PreparedStatement differ]]):

- **`executeQuery`** — one `ResultSet` (never `null`)
- **`executeUpdate`** — DML/DDL row count
- **`execute`** — mixed or unknown results

Then process rows with `next()` / `getXxx` ([[How are database query results processed in JDBC]], [[How do execute, executeQuery, and executeUpdate differ in JDBC]]). Stored procedures use `prepareCall` ([[How do you call a stored procedure from Java]]).

```d2
direction: right
app: "Java app\njava.sql / javax.sql" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
ds: "DataSource\nor DriverManager" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
con: "Connection\nsession" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}
sql: "Statement\nResultSet" {
  width: 180
  height: 80
  style.fill: "#f3e5f5"
}
db: "Database\nvia JDBC driver" {
  width: 200
  height: 80
  style.fill: "#eceff1"
}

app -> ds -> con -> sql -> db
```

**Fig. 1.** The app depends on JDBC interfaces. The driver and URL/DataSource config bind that to a real product.

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import javax.sql.DataSource;

public final class DbIntegration {
    public static String loadName(DataSource ds, int id) throws SQLException {
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

**Listing 1.** End-to-end: factory → session → prepared SQL → result set → auto-close ([[How do you close a database connection properly]]).

In a servlet, inject the `DataSource`, checkout a connection **per request**, and log with `GenericServlet.log` ([[How do you connect to a database and add logging in a servlet]]). That is still this same JDBC loop, not a second database API.

Transactions are a property of the `Connection` (`setAutoCommit`, `commit`, `rollback`, isolation constants). Close during an open transaction is **implementation-defined**. Isolation and statement types stay on that session ([[What transaction isolation levels does JDBC support]]).

JDBC is the **SE API and driver contract**. Your application depends on `java.sql` / `javax.sql`; the vendor JAR supplies the `Driver` / `DataSource` implementation ([[What is JDBC]], [[What is JDBC, an implementation or a specification]]).

> [!warning] Do not hard-code `DriverManager` as “the” integration
> JDBC calls `DataSource` the **preferred** means of getting a connection. In servers that is a JNDI/pool resource. Opening `DriverManager.getConnection` on every request skips pooling and config-by-JNDI.

> [!warning] The `Connection` is the unit you must close
> Leaving it open leaks sockets or pool slots. Nested try-with-resources closes `ResultSet`, then statement, then connection. Commit/rollback **before** `close` if auto-commit is off.

> [!warning] Interfaces are not a database
> Compiling against `java.sql` does not ship a driver. Wrong URL, missing service provider, or a `DataSource` JNDI name that is not bound fails at **`getConnection`**, with `SQLException`.

> [!tip] Interview answer
> Java apps integrate a database through JDBC: a `DataSource` or `DriverManager` yields a `Connection`, you run SQL with statements, read a `ResultSet`, and close resources. Prefer `DataSource` so the server can pool and reconfigure the database without changing call sites. The driver is a separate artifact; your code stays on the JDBC interfaces.

## See also

- [[What is the layered architecture of JDBC]]
- [[What is JDBC]]
- [[How do you register a JDBC driver]]
