<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Testing/Integration #Java/Annotations #SRS

# What is LocalServerPort?

> [!abstract] Short answer
> **`@LocalServerPort`** (`org.springframework.boot.test.web.server`, since **2.7** as this type) injects the **HTTP port the test’s embedded server actually bound**. It is **`@Value("${local.server.port}")`**. Use it on a field or a method/constructor parameter of a **`@SpringBootTest`** that started a **real** server — typically **`webEnvironment = RANDOM_PORT`**. Actuator on a separate port: **`@LocalManagementPort`** (`local.management.port`).

## Property after the container is up

`RANDOM_PORT` sets **`server.port=0`**; the OS picks a free port; the web-server implementation then publishes **`local.server.port`**. That is what the annotation reads. **`DEFINED_PORT`** also starts a server, so the same property exists (often **8080** unless you set `server.port`). **`MOCK` / `NONE`** start **no** HTTP listener — the property is **not** there for this annotation to resolve.

You rarely need the int to call the app: **`RestTestClient` / `TestRestTemplate` / `WebTestClient`** with the matching **`@AutoConfigure…`** already resolve **relative** URIs against the running server. Inject the port when **you** build a URL (another process, a raw socket, a non-Boot client). Modes: [[What is SpringBootTest WebEnvironment]]. Full test: [[What is SpringBootTest]]. Live HTTP: [[How do you test REST endpoints end to end]]. Clients: [[What is TestRestTemplate]], [[What is WebTestClient]].

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class MyWebIntegrationTests {

    @LocalServerPort
    int port;
}
```

**Listing 1.** Conceptual Boot **4.1** how-to. Package **`org.springframework.boot.test.web.server`**.

```java
@Test
void callsWithHandBuiltUrl(@LocalServerPort int port, @Autowired TestRestTemplate rest) {
    String body = rest.getForObject("http://localhost:" + port + "/", String.class);
    assertThat(body).isEqualTo("Hello World");
}
```

**Listing 2.** Conceptual: parameter injection. Prefer **`getForObject("/", String.class)`** when the template is auto-configured for that server.

```d2
direction: down
rand: "RANDOM_PORT\nserver.port=0" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
prop: "local.server.port" {
  width: 200
  height: 40
  style.fill: "#fff3e0"
}
ann: "@LocalServerPort int port" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

rand -> prop -> ann
```

**Fig. 1.** The int is the **bound** port, not the `0` you wrote in properties.

> [!warning] Not for production beans
> The value is written **after** the container initializes. A `@Component` that `@Value("${local.server.port}")` at startup sees it **too early**. Tests inject **after** the server started.

> [!warning] `MOCK` has no listen port
> Default `@SpringBootTest` does **not** start Tomcat/Netty. `@LocalServerPort` then has **nothing to resolve** — it is not a silent **0**. Use **`RANDOM_PORT`** (or **`DEFINED_PORT`**).

> [!warning] Management is a second port
> Split Actuator → **`@LocalManagementPort`**, not `@LocalServerPort`. **`RANDOM_PORT`** randomizes **both** when they differ.

> [!tip] Interview answer
> **`@LocalServerPort` is `@Value("${local.server.port}")` — the port the test server actually bound after `RANDOM_PORT`.** Auto-configured HTTP clients already know it. Do not put this on a production bean.
