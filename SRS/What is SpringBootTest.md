<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Testing/Integration #Java/Annotations #SRS

# What is SpringBootTest?

> [!abstract] Short answer
> **`@SpringBootTest`** (Boot **1.4+**, `org.springframework.boot.test.context`) is the annotation that loads a test **`ApplicationContext` through `SpringApplication`**. That is Boot’s extra on top of `@ContextConfiguration`: **`SpringBootContextLoader`**, search for **`@SpringBootConfiguration`**, **`properties` / `args`**, and **`webEnvironment`**. Default **`webEnvironment` is `MOCK`** — **no** embedded server. **`useMainMethod` defaults to `NEVER`** (since **3.0**). Boot documents these tests as **full integration tests of the entire application**, not unit tests. JUnit **6**: the annotation already carries **`@ExtendWith(SpringExtension)`**. JUnit **4** still needs **`@RunWith(SpringRunner.class)`**.

## Full `SpringApplication` refresh

If you omit **`classes`**, the loader looks for nested `@Configuration`, then walks **up from the test package** to **`@SpringBootApplication` / `@SpringBootConfiguration`**. Scan, `application.properties` / yaml, and **auto-configuration** run as in production (minus test-only overrides). **`classes = {EmployeeService.class, EmployeeRepository.class}`** is a **custom** context: you **drop** Boot auto-config unless those types pull it in — that is **not** “the app under test” and **not** a unit test.

**`RANDOM_PORT` / `DEFINED_PORT`** start a real server (`spring-boot-web-server`); inject the port with **`@LocalServerPort`**. **`NONE`** sets **`WebApplicationType.NONE`**. HTTP clients: **`@AutoConfigureRestTestClient` / `@AutoConfigureTestRestTemplate`**. MVC in-process: **`@AutoConfigureMockMvc`** (not implied by `@SpringBootTest` alone).

A **slice** (`@WebMvcTest`, `@DataJpaTest`) is a **different** `@…Test`: restricted scan and auto-config. Dump “unit-speed `@SpringBootTest` + `@MockBean`” is **`@MockitoBean`** on Boot **4**, and a slice is usually the right tool. Annotation family: [[What are Spring Boot test slices]]. Modes: [[What is SpringBootTest WebEnvironment]]. Recipe: [[How do you write a Spring Boot integration test]]. MVC slice: [[What is the WebMvcTest annotation]]. JPA slice: [[What is the DataJpaTest annotation]].

```java
@SpringBootTest
class ApplicationTests {
    @Test
    void contextLoads() {}
}
```

**Listing 1.** Conceptual Initializr smoke test. Refresh succeeded — not “every URL and security rule works.”

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class SpringBootDemoApplicationTests {
    @LocalServerPort
    int randomServerPort;
}
```

**Listing 2.** Conceptual: **opt in** to a listen port. Default without `webEnvironment` is **`MOCK`**, and **`@LocalServerPort` is unused**.

```d2
direction: down
ann: "@SpringBootTest\nSpringBootContextLoader" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
app: "SpringApplication\nauto-config + properties" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
web: "webEnvironment\nMOCK | RANDOM_PORT | DEFINED_PORT | NONE" {
  width: 340
  height: 50
  style.fill: "#e8f5e9"
}

ann -> app -> web
```

**Fig. 1.** Same machinery as production startup, driven by the test. Slices **do not** use this annotation.

> [!warning] This is not a unit test
> Dump headings that pair `@SpringBootTest` with “unit testing” are **wrong**. Use **`new` + Mockito**, or a **slice**. A `classes = {Service, Repo}` list is a **hand-built** context, not a faster unit.

> [!warning] Default does not bind a port
> **`MOCK`**. `@LocalServerPort` and live **`TestRestTemplate`** need **`RANDOM_PORT` or `DEFINED_PORT`** plus the matching **`@AutoConfigure…`**.

> [!warning] `@RunWith(SpringRunner.class)` is JUnit 4
> On JUnit **5 / 6** the extension is **already** on `@SpringBootTest`. **`@MockBean`** was **removed** in Boot **4**.

> [!tip] Interview answer
> **`@SpringBootTest` loads the Boot application through `SpringApplication` — full auto-config, default mock web, no Tomcat.** Use it for wiring and smoke tests. For one layer, a **slice**. For real HTTP, **`RANDOM_PORT`**. Do not call it a unit test.
