<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: on a Spring integration test, `@Transactional` **rolls back** DB changes after each test so data does not leak.

`@DataJpaTest` is transactional by default. This is **not** the same as `@DirtiesContext` (which rebuilds the whole context).

> [!warning] Unverified traps from the dump
> - Rollback hides whether the app actually commits. Some tests use @Commit / @Rollback(false).
> - Http requests from TestRestTemplate run in another thread — the test’s transaction often does not wrap the server thread (classic trap).
