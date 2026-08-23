<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Annotations #SRS

# Which Spring Data JPA annotations have you used?

> [!abstract] Short answer
> Day-to-day Spring Data JPA work centers on repository annotations such as **`@EnableJpaRepositories`**, **`@Query`**, **`@Modifying`**, **`@EntityGraph`**, **`@Lock`**, **`@QueryHints`**, and **`@Procedure`**, plus Commons helpers like **`@Param`**. Mapping types still use **Jakarta Persistence** annotations (`@Entity`, `@Id`, …) — those are JPA, not Spring Data.

## Configuration and queries

| Annotation | Role |
| --- | --- |
| **`@EnableJpaRepositories`** | Turns on repository scanning / Java config (Boot often does this via auto-config) |
| **`@Query`** | Bind JPQL or native SQL to a repository method |
| **`@Modifying`** | Mark a `@Query` as DML/DDL (`UPDATE`/`DELETE`/…) so it uses `executeUpdate` |
| **`@Param`** | Name bind parameters (Spring Data Commons) for `@Query` / derived methods |

```java
public interface OrderRepository extends JpaRepository<Order, Long> {

  @Query("select o from Order o where o.status = :status")
  List<Order> findActive(@Param("status") OrderStatus status);

  @Modifying
  @Query("update Order o set o.status = :status where o.id = :id")
  int updateStatus(@Param("id") Long id, @Param("status") OrderStatus status);
}
```

**Listing 1.** `@Query` for reads; `@Modifying` + `@Query` for updates (Spring Data JPA query-methods docs).

## Fetch plan, locking, procedures

| Annotation | Role |
| --- | --- |
| **`@EntityGraph`** | Apply a JPA entity graph (named or ad-hoc `attributePaths`) on a query method |
| **`@Lock`** | Set `LockModeType` for the query |
| **`@QueryHints`** | Pass JPA `QueryHint`s |
| **`@Procedure`** | Map a repository method to a stored procedure |

Official docs note these (and `@Query` / `@Modifying`) can also be used as **meta-annotations** for composed annotations.

```d2
direction: right
enable: "@EnableJpaRepositories" {
  style.fill: "#e3f2fd"
}
repo: "Repository methods" {
  style.fill: "#fff3e0"
}
query: "@Query · @Modifying\n@Param" {
  style.fill: "#e8f5e9"
}
extra: "@EntityGraph · @Lock\n@QueryHints · @Procedure" {
  style.fill: "#f3e5f5"
}

enable -> repo
repo -> query
repo -> extra
```

**Fig. 1.** Enable repositories, then decorate methods for SQL shape, fetch, and locks.

## Related but not “Spring Data JPA”

- **JPA mapping:** `@Entity`, `@Table`, `@Id`, `@OneToMany`, `@NamedEntityGraph`, …
- **Spring transactions:** `@Transactional` on service or modifying repository methods
- **Auditing (Commons + JPA setup):** `@CreatedDate`, `@LastModifiedBy`, `@EnableJpaAuditing`, …

> [!warning] Do not call every JPA annotation “Spring Data”
> Interviewers often check whether you separate **Jakarta Persistence** mapping from **Spring Data** repository annotations. `@Entity` is JPA; `@Query` on the repository is Spring Data JPA.

> [!tip] Interview answer
> I use `@EnableJpaRepositories` (or Boot auto-config), `@Query` / `@Param` for explicit JPQL or native SQL, `@Modifying` for updates/deletes, and `@EntityGraph` or `@Lock` when fetch or locking matters. Entity mapping stays on JPA annotations like `@Entity` and `@Id`.

See [[What is the Modifying annotation in Spring Data JPA]], [[What is JOIN FETCH and EntityGraph in Spring Data JPA]], [[How do you define a native query in Spring Data JPA]], and [[What is Spring Data JPA]].
