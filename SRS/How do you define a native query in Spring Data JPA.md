<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use @Query with nativeQuery = true to run plain SQL instead of JPQL. Dumps use this for database-specific SQL that JPQL cannot express.

```java
public interface UserRepository extends JpaRepository<User, Long> {
    @Query(value = "SELECT * FROM users WHERE email_address = ?1", nativeQuery = true)
    User findByEmailNative(String emailAddress);
}
```

JPQL @Query (no nativeQuery flag) works on entity names and fields:

```java
@Query("SELECT u FROM User u WHERE u.status = :status and u.name = :name")
User findUserByStatusAndName(@Param("status") Integer status, @Param("name") String name);
```
> [!warning] Unverified traps from the dump
> - nativeQuery = true switches from entities to tables and columns.
> - Named parameters and positional ?1 both appear in dump examples.
