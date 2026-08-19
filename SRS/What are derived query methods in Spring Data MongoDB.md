<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

MongoRepository generates queries from method names, same Spring Data convention as JPA.

```java
public interface BookRepository extends MongoRepository<Book, String> {
    List<Book> findByAuthor(String author);
    List<Book> findByPagesGreaterThan(int pages);
    List<User> findByAgeGreaterThan(int age);
}
```

Dumps say this covers a large share of CRUD and simple filters. When the parser cannot express $or, $elemMatch, or nested paths, step up to @Query JSON or Criteria on MongoTemplate.
> [!warning] Unverified traps from the dump
> - Derived methods are MQL under the hood, not JPQL.
> - Unindexed multi-field derived queries are called out as a production trap in some dumps.
