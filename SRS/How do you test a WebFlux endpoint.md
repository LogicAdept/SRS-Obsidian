<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Spring/Framework/Testing #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@WebFluxTest(MyController.class)` and `@Autowired WebTestClient`, then `client.get().uri("/greet").exchange().expectStatus().isOk()...`.

`WebTestClient` on `@SpringBootTest(RANDOM_PORT)` for HTTP; SSE via `accept(TEXT_EVENT_STREAM)` plus `StepVerifier` on the response body. They also use `StepVerifier` for unit-testing publishers (`reactor-test`). Always call `.verify()`.

> [!warning] Unverified traps from the dump
> - `@WebFluxTest` is the slice; `WebTestClient` is the client. `MockMvc` is the MVC dump tool, not this stack.

