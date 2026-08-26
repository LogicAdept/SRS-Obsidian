<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# What is `JdbcDaoSupport`?

> [!abstract] Short answer
> **`JdbcDaoSupport`** is a **convenience superclass** for JDBC DAOs: set a **`DataSource`**, get a **`JdbcTemplate`** via **`getJdbcTemplate()`**. Spring’s own JDBC chapter calls it **optional** — you may inject **`JdbcTemplate`** (or **`JdbcClient`**) instead. As of Framework **7.0** it is **`@Deprecated(forRemoval = true)`** in favor of **direct injection**.

## Convenience, not the current style

Docs: subclasses inherit **`setDataSource`**. You **choose** whether to extend it. Typical current example: **`@Repository`** with **`DataSource`** in a constructor / init method and **`new JdbcTemplate(dataSource)`** — no superclass.

Javadoc: mainly for `JdbcTemplate`, but also usable with a raw **`Connection`** or **`org.springframework.jdbc.object`** operations. **`NamedParameterJdbcDaoSupport`** is a subclass. **`setJdbcTemplate`** exists if you already have a configured template.

```java
@Repository
public class JdbcMovieFinder implements MovieFinder {

    private JdbcTemplate jdbcTemplate;

    @Autowired
    public void init(DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
    }
}
```

**Listing 1.** Framework *DAO Support* sample — **no** `JdbcDaoSupport`. Bean wiring: [[How do you configure JdbcTemplate as a bean]]. DAO exceptions: [[What is Spring DAO support]].

```d2
direction: right
old: "extends JdbcDaoSupport\ngetJdbcTemplate()" {
  width: 250
  height: 60
  style.fill: "#fff3e0"
}
now: "inject JdbcTemplate\nor JdbcClient" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}

old -> now
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. Fluent: [[What is JdbcClient]].

> [!warning] Deprecated in 7.0
> New code should not extend it. Interview lists that treat `JdbcDaoSupport` / `HibernateDaoSupport` as the **required** DAO shape are outdated.

> [!warning] Not exception translation by itself
> Translation still comes from **`JdbcTemplate`** / **`@Repository`**. Extending this class is not a substitute for [[How does Spring JDBC translate SQLException]].

> [!tip] Interview answer
> **`JdbcDaoSupport` was a base class that built a `JdbcTemplate` from a `DataSource`.** Docs always called it optional. In 7.0 it is deprecated; inject `JdbcTemplate` or `JdbcClient`.

## See also

- [[What is Spring DAO support]]
- [[What is Spring JdbcTemplate]]
- [[How do you configure JdbcTemplate as a bean]]
