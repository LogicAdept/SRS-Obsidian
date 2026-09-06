<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# What are the advantages of programming directly with JDBC?

> [!abstract] Short answer
> **Direct JDBC** means you call **`java.sql` / `javax.sql`**: you **write the SQL**, create **`Statement` / `PreparedStatement` / `CallableStatement`**, walk the **`ResultSet`**, and **`close()`** the chain. Advantages versus an ORM: **exact SQL**, **no entity model**, **no persistence-context flush/dirty-check**, and full use of JDBC knobs (**result-set type**, fetch size, batch, multiple results, procedure OUT). Hibernate’s own guide says **use ORM and SQL together** — when ORM makes a piece of access harder, use JDBC (including `Session.doWork` on the **same** `Connection`). Versus a template, you keep every JDBC object in your hands; you also take on open/close, loops, and `SQLException`.

## What “directly” buys you

JDBC is already the **standard** API for sending SQL ([[How would you explain in how consist advantages using JDBC]]). Programming **directly** is not “using a driver”; it is **not** going through Hibernate’s `Session.persist` or (in Spring) letting a template own the workflow.

**Against a mapped domain model.** Hibernate sits **on** JDBC (`Session` wraps a `Connection`). It maps classes, dirty-checks, and flushes SQL it generates. Direct JDBC skips that when the unit of work **is the SQL**: reporting, vendor syntax, ETL, DDL, or a procedure you already have. Hibernate: if ORM is making a tricky access worse, “use something better suited” — native SQL or JDBC on the session’s connection ([[What advantages does Hibernate provide over plain JDBC]], [[When would you use JDBC instead of Hibernate in Spring]]). You still **bind** `?`; you do not concatenate ([[How does PreparedStatement mitigate SQL injection compared to Statement]]).

**JDBC-level control.** You choose `executeQuery` vs `executeUpdate` vs `execute` + `getMoreResults`, ResultSet **type/concurrency/holdability**, **fetch size**, **batch** parameter sets, generated keys, `DatabaseMetaData`. Those are `Connection` / `Statement` / `ResultSet` methods, not entity annotations ([[How would you explain ResultSet types scrolling and concurrency modes]], [[How do you organize batch inserts for many rows]]).

**No persistence unit required.** A `DataSource`/`DriverManager` + try-with-resources is enough ([[What are the main JDBC steps to work with a database]]).

Spring’s JDBC chapter shows the cost of going fully direct: **you** would also open/close, iterate, translate exceptions, and demarcate transactions. `JdbcTemplate` / `JdbcClient` still let **you specify the SQL** while Spring owns the tedious parts. “Direct” is the **full** API, not a claim that boilerplate is a feature.

```d2
direction: right
orm: "ORM\nentities, flush" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
tpl: "JdbcTemplate\nyou: SQL + row work" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
raw: "Direct JDBC\nyou: SQL + objects + close" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

orm -> tpl -> raw: "more JDBC visible"
```

**Fig. 1.** Direct JDBC is maximum visibility of `java.sql`. That is the advantage and the work.

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.sql.DataSource;

public final class DirectSelect {
    public static String name(DataSource ds, int id) throws SQLException {
        try (Connection con = ds.getConnection();
             PreparedStatement ps = con.prepareStatement(
                     "SELECT name FROM person WHERE id = ?")) {
            ps.setFetchSize(50);
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? rs.getString(1) : null;
            }
        }
    }
}
```

**Listing 1.** You own SQL, fetch size, binds, and close. An ORM would expect an entity; a template would still take this SQL but hide `Connection`/`close`.

> [!warning] Direct JDBC is not “faster by default”
> You can write worse SQL and leak connections. Hibernate’s point is **performance needs the relational model**, not that `ResultSet` loops always win. Close the chain; bind parameters.

> [!warning] “Direct” does not mean concatenate SQL
> `Statement` + string assembly is injection. Direct and **prepared** are compatible. ORM native queries have the same rule.

> [!tip] Interview answer
> Direct JDBC means you write SQL and drive `Connection`, statements, and `ResultSet` yourself. You get exact SQL and JDBC features without an entity model or flush cycle. Use it for reports, procedures, and anything ORM makes harder — Hibernate says to mix SQL with ORM. You also own resource closing and mapping, which is why templates exist.

## See also

- [[What advantages does Hibernate provide over plain JDBC]]
- [[When would you use JDBC instead of Hibernate in Spring]]
- [[How would you explain in how consist advantages using JDBC]]
- [[What are the main JDBC steps to work with a database]]
