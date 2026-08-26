<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Testing/Integration #Java/Annotations #SRS

# How do you test REST endpoints end to end?

> [!abstract] Short answer
> Use **`@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)`**. That loads a **`WebServerApplicationContext`**, starts the **embedded server** on an **ephemeral port**, and you talk **real HTTP**. Drive it with **`RestTestClient`** (`@AutoConfigureRestTestClient`), **`TestRestTemplate`** (`@AutoConfigureTestRestTemplate`), or **`WebTestClient`** (`@AutoConfigureWebTestClient`, typical when **`spring-webflux`** is on the classpath). Relative URIs are resolved against the running server. **Default `webEnvironment` is `MOCK`**: no Tomcat/Netty. Controller-only speed is **`@WebMvcTest` + MockMvc**, not this.

## Real port, real HTTP, full auto-config

`RANDOM_PORT` sets **`server.port=0`**. Inject the chosen port with **`@LocalServerPort`** if you build URLs by hand. **`DEFINED_PORT`** uses **`application.properties`** or **8080** — Boot recommends random ports so tests do not collide. **`NONE`** is not a web server at all.

Boot **4.1** first sample for a running server is **`RestTestClient`** (`spring-boot-resttestclient`). **`TestRestTemplate`** is the older RestTemplate-shaped helper: **4xx/5xx do not throw**; inspect the **`ResponseEntity`**. It also needs **`spring-boot-restclient`** (that starter auto-configures **`RestClient.Builder`** — keep it on the **main** classpath if production code uses the builder). **`WebTestClient`** works against the live server **or** a mock environment (`@AutoConfigureWebTestClient` without `RANDOM_PORT`).

This is **not** MockMvc. MockMvc stays inside the **Spring MVC layer** (faster; no servlet error pages, no real TLS/container filters). Slice: [[How do you test a Spring MVC controller in isolation]]. Modes: [[What is SpringBootTest WebEnvironment]]. Clients: [[What is TestRestTemplate]], [[What is WebTestClient]]. Outbound stubs while the app still listens: [[How do you mock external HTTP APIs in Spring tests]].

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class MyRandomPortRestTestClientTests {

    @Test
    void exampleTest(@Autowired RestTestClient restClient) {
        restClient.get().uri("/")
                .exchange()
                .expectStatus().isOk()
                .expectBody(String.class).isEqualTo("Hello World");
    }
}
```

**Listing 1.** Conceptual Boot **4.1** end-to-end sample. **`TestRestTemplate`** equivalent: add **`@AutoConfigureTestRestTemplate`** and **`getForObject("/", String.class)`**.

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureTestRestTemplate
class MyRandomPortTestRestTemplateTests {

    @Test
    void exampleTest(@Autowired TestRestTemplate restTemplate) {
        String body = restTemplate.getForObject("/", String.class);
        assertThat(body).isEqualTo("Hello World");
    }
}
```

**Listing 2.** Conceptual: same running server, RestTemplate-shaped client. Do **not** concatenate `http://localhost:` + port unless you need a URL the auto-configured client does not already resolve.

```d2
direction: down
ann: "@SpringBootTest\nRANDOM_PORT" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
server: "Embedded web server\nreal TCP port" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
client: "RestTestClient /\nTestRestTemplate / WebTestClient" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}

ann -> server -> client
```

**Fig. 1.** HTTP leaves the JVM’s mock MVC stack. Filters, error pages, and the embedded container run. Outbound vendor calls are a **separate** problem — stub those with WireMock / MockWebServer / `MockRestServiceServer`, not by switching this test to `@WebMvcTest`.

> [!warning] Default `@SpringBootTest` does not bind a port
> **`MOCK`** is the default. Autowiring `TestRestTemplate` without **`RANDOM_PORT` / `DEFINED_PORT`** and **`@AutoConfigureTestRestTemplate`** is the Boot **4** miss. Dump samples that inject the template with no auto-config annotation are **stale**.

> [!warning] `@Transactional` rollback does not cover the HTTP thread
> Client and server run **in different threads**, so they are **different transactions**. A method-level `@Transactional` on the test **does not** roll back work the server committed while handling the request.

> [!warning] MockMvc is not end-to-end HTTP
> It is faster and correct for **controller + MVC config**. It **cannot** prove servlet-container error pages. Use **`RANDOM_PORT`** for those.

> [!tip] Interview answer
> **`@SpringBootTest(webEnvironment = RANDOM_PORT)` and a real HTTP client** — Boot 4: `RestTestClient` or `TestRestTemplate` with the matching `@AutoConfigure…` annotation. That starts Tomcat/Netty. `@WebMvcTest` + MockMvc is the slice, not the live port.
