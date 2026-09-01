<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Testing/Integration #SRS

# What types of tests does Spring Boot support?

> [!abstract] Short answer
> Boot’s testing chapter names **three** shapes, not ISTQB labels. **Unit:** `new` the class, mock collaborators — **no `ApplicationContext`** (`spring-boot-starter-test` still gives JUnit / Mockito / AssertJ). **Integration:** load a Spring context — **`@SpringBootTest`** is “full integration tests and involve the entire application.” **Slice:** a `@…Test` (`@WebMvcTest`, `@DataJpaTest`, …) that loads **one layer’s** auto-config. A **running server** (`webEnvironment = RANDOM_PORT`) is still `@SpringBootTest`, with real HTTP. There is **no** Boot annotation named “functional test.” Calling `@SpringBootTest` a **unit** test is wrong.

## Unit, slice, full context, optional listen port

Dependency injection exists so you can **unit-test without Spring**. Escalate when the behavior **is** a container feature (auto-config, AOP, MVC mapping, JPA mapping).

| Kind | Typical annotation | What starts |
| --- | --- | --- |
| Unit | `@ExtendWith(MockitoExtension.class)` | **Nothing Spring** |
| Slice | `@WebMvcTest`, `@DataJpaTest`, `@JsonTest`, … | **Narrow** context |
| Integration (mock web) | `@SpringBootTest` (default **`MOCK`**) | Full **`SpringApplication`**, **no** Tomcat |
| Integration (HTTP) | `@SpringBootTest(webEnvironment = RANDOM_PORT)` | Full context **+ embedded server** |

Slices are **not** Mockito-only: they still refresh an **`ApplicationContext`** (and hit the TestContext **cache**). They are **not** `@SpringBootTest`. Two `@…Test` slice annotations on one class are **unsupported**. Unit vs AOP: [[How do you test the service layer in Spring]]. Slices: [[What are Spring Boot test slices]]. Full context: [[What is SpringBootTest]]. Live HTTP: [[How do you test REST endpoints end to end]].

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTests {
    @Mock OrderRepository orders;
    @InjectMocks OrderService service;
}
```

**Listing 1.** Conceptual **unit** test. Boot’s *Testing Spring Applications*: instantiate with **`new`**, mock dependencies.

```java
@SpringBootTest
class ApplicationTests {
    @Test
    void contextLoads() {}
}
```

**Listing 2.** Conceptual **integration** smoke test. Success is **refresh**, not “every URL works.” Add **`RANDOM_PORT`** only when you need a listen port.

```d2
direction: down
unit: "new + Mockito\nno ApplicationContext" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
slice: "@WebMvcTest / @DataJpaTest\nnarrow auto-config" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
full: "@SpringBootTest\nfull SpringApplication" {
  width: 260
  height: 45
  style.fill: "#fff3e0"
}
http: "RANDOM_PORT\nreal HTTP" {
  width: 240
  height: 40
  style.fill: "#ffebee"
}

unit -> slice: "need MVC/JPA wiring"
slice -> full: "need the whole app"
full -> http: "need the container"
```

**Fig. 1.** Cost goes **down → up**. MockMvc in a slice is **not** E2E; **`RANDOM_PORT`** is. Dump “functional / E2E” maps to that last box, not a fourth annotation.

> [!warning] `@SpringBootTest` is not a unit test
> Boot documents it as a **full integration** test. A `contextLoads()` method still boots **auto-config**. Use Mockito **`new`** for a unit.

> [!warning] A slice is not “no Spring”
> `@WebMvcTest` still builds a context (Security included if on the classpath). Faster than `@SpringBootTest`, slower than `@InjectMocks`.

> [!warning] Default `@SpringBootTest` is not E2E HTTP
> **`MOCK`** does not bind a port. End-to-end HTTP is **`RANDOM_PORT`** plus **`RestTestClient` / `TestRestTemplate`**.

> [!tip] Interview answer
> **Four rungs Boot actually ships: Mockito unit, slice `@…Test`, `@SpringBootTest`, and `@SpringBootTest(RANDOM_PORT)`.** Slices are layer-scoped integration, not unit tests. Do not call the full Boot context a unit test.
