<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Framework/Testing #Java/Annotations #SRS

# What is the `@TestConfiguration` annotation?

> [!abstract] Short answer
> **`@TestConfiguration`** (Spring Boot 1.4+, `org.springframework.boot.test.context`) is **`@Configuration` plus `@TestComponent`**. It defines **test-only beans**. Unlike a nested **`@Configuration`**, a nested **`@TestConfiguration` is used in addition to** the application’s primary `@SpringBootConfiguration` / `@SpringBootApplication`. It does **not** stop Boot from auto-detecting that primary class.

## Nested versus top-level

Boot’s `@*Test` annotations search **up the package** for `@SpringBootApplication` / `@SpringBootConfiguration` when you do not set `@ContextConfiguration(classes=…)`. Customizing that primary context:

* **Nested `@TestConfiguration`** — **additive**. Registered for **that test class** (and its context cache key).
* **Nested `@Configuration`** — used **instead of** the application’s primary configuration (Framework default-class detection also looks at **static nested** `@Configuration` types).
* **Top-level `@TestConfiguration`** — **not** picked up by component scanning (`@TestComponent` + Boot’s `TypeExcludeFilter`). **`@Import` it** (or list it on `@SpringBootTest` / `@ContextConfiguration`) where you need it.

```java
@SpringBootTest
class OrderServiceTests {

	@TestConfiguration
	static class ExtraBeans {

		@Bean
		Clock fixedClock() {
			return Clock.fixed(Instant.EPOCH, ZoneOffset.UTC);
		}
	}
}
```

**Listing 1.** Conceptual nested additive config. `proxyBeanMethods` defaults to **`true`** (CGLIB `@Configuration`); Boot samples often set **`proxyBeanMethods = false`**.

```java
@SpringBootTest
@Import(MyTestsConfiguration.class)
class MyTests {}

@TestConfiguration
class MyTestsConfiguration {

	@Bean
	Clock fixedClock() {
		return Clock.fixed(Instant.EPOCH, ZoneOffset.UTC);
	}
}
```

**Listing 2.** Conceptual top-level class: scan will **not** install it until `@Import` (or an explicit `classes` list). If you used `@Configuration` in `src/test/java` without `@TestConfiguration`, a `@SpringBootApplication` scan **can** pick it up for **every** test.

Imported `@TestConfiguration` is processed **earlier** than an inner-class `@TestConfiguration`, and earlier than configuration found by **component scanning** — relevant if you rely on **bean overriding**. Direct `@ComponentScan` (not via `@SpringBootApplication`) must register **`TypeExcludeFilter`** or test config leaks again.

This is **Boot**, not a TestContext annotation. Framework loading is still [[What is the ContextConfiguration annotation]] and [[What is the Spring TestContext Framework]]. Extra beans change the cache key — [[How does the Spring TestContext framework cache the ApplicationContext]].

```d2
direction: down
primary: "@SpringBootApplication\n(auto-detected)" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
nested: "nested @TestConfiguration\n(additive)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
nestedCfg: "nested @Configuration\n(replaces primary)" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}

primary -> nested
```

**Fig. 1.** `@TestConfiguration` keeps the Boot primary class in play. Nested `@Configuration` does not.

> [!warning]Nested Configuration replaces the primary
> A static nested **`@Configuration`** on a `@SpringBootTest` is **not** a small extra bean class. Boot uses it **instead of** `@SpringBootApplication`. Use **`@TestConfiguration`** when you mean “add beans.”

> [!warning]Top-level needs Import
> A top-level `@TestConfiguration` is **excluded from scanning on purpose**. Forgetting `@Import` means the test beans **never load**. Using plain `@Configuration` under `src/test/java` is the opposite bug: those beans can appear in **unrelated** tests.

> [!tip] Interview answer
> **`@TestConfiguration` is Boot’s test-only `@Configuration` that still lets `@SpringBootTest` find the main application class.** Nested, it **adds** beans; nested `@Configuration` **replaces** the primary. On a top-level type it is not component-scanned — `@Import` it. That is how you keep test clocks and stubs out of production scan.
