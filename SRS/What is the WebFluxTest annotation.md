<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Framework/WebFlux #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@WebFluxTest(MyController.class)` loads a WebFlux slice and injects `WebTestClient` to `exchange()` the controller without claiming a full servlet MockMvc setup.

`WebTestClient` also on `@SpringBootTest(RANDOM_PORT)` for end-to-end reactive HTTP, including SSE.

> [!warning] Unverified traps from the dump
> - Not `@WebMvcTest`. Not `MockMvc`.

