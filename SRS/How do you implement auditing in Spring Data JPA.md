<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Auditing tracks who created or changed an entity and when. Spring Data has built-in support.

Steps in the dumps:

1. Add @EnableJpaAuditing to a configuration class.
2. Add @EntityListeners(AuditingEntityListener.class) on the entity.
3. Annotate fields with @CreatedDate, @LastModifiedDate, @CreatedBy, @LastModifiedBy.

```java
@Entity
@EntityListeners(AuditingEntityListener.class)
public class Article {
    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    @CreatedBy
    @Column(updatable = false)
    private String createdBy;

    @LastModifiedBy
    private String modifiedBy;
}
```

For @CreatedBy and @LastModifiedBy you must implement AuditorAware so Spring Data can resolve the current user (often from the security context).
> [!warning] Unverified traps from the dump
> - Date auditing still needs @EnableJpaAuditing plus the entity listener.
> - CreatedBy and LastModifiedBy do nothing useful without an AuditorAware bean.
