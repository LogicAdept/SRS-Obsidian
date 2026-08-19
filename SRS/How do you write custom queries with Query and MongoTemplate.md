<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

@Query on a repository method takes a MongoDB-style JSON query with positional placeholders when derived names are not enough.

MongoTemplate gives Query and Criteria builders for dynamic queries, updates, and aggregations.

```java
@Query("{ 'status': ?0, 'age': { $gte: ?1 } }")
List<User> findActiveUsersOlderThan(String status, int age);

Query query = new Query(Criteria.where("status").is("active").and("age").gte(18));
List<User> users = mongoTemplate.find(query, User.class);
```
> [!warning] Unverified traps from the dump
> - Mongo @Query uses MQL JSON, not JPQL.
> - Criteria is the dump's tool when filters are optional at runtime.
