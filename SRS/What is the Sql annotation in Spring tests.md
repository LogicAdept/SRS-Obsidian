<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Sql` runs SQL scripts before/after a test class or method (`executionPhase`). Used to seed or clean the test database in integration tests.

> [!warning] Unverified traps from the dump
> - Scripts run against the DataSource in the test context, not against production.
