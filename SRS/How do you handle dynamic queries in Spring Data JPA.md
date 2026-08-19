<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list several approaches: @Query, Querydsl, the JPA Criteria API, and Specification.

@Query (static JPQL):

```java
@Query("SELECT u FROM User u WHERE u.name = ?1")
List<User> findByName(String name);
```

Specification wrapping Criteria:

```java
public class UserSpecification implements Specification<User> {
    private String name;
    @Override
    public Predicate toPredicate(Root<User> root, CriteriaQuery<?> query, CriteriaBuilder criteriaBuilder) {
        if (name == null) {
            return criteriaBuilder.isTrue(criteriaBuilder.literal(true));
        }
        return criteriaBuilder.equal(root.get("name"), this.name);
    }
}
```

Querydsl:

```java
public interface UserRepository extends JpaRepository<User, Long>, QuerydslPredicateExecutor<User> {
}
QUser user = QUser.user;
Predicate predicate = user.name.eq("John");
repository.findAll(predicate);
```
> [!warning] Unverified traps from the dump
> - @Query is not dynamic at runtime unless you also branch in code; Specification and Querydsl are the dump's runtime builders.
> - JpaSpecificationExecutor is required before findAll(Specification) works.
