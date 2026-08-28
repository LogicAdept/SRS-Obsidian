<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Testing/JUnit #Java/Annotations #SRS

# What is `SpringExtension`?

> [!abstract] Short answer
> **`SpringExtension`** (Spring Framework 5.0+, `org.springframework.test.context.junit.jupiter`) is the **JUnit Jupiter** adapter for the **TestContext Framework**. `@ExtendWith(SpringExtension.class)` — or a composed annotation that includes it — creates a **`TestContextManager`**, loads the test `ApplicationContext`, injects the test instance, and runs transactional / `@DirtiesContext` callbacks.

## What Jupiter callbacks it implements

It is a JUnit 5 **`Extension`**: `BeforeAllCallback`, `AfterAllCallback`, `TestInstancePostProcessor`, `BeforeEachCallback`, `AfterEachCallback`, `BeforeTestExecutionCallback`, `AfterTestExecutionCallback`, and **`ParameterResolver`**. Each hook **delegates** to `TestContextManager` (`beforeTestClass`, `prepareTestInstance`, `beforeTestMethod`, …).

Register it explicitly, or use Framework composed annotations **`@SpringJUnitConfig`** / **`@SpringJUnitWebConfig`** (they meta-annotate `@ExtendWith(SpringExtension.class)` plus `@ContextConfiguration`, and the web variant adds `@WebAppConfiguration`). Spring Boot 3.5’s **`@SpringBootTest`** also declares `@ExtendWith(SpringExtension.class)` — you do **not** add the extension by hand on a Boot test.

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfig.class)
class SimpleTests {

	@Test
	void testMethod() {
	}
}
```

**Listing 1.** Support-classes example. Equivalent: `@SpringJUnitConfig(TestConfig.class)`.

`SpringExtension` is **not** [[What is SpringRunner]]. `SpringRunner` is JUnit **4** (`@RunWith`). Jupiter uses `@ExtendWith`. Core engine: [[What is the Spring TestContext Framework]]. Context: [[What is the ContextConfiguration annotation]].

```d2
direction: down
jup: "JUnit Jupiter lifecycle" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
ext: "SpringExtension" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
tcm: "TestContextManager" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
di: "prepareTestInstance\n+ ParameterResolver" {
  width: 240
  height: 50
  style.fill: "#fce4ec"
}

jup -> ext
ext -> tcm
tcm -> di
```

**Fig. 1.** Jupiter talks only to the extension. The extension talks only to TestContext.

## Parameter injection (Jupiter-only)

As a `ParameterResolver`, it can inject `ApplicationContext` (or a subtype) and parameters annotated / meta-annotated with `@Autowired`, `@Qualifier`, or `@Value` into **constructors**, `@Test` / `@RepeatedTest` / `@ParameterizedTest`, and lifecycle methods (`@BeforeEach`, `@BeforeTransaction`, …). That is **beyond** JUnit 4 field injection.

If the **constructor** is `@Autowired`, or `@TestConstructor(autowireMode = ALL)`, or the global `spring.test.constructor.autowire.mode=all` property is set, Spring resolves **every** constructor argument — **no other** Jupiter `ParameterResolver` runs for that constructor.

`postProcessTestInstance` also **rejects `@Autowired` on test methods and lifecycle methods** (use a **parameter** `@Autowired OrderService svc` instead of annotating the method).

> [!warning]RunWith SpringRunner is the wrong Jupiter API
> `@RunWith(SpringRunner.class)` is JUnit **4**. A JUnit 5 test needs `@ExtendWith(SpringExtension.class)` or a meta-annotation. A Mockito-only unit test that never loads a Spring context should **not** register `SpringExtension`. Field `@Autowired` stays **unset** if no TestContext manager runs (`DependencyInjectionTestExecutionListener` never fires).

> [!warning]PER_CLASS plus DirtiesContext plus constructor injection
> `@TestInstance(PER_CLASS)` caches the test instance. If `@DirtiesContext` closes the context between methods, constructor-injected fields still point at the **old** beans. Use **field or setter** injection so TestContext can re-inject.

> [!tip] Interview answer
> **`SpringExtension` is how JUnit 5 joins TestContext.** Put `@ExtendWith(SpringExtension.class)` or `@SpringJUnitConfig` (Boot: `@SpringBootTest` already includes the extension). It prepares the test instance, can inject method and constructor parameters, and is not `SpringRunner`. Skip it when the test is plain Mockito with no Spring context.
