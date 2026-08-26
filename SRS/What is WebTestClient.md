<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Framework/WebFlux #Testing/Integration #SRS

# What is WebTestClient?

> [!abstract] Short answer
> **`WebTestClient`** (`org.springframework.test.web.reactive.server`, Framework **5.0+**) is the **test HTTP client** that **wraps `WebClient`** and adds **`exchange().expectStatus() / expectBody()`**. Bind **without a server** (`bindToController`, `bindToRouterFunction`, `bindToApplicationContext`) or **`bindToServer()`** for live HTTP. Boot: **`@WebFluxTest` auto-configures it**; otherwise **`@AutoConfigureWebTestClient`** (`org.springframework.boot.webtestclient.autoconfigure`). It is **not** production **`WebClient`** and **not** **`MockMvc`**.

## Same request API as `WebClient`, then assertions

Up to **`exchange()`** the fluent calls match **`WebClient`**. After that you **verify**: chained **`expect*`**, **`expectAll`** (soft), **`expectBody().json(...)`** / **`jsonPath`**, or **`returnResult`** + **`StepVerifier`** for SSE / NDJSON. MVC without a socket uses **`MockMvcWebTestClient`** (MockMvc underneath), not `WebTestClient.bindToController`.

Boot **4.1**: mock `@SpringBootTest` can plug MockMvc into **`WebTestClient`** via **`@AutoConfigureWebTestClient`**. **`RANDOM_PORT`** + the same annotation talks **real HTTP**. **`@WebMvcTest`** is still **MockMvc** (or **`RestTestClient`** with MockMvc as the server) — dumps that pair `WebTestClient` with **`@WebMvcTest`** skip that split. vs production client: [[What is the difference between WebClient and WebTestClient]]. Slice: [[What is the WebFluxTest annotation]]. How-to: [[How do you test a WebFlux endpoint]]. Blocking sibling: [[What is TestRestTemplate]]. Modes: [[What is SpringBootTest WebEnvironment]].

```java
@WebFluxTest(UserVehicleController.class)
class MyControllerTests {

    @Autowired WebTestClient webClient;

    @Test
    void testExample() {
        this.webClient.get().uri("/sboot/vehicle")
                .exchange()
                .expectStatus().isOk()
                .expectBody(String.class).isEqualTo("Honda Civic");
    }
}
```

**Listing 1.** Conceptual Boot **4.1** slice — **no** Netty. Field type is **`WebTestClient`** even if named `webClient`.

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureWebTestClient
class MyRandomPortWebTestClientTests {

    @Test
    void exampleTest(@Autowired WebTestClient webClient) {
        webClient.get().uri("/").exchange().expectStatus().isOk();
    }
}
```

**Listing 2.** Conceptual: live server. Manual equivalent: **`WebTestClient.bindToServer().baseUrl(...).build()`**.

```d2
direction: down
bind: "bindToController / Context / Router\nor bindToServer" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
api: "get().uri().exchange()" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
assert: "expectStatus / expectBody\nor StepVerifier" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

bind -> api -> assert
```

**Fig. 1.** Mock bind never opens a socket. **`bindToServer`** does.

> [!warning] Not a production bean
> Application code injects **`WebClient`**. Tests inject **`WebTestClient`**. No **`expectStatus`** on the production type.

> [!warning] `@WebMvcTest` does not mean `WebTestClient`
> The MVC slice auto-configures **MockMvc**. To reuse this fluent API on servlet MVC, Boot plugs MockMvc in, or you call **`MockMvcWebTestClient`**. WebFlux slice: **`@WebFluxTest`**.

> [!warning] Streams need `verify()`
> **`returnResult` + `StepVerifier.create(…).thenCancel().verify()`**. A chain of **`expectNext` without `verify()` never subscribes**.

> [!tip] Interview answer
> **`WebTestClient` wraps `WebClient` for tests: `exchange()` then `expectStatus` / `expectBody`.** Mock-bind a WebFlux app or `bindToServer` for real HTTP. `@WebFluxTest` gives it to you. Production still uses `WebClient`.
