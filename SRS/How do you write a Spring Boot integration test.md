<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Testing/Integration #Java/Annotations #SRS

# How do you write a Spring Boot integration test?

> [!abstract] Short answer
> Put **`@SpringBootTest`** on the class. That loads an **`ApplicationContext` through `SpringApplication`** (auto-config, property files, the same type of refresh as production). **Default `webEnvironment` is `MOCK`**: full context, **no** embedded server — pair with **`@AutoConfigureMockMvc`** if you want in-process HTTP. For a **real port**: **`webEnvironment = RANDOM_PORT`** (needs **`spring-boot-web-server`**) and a client — Boot **4.1**: **`@AutoConfigureRestTestClient`** / **`@AutoConfigureTestRestTemplate`**. JUnit **6** already has **`@ExtendWith(SpringExtension)`** on `@SpringBootTest`; **`@RunWith(SpringRunner.class)` is JUnit 4 only**. Slices (`@WebMvcTest`, `@DataJpaTest`) are **not** this.

## Full `SpringApplication`, then pick the web mode

Omit **`classes`** unless you want a **narrow** set of component classes. Search order: nested `@Configuration`, then **`@SpringBootConfiguration` / `@SpringBootApplication`** walking **up from the test package**. **`useMainMethod` defaults to `NEVER`** (since **3.0**). Extra env: **`properties` / `args`**.

**`DEFINED_PORT`** binds **`server.port`** from config or **8080** (port fights in parallel CI). **`NONE`** sets **`WebApplicationType.NONE`**. **`@LocalServerPort`** injects the bound port after **`RANDOM_PORT` / `DEFINED_PORT`**. Relative URIs on the auto-configured clients already point at that server — you do **not** have to concatenate `http://localhost:` unless you build the URL yourself.

This is slower than a slice: every auto-config class runs. Context **cache** reuses the same key. HTTP on a real port is a **different thread** than the test, so method-level **`@Transactional` rollback does not undo server-side work**. Annotation: [[What is SpringBootTest]]. Modes: [[What is SpringBootTest WebEnvironment]]. Live HTTP recipe: [[How do you test REST endpoints end to end]]. Slice + MockMvc: [[How do you write a MockMvc test]]. Slices: [[What are Spring Boot test slices]].

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureTestRestTemplate
class SurveyControllerIT {

    @Test
    void exampleTest(@Autowired TestRestTemplate restTemplate) {
        String body = restTemplate.getForObject("/", String.class);
        assertThat(body).isEqualTo("Hello World");
    }
}
```

**Listing 1.** Conceptual Boot **4.1** full-stack HTTP. Dump samples with **`@RunWith(SpringRunner.class)`** and **`exchange("http://localhost:" + port, …)`** are the JUnit **4** / hand-built URL variant. Prefer **`RestTestClient`** + **`@AutoConfigureRestTestClient`** on current Boot.

```java
@SpringBootTest
@AutoConfigureMockMvc
class MyApplicationIntegrationTests {

    @Test
    void home(@Autowired MockMvc mvc) throws Exception {
        mvc.perform(get("/")).andExpect(status().isOk());
    }
}
```

**Listing 2.** Conceptual: still an **integration** test (full context), but **MOCK** — no Tomcat. Faster than **`RANDOM_PORT`**; cannot assert servlet error pages.

```d2
direction: down
boot: "@SpringBootTest\nSpringApplication refresh" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
mock: "MOCK + MockMvc\nno listen port" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
live: "RANDOM_PORT\nreal HTTP client" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
slice: "@WebMvcTest / @DataJpaTest\nnarrow auto-config" {
  width: 280
  height: 50
  style.fill: "#f3e5f5"
}

boot -> mock
boot -> live
slice -> mock: "not this annotation"
```

**Fig. 1.** Integration = **production-shaped context**. A slice is a **different** `@…Test`. `classes = {Service.class, Repo.class}` is a **custom** context, not “the Boot app.”

> [!warning] `@RunWith(SpringRunner.class)` is JUnit 4
> On JUnit **5 / 6** it is dead weight or a wrong runner. **`@SpringBootTest` already meta-annotates `SpringExtension`.**

> [!warning] Default `@SpringBootTest` does not bind a port
> **`MOCK`**. `TestRestTemplate` / `RestTestClient` against a live server need **`RANDOM_PORT` or `DEFINED_PORT`** plus the matching **`@AutoConfigure…`**. **`@LocalServerPort` is unused under `MOCK`.**

> [!warning] `classes = Application.class` is optional, not required
> If you **do** set `classes` to a handful of `@Service` types, you **drop** auto-config unless those classes pull it in. That is no longer “the application under test.”

> [!tip] Interview answer
> **`@SpringBootTest` for a full Boot context.** **`MOCK` + MockMvc`** if you do not need a listen port; **`RANDOM_PORT` + RestTestClient / TestRestTemplate`** for real HTTP. Use **`@WebMvcTest` / `@DataJpaTest`** when you only want that slice. Do not copy `@RunWith(SpringRunner)` onto JUnit 6.
