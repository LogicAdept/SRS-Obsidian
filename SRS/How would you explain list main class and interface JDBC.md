<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# How would you explain list main class and interface JDBC?

> [!abstract] Short answer
> The types you actually name in an interview are the **connection factories** (`DriverManager`, preferred **`DataSource`**), the **`Connection` session**, the **statement chain** (`Statement` → `PreparedStatement` → `CallableStatement`), **`ResultSet`**, and two **metadata** interfaces (`ResultSetMetaData`, `DatabaseMetaData`). **`Driver`** is the SPI a vendor implements. Pooling/XA types (`PooledConnection`, `XAConnection`, `ConnectionPoolDataSource`, `XADataSource`) sit **behind** a `DataSource` — applications do not call them as a second API.

The English title is truncated. The dump question is **list the main JDBC classes and interfaces**.

## Core API types

`java.sql` is the JDBC **core** API; `javax.sql` is the **Optional Package** API (both in Java SE). Module `java.sql` defines the JDBC API and **uses** `java.sql.Driver` ([[What is JDBC]]).

| Type | Kind | Official role |
| --- | --- | --- |
| `DriverManager` | class | Basic service for **managing JDBC drivers**; `getConnection` with a `jdbc:subprotocol:subname` URL |
| `Driver` | interface | What **every driver class must implement**; generally used only by `DriverManager` |
| `DataSource` | interface | **Preferred** factory for connections to a **physical** data source |
| `Connection` | interface | A **session** with a database; create statements; transactions |
| `Statement` | interface | Execute **static** SQL |
| `PreparedStatement` | interface | **Precompiled** SQL + `?` IN parameters |
| `CallableStatement` | interface | **Stored procedures** (call escape, OUT params) |
| `ResultSet` | interface | Table of rows; **cursor** |
| `ResultSetMetaData` | interface | **Columns** of a `ResultSet` |
| `DatabaseMetaData` | interface | The **database as a whole** |

`DriverManager` does **not** “load the driver for you” in the dump’s Class.forName sense. JDBC 4.0+ drivers on the classpath are discovered as `java.sql.Driver` services; you still call `getConnection`. `DataSource` is **not** a prettier `DriverManager`: it can hide URL/user settings, and pooling/XA exist only when the implementation is wired to middle-tier infrastructure. Connections from `DriverManager` do **not** get that pooling/XA story ([[How do you establish a database connection in Java]]).

`Connection` creates statements (`createStatement` / `prepareStatement` / `prepareCall`) and holds transaction control (`setAutoCommit`, `commit`, `rollback`). It does not “form queries” by itself ([[How do JDBC interface types such as Statement and PreparedStatement differ]], [[What transaction isolation levels does JDBC support]]).

`javax.sql.PooledConnection` / `ConnectionPoolDataSource` are for a **pool manager**. `XADataSource` / `XAConnection` are for a **transaction manager**; the application “does not use them directly.” App code still sees `java.sql.Connection` from `DataSource.getConnection()` ([[How does close behave when using a JDBC connection pool]]).

`ParameterMetaData` describes `PreparedStatement` parameters. `Savepoint` is a rollback marker. `RowSet` is a JavaBeans-style set in `javax.sql`. Those are real API pieces, not the first list on a whiteboard ([[What JDBC API pieces are used to build and execute database queries]]).

```d2
direction: right
factory: "DriverManager\nor DataSource" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
con: "Connection" {
  width: 160
  height: 70
  style.fill: "#e3f2fd"
}
stmt: "Statement\nPreparedStatement\nCallableStatement" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
rs: "ResultSet" {
  width: 140
  height: 70
  style.fill: "#f3e5f5"
}

factory -> con
con -> stmt
stmt -> rs
```

**Fig. 1.** Factories produce a session; the session produces statements; statements produce a `ResultSet`. Metadata hangs off the connection or the set.

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import javax.sql.DataSource;

public final class JdbcMainTypes {
    public static int columnCount(DataSource ds) throws SQLException {
        try (Connection con = ds.getConnection();
             PreparedStatement ps = con.prepareStatement("SELECT 1");
             ResultSet rs = ps.executeQuery()) {
            ResultSetMetaData md = rs.getMetaData();
            return md.getColumnCount();
        }
    }
}
```

**Listing 1.** The objects you hold: `DataSource` → `Connection` → `PreparedStatement` → `ResultSet` → `ResultSetMetaData`. `con.getMetaData()` is `DatabaseMetaData`.

> [!warning] Do not treat pool/XA interfaces as the application’s connection API
> You close the **logical** `java.sql.Connection`. You do not call `PooledConnection.close()` from business code. Dump typo `javax.sq1.XADataSource` is `javax.sql.XADataSource`.

> [!warning] `DriverManager` vs `DataSource` are both factories, not equivalents
> Prefer `DataSource`. `DriverManager` is the original mechanism and remains valid. Dump “DataSource does the same tasks, only nicer” skips pooling, JNDI, and transparent properties.

> [!tip] Interview answer
> Main JDBC types: `DriverManager` or preferred `DataSource` to get a `Connection`; `Statement`, `PreparedStatement`, or `CallableStatement` to run SQL; `ResultSet` to read rows; `DatabaseMetaData` and `ResultSetMetaData` for catalog and column shape. Vendors implement `Driver`. Pooling and XA types are infrastructure behind `DataSource`, not a second set of objects your servlet calls.

## See also

- [[What is JDBC]]
- [[How do JDBC interface types such as Statement and PreparedStatement differ]]
- [[What is JDBC ResultSet]]
- [[What JDBC API pieces are used to build and execute database queries]]
