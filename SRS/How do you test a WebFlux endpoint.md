<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Spring/Framework/Testing #SRS

# How do you test a WebFlux endpoint?

> [!abstract] Short answer
> Slice: **`@WebFluxTest(MyController.class)`** autowires **`WebTestClient`** (no full HTTP server). Full context: **`@SpringBootTest` + `@AutoConfigureWebTestClient`**. Real Netty: **`webEnvironment = RANDOM_PORT`**. Drive **`get().uri(…).exchange().expectStatus()…`**. MockMvc is the **MVC** tool, not this stack.

## Slice vs running server

Spring Boot *Auto-configured Spring WebFlux Tests*: `@WebFluxTest` (module `spring-boot-webflux-test`) auto-configures WebFlux and **limits** scanning to `@Controller`, `@ControllerAdvice`, Jackson/JSON components, converters, `WebFluxConfigurer`. Regular `@Component` beans are **not** picked up — mock collaborators (`@MockitoBean` / `@MockBean`). It **also auto-configures `WebTestClient`** so you can hit controllers **without starting a server**.

```java
@WebFluxTest(UserVehicleController.class)
class MyControllerTests {

    @Autowired
    private WebTestClient webClient;

    @MockitoBean
    private UserVehicleService userVehicleService;

    @Test
    void testExample() {
        given(this.userVehicleService.getVehicleDetails("sboot"))
                .willReturn(new VehicleDetails("Honda", "Civic"));
        this.webClient.get().uri("/sboot/vehicle")
                .accept(MediaType.TEXT_PLAIN)
                .exchange()
                .expectStatus().isOk()
                .expectBody(String.class).isEqualTo("Honda Civic");
    }
}
```

**Listing 1.** Conceptual `@WebFluxTest` from Spring Boot testing docs. Annotation: [[What is the WebFluxTest annotation]]. Client vs `WebClient`: [[What is the difference between WebClient and WebTestClient]].

Non-slice: `@SpringBootTest` + `@AutoConfigureWebTestClient` (mock WebFlux environment). **`RANDOM_PORT`** starts the embedded reactive server; use a bound `WebTestClient` / HTTP client against that port.

Streaming (SSE): `accept(TEXT_EVENT_STREAM)`, `returnResult(…)`, then **`StepVerifier`** + **`thenCancel()`** — [[How do you implement Server-Sent Events in WebFlux]].

Reactor *Testing*: unit-test a `Mono`/`Flux` with `StepVerifier.create(…).expectNext(…).verify()`. **`verify()` (or `verifyComplete()` / `verifyError()`) is required** — without it the script never subscribes.

```d2
direction: down
slice: "@WebFluxTest\nWebTestClient mock" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
boot: "@SpringBootTest +\n@AutoConfigureWebTestClient" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
live: "RANDOM_PORT\nreal Netty" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

slice -> boot -> live: "more of the stack"
```

**Fig. 1.** Mock `WebTestClient` is WebFlux-only; MVC slices use MockMvc.

> [!warning] `@WebFluxTest` misses `RouterFunction` and `SecurityWebFilterChain`
> Boot: import those beans (`@Import`) or use `@SpringBootTest`. Functional routes are not auto-detected.

> [!warning] Always trigger `StepVerifier`
> Reactor: call **`verify()`**. A chain of `expectNext` without it does not run the sequence.

> [!warning] Not MockMvc
> MockMvc talks to the servlet `DispatcherServlet`. WebFlux tests use **`WebTestClient`**.

> [!tip] Interview answer
> **`@WebFluxTest` + autowired `WebTestClient`: `exchange()` then `expectStatus` / `expectBody`.** Mock services. Full app: `@SpringBootTest` and `@AutoConfigureWebTestClient`, or `RANDOM_PORT` for a real server. SSE: `StepVerifier` and cancel. MockMvc is the wrong client.
