<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #SRS

# What is the Spring TestContext Framework?

> [!abstract] Short answer
> The **Spring TestContext Framework** (`org.springframework.test.context`, Spring Framework 6.2) is **annotation-driven integration-test infrastructure** that is **agnostic of JUnit 4, JUnit Jupiter, and TestNG**. It loads an **`ApplicationContext`**, **injects the test instance**, can wrap methods in a **transaction**, and **caches** that context for later tests with the **same configuration** in the **same JVM**.

## Core types, not a JUnit plugin

A **`TestContextManager`** is created **per test class**. It owns a **`TestContext`** (current test state + context cache lookup) and fires events to **`TestExecutionListener`s** (DI, transactions, `@DirtiesContext`, …). A **`SmartContextLoader`** actually builds the `ApplicationContext` from `@ContextConfiguration` (component classes, XML, Groovy, initializers, profiles, test property sources, web).

You do **not** have to extend `AbstractJUnit4SpringContextTests` / `AbstractTestNGSpringContextTests`. POJO tests plug in through [[What is SpringExtension]] (JUnit Jupiter), [[What is SpringRunner]] (JUnit 4.12+), JUnit 4 **`SpringClassRule` / `SpringMethodRule`**, or TestNG base classes. Configuration is [[What is the ContextConfiguration annotation]] and friends, not a runner-specific API.

```d2
direction: down
mgr: "TestContextManager\n(one per test class)" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
ctx: "TestContext" {
  width: 200
  height: 40
  style.fill: "#fff3e0"
}
loader: "SmartContextLoader" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
cache: "static ContextCache" {
  width: 200
  height: 40
  style.fill: "#fce4ec"
}
listeners: "TestExecutionListener\n(DI, tx, DirtiesContext, …)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}

mgr -> ctx
mgr -> listeners
ctx -> loader
ctx -> cache
```

**Fig. 1.** Framework-agnostic core. JUnit/TestNG adapters only call `TestContextManager` at lifecycle points.

Default loaders: **`DelegatingSmartContextLoader`**, or **`WebDelegatingSmartContextLoader`** when **`@WebAppConfiguration`** is present.

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfig.class)
class RepositoryTests {

	@Autowired
	TitleRepository titles;

	@Test
	void findById() {
		assertNotNull(titles.findById(10L));
	}
}
```

**Listing 1.** Conceptual Jupiter POJO test: extension + `@ContextConfiguration`. Shorthand: `@SpringJUnitConfig(TestConfig.class)`. DI is `DependencyInjectionTestExecutionListener` (on by default).

## Caching is the expensive part

After the first load, the context is stored in a **static** cache keyed by the **full** configuration tuple: `@ContextConfiguration` locations/classes/loader/initializers, `ContextCustomizer`s (`@DynamicPropertySource`, `@MockitoBean` / `@TestBean`, Boot extras), parent from `@ContextHierarchy`, `@ActiveProfiles`, `@TestPropertySource`, `@WebAppConfiguration` resource path. Same key → **reuse**. Default **max size 32**, LRU eviction. Details: [[How does the Spring TestContext framework cache the ApplicationContext]]. Corrupt or mutated container: [[What is DirtiesContext]].

`@SpringBootTest` is **Boot** on top of this framework (`SpringBootContextLoader`, `@SpringBootConfiguration` search). It is not a TestContext class.

> [!warning]Forked JVMs never share the cache
> The cache is a **static** variable. Maven Surefire **`forkMode=always`** / **`pertest`** (or any new JVM per class) **drops** it. A one-line `@ActiveProfiles` / `@TestPropertySource` / extra `@MockitoBean` difference is a **new** key and a **second** refresh in the **same** process.

> [!tip] Interview answer
> **TestContext is Spring’s test-framework-agnostic engine: `TestContextManager` plus listeners and a `SmartContextLoader`.** It loads and **caches** an `ApplicationContext` so many test classes can share one refresh. JUnit 5 talks to it through `SpringExtension`, JUnit 4 through `SpringRunner`. `@ContextConfiguration` (or Boot’s `@SpringBootTest`) is how you describe the context, not how the engine itself is named.
