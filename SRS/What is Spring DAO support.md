<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# What is Spring DAO support?

> [!abstract] Short answer
> Spring **DAO support** is the **shared data-access programming model**: **`DataAccessException`** as an **unchecked** root, **translation** from JDBC / JPA / Hibernate failures, and **`@Repository`** so DAOs stay free of vendor catch blocks. The point is **consistent exceptions and wiring**, not a magic switch from JDBC to Hibernate with one annotation.

## Same hierarchy, different resources

Docs: work with JDBC, Hibernate, or JPA **the same way**; **switch technologies more easily**; **do not catch technology-specific exceptions** in business code. JDBC **`SQLException`** and ORM exceptions wrap into **`org.springframework.dao`**. You can still **mix JDBC** next to ORM under that model.

**`@Repository`** is the documented way to get **exception translation** plus component scanning. Inject the resource the technology needs: **`DataSource`** / **`JdbcTemplate`** for JDBC, **`EntityManager`** for JPA, **`SessionFactory`** for classic Hibernate.

Support superclasses (`JdbcDaoSupport`, old `HibernateDaoSupport`, …) were **optional conveniences**. JDBC docs show **constructor / init `JdbcTemplate`**. **`JdbcDaoSupport` is deprecated for removal in 7.0**.

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

**Listing 1.** Framework JDBC DAO — `@Repository` + `DataSource`, not a support superclass. Hierarchy: [[What is the DataAccessException hierarchy]]. Translation: [[How does Spring JDBC translate SQLException]]. Superclass: [[What is JdbcDaoSupport]].

```d2
direction: down
tech: "JDBC / JPA / Hibernate" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
tr: "@Repository + translator" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
ex: "DataAccessException" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

tech -> tr -> ex
```

**Fig. 1.** Template: [[What is Spring JdbcTemplate]]. vs JPA repositories: [[What is the difference between Spring JDBC and Spring Data JPA]].

> [!warning] Switching is not one annotation
> You still rewrite mapping and queries. DAO support shares **exceptions and DI**, not SQL ↔ entities.

> [!warning] Interceptor-style ORM without translation
> If you use interceptor-based Hibernate/JPA access, **you** must convert **`HibernateException` / `PersistenceException`** (e.g. `SessionFactoryUtils.convertHibernateAccessException`) unless `@Repository` advice is in play.

> [!tip] Interview answer
> **Spring DAO support is a common unchecked `DataAccessException` tree plus `@Repository` translation.** JDBC and ORM can share that model. It does not replace writing SQL or mapping entities.

## See also

- [[What is the DataAccessException hierarchy]]
- [[What is JdbcDaoSupport]]
- [[How does Spring JDBC translate SQLException]]
