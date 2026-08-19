<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: unit (component in isolation), integration (several layers / DB / server), functional / E2E, and **slice** tests (`@WebMvcTest`, `@DataJpaTest`, …) that load one layer.

`@SpringBootTest` is the full-context integration style; Mockito-only tests are unit tests without Boot.

> [!warning] Unverified traps from the dump
> - Calling @SpringBootTest a “unit test” (some dumps do) is a popular lie.
