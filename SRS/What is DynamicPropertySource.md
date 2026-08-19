<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@DynamicPropertySource` lets a test **register properties at runtime** (static method + `DynamicPropertyRegistry`). Dumps: useful with **Testcontainers** so `spring.datasource.url` matches the container’s mapped port.

> [!warning] Unverified traps from the dump
> - The method must be static. @TestPropertySource is compile-time / file-based and cannot see a random Docker port.
