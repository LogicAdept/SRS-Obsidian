<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Mocking #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps offer two paths:

1. Pure unit: `@ExtendWith(MockitoExtension.class)`, `@Mock` / `@InjectMocks` — **no** Spring context.
2. Spring: `@SpringBootTest` (or a thin `@SpringBootTest(classes=...)`) plus `@MockBean` for repositories.

Prefer (1) unless you need real Spring AOP/validation on the service.

> [!warning] Unverified traps from the dump
> - Using @SpringBootTest for every service test is the slow default dumps warn about.
