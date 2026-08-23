<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/Spring/Data/JPA #SRS

# What is the difference between Spring JDBC and Spring Data JPA?

> [!abstract] Short answer
> **Spring JDBC** (Framework: **`JdbcTemplate`** and friends) is **SQL you write** in repository/DAO **classes**, with **manual row mapping**. **Spring Data JPA** is **repository interfaces** over **JPA entities** — derived/`@Query` methods, ORM lifecycle, little or no hand-written SQL for CRUD. Same relational database; different abstraction level.

## Side-by-side

| | Spring JDBC (`JdbcTemplate`) | Spring Data JPA |
| --- | --- | --- |
| Shape | Concrete `@Repository` / DAO classes | Interfaces (`JpaRepository`, …) |
| SQL | You supply strings; template runs them | Derived methods → JPQL; optional `@Query` / native |
| Mapping | `RowMapper`, `ResultSetExtractor`, … | `@Entity` / `@Table` / `@Id` via JPA provider |
| What Spring owns | Connections, statements, exception translation | Generated repository impl + `EntityManager` use |
| Typical inject | `JdbcTemplate` (or `NamedParameterJdbcTemplate`) | Repository bean; no template required |

Framework docs: with `JdbcTemplate` you provide SQL and extract results; Spring opens/closes resources and translates `SQLException` into `org.springframework.dao`. Spring Data JPA’s goal is to cut repository boilerplate on top of JPA — not to replace JDBC for every SQL-heavy path.

```java
@Repository
class OrderJdbcDao {
  private final JdbcTemplate jdbc;
  OrderJdbcDao(JdbcTemplate jdbc) { this.jdbc = jdbc; }

  Optional<Order> findById(long id) {
    List<Order> rows = jdbc.query(
        "select id, total from orders where id = ?",
        (rs, i) -> new Order(rs.getLong("id"), rs.getBigDecimal("total")),
        id);
    return rows.stream().findFirst();
  }
}

public interface OrderRepository extends JpaRepository<OrderEntity, Long> {
  List<OrderEntity> findByCustomerId(Long customerId);
}
```

**Listing 1.** JDBC: class + SQL + `RowMapper`. JPA: interface + entity mapping / derived query (conceptual contrast).

```d2
direction: right
app: "Application" {
  style.fill: "#e3f2fd"
}
jdbc: "JdbcTemplate DAO\nSQL + RowMapper" {
  style.fill: "#fff3e0"
}
jpa: "JpaRepository\n@Entity + EntityManager" {
  style.fill: "#e8f5e9"
}
db: "Relational DB" {
  style.fill: "#f3e5f5"
}

app -> jdbc -> db
app -> jpa -> db
```

**Fig. 1.** Two Spring stacks to the same kind of database: explicit SQL vs JPA ORM repositories.

## What this comparison is not

- Not “JDBC the API vs Hibernate.” Spring JDBC still uses JDBC under `JdbcTemplate`; Spring Data JPA uses a JPA provider (often Hibernate in Boot).
- Not **Spring Data JDBC** (a separate Spring Data module with interface repositories over SQL). Here “Spring JDBC” means the **Framework data-access JDBC** support.

Both styles can return domain objects without the caller touching a raw `ResultSet` — JDBC via mappers; JPA via entity mapping. Prefer JDBC when you want full SQL control or thin tables; prefer Spring Data JPA when CRUD/derived queries and a managed entity model fit.

> [!warning] Mixing models without care
> Sharing the same tables through both `JdbcTemplate` and JPA entities can fight over caching, dirty checking, and schema assumptions. Pick a primary stack per aggregate, or isolate JDBC to reporting/bulk paths.

> [!tip] Interview answer
> Spring JDBC is `JdbcTemplate` DAOs: you write SQL and map rows. Spring Data JPA is repository interfaces over `@Entity` types with derived or `@Query` methods. Same database family; JDBC is explicit SQL, Data JPA is ORM repositories. Do not confuse this with Spring Data JDBC.

See [[What is Spring JdbcTemplate]], [[What is Spring Data JPA]], [[What is a RowMapper in Spring JDBC]], and [[What are the pros and cons of EntityManager versus Spring Data JPA repositories]].
