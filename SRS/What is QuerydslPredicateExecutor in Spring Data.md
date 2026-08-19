<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

QuerydslPredicateExecutor is a Spring Data fragment that lets a repository accept Querydsl Predicate objects for type-safe dynamic queries.

```java
public interface UserRepository extends JpaRepository<User, Long>, QuerydslPredicateExecutor<User> {
}

QUser user = QUser.user;
Predicate predicate = user.name.eq("John");
repository.findAll(predicate);
```

Dumps list it next to @Query and Specification as a way to build dynamic filters.
> [!warning] Unverified traps from the dump
> - You need the generated Q-types (QUser) on the classpath.
> - This is an extra interface mix-in, not something CrudRepository gives you by default.
