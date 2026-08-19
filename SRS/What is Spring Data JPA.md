<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Data JPA is a Spring module that simplifies database operations by providing ready-made repository interfaces for CRUD without writing SQL. It sits on top of JPA and internally uses Hibernate as the default ORM provider.

It provides JpaRepository for CRUD plus pagination and sorting, reduces boilerplate by generating queries automatically, and supports JPQL and custom queries with @Query.

Example:

```java
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByLastName(String lastName);
}
```
> [!warning] Unverified traps from the dump
> - Dumps treat Hibernate as the default JPA provider; the JPA implementation is configurable.
> - Spring Data JPA is not itself a JPA implementation.
