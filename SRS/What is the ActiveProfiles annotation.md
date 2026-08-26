<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS

# What is the ActiveProfiles annotation?

> [!abstract] Short answer
> **`@ActiveProfiles`** (`org.springframework.test.context`, since **3.1**) is a **class-level** TestContext annotation that names which **bean-definition profiles** are active when the test **`ApplicationContext` loads**. Example: **`@ActiveProfiles("dev")`** or **`{"dev", "integration"}`**. Default **`inheritProfiles = true`**: subclass profiles are **appended** to the superclass list. **`inheritProfiles = false`** **replaces** them. Custom **`resolver`**: **`ActiveProfilesResolver`**. It is **not** **`@TestPropertySource`**.

## Profiles for this context, not a JVM flag

When this annotation is **present**, the TestContext Framework **ignores `spring.profiles.active`** (system property or env var). Need that property to win? Implement **`ActiveProfilesResolver`** (docs show **`SystemPropertyOverrideActiveProfilesResolver`**) and usually **`inheritProfiles = false`**. Default resolver is **`DefaultActiveProfilesResolver`**. Nested tests inherit from the enclosing class unless **`@NestedTestConfiguration`** says otherwise.

`@Profile("dev")` beans load only if **`dev` is in that active set**. The profile list is part of the **`MergedContextConfiguration` cache key** — a class with `@ActiveProfiles("test")` does **not** share a context with one that omits it. Contrast: [[What is the difference between ActiveProfiles and TestPropertySource]]. Properties without switching profiles: [[What is the TestPropertySource annotation]]. Cache: [[How does the Spring TestContext framework cache the ApplicationContext]]. Framework: [[What is the Spring TestContext Framework]]. Loader: [[What is the ContextConfiguration annotation]].

```java
@ContextConfiguration
@ActiveProfiles("dev")
class DeveloperTests { }
```

**Listing 1.** Conceptual Framework **7**. One profile.

```java
@ActiveProfiles("base")
@ContextConfiguration
class BaseTest { }

@ActiveProfiles("extended")
@ContextConfiguration
class ExtendedTest extends BaseTest { }
```

**Listing 2.** Conceptual JavaDoc: **`ExtendedTest` gets `base` and `extended`** because inherit defaults **true**.

```d2
direction: down
ann: "@ActiveProfiles(\"test\")" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
env: "Environment active profiles" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
beans: "@Profile(\"test\") beans" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

ann -> env -> beans
```

**Fig. 1.** `application-test.properties` / `@Profile` beans follow **this** list, not a leftover JVM `-Dspring.profiles.active`.

> [!warning] `@ActiveProfiles` wins over `spring.profiles.active`
> Declaring the annotation **drops** the usual property. A CI `-Dspring.profiles.active=ci` **does nothing** unless you write a **resolver**.

> [!warning] Not `@TestPropertySource`
> Profiles select **which property files and `@Profile` configs** load. **`@TestPropertySource`** adds **keys** (highest test-property precedence) **without** activating a profile name.

> [!warning] Different profiles, different cache slot
> `@ActiveProfiles("test")` on one class and omitted on another → **two** refreshes. That is expected, not a leak.

> [!tip] Interview answer
> **`@ActiveProfiles` sets which Spring profiles the test context starts with.** Subclasses inherit and append by default. It ignores `spring.profiles.active` unless you plug in an `ActiveProfilesResolver`. Use `@TestPropertySource` to override keys, not to switch profiles.
