<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Spring/Boot/Properties #SRS

# What is the Spring Environment?

> [!abstract] Short answer
> `Environment` (since **3.1**, `org.springframework.core.env`) is the container’s model of the **runtime**: **profiles** (which bean-definition groups are active) and **properties** (a searchable chain of `PropertySource`s). It extends `PropertyResolver` (`containsProperty`, `getProperty`, placeholder resolution). `ApplicationContext.getEnvironment()` returns a `ConfigurableEnvironment` you can mutate **before** `refresh()`. It is **not** SpEL.

## Two jobs: profiles and property sources

**Profiles.** A profile is a named group of definitions registered only while it is active (`@Profile`, XML `profile` on `<beans>`). The `Environment` answers which profiles are **explicitly** active (`getActiveProfiles`) and which apply as **defaults** when none were set (`getDefaultProfiles`, name `"default"`, `spring.profiles.default`). `matchesProfiles("p1 & p2")` (since **5.3.28**) tests expressions against the active set, or against defaults if nothing was activated ([[What is the Profile annotation in Spring]], [[How do you activate a Spring profile]]). `acceptsProfiles(String…)` is **deprecated since 5.1**.

**Properties.** `StandardEnvironment` ships two sources: JVM **system properties** (higher precedence) then OS **environment variables**. Values are **not** merged — an earlier source **replaces** the key. `StandardServletEnvironment` adds servlet config, servlet context parameters, and JNDI when available (those sit **above** JVM properties).

```java
ApplicationContext ctx = new GenericApplicationContext();
Environment env = ctx.getEnvironment();
boolean present = env.containsProperty("my-property");
String value = env.getProperty("my-property");
```

**Listing 1.** Conceptual. `true` if `my-property` exists as a system property or OS env var (standalone `StandardEnvironment`).

```java
ConfigurableApplicationContext ctx = new GenericApplicationContext();
ctx.getEnvironment().getPropertySources().addFirst(new MyPropertySource());
ctx.refresh();
```

**Listing 2.** Conceptual. `addFirst` wins on clashes. `@PropertySource` on `@Configuration` is the declarative form ([[What is the PropertySource annotation in Spring]]). Configure sources **before** `refresh()`.

Beans may be `EnvironmentAware` or inject `Environment`. Most code should not: `${…}` in definitions and `@Value("${…}")` go through `PropertySourcesPlaceholderConfigurer`, which is `EnvironmentAware` ([[What is PropertySourcesPlaceholderConfigurer]], [[How does the Value annotation inject properties]]). `#{…}` is SpEL, a different language.

Spring **Boot** uses this same `Environment`. `application.properties` / `application-{profile}.properties`, command line, and extra Boot sources are additional `PropertySource`s with Boot’s override order — not a second property API.

```d2
direction: down
env: "Environment" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
prof: "active / default profiles" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
src: "PropertySource chain" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
use: "getProperty / ${…} / @Profile" {
  width: 240
  height: 40
  style.fill: "#f3e5f5"
}

env -> prof
env -> src
prof -> use
src -> use
```

**Fig. 1.** One abstraction: which definitions load, and where key/value lookup walks.

> [!warning] First matching source wins the whole value
> Duplicate keys are not merged. In `StandardEnvironment`, `-Dmy-property` beats an OS env var of the same name. In Boot, command line and `application.properties` sit **above** a typical `@PropertySource` file.

> [!warning] Query `Environment` after it is composed
> `@PropertySource` entries appear only at **refresh**. Boot `logging.*` / `spring.main.*` are read **earlier**. Mutate `ConfigurableEnvironment` before `refresh()`, or use sources Boot loads at bootstrap.

> [!tip] Interview answer
> Environment, since 3.1, is profiles plus a PropertySource chain. Profiles decide which bean definitions register; getProperty walks sources in precedence order, system properties beating OS env in StandardEnvironment. Boot still uses this type — application.properties is just more sources, not a different mechanism.
