<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #Java/Spring/Core/IoC/Configuration #SRS

# What is a Spring profile?

> [!abstract] Short answer
> A **profile** is a **named grouping** on the **`Environment`**: beans and config data that apply only when that name is **active**. Activate with **`spring.profiles.active`** (file / env / CLI). **`@Profile`** **gates registration** of a `@Component` / `@Configuration` / `@Bean`. Boot also loads **`application-{profile}.properties`** / YAML from the same locations as `application.properties`. It does **not** mean “unannotated beans are the default profile.”

## One Environment switch, two consumers

Profiles are a **Framework** `Environment` feature (Boot uses the same names). If **no** profile is activated, the fallback name is **`default`** (`spring.profiles.default`; `none` turns that off) ([[How do you activate a Spring profile]]).

```java
@Configuration(proxyBeanMethods = false)
@Profile("prod")
public class ProdConfigurations {
	// registered only when prod is active
}
```

**Listing 1.** `@Profile` is `@Conditional` (`ProfileCondition` → `Environment.matchesProfiles`). A type **without** `@Profile` is **always** a candidate — that is **not** profile `"default"`. Expressions: `!` / `&` / `|` (parenthesize if you mix `&` and `|`). Array values are **OR** ([[What is the Profile annotation in Spring]]).

```properties
# application.properties — always considered
spring.application.name=demo

# application-prod.properties — overlay when prod is active
spring.datasource.url=jdbc:postgresql:prod
```

**Listing 2.** Profile **files** use basename **`application-{profile}`** (or `myproject-{profile}` if you set `spring.config.name`). They **overlay** the non-profile file from the **same locations**; several actives → **last-wins** ([[How do profile-specific property files work in Spring Boot]], [[What configuration file names does Spring Boot use]]). `spring.profiles.include` **adds** names; `spring.profiles.group.*` expands one name into several.

```d2
direction: down
env: "Environment\nspring.profiles.active" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
beans: "@Profile on @Bean / @Configuration" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
files: "application-{profile}.yaml" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

env -> beans
env -> files
```

**Fig. 1.** Same active set drives **which beans exist** and **which property documents overlay**. CLI `--spring.profiles.active` **replaces** the list from `application.properties` ([[What is Spring Boot property source precedence]]). Tests: `@ActiveProfiles`.

> [!warning] `@Profile` does not turn a profile on
> Putting `@Profile("dev")` on a class does **not** activate `dev`. If that bean is required and `dev` is off, injection fails (`NoSuchBeanDefinitionException`). `@Profile` on **overloaded** `@Bean` methods cannot pick one overload.

> [!warning] `application-dev.properties` is not loaded just because the file exists
> The `{profile}` token must match an **active** (or default) profile. `dev` / `qa` / `prod` are **conventions**, not built-in Boot environments. Do not confuse profiles with **Maven** profiles.

> [!tip] Interview answer
> A Spring profile is a named Environment flag. I activate it with spring.profiles.active. Then @Profile beans register and application-prod properties overlay the base file. Beans with no @Profile are always there; default is only the fallback profile name when nothing is active.
