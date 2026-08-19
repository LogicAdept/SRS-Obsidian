<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

By default, Spring Data repository methods mapped with @Query are treated as read-only SELECT statements. If you run UPDATE or DELETE with only @Query, dumps say Spring Data throws InvalidDataAccessApiUsageException.

To execute DML, combine @Query with @Modifying. DML must run in a transaction, so @Transactional is often used with @Modifying.

```java
public interface UserRepository extends JpaRepository<User, Long> {
    @Modifying
    @Transactional
    @Query("UPDATE User u SET u.active = false WHERE u.lastLoginDate < :date")
    int deactivateInactiveUsers(@Param("date") LocalDate date);
}
```
> [!warning] Unverified traps from the dump
> - Dumps claim @Query alone is strictly SELECT; @Modifying is required for UPDATE or DELETE.
> - The modifying method typically returns the number of rows affected.
