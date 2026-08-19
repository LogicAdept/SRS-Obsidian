<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Derived query methods are repository methods whose names define the query. Spring parses the method name and generates JPQL or SQL.

No @Query is needed for simple cases. Naming follows conventions such as findBy, countBy, and deleteBy. Example: findByName(String name) fetches rows whose name matches.

Further dump examples:

```java
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByLastName(String lastName);
    List<User> findByAgeGreaterThan(int age);
    Employee findByEmailAddress(String emailAddress);
    List<Employee> findByFirstnameAndLastname(String firstname, String lastname);
    List<Employee> findByStartDateBetween(Date start, Date end);
    List<Employee> findByActiveTrueOrderByLastnameDesc();
}
```

When the name becomes unreadable (many And/GreaterThan clauses), dumps say switch to @Query.
> [!warning] Unverified traps from the dump
> - Property names in the method must match entity fields or the bootstrap fails.
> - Dumps still show findBy as the main prefix; readBy and deleteBy appear as siblings.
