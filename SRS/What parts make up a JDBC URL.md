<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# What parts make up a JDBC URL?

> [!abstract] Short answer
> A JDBC URL has **three colon-separated parts**: **`jdbc:<subprotocol>:<subname>`**. **`jdbc`** is always the protocol. **Subprotocol** names the driver or connectivity mechanism (`mysql`, `derby`, historically `odbc`) and may be implemented by **one or more** drivers. **Subname** locates the data source; its syntax is **chosen by the driver writer** and may include a **subsubname**. A common network shape is **`//hostname:port/subsubname`**, but that is a **convention**, not the only legal subname. `DriverManager.getConnection` takes this string; a **`null` URL throws `SQLException`**.

## Three parts

JDBC URLs exist so the **right `Driver` recognizes** the source. Driver writers define the concrete string; JDBC **recommends** the three-part form. `DriverManager` documents the parameter as “a database url of the form `jdbc:subprotocol:subname`.” `Driver.acceptsURL` is typically `true` when the driver understands that **subprotocol** ([[How do you establish a database connection in Java]], [[How do you register a JDBC driver]]).

| Part | Meaning |
| --- | --- |
| **`jdbc`** | Protocol. **Always** `jdbc`. |
| **Subprotocol** | Driver or mechanism name. Example reserved in the JDBC guide: **`odbc`** for ODBC-style data source names (`jdbc:odbc:fred`). A **naming service** can be the subprotocol (`jdbc:dcenaming:accounts-payable`) so the URL holds a **logical** name. |
| **Subname** | Enough information to **locate** the source. May be as short as a local DSN (`fred`) or a driver-defined tree including a **subsubname**. For Internet access, the guide’s convention is **`//hostname:port/subsubname`** (example: `jdbc:dbnet://wombat:356/fred`). |

The **exact** connection-URL syntax is **specified by the DBMS driver**. Tutorial shapes:

- MySQL Connector/J: `jdbc:mysql://[host][,failover…][:port]/[database][?prop=value&…]` — e.g. `jdbc:mysql://localhost:3306/Test` (port default **3306**, host default **127.0.0.1** if omitted).
- Java DB / Derby: `jdbc:derby:[subsubprotocol:][databaseName][;attribute=value]*` — e.g. `jdbc:derby:testdb;create=true` (**no** `//host:port`).

User and password are **normally** passed as `getConnection(url, user, password)` or a `Properties` object with `"user"` / `"password"`. If the same property appears **both** in the URL and in `Properties` / user-password arguments, **which value wins is implementation-defined** — set each property **once**.

```d2
direction: right
p: "jdbc" {
  width: 90
  height: 45
  style.fill: "#e3f2fd"
}
s: "subprotocol\nmysql, derby, …" {
  width: 180
  height: 55
  style.fill: "#fff3e0"
}
n: "subname\ndriver-defined locator" {
  width: 200
  height: 55
  style.fill: "#e8f5e9"
}

p -> s -> n
```

**Fig. 1.** Always three colon-separated fields. Only `jdbc` is fixed; the rest is the driver’s dialect.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public final class JdbcUrlParts {
    public static Connection open(String url, String user, String password)
            throws SQLException {
        return DriverManager.getConnection(url, user, password);
    }
}
```

**Listing 1.** `url` must match `jdbc:subprotocol:subname`. A loaded `Driver` that `acceptsURL` that subprotocol supplies the `Connection`. Prefer a `DataSource` when the URL should stay out of application code ([[What is the layered architecture of JDBC]]).

The `odbc` subprotocol allowed attributes after the DSN: `jdbc:odbc:<data-source-name>[;<attribute-name>=<attribute-value>]*`. That form belonged with the **JDBC-ODBC Bridge**, which **Java SE 8 removed**. Do not treat `jdbc:odbc:…` as something a current JRE can open by itself.

> [!warning] `//host:port/database` is not universal
> Derby embedded URLs have **no** host. ODBC-style subnames were a DSN. MySQL puts properties after `?`. Copying one vendor’s URL into another driver’s `getConnection` fails at `acceptsURL` / `connect`, not at compile time.

> [!warning] Duplicate user/password in URL and arguments
> Precedence is **implementation-defined**. Portable code sets credentials in **one** place.

> [!warning] `null` URL throws; wrong subprotocol does not compile-fail
> `getConnection` throws `SQLException` if `url` is `null`. If no loaded driver accepts the subprotocol, you also get `SQLException` at connect time.

> [!tip] Interview answer
> A JDBC URL is `jdbc:subprotocol:subname`. `jdbc` is fixed; the subprotocol selects the driver; the subname is whatever that driver needs to find the data source. Network URLs often look like `jdbc:mysql://localhost:3306/Test`, but Derby-style `jdbc:derby:testdb;create=true` is equally valid. The driver, not JDBC, defines the subname grammar.

## See also

- [[How do you establish a database connection in Java]]
- [[How do you register a JDBC driver]]
- [[What is the layered architecture of JDBC]]
- [[What is JDBC]]
