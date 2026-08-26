<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Testing/Integration #Java/Annotations #SRS

# What is SpringBootTest WebEnvironment?

> [!abstract] Short answer
> **`SpringBootTest.WebEnvironment`** (nested enum on **`@SpringBootTest`**, since **1.4**) chooses **whether a web server starts**. Default **`MOCK`**: mock web environment, **no** embedded server. **`RANDOM_PORT`** starts a real server and sets **`server.port=0`** (ephemeral listen). **`DEFINED_PORT`** uses **`application.properties`** or **8080**. **`NONE`** sets **`WebApplicationType.NONE`**. Live HTTP needs **`RANDOM_PORT` or `DEFINED_PORT`** plus **`spring-boot-web-server`**. Inject the bound port with **`@LocalServerPort`**.

## Four modes

By default **`@SpringBootTest` does not start a server**. The attribute:

- **`MOCK`** — web `ApplicationContext` with a **mock** servlet (or **reactive** mock if only WebFlux). No web APIs on the classpath → ordinary non-web context. Pair with **`@AutoConfigureMockMvc`** or **`@AutoConfigureWebTestClient`**.
- **`RANDOM_PORT`** — **`WebServerApplicationContext`**, real embedded server, **`server.port=0`**. Boot **recommends** this so parallel tests do not collide. A **separate** management port also gets a random bind if you split Actuator.
- **`DEFINED_PORT`** — real server, **no** `server.port=0`. Collision risk on **8080**.
- **`NONE`** — `SpringApplication` with **no** web environment (mock or real).

`isEmbedded()` is true for the two **PORT** values. Full annotation: [[What is SpringBootTest]]. Port injection: [[What is LocalServerPort]]. Live HTTP: [[How do you test REST endpoints end to end]]. Clients: [[What is TestRestTemplate]], [[What is WebTestClient]]. In-process MVC: [[What is MockMvc]].

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class MyRandomPortRestTestClientTests {

    @Test
    void exampleTest(@Autowired RestTestClient restClient) {
        restClient.get().uri("/").exchange().expectStatus().isOk();
    }
}
```

**Listing 1.** Conceptual Boot **4.1**. Relative URIs hit the **running** server.

```java
@SpringBootTest  // webEnvironment defaults to MOCK
@AutoConfigureMockMvc
class MockWebTests {
    @Autowired MockMvc mvc;
}
```

**Listing 2.** Conceptual: **no** Tomcat. `@LocalServerPort` is unused.

```d2
direction: down
mock: "MOCK\nno listen port" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
rand: "RANDOM_PORT\nserver.port=0" {
  width: 220
  height: 45
  style.fill: "#fff3e0"
}
def: "DEFINED_PORT\n8080 / properties" {
  width: 230
  height: 45
  style.fill: "#fce4ec"
}
none: "NONE\nWebApplicationType.NONE" {
  width: 250
  height: 45
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Same `@SpringBootTest` loader; only **PORT** modes bind a socket.

> [!warning] `RANDOM_PORT` is not MockMvc
> Real TCP, real container, **different thread**. `@WithMockUser` **does not** ride the HTTP call. `@Transactional` on the test **does not** roll back work the **server** did in its thread.

> [!warning] Default is `MOCK`
> Omitting `webEnvironment` and then autowiring **`TestRestTemplate`** against `localhost:8080` tests **nothing** that this class started. Add **`RANDOM_PORT`** and **`@AutoConfigureTestRestTemplate`** / **`@AutoConfigureRestTestClient`**.

> [!warning] `DEFINED_PORT` fights other processes
> Two test JVMs on **8080** fail to bind. Prefer **`RANDOM_PORT`**.

> [!tip] Interview answer
> **`webEnvironment` on `@SpringBootTest`: default `MOCK` (no server), `RANDOM_PORT` for real HTTP on an ephemeral port, `DEFINED_PORT` for a fixed port, `NONE` for no web at all.** Use `@LocalServerPort` when you started a server.
