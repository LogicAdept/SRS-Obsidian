<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Testing/Integration #Java/Annotations #SRS

# How do you ensure the Spring application context loads in a test?

> [!abstract] Short answer
> Put **`@SpringBootTest`** on a JUnit class (Boot **1.4+**; Boot **4.1** already includes **`@ExtendWith(SpringExtension)`**). The TestContext Framework loads an **`ApplicationContext` through `SpringApplication`** before the tests. An empty **`contextLoads()`** method is enough: if refresh fails (missing bean, bad auto-config), the test fails. Default **`webEnvironment = MOCK`**: **no embedded server**. Search walks **up from the test package** to **`@SpringBootApplication` / `@SpringBootConfiguration`**. Non-Boot: **`@ContextConfiguration`** (or **`@SpringJUnitConfig`**). JUnit **4** still needs **`@RunWith(SpringRunner.class)`**.

## Load the context; the empty method is the assertion

`@SpringBootTest` is the Boot alternative to **`@ContextConfiguration`**. It uses **`SpringBootContextLoader`**, finds the primary config if you omit `classes`, and supports **`properties`**, **`args`**, **`webEnvironment`**, and **`useMainMethod`** (default **`NEVER`** since **3.0** — **`main` is not called**).

Default **`MOCK`**: web `ApplicationContext`, **no** Tomcat/Netty. No web on the classpath → ordinary non-web context. **`RANDOM_PORT` / `DEFINED_PORT`** start a real server; that is a different smoke test.

The TestContext Framework **caches** contexts that share the same configuration, so many `contextLoads` classes with the same setup pay **one** refresh. Framework **6.1+**: after a failed load for a cache key, further attempts are skipped (`IllegalStateException`; threshold default **1**, override **`spring.test.context.failure.threshold`**).

Slices (`@WebMvcTest`, …) are **not** this check — they load a **narrow** context. Full app: [[What is SpringBootTest]]. Slices: [[What are Spring Boot test slices]]. Cache: [[How does the Spring TestContext framework cache the ApplicationContext]]. Extension: [[What is SpringExtension]].

```java
@SpringBootTest
class ApplicationContextLoadTest {

    @Test
    void contextLoads() {
    }
}
```

**Listing 1.** Conceptual Initializr / Boot smoke test. Success means **refresh completed**, not that every URL or security rule works.

```d2
direction: down
ann: "@SpringBootTest\nSpringExtension" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
find: "Find @SpringBootApplication\nwalk packages upward" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
load: "SpringApplication\nrefresh ApplicationContext" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
ok: "Empty @Test passes" {
  width: 220
  height: 40
  style.fill: "#c8e6c9"
}

ann -> find -> load -> ok
```

**Fig. 1.** The assertion is **context construction**. HTTP, JDBC, and method security are untested until you call them.

> [!warning] Green `contextLoads` is not a web or security test
> **`MOCK`** does not start a server and does not run a request. Broken `SecurityFilterChain` mappings or a 404 stay hidden. Use MockMvc / **`RANDOM_PORT`** for HTTP.

> [!warning] The test must sit where the search can find the application class
> Discovery walks **up** from the **test’s package**. A test in a **sibling** root package never finds `@SpringBootApplication` → context load fails. Put tests under the same tree, or set **`classes`**.

> [!warning] `main()` customizations are skipped by default
> **`useMainMethod = NEVER`**. Banner, extra profiles, or `SpringApplication` tweaks in `main` are **not** in this context unless you set **`ALWAYS` / `WHEN_AVAILABLE`**.

> [!tip] Interview answer
> **`@SpringBootTest` plus an empty `contextLoads` test.** The TestContext Framework starts the Boot context; if refresh throws, the test fails. Default is a **mock** web environment, not a live port. It proves wiring at startup, not that endpoints work.
