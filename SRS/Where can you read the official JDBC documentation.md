<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# Where can you read the official JDBC documentation?

> [!abstract] Short answer
> Start with the **Java SE API javadoc** for module **`java.sql`**: packages **`java.sql`** (core) and **`javax.sql`** (DataSource, pooling, XA, RowSet). That is the JDBC API that ships in the JDK (Java SE 21 documents it as **JDBC 4.3**). The **specification** is JCP **JSR 221** (JDBC API Specification), with the **reference implementation** and **TCK** on **Java SE**. For narrative how-to, the package pages point at the **Java Tutorials** lesson **JDBC Basics** (trail **JDBC Database Access**) and the book **JDBC API Tutorial and Reference, Third Edition**. **Driver** manuals cover URL subnames and **optional** features the JDK javadoc cannot guarantee.

## Spec, JDK javadoc, tutorial, driver

JDBC is a **specification plus pluggable drivers**, not a blog post ([[What is JDBC, an implementation or a specification]]). Official reading order:

1. **Java SE API Specification (javadoc)** — Module `java.sql` “defines the JDBC API.” Package `java.sql` is the API for accessing tabular data and installing drivers; `javax.sql` is the server-side / `DataSource` API. Both packages are **Related Documentation** on those package pages. Use the javadoc **for the Java SE version you compile against**.
2. **JSR 221 — JDBC API Specification** — the JCP spec (maintenance releases; Java SE’s `java.sql` javadoc currently describes **JDBC 4.3**). Download the spec PDF and the spec javadocs from the JCP JSR 221 pages. The **RI** and **TCK** are those of the corresponding **Java SE** release, not a separate “JDBC installer.”
3. **Java Tutorials → JDBC Database Access → JDBC Basics** — listed under **Related Documentation** on `java.sql`. Connection URLs, `DriverManager` vs `DataSource`, statement processing. The trail is written against **JDK 8** samples; prefer the **current** SE javadoc when they disagree.
4. **JDBC API Tutorial and Reference, Third Edition** — the Java Series book named on both `java.sql` and `javax.sql` package pages (Addison-Wesley). Older get-started chapters in the JDK **technotes JDBC guide** are based on the Second Edition of that book.
5. **Your JDBC driver’s documentation** — package `java.sql` warns that **many features are optional**; “always check your driver’s documentation.” URL **subname** grammar is **driver-defined** ([[What parts make up a JDBC URL]]). Platform notes such as **JDBC-ODBC Bridge removed in Java SE 8** live in the Java SE **JDBC API** / compatibility notes, not in a vendor README.

```d2
direction: down
spec: "JSR 221\nJDBC API Specification" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
se: "Java SE javadoc\njava.sql + javax.sql" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
tut: "Java Tutorials\nJDBC Basics" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
drv: "Vendor driver docs\nURL, optional features" {
  width: 280
  height: 50
}

spec -> se
se -> tut
se -> drv
```

**Fig. 1.** Spec defines the contract; SE javadoc is what you compile against; tutorials teach the loop; the driver fills in what the spec leaves optional.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public final class OfficialJdbcTypes {
    public static Connection open(String url, String user, String password)
            throws SQLException {
        return DriverManager.getConnection(url, user, password);
    }
}
```

**Listing 1.** These types are specified in the **Java SE `java.sql` javadoc**. `DriverManager.getConnection` is documented there; the legal `jdbc:subprotocol:subname` string is documented by **that driver**.

Do **not** treat interview dumps, blogs, or unofficial “JDBC tutorials” as the API. If a behavior is not in the SE javadoc, JSR 221, or the driver guide for the JAR on the classpath, it is not a portable JDBC guarantee.

> [!warning] SE javadoc is not your PostgreSQL (or MySQL) manual
> Optional JDBC features vary by driver. A method in `Connection` can still throw `SQLFeatureNotSupportedException`. After the JDK pages, open **that** driver’s guide for isolation defaults, URL properties, and fetch size.

> [!warning] Tutorial samples are not the spec
> JDBC Basics still demonstrates `DriverManager` because it is simpler; the API’s **preferred** factory is `javax.sql.DataSource`. JDK 8-era samples also predate later JDBC 4.3 methods. When in doubt, believe the **SE javadoc** for your version.

> [!warning] JCP maintenance can move past the JDK you run
> JSR 221 keeps getting maintenance reviews. Java SE 21’s packages are labeled **JDBC 4.3**. Do not assume a newer JCP PDF applies to an older JDK, or that every 4.3 optional method exists in a given driver.

> [!tip] Interview answer
> Official JDBC docs are the Java SE javadoc for `java.sql` and `javax.sql`, plus JSR 221 on the JCP. The package pages also point to the Java Tutorials JDBC Basics lesson and the JDBC API Tutorial and Reference book. For URLs and optional features you still need the vendor driver documentation that matches the JAR you actually load.

## See also

- [[What is JDBC, an implementation or a specification]]
- [[What is JDBC]]
- [[What parts make up a JDBC URL]]
- [[What is the layered architecture of JDBC]]
