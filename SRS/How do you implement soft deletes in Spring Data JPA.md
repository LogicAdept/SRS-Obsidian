<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Soft delete keeps the row and marks it deleted.

1. Add a boolean field on the entity, default false.

```java
@Entity
public class MyEntity {
    @Id
    private Long id;
    private Boolean deleted = false;
}
```

2. Filter reads so deleted rows are hidden.

```java
public interface MyEntityRepository extends JpaRepository<MyEntity, Long> {
    @Query("SELECT e FROM MyEntity e WHERE e.deleted = false")
    List<MyEntity> findAllNotDeleted();
}
```

3. Delete by setting the flag and saving, inside a transaction.

```java
@Transactional
public void softDelete(Long id) {
    MyEntity entity = repository.findById(id).orElseThrow(() -> new EntityNotFoundException());
    entity.setDeleted(true);
    repository.save(entity);
}
```
> [!warning] Unverified traps from the dump
> - Plain findAll and deleteById from JpaRepository still see or remove the physical row unless you override them.
> - The dump's finder is a custom method, not an automatic global filter.
