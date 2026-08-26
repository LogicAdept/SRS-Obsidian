<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Framework/WebMvc #Testing/Mocking #SRS

# What is MockMvc?

> [!abstract] Short answer
> **`MockMvc`** (`org.springframework.test.web.servlet`) is Spring’s **server-side MVC test driver**. It runs the **`DispatcherServlet`** with **mock Servlet API** request/response objects from **`spring-test`** — **full Spring MVC handling, no running server**. Hamcrest: **`perform(get("/…")).andExpect(status().isOk())`**. AssertJ: **`MockMvcTester`**. You can also plug MockMvc in as the server behind **`WebTestClient`**. It is **not** Tomcat and **not** `RANDOM_PORT`.

## DispatcherServlet, mock request/response

Plain `new Controller()` skips mappings, binding, converters, `@ExceptionHandler`. MockMvc is the next step. Two builders (`MockMvcBuilders`):

- **`webAppContextSetup(wac)`** — real MVC config, cached `WebApplicationContext` (what **`@WebMvcTest`** / **`@AutoConfigureMockMvc`** use). Override services with **`@MockitoBean`**.
- **`standaloneSetup(controller)`** — one controller, programmatic MVC, **no** Spring MVC config loaded. You still need integration tests for `WebMvcConfigurer` / Security.

Boot: **`@WebMvcTest` auto-configures `MockMvc`**. **`@SpringBootTest` does not** — add **`@AutoConfigureMockMvc`**. **`addFilters` defaults true** (Security filters run). How to assert: [[How do you write a MockMvc test]]. Slice: [[What is the WebMvcTest annotation]]. Isolation: [[How do you test a Spring MVC controller in isolation]]. Live HTTP: [[How do you test REST endpoints end to end]]. Enable on full context: [[What is AutoConfigureMockMvc]].

```java
mockMvc.perform(get("/accounts/1")).andExpect(status().isOk());
```

**Listing 1.** Conceptual Framework Hamcrest. Static imports: **`MockMvcRequestBuilders.*`**, **`MockMvcResultMatchers.*`**.

```java
assertThat(mvc.get().uri("/")).hasStatusOk().hasBodyTextEqualTo("Hello World");
```

**Listing 2.** Conceptual Boot **4.1** **`MockMvcTester`**. Same in-process stack, AssertJ API.

```d2
direction: down
client: "perform(get) / MockMvcTester" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
ds: "DispatcherServlet\nmock HttpServletRequest" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
out: "andExpect / jsonPath / view" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}

client -> ds -> out
```

**Fig. 1.** No TCP. Servlet-container **error pages** and real TLS/filters below MVC **cannot** be asserted here — use **`RANDOM_PORT`**.

> [!warning] `@SpringBootTest` does not give you MockMvc
> Autowire fails until **`@AutoConfigureMockMvc`**. The slice **`@WebMvcTest`** already registers it. That full context is still **slow**; MockMvc does not make `@SpringBootTest` a slice.

> [!warning] Not end-to-end HTTP
> MockMvc stops at the **Spring MVC layer**. Boot’s error-page support lives on the **servlet container**.

> [!warning] Filters and CSRF still apply
> Default Boot MockMvc **registers filters**. Unauthenticated **401 / 302**; POST without **`csrf()`** is **403**. Manual `MockMvcBuilders` needs **`.apply(springSecurity())`** for Security’s test support.

> [!tip] Interview answer
> **MockMvc drives `DispatcherServlet` with mock Servlet requests — no Tomcat.** `perform` + `andExpect`, or Boot 4 `MockMvcTester`. Get it from `@WebMvcTest` or `@SpringBootTest` + `@AutoConfigureMockMvc`. For a real port, that is a different test.
