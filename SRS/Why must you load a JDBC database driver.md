<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# Why must you load a JDBC database driver?

> [!abstract] Short answer
> **JDBC is the API; the driver is the implementation** that speaks the database. `DriverManager.getConnection` only succeeds if some **loaded** `java.sql.Driver` **recognizes the URL** and returns a `Connection`. Loading the driver class runs its **static initializer**, which **`registerDriver`s** an instance. Without that, there is nobody to accept `jdbc:subprotocol:subname`. JDBC **4.0+** still loads drivers — from **`META-INF/services/java.sql.Driver`** (and `jdbc.drivers`) — so **`Class.forName` is often unnecessary**, but the **driver JAR must still be on the classpath**.

## The API has no wire protocol

Package `java.sql` is a **framework** for installing **different drivers dynamically**. Spec chapter 9: every JDBC driver **implements `Driver`** and **must** have a **static initializer** that constructs an instance and calls `DriverManager.registerDriver`. `Class.forName("com.acme.jdbc.AcmeJdbcDriver")` loads that class; the initializer registers it. Drivers also need a **niladic constructor** so this mechanism works.

`DriverManager` then **finds a driver that recognizes the URL**. It passes the URL to each registered driver’s `connect`. `acceptsURL` is how it can test the list. A driver that understands the subprotocol returns a `Connection`; otherwise `connect` returns **`null`**. JDBC 1.0 `DriverManager` **required the application to load a specific driver**. `DataSource.getConnection` is **preferred** (JDBC 2.0+), but a vendor `DataSource` still **is** a driver implementation — it does not replace having one.

JDBC **4.0** (Java SE 6) added the **service-provider** mechanism. `DriverManager` loads `java.sql.Driver` providers from **`META-INF/services/java.sql.Driver`** and class names in the **`jdbc.drivers`** system property. Official `DriverManager` javadoc: applications **no longer need** `Class.forName()` for those drivers; old `forName` code **keeps working**. Loading still happens — **automatically**, the first time `DriverManager` needs the list.

```d2
direction: down
api: "java.sql API\nDriverManager · Connection" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
load: "load Driver class\n(forName, SPI, or jdbc.drivers)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
reg: "static initializer\nregisterDriver(this)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
db: "Driver.connect(url)\nDBMS wire protocol" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}

api -> load -> reg -> db
```

**Fig. 1.** The JDK types do not talk to PostgreSQL or Oracle. A registered `Driver` does ([[What is JDBC, an implementation or a specification]], [[How do you register a JDBC driver]]).

> [!warning] “Load” is not always `Class.forName`
> A missing driver JAR still fails (`SQLException`, no suitable driver) even on Java 21. A **pre-4.0** driver **without** a service file still needs an explicit load. `Class.forName` does **not** download a driver; it only initializes a class that is **already** visible to the class loader ([[How do you establish a database connection in Java]]).

```java
Class.forName("com.acme.jdbc.AcmeJdbcDriver");
try (Connection con = DriverManager.getConnection(
        "jdbc:acme:db1", "user", "passwd")) {
    // first registered Driver that accepts jdbc:acme:… supplies Connection
}

// JDBC 4.0+ JAR with META-INF/services/java.sql.Driver already on the classpath:
try (Connection con = DriverManager.getConnection(url, user, passwd)) {
    // DriverManager loaded providers; forName omitted
}
```

**Listing 1.** Spec pattern: load so `registerDriver` runs, then `getConnection`. The second block is the same `getConnection` after **automatic** load ([[What is JDBC]]).

> [!tip] Interview answer
> You load a JDBC driver because the JDK only ships the JDBC API — `DriverManager` has no PostgreSQL or Oracle protocol of its own. Loading the `Driver` class registers an instance so `getConnection` can hand the URL to something that `connect`s. Since JDBC 4.0 a compliant driver on the classpath is discovered as a `java.sql.Driver` service, so you often skip `Class.forName`, but you still must ship and load that implementation. `DataSource` is preferred and still uses a driver under the hood.
