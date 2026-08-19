<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Integration #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `TestEntityManager` in `@DataJpaTest`; or `@Sql` scripts around each method:

```java
@Sql(scripts = "classpath:db/setup_data.sql", executionPhase = BEFORE_TEST_METHOD)
@Sql(scripts = "classpath:db/cleanup_data.sql", executionPhase = AFTER_TEST_METHOD)
```

Plus `@Transactional` rollback so tests stay isolated.

> [!warning] Unverified traps from the dump
> - @Sql AFTER_TEST_METHOD may not run the same way if the test transaction rolls back first — order is a fill-tag check.
