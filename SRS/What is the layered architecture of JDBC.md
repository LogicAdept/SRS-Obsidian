<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# What is the layered architecture of JDBC?

> [!abstract] Short answer
> JDBC is **layered**: a Java **application** talks to the **JDBC API** (`java.sql` + `javax.sql`); a **vendor driver** implements **`java.sql.Driver`** on top of one **data source**. Deployment is **two-tier** (app + driver on the client, data source on the server) or **three-tier** (thin client, middle-tier server with app server + drivers, data source underneath). Drivers themselves are classified **Type 1–4** by how they reach the source. **`DataSource`** is the preferred factory; pooling and XA live in the **middle-tier** APIs.

## API layer, driver layer, data source

The JDBC API is a **standard interface** so one program can reach many sources. Module `java.sql` defines that API. The driver is the **implementation** of `java.sql.Driver` (and of `Connection` / statements / `ResultSet`). `DriverManager` is a **JDK** class that picks a loaded driver for a `jdbc:subprotocol:subname` URL; it is not the database engine ([[What is JDBC, an implementation or a specification]], [[What is JDBC]]).

Two connect mechanisms sit in that API layer ([[How do you establish a database connection in Java]]):

- **`DriverManager`** — original; the app supplies a hard-coded URL.
- **`DataSource`** — preferred; properties name the source so callers do not hard-code driver details. `ConnectionPoolDataSource` and `XADataSource` extend that for **physical-connection reuse** and **distributed transactions**. Applications use `DataSource` / `RowSet` **directly**; pooling and XA types are **middle-tier infrastructure**.

```d2
direction: down
app: "Application\nConnection, Statement, ResultSet" {
  width: 300
  height: 60
  style.fill: "#e3f2fd"
}
api: "JDBC API\njava.sql + javax.sql" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
drv: "Driver layer\njava.sql.Driver (Type 1–4)" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
src: "Data source\nRDBMS or other tabular store" {
  width: 280
  height: 50
}

app -> api -> drv -> src
```

**Fig. 1.** Logical software layers. The JDK ships the API; a vendor JAR supplies the driver.

## Two-tier vs three-tier

These are **logical** layouts; they can map onto many physical machines.

**Two-tier.** Client layer = application **and** JDBC driver(s). The app owns presentation, business logic, multi-statement / distributed transaction management, and **physical** connections. It talks **directly** to the driver. Spec drawbacks: infrastructure mixed into the app, less portable if tuned to one DBMS, and holding physical connections until exit **limits concurrency**.

**Three-tier.** (1) **Client** — presentation only; no driver knowledge. (2) **Middle-tier server** — business logic against **`DataSource` and logical connections**; an application server pools physical connections, manages transactions, and can hide driver differences; JDBC **drivers** still sit here and implement the API (including a relational façade if the source is not an RDBMS). (3) **Data source** — DBMS, files, OO store, warehouse, spreadsheet — anything with a JDBC driver. This split is aimed at performance, scalability, and availability. In a **Java EE** container, components typically do **not** call JDBC transaction/`DataSource` management themselves; the **container** does.

```d2
direction: right
two: "Two-tier\napp + driver | data source" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
three: "Three-tier\nclient | app server + drivers | data source" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

two -> three: "middle tier added"
```

**Fig. 2.** Two-tier talks to the driver in-process with the app. Three-tier puts drivers and pooling behind an application server.

## Driver types (how the driver layer is built)

JDBC 3.0 groups implementations as:

| Type | What it is |
| --- | --- |
| **1** | JDBC API mapped to another API (e.g. ODBC). Needs a **native** library. Spec example: **JDBC-ODBC Bridge**. |
| **2** | Part Java, part **native** client library for that source. Portability limited. |
| **3** | **Pure Java** client to a **middleware** server (DB-independent protocol); middleware talks to the source. |
| **4** | **Pure Java**; implements that source’s **network protocol**; client connects **directly**. |

The Bridge was a Type 1 example in the spec. **Java SE 8 removed the JDBC-ODBC Bridge** from the JDK. Types 1 and 2 still describe native-library drivers from vendors; they are not “included in the JRE.”

```java
import java.sql.Connection;
import java.sql.SQLException;

import javax.sql.DataSource;

public final class JdbcLayers {
    public static Connection logicalConnection(DataSource ds) throws SQLException {
        return ds.getConnection();
    }
}
```

**Listing 1.** Preferred API-layer factory. In three-tier, `ds` is often a pooled or XA `DataSource` from the application server; the object you get is a **logical** `Connection`. Close it so the pool can reuse the physical one ([[What are database connection pools for]]).

> [!warning] Two-tier does not magically pool
> Holding a physical connection for the life of the client is the two-tier default shape. `DriverManager.getConnection` is **not** a pool. Pooling is a **`DataSource` implementation** wired to middle-tier infrastructure.

> [!warning] Type 1 is not “the JDK driver”
> The JDBC-ODBC Bridge shipped with older JDKs and **is gone as of Java SE 8**. A Type 1 or Type 2 driver still needs native code on the machine that loads it. Do not assume a modern JRE can talk ODBC by itself.

> [!warning] Three-tier XA is not `Connection.commit`
> Connections from an XA `DataSource` participate in the **transaction manager**. The application must not call `commit` / `rollback` or `setAutoCommit(true)` on those handles.

> [!tip] Interview answer
> JDBC’s architecture is an application on the JDBC API, a pluggable driver, and a data source. You deploy that as two-tier — app plus driver talking to the database — or three-tier, where an application server owns pooling, transactions, and drivers and the client stays thin. Drivers are Type 1–4 by native vs pure Java and whether they go through middleware; Type 4 is a pure-Java direct protocol. `DataSource` is the preferred API-layer factory.

## See also

- [[What is JDBC, an implementation or a specification]]
- [[How do you establish a database connection in Java]]
- [[What is JDBC]]
- [[What are database connection pools for]]
