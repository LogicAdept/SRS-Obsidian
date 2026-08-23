<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #SRS

# Which common Spring Boot starters do you know?

> [!abstract] Short answer
> **Starters are curated dependency bundles** under **`org.springframework.boot`** named **`spring-boot-starter-*`**. They pull in a **consistent, BOM-managed** set of libraries plus **auto-configuration** for a capability — you declare the starter, not a long list of versions. Interview staples: **`starter`**, **`starter-web`**, **`starter-data-jpa`**, **`starter-jdbc`**, **`starter-security`**, **`starter-validation`**, **`starter-aspectj`**, **`starter-test`**.

## What a starter is

Spring Boot's build-systems guide defines starters as **convenient dependency descriptors** — a one-stop dependency that gets a feature running with **supported transitive versions** from **`spring-boot-dependencies`**.

Official starters use the prefix **`spring-boot-starter-`**. Third-party starters should **not** use that prefix (reserved for Spring Boot artifacts).

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

**Listing 1.** No version tag — the Boot BOM supplies it ([[Why can you omit library versions in a Spring Boot project]]).

## Common application starters

| Starter | Brings in (summary) |
|---|---|
| **`spring-boot-starter`** | Core Boot: **auto-configuration**, **logging** (Logback), **YAML** support |
| **`spring-boot-starter-web`** | **Spring MVC** REST/web apps + **embedded Tomcat** (default) — [[Which embedded containers are supported by Spring Boot]] |
| **`spring-boot-starter-webflux`** | **Reactive** web stack + **Reactor Netty** (not Tomcat) |
| **`spring-boot-starter-jdbc`** | **JDBC** + **HikariCP** pool (no JPA) |
| **`spring-boot-starter-data-jpa`** | **Spring Data JPA** + **Hibernate** as default JPA provider |
| **`spring-boot-starter-security`** | **Spring Security** filter chain + crypto/password support |
| **`spring-boot-starter-validation`** | **Jakarta Bean Validation** + **Hibernate Validator** |
| **`spring-boot-starter-aspectj`** | **Spring AOP** + **AspectJ** weaving support (modern name; legacy dumps say `starter-aop`) |
| **`spring-boot-starter-test`** | **JUnit Jupiter**, **Mockito**, **AssertJ**, Spring Test, MockMvc helpers |
| **`spring-boot-starter-actuator`** | Production **metrics, health, info** endpoints |

Production starters also exist for **caching**, **batch**, **AMQP/Rabbit**, **Kafka**, **OAuth2**, **GraphQL**, and many data stores — same naming pattern.

```d2
direction: right
pom: "pom.xml\none starter dep" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
bom: "spring-boot-dependencies\n(managed versions)" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
auto: "Auto-configuration\n+ libraries" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}

pom -> bom -> auto
```

**Fig. 1.** A starter is the entry point; the BOM and auto-config do the wiring.

> [!warning] Pick the starter that matches the stack
> **`starter-web`** and **`starter-webflux`** are different runtimes — do not assume both unless you intentionally run hybrid setups. **`starter-jdbc`** alone does not give JPA; use **`starter-data-jpa`** when you want repositories and **`EntityManager`**. **`starter-test`** is **`test` scope** in typical parent POM setups — not for production classpath.

> [!tip] Interview answer
> Starters are org.springframework.boot dependency bundles with managed versions and auto-config. Common ones: starter (core), starter-web for MVC+Tomcat, starter-data-jpa, starter-jdbc, starter-security, starter-validation, starter-aspectj for AOP, starter-test for JUnit/Mockito. Name pattern is spring-boot-starter-*; third parties must not use that prefix.
