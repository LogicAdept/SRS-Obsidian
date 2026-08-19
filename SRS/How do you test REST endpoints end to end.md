<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Integration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `@SpringBootTest(webEnvironment = RANDOM_PORT)` plus `TestRestTemplate` or `WebTestClient`.

That starts the app and talks HTTP. For controller-only speed, dumps send you to `@WebMvcTest` + MockMvc instead.

> [!warning] Unverified traps from the dump
> - End-to-end still often mocks third-party HTTP (WireMock / MockRestServiceServer) so the test does not hit the real vendor.
