<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Spring/Core/IoC/Configuration #SRS

# What is the difference between Spring Boot auto configuration and plain Spring context?

> [!abstract] Short answer
> A **plain Spring context** only gets beans you **register**: `@Configuration` / `@Bean`, `@ComponentScan`, or XML. **Auto-configuration** is still that same `ApplicationContext`, plus Boot **importing** extra `@Configuration` classes discovered from **`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`**, each gated by **`@ConditionalOn*`**. It is **not** a second container. Boot 3 dropped the `EnableAutoConfiguration` key in `spring.factories`.

## Same `ApplicationContext`, extra imports

Framework: `ApplicationContext` reads **your** metadata and creates beans ([[How does a Spring IoC container differ from a web container or EJB container]]). Nothing on the classpath becomes a bean unless you scan it, `@Import` it, or list it in XML.

```java
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
```

**Listing 1.** Plain context: `AppConfig` (and what it imports/scans) is the whole story. Tomcat, DataSource, Jackson appear **only** if you declare them.

Boot’s `@EnableAutoConfiguration` (usually via `@SpringBootApplication`) runs `AutoConfigurationImportSelector`. It loads class names from **`AutoConfiguration.imports`**, filters them, then registers those classes as configuration. Conditions (`@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`, …) decide **whether** each `@Bean` method runs. User configuration is processed **first**; auto-config **backs off** when you already defined the bean ([[How does Spring Boot auto-configuration decide which beans to create]], [[How does Spring Boot find auto-configuration classes]]).

```text
META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
```

**Listing 2.** One fully-qualified class name per line (starters ship their own files). Debug with Boot’s **`debug`** property / `/actuator/conditions` ([[How can you debug which auto-configuration classes applied]]). Disable a class with `exclude` / `spring.autoconfigure.exclude` — that does **not** remove the jar.

```d2
direction: down
plain: "Plain context\nonly your @Configuration" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
boot: "@EnableAutoConfiguration\n+ .imports list" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
same: "One ApplicationContext\nbeans from both" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

plain -> same
boot -> same
```

**Fig. 1.** Starters ≠ auto-config: a starter is a **dependency BOM**; auto-config is **conditional `@Configuration`**. You can run Framework **without** `@EnableAutoConfiguration`. A Boot app **is** a Spring context with that import step ([[What is the difference between Spring Boot and the core Spring Framework]], [[What is the EnableAutoConfiguration annotation]]).

> [!warning] Auto-config is not “Spring without a context”
> Dump that only recites `@Conditional` + the `.imports` path misses the contrast: **plain** = explicit registration; **auto-config** = **conditional imports into the same context**. `@ConditionalOnMissingBean` only sees beans **already registered**.

> [!warning] Do not look in `spring.factories` on Boot 3+
> Boot **3** removed `EnableAutoConfiguration` from `spring.factories`. The `.imports` resource is the discovery file. `spring.factories` still exists for other keys; it is **not** how auto-config is found.

> [!tip] Interview answer
> A plain Spring context only contains what I register or scan. Boot auto-configuration imports extra configuration classes from AutoConfiguration.imports if the conditions match. It is the same ApplicationContext. I can replace a default bean with my own because of ConditionalOnMissingBean, or exclude a class entirely.
