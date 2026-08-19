<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

Untrusted draft. Confirm against a Spring Boot testing dump before treating as exam-ready.

> [!NOTE]
> **Answer**
> `@TestPropertySource` tells the test which properties file (or inline properties) to use while the test ApplicationContext starts. A dump frames it as a way to override production properties or to use a different property set only for tests.

> [!WARNING]
> **Traps**
> Unverified traps from the dump. That is not the same as `@ActiveProfiles`: profiles select a named environment, `@TestPropertySource` injects a property source. `@DynamicPropertySource` is the later Boot-era hook for values that are only known at runtime, for example a Testcontainers port.

---
