<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS

# How do you implement soft deletes in Spring Data JPA?

> [!abstract] Short answer
> Spring Data JPA has no built-in soft delete. Keep a **deleted flag** (or timestamp) on the entity, hide deleted rows from reads, and turn deletes into **updates** — either explicitly in service code or via Hibernate `@SQLDelete` / `@SQLRestriction` (or Hibernate 6.5+ `@SoftDelete`) so `repository.delete` does not issue `DELETE`.

## Flag column and filtered reads

Add a marker field and exclude deleted rows from queries. Plain `findAll()` and `findById()` still return deleted rows unless you add a global filter.

```java
@Entity
public class Article {

  @Id
  private Long id;

  private boolean deleted = false;
}

public interface ArticleRepository extends JpaRepository<Article, Long> {

  @Query("SELECT a FROM Article a WHERE a.deleted = false")
  List<Article> findAllActive();
}
```

**Listing 1.** Manual soft delete: custom finder excludes `deleted = true` (application-level pattern; not automatic on every query).

```java
@Transactional
public void softDelete(Long id) {
  Article article = repository.findById(id)
      .orElseThrow(() -> new EntityNotFoundException(id.toString()));
  article.setDeleted(true);
  repository.save(article);
}
```

**Listing 2.** Logical delete as update + `save`, not `deleteById`.

## Make repository deletes logical (Hibernate)

To intercept `repository.delete(entity)` / derived deletes, map Hibernate’s delete statement to an `UPDATE` and add a read restriction so generated SQL skips deleted rows.

```java
@Entity
@SQLDelete(sql = "UPDATE article SET deleted = true WHERE id = ?")
@SQLRestriction("deleted = false")
public class Article {

  @Id
  private Long id;

  private boolean deleted = false;
}
```

**Listing 3.** `@SQLDelete` replaces physical `DELETE`; `@SQLRestriction` filters selects (Hibernate ORM; Hibernate 6 replaces deprecated `@Where`).

Hibernate **6.5+** offers `@SoftDelete` on the entity for the same idea with less boilerplate. Spring Data derived **`deleteBy…`** methods may load matching entities and call `delete` one-by-one so JPA lifecycle callbacks run — different from a bulk `@Modifying` JPQL delete.

```d2
direction: right
call: "deleteById / delete(entity)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
hib: "@SQLDelete → UPDATE\n@SQLRestriction on SELECT" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
row: "Row stays in DB\ndeleted = true" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

call -> hib -> row
```

**Fig. 1.** Repository delete API unchanged; persistence provider emits an update instead of `DELETE`.

> [!warning] Nothing is automatic by default
> A bare `deleted` field plus `JpaRepository` does not filter reads or soft-delete on `deleteById`. Native SQL, `@Query` without the predicate, and second-level cache can still expose or resurrect deleted rows unless every path respects the flag.

See [[What is Spring Data JPA]], [[What is the Modifying annotation in Spring Data JPA]], and [[What is the difference between save and saveAndFlush in Spring Data JPA]].

> [!tip] Interview answer
> Spring Data JPA does not soft-delete for you. I add a deleted flag, filter queries or use Hibernate `@SQLRestriction`, and either update the flag in a service method or map deletes with `@SQLDelete` so `repository.delete` runs an UPDATE. Without that mapping, `deleteById` still removes the physical row.
