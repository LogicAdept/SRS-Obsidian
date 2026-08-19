<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Testing/JUnit #Java/Annotations #SRS #New

Untrusted draft. Confirm against a Spring Boot testing dump before treating as exam-ready.

> [!NOTE]
> **Answer**
> `SpringExtension` is the JUnit 5 TestContext bridge. Interview dumps that still show `@RunWith(SpringRunner.class)` say JUnit 5 tests use `SpringExtension` instead of `SpringRunner`. `@SpringBootTest` already registers that extension, so you usually do not add `@ExtendWith(SpringExtension.class)` by hand on a Boot test.

> [!WARNING]
> **Traps**
> Unverified traps from the dump. `SpringRunner` is a JUnit 4 alias. Mixing `@RunWith(SpringRunner.class)` on a JUnit 5 test is the wrong runner. Plain Mockito tests that never load a Spring context do not need `SpringExtension`.

---
