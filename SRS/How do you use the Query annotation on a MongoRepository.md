<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When a method name or Criteria is not enough, @Query takes a raw Mongo JSON query string.

```java
@Query("{'_id':'123'}")
@Query("{ 'status': ?0, 'age': { $gte: ?1 } }")
List<User> findActiveUsersOlderThan(String status, int age);
```

This is level 2 in layered dumps: derived methods, then @Query MQL, then Criteria plus MongoTemplate, then Aggregation pipelines.
> [!warning] Unverified traps from the dump
> - Placeholders are ?0-style JSON, not JPQL named parameters, in these examples.
> - @Query here is still a repository method; Aggregation stays on the template.
