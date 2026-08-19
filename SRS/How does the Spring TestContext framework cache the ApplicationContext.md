<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #SRS #New

Untrusted draft. Confirm against a Spring Boot testing dump before treating as exam-ready.

> [!NOTE]
> **Answer**
> The TestContext framework can reuse one ApplicationContext across test classes that share the same configuration, so the suite does not rebuild the context for every class. A dump presents that cache as the reason Spring tests stay fast when many classes use the same setup.

> [!WARNING]
> **Traps**
> Unverified traps from the dump. `@DirtiesContext` tells Spring the cached context is dirty and a new one must be created for the next test; a testing overview warns to use that sparingly because building a context is expensive. Changing profiles, `@TestPropertySource`, or mock beans can also mean a different cache entry rather than the context you thought you were sharing.

---
