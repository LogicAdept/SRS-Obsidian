<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# Is `JdbcTemplate` thread-safe?

> [!abstract] Short answer
> **Yes — once configured.** Spring: you can **share one instance** across many DAOs. It is **stateful** only in holding a **`DataSource`** (and translators, fetch size, …), **not** conversational per-call state. Configure it as a **singleton bean** (or `new JdbcTemplate(dataSource)` in a singleton DAO). That does **not** make a non-pooled `DataSource` or a **stateful `RowMapper` field** safe.

## Shared template, not shared conversation

Spring *JdbcTemplate Best Practices*: thread-safe after configuration → inject the **same** reference into multiple repositories. Javadoc: same NOTE.

```java
public class JdbcCorporateEventDao implements CorporateEventDao {

    private final JdbcTemplate jdbcTemplate;

    public JdbcCorporateEventDao(DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
    }
}
```

**Listing 1.** Conceptual Framework constructor style — one template per DAO, typically one `DataSource` for the app. Central API: [[What is Spring JdbcTemplate]].

Do **not** `new JdbcTemplate(ds)` on every request. Docs: seldom necessary to create a new instance each time you run SQL. Several databases → **several `DataSource`s and templates**.

```d2
direction: down
dao1: "OrderDao" {
  width: 140
  height: 45
  style.fill: "#e3f2fd"
}
dao2: "ActorDao" {
  width: 140
  height: 45
  style.fill: "#e3f2fd"
}
jt: "one JdbcTemplate\n(singleton)" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
ds: "DataSource" {
  width: 180
  height: 45
  style.fill: "#e8f5e9"
}

dao1 -> jt
dao2 -> jt
jt -> ds
```

**Fig. 1.** Concurrent calls borrow **connections** from the pool; they do not mutate the template’s configuration. Pool: [[What is connection pooling in Spring JDBC]]. Bean setup: [[How do you configure JdbcTemplate as a bean]].

`NamedParameterJdbcTemplate` is documented the same way (wraps / shares a `JdbcTemplate`). **`JdbcClient`** is a facade over those templates — share the **configured** delegate, not a per-thread client you rebuild from scratch unless you have a reason.

> [!warning] Thread-safe template ≠ thread-safe everything
> A `RowMapper` that writes **instance fields**, a mutable SQL `StringBuilder` shared across calls, or a `DataSource` that is not safe for concurrent `getConnection` can still break. Keep mappers **stateless**.

> [!warning] Do not reconfigure after publish
> Changing `setDataSource` / `setExceptionTranslator` on a live singleton while requests run is not the “once configured” contract.

> [!tip] Interview answer
> **`JdbcTemplate` is thread-safe once configured — one Spring singleton is the usual design.** It keeps a `DataSource`, not a current `ResultSet`. Share it; do not allocate per query. Safety of connections is the pool’s job.

## See also

- [[What is Spring JdbcTemplate]]
- [[What is Spring JDBC]]
- [[What is NamedParameterJdbcTemplate]]
- [[How do you configure JdbcTemplate as a bean]]
- [[How do you configure a DataSource in Spring]]
- [[What is HikariCP in Spring Boot]]
