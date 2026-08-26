<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Framework/WebFlux #Java/Annotations #SRS

# What is the `WebFluxTest` annotation?

> [!abstract] Short answer
> **`@WebFluxTest`** is Boot’s **WebFlux slice**: it auto-configures WebFlux infrastructure, **limits** component scan to web types (`@Controller`, `@ControllerAdvice`, converters, `WebFluxConfigurer`, …), and **auto-configures `WebTestClient`**. Hit the controller with **`exchange()`** — **no full servlet MockMvc**, **no** full `@SpringBootTest` context unless you choose that instead.

## Slice, not the whole app

Boot *Auto-configured Spring WebFlux Tests* (`spring-boot-webflux-test`): regular `@Component` / `@ConfigurationProperties` are **not** scanned. Mock collaborators with **`@MockitoBean`** (or `@MockBean`). Use **`@Import`** for extra beans.

Boot **does not** auto-detect:

- **`RouterFunction`** routes — `@Import` the `@Bean` or use `@SpringBootTest`
- custom **`SecurityWebFilterChain`** — same

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

**Listing 1.** Conceptual Boot sample. Full stack / SSE / live Netty: `@SpringBootTest` + `@AutoConfigureWebTestClient` or `RANDOM_PORT` — [[How do you test a WebFlux endpoint]]. Client vs production: [[What is the difference between WebClient and WebTestClient]].

Javadoc also lists **`WebFilter`** / **`WebExceptionHandler`** among types the slice may include; **functional routes and Security filter-chain beans still need an import**.

```d2
direction: down
slice: "@WebFluxTest\nWebTestClient mock" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
full: "@SpringBootTest\n+ WebTestClient" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}

slice -> full: "need routers / security / more beans"
```

**Fig. 1.** Not `@WebMvcTest` / MockMvc.

> [!warning] Wrong slice
> `@WebMvcTest` is **MVC**. `@WebFluxTest` is **WebFlux**. Mixing them with the wrong client fails.

> [!warning] Empty `controllers` attribute
> Default can load **all** `@Controller` beans in the slice filters — be explicit in focused tests.

> [!tip] Interview answer
> **`@WebFluxTest(MyController.class)` loads a WebFlux slice and autowires `WebTestClient`.** Mock services. Import `RouterFunction` / `SecurityWebFilterChain` if you need them. End-to-end: `@SpringBootTest`.

## See also

- [[How do you test a WebFlux endpoint]]
- [[What is the difference between WebClient and WebTestClient]]
- [[What is WebClient]]
- [[What are router functions in WebFlux]]
- [[What is SecurityWebFilterChain]]
- [[How do you implement a reactive REST controller in WebFlux]]
