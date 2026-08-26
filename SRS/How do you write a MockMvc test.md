<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Framework/WebMvc #Testing/Mocking #Java/Annotations #SRS

# How do you write a MockMvc test?

> [!abstract] Short answer
> Get a **`MockMvc`** (Boot: **`@WebMvcTest`** or **`@SpringBootTest` + `@AutoConfigureMockMvc`**). Static-import **`MockMvcRequestBuilders.*`** and **`MockMvcResultMatchers.*`**. Call **`perform(get("/…"))`**, then **`andExpect(status().isOk())`**, **`jsonPath("$.field").value(…)`**, **`view().name(…)`**, **`model()`**. **`andExpect` stops at the first failure**; **`andExpectAll`** reports every matcher. AssertJ path: autowire **`MockMvcTester`** and **`assertThat(mvc.get().uri("/")).hasStatusOk()`**. This is **not** a real port — no Tomcat.

## perform, then matchers

`perform` takes a **`RequestBuilder`**: `get("/accounts/{id}", 1)`, `post(…)`, `.accept(APPLICATION_JSON)`, `.param("name", "…")`, `.content(…)` / `.contentType(…)`. Prefer **URI without** context path; if you include `/app`, set **`contextPath`** (or `defaultRequest`) so mappings still hit.

Matchers: **response** (`status`, `header`, `content`, `jsonPath`, `xpath`) and **MVC** (`view`, `model`, `flash`, `handler`, `forwardedUrl`). JSON in-framework: **`jsonPath("$.person.name").value("Jason")`** or **`content().json("{…}")`** (needs **JSONassert**; default compare is **lenient** — extra fields and unordered arrays allowed). Framework **6.2+**: **`content().json(expected, JsonCompareMode.STRICT)`**; boolean **`json(json, false)`** is **deprecated**. Dump **`JSONAssert.assertEquals(expected, body, false)`** after **`andReturn()`** is the same **lenient** mode on the raw string — not required if you stay on **`andExpect`**.

`andReturn()` yields **`MvcResult`** when a matcher is not enough. **`andDo(print())`** dumps the result (`MockMvcResultHandlers`). Setup: [[How do you test a Spring MVC controller in isolation]]. What MockMvc is: [[What is MockMvc]]. Live HTTP: [[How do you test REST endpoints end to end]]. Lenient JSON: [[What is JSONAssert]].

```java
@SpringBootTest
@AutoConfigureMockMvc
class MyMockMvcTests {

    @Test
    void testWithMockMvc(@Autowired MockMvc mvc) throws Exception {
        mvc.perform(get("/"))
                .andExpect(status().isOk())
                .andExpect(content().string("Hello World"));
    }

    @Test
    void testWithMockMvcTester(@Autowired MockMvcTester mvc) {
        assertThat(mvc.get().uri("/"))
                .hasStatusOk()
                .hasBodyTextEqualTo("Hello World");
    }
}
```

**Listing 1.** Conceptual Boot **4.1**. Slice tests swap `@SpringBootTest` for **`@WebMvcTest(TheController.class)`** and **`@MockitoBean`** the service.

```java
mockMvc.perform(get("/person/1"))
        .andExpect(status().isOk())
        .andExpect(content().contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.person.name").value("Jason"));
```

**Listing 2.** Conceptual Framework **7** Hamcrest chain. First failed **`andExpect`** skips the rest; use **`andExpectAll(…)`** to see every mismatch.

```d2
direction: down
req: "MockMvcRequestBuilders\nget / post / param" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
mvc: "MockMvc.perform\nDispatcherServlet in-process" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
exp: "andExpect / jsonPath / view" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}

req -> mvc -> exp
```

**Fig. 1.** No TCP. Filters run if Boot registered them (`@AutoConfigureMockMvc` **`addFilters` defaults true**). Error **pages** still need a real server.

> [!warning] `JSONAssert.assertEquals(..., false)` hides extras
> **`strict = false`** is **extensible** JSON: leftover properties and **unordered arrays** still pass. Prefer **`jsonPath`** for the fields you care about, or **`JsonCompareMode.STRICT`**.

> [!warning] `@SpringBootTest` does not give you `MockMvc`
> Add **`@AutoConfigureMockMvc`**. **`@WebMvcTest`** already does. **`andReturn()`** without **`andExpect(status())`** can ignore a **500**.

> [!warning] POST + Security
> CSRF is on by default. **`.with(csrf())`** or you get **403**, not a JSON mismatch.

> [!tip] Interview answer
> **`mockMvc.perform(get("/…")).andExpect(status().isOk()).andExpect(jsonPath("$.x").value(…))`.** Boot 4 also has **`MockMvcTester`**. That is the MVC layer, not `RANDOM_PORT`. Do not assert the whole body with lenient JSONAssert unless you mean to ignore extra fields.
