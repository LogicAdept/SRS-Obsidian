<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Testing/Testcontainers #Java/Annotations #SRS

# What is `@DynamicPropertySource`?

> [!abstract] Short answer
> **`@DynamicPropertySource`** (Spring Framework **5.2.5+**) marks a **`static`** method on an integration test that takes **`DynamicPropertyRegistry`** and **`registry.add(name, Supplier)`**. The supplier runs **when the property is resolved**, so values that exist only at runtime (a Testcontainers **mapped port**, an external process) can enter the test `Environment`. Precedence is **above** [[What is the TestPropertySource annotation]].

## Why not a properties file

`@TestPropertySource` is **class-level** files and literal strings. It cannot read a Docker-mapped port assigned when the container starts. Spring’s TestContext chapter designed dynamic sources for **Testcontainers**, but any resource whose lifecycle is **outside** the `ApplicationContext` is in scope. Framework **6.2** also has **`DynamicPropertyRegistrar`** beans **inside** the context for values sourced from other beans (`accept(registry)` runs before singleton pre-instantiation; touching other beans **eagerly** initializes them).

```java
@SpringJUnitConfig(/* ... */)
@Testcontainers
class ExampleIntegrationTests {

	@Container
	static GenericContainer<?> redis =
			new GenericContainer<>("redis:5.0.3-alpine").withExposedPorts(6379);

	@DynamicPropertySource
	static void redisProperties(DynamicPropertyRegistry registry) {
		registry.add("redis.host", redis::getHost);
		registry.add("redis.port", redis::getFirstMappedPort);
	}
}
```

**Listing 1.** Conceptual Spring 6.2 Testcontainers example: method references as suppliers. Beans then use `@Value("${redis.port}")` or `Environment`.

The method **must be `static`** and take **exactly** `DynamicPropertyRegistry`. Inheritance from superclasses, interfaces, and enclosing classes works like other TestContext annotations. Engine: [[What is the Spring TestContext Framework]].

```d2
direction: down
ext: "container / external resource" {
  width: 260
  height: 45
  style.fill: "#fff3e0"
}
ann: "@DynamicPropertySource\nstatic method" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
env: "Environment (highest test PS)" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}

ext -> ann
ann -> env
```

**Fig. 1.** `add` stores a **Supplier**, not a snapshot string, until something resolves the key.

**Precedence:** dynamic → `@TestPropertySource` (inlined then files) → OS env / JVM system / `@PropertySource`. Dynamic entries participate in the context cache (customizers) — [[How does the Spring TestContext framework cache the ApplicationContext]].

> [!warning]Method must be static
> An instance method will not register. Kotlin needs **`@JvmStatic`** on a `companion object` method. `@TestPropertySource` still cannot see a random mapped port: put the **supplier** here, not a hardcoded URL in a `.properties` file.

> [!warning]Base class plus changing ports
> If a **base class** declares `@DynamicPropertySource` and **subclasses** get **different** dynamic values, reuse of the cached context is wrong. Annotate the base with [[What is DirtiesContext]] so each subclass refreshes. A `DynamicPropertyRegistrar` `@Bean` eagerly inits any beans it touches.

> [!tip] Interview answer
> **`@DynamicPropertySource` is a static test method that pushes lazy `Supplier` values into the `Environment`.** It sits above `@TestPropertySource` and is the Testcontainers hook for host and mapped port. The method must be static and take `DynamicPropertyRegistry`. If subclasses change those values, dirty the context.
