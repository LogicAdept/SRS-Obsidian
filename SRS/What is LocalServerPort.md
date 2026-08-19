<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@LocalServerPort` injects the actual port when `@SpringBootTest(webEnvironment = RANDOM_PORT)` (or DEFINED_PORT) started an embedded server.

Used to build URLs for `TestRestTemplate` / `WebTestClient` in integration tests.

> [!warning] Unverified traps from the dump
> - It is 0 / unused if webEnvironment is MOCK (no real server).
