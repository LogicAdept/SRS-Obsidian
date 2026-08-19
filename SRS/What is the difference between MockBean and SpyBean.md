<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #Testing/Mocking #SRS #New

Untrusted draft. Confirm against a Spring Boot testing dump before treating as exam-ready.

> [!NOTE]
> **Answer**
> `@MockBean` replaces a bean in the test ApplicationContext with a Mockito mock. `@SpyBean` wraps the existing bean as a Mockito spy so real methods still run unless you stub them. A testing overview says the mock or spy is then available to other beans that depend on that type.

> [!WARNING]
> **Traps**
> Unverified traps from the dump. Spring Boot 3.4 deprecates both: `@MockitoBean` replaces `@MockBean`, `@MockitoSpyBean` replaces `@SpyBean`. A spy still hits the real collaborator for unstubbed calls, so it is not a full isolation mock. Either annotation typically forces a new context relative to tests that do not declare the same mock beans.

---
