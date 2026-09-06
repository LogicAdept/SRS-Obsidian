<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# How do you establish a database connection in Java?

> [!abstract] Short answer
> Call **`getConnection()`** on a **`javax.sql.DataSource`** (the JDBC **preferred** factory, usually from JNDI) or on **`java.sql.DriverManager`**. You get a **`java.sql.Connection`**: a **session** with that database. The JDBC URL is **`jdbc:subprotocol:subname`**. `DriverManager` picks a loaded `Driver` that understands the URL; `DataSource` already knows how to reach its source. Close the `Connection` when the session ends ([[How do you close a database connection properly]]).

## Preferred: `DataSource.getConnection`

A `DataSource` is a **factory for connections** to the physical source it represents and “the preferred means of getting a connection.” Typical implementations are registered with **JNDI**. `getConnection()` and `getConnection(user, password)` return a `Connection` or throw `SQLException` / `SQLTimeoutException` (login timeout). Three implementation styles exist: basic, **connection pooling**, and **distributed transaction** (almost always pooled). Changing server properties on the `DataSource` avoids rewriting callers ([[What are database connection pools for]]).

In a Jakarta servlet the factory is often `@Resource`-injected; each request still calls `getConnection()` ([[How do you connect to a database and add logging in a servlet]]).

## Also: `DriverManager.getConnection`

`DriverManager` is “the basic service for managing a set of JDBC drivers.” Its own javadoc points at `DataSource` as the **preferred** connect path. Three static overloads:

- `getConnection(String url)`
- `getConnection(String url, String user, String password)`
- `getConnection(String url, Properties info)` — **normally** include `"user"` and `"password"`

`url` has the form `jdbc:subprotocol:subname` ([[What parts make up a JDBC URL]]). A **`null` url** throws `SQLException`. The manager selects a suitable driver from those loaded at initialization (`jdbc.drivers` plus `java.sql.Driver` **service providers**) and those registered with the current application class loader ([[How do you register a JDBC driver]], [[Why must you load a JDBC database driver]]).

If user/password (or another property) appears **both** in the URL and in `Properties` / the user-password arguments, **precedence is implementation-defined**. Specify each property **once**.

```d2
direction: down
pref: "DataSource\nJNDI / pool (preferred)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
basic: "DriverManager.getConnection\njdbc:subprotocol:subname" {
  width: 320
  height: 70
  style.fill: "#fff3e0"
}
con: "Connection\nsession for SQL" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}

pref -> con
basic -> con
```

**Fig. 1.** Same `Connection` type either way. `DataSource` is what JDBC tells you to use when a naming/pooling layer exists.

```java
import java.sql.Connection;
import java.sql.SQLException;

import javax.sql.DataSource;

public final class EstablishConnection {
    public static Connection open(DataSource ds) throws SQLException {
        return ds.getConnection();
    }
}
```

**Listing 1.** Preferred open. The caller must `close()` the returned handle (try-with-resources at the use site).

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public final class EstablishWithUrl {
    public static Connection open(String url, String user, String password)
            throws SQLException {
        return DriverManager.getConnection(url, user, password);
    }
}
```

**Listing 2.** Basic `DriverManager` path. Does **not** by itself create a pool.

The object you hold is the session: `createStatement` / `prepareStatement` / `prepareCall` live on it ([[How do JDBC interface types such as Statement and PreparedStatement differ]], [[What JDBC statement types exist]]). Establishing a connection is **not** executing SQL; that is `executeQuery` / `executeUpdate` afterward ([[How are database query results processed in JDBC]]).

> [!warning] `DriverManager.getConnection` is not pooling
> A successful return is one session. Calling it on every web request without a pooling `DataSource` opens a new physical connection each time. `DataSource` javadoc’s pooling implementation is the type that “will automatically participate in connection pooling.”

> [!warning] Duplicate user/password in URL and arguments
> The winner is **implementation-defined**. Portable code sets credentials in **one** place.

> [!warning] No driver for that URL
> `getConnection` only searches **loaded** drivers. A missing service provider or `jdbc.drivers` entry fails at connect time with `SQLException`, not at compile time.

> [!tip] Interview answer
> In Java you establish a JDBC session by calling `getConnection` on a `DataSource` or on `DriverManager`. `DataSource` is the preferred factory, usually from JNDI or a pool. `DriverManager` takes a `jdbc:subprotocol:subname` URL and optional user/password. Close the `Connection` when you are done.

## See also

- [[What is JDBC]]
- [[How do you register a JDBC driver]]
- [[How do you integrate a database with a Java application]]
- [[What parts make up a JDBC URL]]
