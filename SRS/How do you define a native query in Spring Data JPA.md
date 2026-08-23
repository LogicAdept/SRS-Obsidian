<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Annotations #SRS

# How do you define a native query in Spring Data JPA?

> [!abstract] Short answer
> Put SQL in `@Query(value = "…", nativeQuery = true)` on a repository method, or use the composed `@NativeQuery` shortcut. Parameters bind with `?1` / `?2` or `@Param` names. JPQL queries (default) use entity and attribute names instead of table and column names.

## Native SQL on a repository method

Spring Data JPA runs the string literally against the database when `nativeQuery = true`. Use this for vendor-specific SQL, functions, or joins that JPQL cannot express cleanly.

```java
public interface UserRepository extends JpaRepository<User, Long> {

  @Query(value = "SELECT * FROM users WHERE email_address = ?1", nativeQuery = true)
  User findByEmailNative(String emailAddress);

  @NativeQuery("SELECT * FROM users WHERE status = :status AND name = :name")
  User findByStatusAndName(@Param("status") Integer status, @Param("name") String name);
}
```

**Listing 1.** `@Query(nativeQuery = true)` or `@NativeQuery` (alias for the same flag) on a finder method.

Compare with JPQL — no `nativeQuery` flag, entity names and fields:

```java
@Query("SELECT u FROM User u WHERE u.status = :status AND u.name = :name")
User findUserByStatusAndName(@Param("status") Integer status, @Param("name") String name);
```

**Listing 2.** JPQL targets the persistence model; native SQL targets tables/columns.

```d2
direction: right
repo: "Repository @Query method" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
flag: "nativeQuery = true\nor @NativeQuery" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
sql: "Vendor SQL\nSELECT … FROM table" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
map: "JPA maps rows → entity\nor Tuple / Map" {
  width: 240
  height: 70
  style.fill: "#f3e5f5"
}

repo -> flag -> sql -> map
```

**Fig. 1.** Native queries skip JPQL parsing and hit the database schema directly.

## Parameters, pagination, and pitfalls

Positional placeholders use **1-based** indices (`?1`, `?2`). Named parameters use `:name` with `@Param`. With `-parameters` on the compiler, `@Param` can be omitted for named parameters on some Spring Data versions.

For paginated native queries, declare an explicit **`countQuery`** (or a named native count query with a `.count` suffix) — Spring Data cannot reliably rewrite arbitrary native SQL for `COUNT` on its own. Complex native SQL may need JSqlParser on the classpath or a hand-written count. Return types can be entities (when columns align), `Tuple`, or `Map` for raw projections; `@NativeQuery` also supports `sqlResultSetMapping` for `@SqlResultSetMapping`.

> [!warning] You lose database portability
> Native SQL ties the repository to table/column names and dialect features. Renaming an `@Column` does not update the SQL string. Pagination without `countQuery` may fail or be unreliable on non-trivial statements.

See [[What is Spring Data JPA]], [[What are derived query methods in Spring Data JPA]], and [[How do you handle dynamic queries in Spring Data JPA]].

> [!tip] Interview answer
> I define native queries with `@Query(value = "SELECT …", nativeQuery = true)` or `@NativeQuery` on the repository method. That runs plain SQL instead of JPQL, so I use real table and column names and accept vendor lock-in. For pages I add an explicit `countQuery`, and I bind parameters with `?1` or `@Param`.
