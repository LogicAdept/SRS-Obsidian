<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

Untrusted draft. Confirm against a Spring Boot testing dump before treating as exam-ready.

> [!NOTE]
> **Answer**
> `@ActiveProfiles` switches which Spring profiles are active for the test context. `@TestPropertySource` adds or overrides property values from a file or inline list for that test. One selects a named environment; the other injects configuration keys.

> [!WARNING]
> **Traps**
> Unverified traps from the dump. You can need both on one class: a `test` profile plus a handful of overridden keys. Neither annotation is a substitute for `@MockBean` or for rebuilding the context after you mutate shared static state.

---
