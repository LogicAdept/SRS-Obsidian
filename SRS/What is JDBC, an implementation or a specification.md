<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# What is JDBC, an implementation or a specification?

> [!abstract] Short answer
> **JDBC is a specification** — the **JDBC API** (JCP **JSR 221**; in Java SE that API is **JDBC 4.3**). It is **not** a database product and **not** one vendor’s driver. The JDK ships the **API** (`java.sql` + `javax.sql`, module **`java.sql`**). A **JDBC driver** is an **implementation**: a class that implements **`java.sql.Driver`** (and the `Connection` / `Statement` / `ResultSet` types you actually call). Java SE also supplies the spec’s **reference implementation** and **TCK**; `Driver.jdbcCompliant()` may be `true` only after the **compliance tests**.

## Specification first, then pluggable implementations

JSR 221 is titled **JDBC API Specification**. The JCP deliverable is a **specification**, plus a **reference implementation** and **Technology Compatibility Kit** (for JDBC 4.3, those RI/TCK artifacts are the **Java SE** platform’s). The spec’s own audience is “vendors of … **drivers that implement the JDBC API**,” plus application servers and tools — and “a starting point for developers of **other APIs layered on top** of the JDBC API.”

Module `java.sql` “defines the JDBC API.” Package `java.sql` is the API for accessing tabular data **and** “a framework whereby **different drivers can be installed dynamically**.” That split is the interview distinction ([[What is JDBC]], [[What is JDBC]]):

- **Specification / API** — interfaces and JDK types you compile against: `Connection`, `Statement`, `PreparedStatement`, `ResultSet`, `Driver`, `DataSource`, `SQLException`, `DriverManager`, `Types`, …
- **Implementation** — a vendor **driver**. `Driver` is “the interface that every driver class must implement.” `DataSource` “is implemented by a driver vendor.” `DriverManager` (a JDK class) asks each **loaded** `Driver` to accept a `jdbc:subprotocol:subname` URL ([[How do you register a JDBC driver]], [[How do you establish a database connection in Java]]).

The API “allows for a broad range of implementations.” Many JDBC features are **optional**; drivers differ. `jdbcCompliant()` is `true` only if the driver passed the JDBC compliance tests (full JDBC API and SQL 92 Entry Level). A lightweight or special-purpose driver may still implement the framework and must report `false` if it did not pass those tests.

```d2
direction: down
spec: "JDBC API Specification\nJSR 221 · java.sql + javax.sql" {
  width: 340
  height: 70
  style.fill: "#e3f2fd"
}
jdk: "Java SE\nAPI types + DriverManager\nRI and TCK" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
drv: "Vendor driver\nimplements java.sql.Driver" {
  width: 300
  height: 65
  style.fill: "#e8f5e9"
}
db: "A particular data source" {
  width: 240
  height: 50
}

spec -> jdk
spec -> drv
drv -> db
```

**Fig. 1.** JDBC names the **contract**. Java SE ships the API (and the JCP RI/TCK). The driver is the **implementation** that talks to one source.

```java
import java.sql.Connection;
import java.sql.Driver;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.stream.Collectors;

public final class JdbcSpecVsImplementation {
    public static Connection open(String url, String user, String password)
            throws SQLException {
        return DriverManager.getConnection(url, user, password);
    }

    public static String loadedDrivers() {
        return DriverManager.drivers()
                .map(Driver::getClass)
                .map(Class::getName)
                .collect(Collectors.joining(", "));
    }
}
```

**Listing 1.** You program the **API** (`DriverManager`, `Connection`). The `Connection` you receive is the **driver’s** object. `drivers()` lists loaded **implementations** of `java.sql.Driver` (JDBC 4.3).

Higher-level persistence libraries sit **on top of** this API; they do not replace the specification. You still need a driver JAR that matches the URL’s subprotocol.

> [!warning] The JDK API is not a PostgreSQL (or Oracle) driver
> Compiling against `java.sql` does not put a wire protocol on the classpath. Without a vendor `Driver` that `acceptsURL` for that `jdbc:subprotocol:subname`, `getConnection` has no implementation for that source.

> [!warning] “JDBC compliant” is a test result, not a class file
> Shipping a class that implements `Driver` is an implementation. Reporting `jdbcCompliant() == true` is allowed **only** after the JDBC compliance tests. Optional API pieces can still be missing; `SQLFeatureNotSupportedException` is part of the contract.

> [!warning] `DriverManager` is a JDK class, not “the JDBC implementation”
> It is the **manager** for a set of drivers. The session object (`Connection`) and the SQL engine behind it come from the **driver** (and the database). `DataSource` is still the preferred factory; a pooling/XA `DataSource` is also a vendor or server **implementation** of the API.

> [!tip] Interview answer
> JDBC is a specification — the JDBC API, JSR 221 — not a database and not one vendor’s library. The JDK ships `java.sql` and `javax.sql`; a driver implements `java.sql.Driver` and supplies the `Connection` you use. Java SE also hosts the spec’s RI and TCK; `jdbcCompliant()` is true only after those tests. You write to the API and plug in a driver for the target database.

## See also

- [[What is JDBC]]
- [[What is JDBC]]
- [[How do you register a JDBC driver]]
- [[How do you establish a database connection in Java]]
