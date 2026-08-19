<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

Untrusted draft. Confirm against a Spring Boot testing dump before treating as exam-ready.

> [!NOTE]
> **Answer**
> `@JdbcTest` is a Spring Boot slice for JDBC-based repositories. A testing overview says it loads only the JDBC-related parts of the application context. If the code under test uses Spring Data JDBC, that same overview says to use `@DataJdbcTest` instead of `@JdbcTest`.

> [!WARNING]
> **Traps**
> Unverified traps from the dump. It is not `@DataJpaTest`: JPA slices bring EntityManager and Spring Data JPA. It also does not start the full web stack. Pick `@JdbcTest` versus `@DataJdbcTest` from the data access style, not from habit.

---
