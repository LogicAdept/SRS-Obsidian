<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Integration #SRS #New

Untrusted draft. Confirm against a Spring Boot testing dump before treating as exam-ready.

> [!NOTE]
> **Answer**
> A Spring Boot testing overview splits the three by stack. `MockMvc` is the fluent client for MVC tests, typically with `@WebMvcTest`. `TestRestTemplate` is the fluent client for REST tests, typically with `@SpringBootTest`. `WebTestClient` is another fluent HTTP test client, used with `@SpringBootTest` or `@WebMvcTest`, and interview dumps also use it for random-port end-to-end tests and for WebFlux.

> [!WARNING]
> **Traps**
> Unverified traps from the dump. `MockMvc` does not prove that Tomcat or Netty actually listened on a port. `TestRestTemplate` needs a real server environment such as `RANDOM_PORT` if you want HTTP over the wire. Do not treat `WebTestClient` as production `WebClient`.

---
