<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS

# What is the `@TestPropertySource` annotation?

> [!abstract] Short answer
> **`@TestPropertySource`** (Spring Framework 4.1+) on a **test class** adds test **`PropertySources`** to the `Environment` of the TestContext `ApplicationContext`: **resource `locations`** and/or **inlined `properties`**. Those values **override** OS environment, JVM system properties, and application `@PropertySource` entries. They do **not** activate bean-definition profiles — that is [[What is the ActiveProfiles annotation]].

## Locations, inlined pairs, defaults

Use it with [[What is the ContextConfiguration annotation]] (any `SmartContextLoader`; not the old `ContextLoader` SPI). `value` aliases `locations`. A plain path is **classpath-relative to the test package**; a leading `/` is an **absolute classpath** resource. As of Framework **6.1**: location **patterns** (`classpath*:/config/*.properties`), custom **`PropertySourceFactory`** (YAML/JSON, …), **text blocks** for inlined pairs, and a resource **`encoding`**.

Empty `@TestPropertySource` on `com.example.MyTest` looks for **`classpath:com/example/MyTest.properties`**. If that file is missing → **`IllegalStateException`**.

```java
@ContextConfiguration
@TestPropertySource(
	locations = "/test.properties",
	properties = {"timezone = GMT", "port = 4242"}
)
class MyIntegrationTests {
}
```

**Listing 1.** File plus inlined pairs. Syntax is Java properties: `key=value`, `key:value`, or `key value`. Repeatable: later `@TestPropertySource` declarations override earlier ones; **directly present** annotations beat **meta**-annotations.

**Precedence (high → low):** [[What is DynamicPropertySource]] → **inlined `properties`** → **location files** → system / env / app `@PropertySource`. `inheritLocations` and `inheritProperties` default **`true`** (subclass **appends**; later names shadow earlier). `false` **replaces** the inherited list. Nested tests inherit from enclosing classes by default.

```d2
direction: down
ann: "@TestPropertySource" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
env: "Environment PropertySources" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
ctx: "test ApplicationContext" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

ann -> env
env -> ctx
```

**Fig. 1.** Test property sources are `Environment` entries, not a second `ApplicationContext`. Cache key includes descriptors and inlined strings — [[How does the Spring TestContext framework cache the ApplicationContext]].

> [!warning]Inlined strings are cache keys
> `"port = 4242"` and `"port=4242"` are **different** context-cache keys. Use one spacing style (docs recommend `key = value`) and do not mix text blocks with arrays for the same suite if you want cache hits. A location **pattern** vs an explicit file list is also a different key even when they resolve to the same files.

> [!warning]Empty annotation is not a no-op
> `@TestPropertySource` with **no** `locations` or `properties` still requires the **default** `MyTest.properties` next to the test class. Missing file fails startup. It still does not turn on a `test` **profile**.

> [!tip] Interview answer
> **`@TestPropertySource` injects a high-precedence `PropertySource` into the test `Environment` — files, inlined keys, or both.** It overrides system and application properties; `@DynamicPropertySource` still sits above it. It is not `@ActiveProfiles`. Empty use means “load `FullyQualifiedTest.properties` or fail.”
