<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Framework/WebMvc #Java/Spring/Framework/WebFlux #Testing/Integration #SRS

# What is the difference between MockMvc TestRestTemplate and WebTestClient?

> [!abstract] Short answer
> **`MockMvc`** drives **`DispatcherServlet` with mock Servlet requests** — **no listen port**. **`TestRestTemplate`** is a **blocking HTTP client** (`RestTemplate`-shaped): **4xx/5xx do not throw**; use it against a **real** server (`RANDOM_PORT` / `DEFINED_PORT`). **`WebTestClient`** wraps **`WebClient`** and adds **`exchange().expectStatus()`**; it **mock-binds** a WebFlux (or MockMvc) app **or** **`bindToServer()`**. Dumps that call all three “fluent REST clients for `@WebMvcTest`” mix the stacks. Boot **4.1** also has **`RestTestClient`** (fluent, MockMvc or live) — not one of these three names.

## Layer vs wire vs assertion DSL

| | **MockMvc** | **TestRestTemplate** | **WebTestClient** |
| --- | --- | --- | --- |
| Stack | Servlet MVC | Any HTTP server | WebFlux mock, MockMvc plug-in, or live HTTP |
| Typical Boot | `@WebMvcTest` or `@AutoConfigureMockMvc` | `@SpringBootTest` + **PORT** + `@AutoConfigureTestRestTemplate` | `@WebFluxTest` or `@AutoConfigureWebTestClient` |
| Socket | No | Yes (auto-config) | Only **`bindToServer` / RANDOM_PORT** |
| API | `perform` / `MockMvcTester` | `getForEntity` / `exchange` | `get().uri().exchange().expect…` |

MockMvc stops at the **Spring MVC layer**. Boot’s **error pages** live on the **container** — you cannot assert a custom error HTML with MockMvc. **`TestRestTemplate`** and live **`WebTestClient`** go through **TCP**, filters, and the real server thread (`@WithMockUser` **does not** ride along). Mock: [[What is MockMvc]]. Blocking client: [[What is TestRestTemplate]]. Reactive test client: [[What is WebTestClient]]. Modes: [[What is SpringBootTest WebEnvironment]]. End-to-end: [[How do you test REST endpoints end to end]].

```java
mockMvc.perform(get("/")).andExpect(status().isOk());
```

**Listing 1.** Conceptual: in-process MVC. `@WebMvcTest` already has MockMvc.

```java
restTemplate.getForObject("/", String.class);           // TestRestTemplate, RANDOM_PORT
webClient.get().uri("/").exchange().expectStatus().isOk(); // WebTestClient
```

**Listing 2.** Conceptual Boot **4.1**. Relative URIs on the auto-configured HTTP clients hit the **embedded** server.

```d2
direction: down
mvc: "MockMvc\nDispatcherServlet" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
trt: "TestRestTemplate\nreal HTTP" {
  width: 220
  height: 45
  style.fill: "#fff3e0"
}
wtc: "WebTestClient\nmock bind or HTTP" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Same assertion goal; different servers. **`WebTestClient` on MOCK** can still be MockMvc underneath.

> [!warning] `TestRestTemplate` is not fluent and not `@WebMvcTest`
> It is **`getForEntity`**, not `expectStatus`. Default **`@SpringBootTest` is `MOCK`** — without **`RANDOM_PORT`** this client is not talking to a server this test started. Boot **4** also needs **`@AutoConfigureTestRestTemplate`**.

> [!warning] `@WebMvcTest` does not auto-wire `WebTestClient`
> That slice is **MockMvc**. **`@WebFluxTest`** auto-configures **`WebTestClient`**. Production code still uses **`WebClient`**, not this type.

> [!warning] MockMvc never proves a port
> No Tomcat/Netty bind. Container error pages, real TLS, and **`RANDOM_PORT` security on another thread** need a **PORT** environment plus **`TestRestTemplate` / `WebTestClient` / `RestTestClient`**.

> [!tip] Interview answer
> **MockMvc tests Spring MVC in-process with no server. TestRestTemplate is RestTemplate for tests against a real port (4xx do not throw). WebTestClient is the WebClient-shaped test client — mock WebFlux or live HTTP.** Pick by stack and whether you need a listen port.
