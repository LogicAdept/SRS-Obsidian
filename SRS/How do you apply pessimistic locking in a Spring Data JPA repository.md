<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Pessimistic locking assumes conflicts are frequent. It locks the database row with SQL such as SELECT ... FOR UPDATE so other transactions cannot access the row until the lock is released.

Implementation in the dump: put @Lock on the repository method.

```java
public interface BankAccountRepository extends JpaRepository<BankAccount, Long> {
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT b FROM BankAccount b WHERE b.id = :id")
    Optional<BankAccount> findByIdForUpdate(@Param("id") Long id);
}
```

Optimistic locking in the same dump uses a @Version field and throws OptimisticLockException if versions do not match.
> [!warning] Unverified traps from the dump
> - Dumps contrast this with @Version optimistic locking, which does not lock the row up front.
> - @Lock is shown on a query method, not as a global entity default.
