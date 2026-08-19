<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

Untrusted draft. Confirm against a Spring Boot testing dump before treating as exam-ready.

> [!NOTE]
> **Answer**
> `@ActiveProfiles` names which Spring profile or profiles should be active while that test class runs, so the test context loads the beans and property sources that belong to those profiles.

> [!WARNING]
> **Traps**
> Unverified traps from the dump. `@TestPropertySource` is a different knob: it points at a properties file or inlined properties for the test, it does not switch the active profile by itself. A dump lists `@ActiveProfiles` as the annotation that specifies which profile should be active during testing.

---
