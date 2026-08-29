<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS

# What is Spring Modulith?

> [!abstract] Short answer
> **Spring Modulith** is an opinionated toolkit for **domain-driven, modular Spring Boot** apps: **packages as application modules**, **ArchUnit-backed `verify()`**, **docs**, **module tests**, and **events** (`@ApplicationModuleListener` + an **event publication registry**). It is **not** Spring Cloud and **not** a way to split a JAR into services. Import **`spring-modulith-bom`** (`org.springframework.modulith`, current docs **2.1.1**).

## Functional modules on one Boot app

Official overview: Boot already opinions **technical** arrangement; Modulith opinions **functional** structure so the app stays changeable. An **application module** has a **provided** API (beans + events), **internals**, and a **required** API (beans, listeners, properties). Default: each **direct sub-package** of the `@SpringBootApplication` package is a module ([[What is @SpringBootApplication]]). Simple module = that package’s **public** types. Sub-packages (e.g. `order.internal`) are **internal** — other modules must not reference them even if types are `public` (the compiler will not save you). Extra API packages: `@NamedInterface` on `package-info.java`. Nested modules (1.3+): `@ApplicationModule` on a nested package.

```java
ApplicationModules.of(Application.class).verify();
```

**Listing 1.** `spring-modulith-core`. Rules: **no cycles**, access **API packages only**, optional `@ApplicationModule(allowedDependencies = "order")`. Violations: `verify()` throws; `detectViolations()` to filter. Open modules (`type = OPEN`) exist for **legacy** moves — official: in a finished modularization they usually mean **weak packaging**.

```java
@ApplicationModuleListener
void on(OrderCompleted event) { /* … */ }
```

**Listing 2.** Preferred inter-module style is **events**, not injecting the other module’s `@Service`. The annotation is the shortcut for **async + `@TransactionalEventListener` + `REQUIRES_NEW`**. The **registry** writes a log row **in the business transaction** per transactional listener and marks it complete on success; set `spring.modulith.events.republish-outstanding-events-on-restart` to replay unfinished publications. Tests: `@ApplicationModuleTest` + `PublishedEvents` ([[What is Spring Boot]]).

```d2
direction: down
app: "@SpringBootApplication\nexample" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
order: "example.order\nAPI" {
  width: 180
  height: 45
  style.fill: "#e8f5e9"
}
inv: "example.inventory\nAPI" {
  width: 180
  height: 45
  style.fill: "#fff3e0"
}
hid: "order.internal\nforbidden from inventory" {
  width: 240
  height: 45
  style.fill: "#fce4ec"
}

app -> order
app -> inv
order -> hid
```

**Fig. 1.** One process, many modules ([[What is Spring Boot]]). Document the arrangement; observe it with the insight/actuator artifacts. jMolecules ArchUnit rules run **if that library is on the classpath**.

> [!warning] Not microservices and not JPMS
> Modulith does **not** replace Spring Cloud, Kafka topology, or OSGi. “Extract later” is not the product pitch — official goal is a **modular monolith you can keep changing**. Java `public` on an internal type still compiles; **`verify()`** is the gate.

> [!warning] Sync `publishEvent` keeps one transaction
> Default publication is **synchronous**; listeners widen the TX. Jumping to `@Async` **without** the registry can **drop** the event if the listener never runs. Use `@ApplicationModuleListener` (or equivalent) when the work is secondary.

> [!tip] Interview answer
> Modulith is how I structure a Spring Boot monolith into package modules. Direct sub-packages of the main class are modules. I call ApplicationModules.verify so internals and cycles fail the build. Modules talk with application events and ApplicationModuleListener, not with each other’s internals. It is not Spring Cloud.
