<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Mocking #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump claim: `@MockBean` is Spring-specific, `@MockitoBean` is Mockito-specific; both create mocks.

Treat as unverified — naming in Boot 3.4+ moved Spring’s mock-bean support toward `@MockitoBean`.

> [!warning] Unverified traps from the dump
> - This dump likely confuses Mockito’s @Mock with Spring Boot’s @MockitoBean. Verify against current Boot docs in fill-tag.
