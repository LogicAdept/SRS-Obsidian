<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@DirtiesContext`: the `ApplicationContext` was mutated (singleton state, bean definition). Spring **closes and rebuilds** the context for the next test. Expensive.

`@Transactional` on the test: **roll back the database** after the test. Context stays cached.

Use rollback (or SQL cleanup) for data; dirty the context only when beans themselves were changed.

> [!warning] Unverified traps from the dump
> - Overusing @DirtiesContext destroys TestContext cache and makes suites slow.
