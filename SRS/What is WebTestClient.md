<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Integration #SRS #New

Untrusted draft. Confirm against a Spring Boot testing dump before treating as exam-ready.

> [!NOTE]
> **Answer**
> `WebTestClient` is a fluent HTTP client for tests. A testing overview says it sends requests and reads responses and is typically used with `@SpringBootTest` or `@WebMvcTest`. A Spring Boot interview dump also names it for end-to-end tests on a random port and for testing reactive WebFlux code, alongside `StepVerifier`.

> [!WARNING]
> **Traps**
> Unverified traps from the dump. It is not the same client as production `WebClient`. `TestRestTemplate` is the blocking RestTemplate-style helper on `@SpringBootTest`; `MockMvc` stays inside the servlet stack without a real HTTP server unless you combine it with a full web environment.

---
