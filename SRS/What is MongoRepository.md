<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Data MongoDB is Spring's abstraction over the MongoDB Java driver: object-document mapping, template operations, and repository interfaces.

MongoRepository<T, ID> extends CrudRepository and PagingAndSortingRepository. You get save, find, delete, and pagination for free, plus derived query methods from method names.

```java
public interface UserRepository extends MongoRepository<User, String> {
    List<User> findByStatusAndAgeGreaterThan(String status, int age);
    Optional<User> findByEmail(String email);
}
```

Other dumps also say it extends QueryByExampleExecutor.
> [!warning] Unverified traps from the dump
> - The id type in dump examples is often String, mapped to MongoDB _id.
> - Derived finders are generated from method names the same way as in other Spring Data modules.
