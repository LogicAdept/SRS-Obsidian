<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# What is JDBC?

> [!abstract] Short answer
> **JDBC** is the **Java API for accessing tabular data**, especially relational databases. Module **`java.sql`** “defines the JDBC API”: packages **`java.sql`** (core) and **`javax.sql`** (the old Optional Package — both ship in **Java SE**). Applications use **`Connection`**, **`Statement` / `PreparedStatement` / `CallableStatement`**, **`ResultSet`**. A **vendor driver** implements **`java.sql.Driver`** and understands a **`jdbc:subprotocol:subname`** URL. **`DataSource`** is the **preferred** connection factory; **`DriverManager`** remains valid.

## API plus pluggable drivers

Package `java.sql` is “the API for accessing and processing data stored in a data source (usually a relational database) using the Java programming language,” including “a framework whereby **different drivers can be installed dynamically**.” It is “mainly geared to passing **SQL** statements,” but can read/write other **tabular** sources (`javax.sql.RowSet`). That is JDBC: a **standard Java interface**, not a particular database product ([[What is JDBC, an implementation or a specification]]).

`javax.sql` adds **`DataSource`** (preferred over `DriverManager`), pooling, distributed transactions, rowsets. Together they are the JDBC API in Java SE (Java SE 21 javadoc labels it **JDBC 4.3**; later JCP maintenance exists).

A **driver** is database-specific. It registers as a `java.sql.Driver` (class-load / **SPI** / optional `jdbc.drivers`). `DriverManager.getConnection` picks a loaded driver that accepts the URL. JDBC 4.0+ drivers on the classpath are discovered automatically ([[How do you register a JDBC driver]], [[How do you establish a database connection in Java]]).

Typical loop: get a `Connection`, create a statement, execute, walk a `ResultSet`, close ([[What are the main JDBC steps to work with a database]]). Default **auto-commit** is **on**: each statement commits unless you `setAutoCommit(false)` then `commit` / `rollback`. If a `DataSource` joins a **distributed (XA)** transaction, the application must not call `Connection.commit` / `rollback` or `setAutoCommit(true)` — the transaction manager owns those. SQL dialects and optional features still vary — check the **driver** ([[How would you explain in how consist advantages using JDBC]], [[What is the layered architecture of JDBC]]).

```d2
direction: down
api: "JDBC API\njava.sql + javax.sql" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
drv: "Vendor Driver" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
db: "Data source" {
  width: 180
  height: 45
}

api -> drv -> db
```

**Fig. 1.** JDBC is the API in the JDK plus a driver for that source.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public final class WhatIsJdbc {
    public static Connection open(String url, String user, String password)
            throws SQLException {
        return DriverManager.getConnection(url, user, password);
    }
}
```

**Listing 1.** `DriverManager` and `Connection` are API types. Prefer `DataSource.getConnection` when you have one. The URL is `jdbc:subprotocol:subname`.

The dump’s “industrial standard” and “only `java.sql`” are incomplete: **`javax.sql` is part of the API**, and `DataSource` is preferred. Driver **self-registration** is real; so is **service-loader** discovery. An old tutorial also lists a test suite and JDBC-ODBC Bridge — those are not what you ship in an app today.

> [!warning] JDBC is not a PostgreSQL (or Oracle) driver
> The JDK does not talk the wire protocol. Without a vendor `Driver`, `getConnection` has nothing for that URL. Optional JDBC features differ by driver.

> [!warning] `DriverManager` is the basic factory, not the preferred one
> `javax.sql.DataSource` is preferred (transparent properties, pooling when wired). `DriverManager.getConnection` still works; it does **not** by itself pool connections.

> [!warning] Auto-commit is on until you turn it off
> Forgetting `setAutoCommit(false)` splits a multi-statement unit of work into several transactions.

> [!tip] Interview answer
> JDBC is Java’s standard API for SQL/tabular data, in `java.sql` and `javax.sql`. You program `Connection`, statements, and `ResultSet`; a vendor driver implements `java.sql.Driver` and matches `jdbc:subprotocol:subname`. `DataSource` is the preferred way to get a connection. It is a specification plus drivers, not a database.

## See also

- [[What is JDBC, an implementation or a specification]]
- [[How do you establish a database connection in Java]]
- [[What are the main JDBC steps to work with a database]]
- [[How do you close a database connection properly]]
- [[What is the layered architecture of JDBC]]
