<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Annotations #SRS

# What is @SpringBootApplication?

> [!abstract] Short answer
> **`@SpringBootApplication`** is Boot’s **composed** entry annotation: **`@SpringBootConfiguration` + `@EnableAutoConfiguration` + `@ComponentScan`**. Put it on the **primary** class (usually with `main`). It registers extra `@Bean`s, **opts in** to auto-configuration, and **scans that class’s package** (and below). It is **not** a fourth Spring container and **not** “`@Configuration` plus JPA.”

## A meta-annotation, not a runtime engine

Official javadoc: equivalent to those three. `@SpringBootConfiguration` **is** `@Configuration` specialized so tests can find “the” application config — **one** per app. `@EnableAutoConfiguration` imports **`AutoConfigurationImportSelector`** ([[What is the EnableAutoConfiguration annotation]]). `@ComponentScan` defaults to the **annotated class’s package** ([[Why should the SpringBootApplication class sit in the root package]]). That package is also the default **auto-configuration package** (`@Entity` scan, Spring Data, and so on).

```java
package com.example.myapplication;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MyApplication {

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}
}
```

**Listing 1.** Usual form. The annotation **aliases** `exclude` / `excludeName` (auto-config) and scan attributes (`scanBasePackages`, …). Built-in scan **exclude filters**: **`TypeExcludeFilter`** (test-only types) and **`AutoConfigurationExcludeFilter`** (classes already listed as auto-config).

```java
@SpringBootConfiguration(proxyBeanMethods = false)
@EnableAutoConfiguration
@Import({ SomeConfiguration.class, AnotherConfiguration.class })
public class MyApplication {

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}
}
```

**Listing 2.** Official split: none of the three features is mandatory. Without `@ComponentScan`, `@Component` and `@ConfigurationProperties` types are **not** detected. Auto-config classes still come from **`.imports` files**, not from this scan ([[How does Spring Boot find auto-configuration classes]], [[How do you disable a specific auto-configuration class]]).

```d2
direction: down
sba: "@SpringBootApplication" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
cfg: "@SpringBootConfiguration" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
eac: "@EnableAutoConfiguration" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
scan: "@ComponentScan" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}

sba -> cfg
sba -> eac
sba -> scan
```

**Fig. 1.** Composition. Auto-config classes come from **`.imports` files**, not from this scan ([[How does Spring Boot find auto-configuration classes]]). Conditions still decide which beans are created ([[How do ConditionalOn annotations drive auto-configuration]]). `SpringApplication.run` still creates the `ApplicationContext` ([[What is the SpringApplication class]]).

> [!warning] Interview shorthand drops `@SpringBootConfiguration`
> “`@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`” is close but skips Boot’s configuration type (test detection, **single** `@SpringBootConfiguration`). A JDBC jar on the classpath does **not** auto-configure JPA.

> [!warning] Nested package = incomplete scan
> `…web.MyApplication` only scans `…web`. Sibling `…service` packages are missed unless you set `scanBasePackages` or move `main` up. The **default package** makes scan read **every jar**. A raw `@ComponentScan` on the same class does **not** automatically keep Boot’s `TypeExcludeFilter`. Two `@SpringBootConfiguration` types in one app fight test (and “the” application) detection.

> [!tip] Interview answer
> @SpringBootApplication is SpringBootConfiguration plus EnableAutoConfiguration plus ComponentScan. I put it on main in the root package. Auto-config still only creates beans whose conditions match. I can split the three annotations if I do not want a scan.
