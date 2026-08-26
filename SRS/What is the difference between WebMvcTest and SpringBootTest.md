<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the difference between WebMvcTest and SpringBootTest?

> [!abstract] Short answer
> **`@WebMvcTest`** is a **slice**: MVC auto-config only, scan limited to **`@Controller` / advice / MVC / `SecurityFilterChain`**, **`MockMvc` auto-configured**, **no** `@Service` / `@Repository` / DB. **`@SpringBootTest`** loads the app through **`SpringApplication`** — **full auto-config**, default **`webEnvironment = MOCK`** (**no** server, **no** MockMvc until **`@AutoConfigureMockMvc`**). For a **listen port** use **`RANDOM_PORT`**. They are **both** `@…Test` annotations: **do not put both on one class**.

## Slice vs full `SpringApplication`

`@WebMvcTest(controllers = …)` exists to test **URL mapping without database calls**. Collaborators: **`@MockitoBean`** (Boot **4** **removed `@MockBean`**) or **`@Import`**. Security on the classpath **is** auto-configured — there is **no `secure`**. Fast, cached, still **in-process** (no Tomcat error pages).

`@SpringBootTest` is **not** a slice. Omit `classes` → search up to **`@SpringBootApplication`**. Real beans unless you override them. HTTP choices: **`@AutoConfigureMockMvc`** (still no port) or **`RANDOM_PORT`** + **`RestTestClient` / `TestRestTemplate`**. Framework’s **`@ContextConfiguration`** is the lower-level loader; Boot’s annotation is the **`SpringApplication`** alternative. Slice family: [[What are Spring Boot test slices]]. MVC slice: [[What is the WebMvcTest annotation]]. Full: [[What is SpringBootTest]]. Modes: [[What is SpringBootTest WebEnvironment]]. Isolation how-to: [[How do you test a Spring MVC controller in isolation]].

```java
@WebMvcTest(UserVehicleController.class)
class MyControllerTests {
    @Autowired MockMvcTester mvc;
    @MockitoBean UserVehicleService userVehicleService;
}
```

**Listing 1.** Conceptual Boot **4.1** slice. No `@Repository`.

```java
@SpringBootTest
@AutoConfigureMockMvc
class FullContextMockMvcTests { }

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureTestRestTemplate
class HttpOverTheWireTests { }
```

**Listing 2.** Conceptual: same full auto-config; only the **PORT** variant binds a socket.

```d2
direction: down
slice: "@WebMvcTest\ncontrollers + MockMvc" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
full: "@SpringBootTest\nall auto-config" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
mock: "+ @AutoConfigureMockMvc\nstill no port" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

full -> mock
```

**Fig. 1.** Want MockMvc **and** the whole app? **`@SpringBootTest` + `@AutoConfigureMockMvc`**, not two `@…Test` types.

> [!warning] Two `@…Test` annotations on one class are unsupported
> **`@WebMvcTest` + `@SpringBootTest`** (or `@WebMvcTest` + `@DataJpaTest`) is **not** a supported combination. Pick **one** `@…Test` and add the other slice’s **`@AutoConfigure…`** by hand.

> [!warning] `@SpringBootTest` does not give you MockMvc
> Autowire fails until **`@AutoConfigureMockMvc`**. Default **`MOCK`** also does **not** start Tomcat.

> [!warning] The slice has no `@Service`
> Constructor injection of a service **fails** unless you **`@MockitoBean`** / **`@Import`**. That is the point of the slice — not a broken test.

> [!tip] Interview answer
> **`@WebMvcTest` is the MVC slice plus MockMvc, no services or DB. `@SpringBootTest` is the full Boot application.** Do not stack them. Need MockMvc on the full context: `@AutoConfigureMockMvc`. Need real HTTP: `RANDOM_PORT`.
