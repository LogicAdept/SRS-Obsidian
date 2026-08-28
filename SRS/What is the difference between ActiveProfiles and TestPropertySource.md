<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS

# What is the difference between `@ActiveProfiles` and `@TestPropertySource`?

> [!abstract] Short answer
> **`@ActiveProfiles`** (Framework 3.1+) sets **which bean-definition profiles** are active when TestContext **loads** the `ApplicationContext` (`@Profile("dev")` config classes, XML `<beans profile="dev">`). **`@TestPropertySource`** (4.1+) adds **`Environment` property keys** (files and/or inlined pairs) with high precedence. One chooses **which beans exist**; the other **overrides configuration values**. You often need **both**.

## Two knobs on the same test

| | `@ActiveProfiles` | `@TestPropertySource` |
| --- | --- | --- |
| **Question** | Which `@Profile` / XML profile slices load? | Which `Environment` keys win? |
| **Typical value** | `"test"`, `"dev"` | `spring.datasource.url`, `timezone = GMT` |
| **Does not** | Insert arbitrary property keys | Activate a named profile by itself |
| **Inheritance** | `inheritProfiles` default **true** | `inheritLocations` / `inheritProperties` default **true** |

`@ActiveProfiles("dev")` loads the `dev` `DataSource` `@Bean` and **skips** `production` / may skip `default` (the `default` profile applies only when **no** other profile is active). `@TestPropertySource(properties = "timezone = GMT")` does **not** turn on `dev`; it only puts `timezone` in the `Environment`.

```java
@SpringJUnitConfig({
		TransferServiceConfig.class,
		StandaloneDataConfig.class,
		JndiDataConfig.class,
		DefaultDataConfig.class})
@ActiveProfiles("dev")
@TestPropertySource(properties = "logging.level.com.bank = DEBUG")
class TransferServiceTest {
}
```

**Listing 1.** Conceptual: profile selects `StandaloneDataConfig`; the inlined property only tweaks logging. Neither replaces a bean override (`@MockitoBean`) or [[What is DirtiesContext]].

When `@ActiveProfiles` is **present**, TestContext **does not** read **`spring.profiles.active`** from a JVM system property or OS environment variable. To let that property win, register a custom **`ActiveProfilesResolver`**. `@TestPropertySource` **does** override system properties for **ordinary keys**, but that is still not profile activation.

```d2
direction: right
profiles: "@ActiveProfiles\nwhich @Profile beans" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
props: "@TestPropertySource\nEnvironment keys" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
dyn: "@DynamicPropertySource\nlazy runtime values" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}

profiles -> props: "often together"
props -> dyn: "dyn wins keys"
```

**Fig. 1.** Profiles and property sources are independent cache-key parts (`activeProfiles` vs property descriptors). Runtime ports: [[What is DynamicPropertySource]]. Files/inlined: [[What is the TestPropertySource annotation]]. Profiles: [[What is the ActiveProfiles annotation]]. Cache: [[How does the Spring TestContext framework cache the ApplicationContext]].

> [!warning]ActiveProfiles ignores spring.profiles.active
> Declaring `@ActiveProfiles("test")` **pins** the test to `test` even if the CI JVM sets `spring.profiles.active=prod`. That is Framework TestContext behavior, not a bug. Use an `ActiveProfilesResolver` if you want the system property to override.

> [!warning]A property is not a profile
> `@TestPropertySource(properties = "spring.profiles.active = test")` is **not** the documented way to choose bean profiles for TestContext. Set **`@ActiveProfiles`**. A different profile **or** a different inlined string is a **new** cached context.

> [!tip] Interview answer
> **`@ActiveProfiles` chooses bean-definition profiles; `@TestPropertySource` injects `Environment` keys.** Use a `test` profile for test-only `@Configuration` / XML slices, and `@TestPropertySource` for a few overridden keys. They stack. Dynamic properties sit above test property sources. `@ActiveProfiles` on the class ignores `spring.profiles.active` unless you install a custom resolver.
