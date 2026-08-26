<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Spring/Framework/Testing #SRS

# What is the difference between `WebClient` and `WebTestClient`?

> [!abstract] Short answer
> **`WebClient`** is the **production** reactive HTTP client. **`WebTestClient`** is a **test client** that **uses `WebClient` internally** and adds **assertions** (`expectStatus()`, `expectBody()`). It can **bind to a mock WebFlux app** (no live HTTP server) or **`bindToServer()`** against a real port. It is **not** MockMvc and **not** a bean you inject into application code.

## Production vs test facade

Spring *WebClient*: fluent, non-blocking, Reactor — [[What is WebClient]].

`WebTestClient` javadoc (since **5.0**): client for **testing web servers**; fluent **verify** API. Bind:

- `bindToController` / `bindToRouterFunction` — mock server, `@EnableWebFlux`-equivalent
- `bindToApplicationContext` / `bindToWebHandler` — mock request/response
- `bindToServer()` — live HTTP

Boot: `@WebFluxTest` **auto-configures `WebTestClient`**. Full app: `@SpringBootTest` + `@AutoConfigureWebTestClient`, or **`RANDOM_PORT`**. How-to: [[How do you test a WebFlux endpoint]].

```java
this.webClient.get().uri("/sboot/vehicle")
        .accept(MediaType.TEXT_PLAIN)
        .exchange()
        .expectStatus().isOk()
        .expectBody(String.class).isEqualTo("Honda Civic");
```

**Listing 1.** Conceptual Boot slice assertion API — `exchange()` then expectations. Production code uses `retrieve().bodyToMono`, not `expectStatus`.

```d2
direction: down
prod: "Application\nWebClient" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}
test: "Test\nWebTestClient" {
  width: 220
  height: 55
  style.fill: "#fff3e0"
}
mock: "Mock WebFlux\nor live server" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}

test -> mock
prod -> mock: "only bindToServer / real HTTP"
```

**Fig. 1.** Dump “thin shell around `WebClient`” is fair for the **HTTP** path; mock bind **does not** open a socket.

> [!warning] Do not use `WebClient` as MockMvc
> No `expectStatus` chain. For MVC slices use **MockMvc**. For WebFlux slices use **`WebTestClient`**.

> [!warning] Same class name `webClient` in Boot samples
> The field is often named `webClient` but the type is **`WebTestClient`**. Production `WebClient` is a different type.

> [!tip] Interview answer
> **`WebClient` calls HTTP in production. `WebTestClient` tests a WebFlux app — mock bind or live server — with assertion DSL.** Internally it can use `WebClient`. MockMvc is the servlet test API.

## See also

- [[What is WebClient]]
- [[How do you test a WebFlux endpoint]]
- [[What is the WebFluxTest annotation]]
- [[What is bodyToMono]]
- [[How do you implement Server-Sent Events in WebFlux]]
