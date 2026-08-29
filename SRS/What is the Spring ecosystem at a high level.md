<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS

# What is the Spring ecosystem at a high level?

> [!abstract] Short answer
> **“Spring”** in conversation usually means the **whole family of projects**, not only **`spring-framework`**. The **Spring Framework** is the **foundation**: modular IoC container, AOP, JDBC/TX, Servlet **MVC**, reactive **WebFlux** ([[What is the Spring Framework]]). **Other projects sit on that foundation**, each with its **own repository, issue tracker, and release cadence**. Overview names **Spring Boot**, **Spring Security**, **Spring Data**, **Spring Cloud**, **Spring Batch**, “among others.” Boot is the usual **way to start** a production app; it **assembles** the Framework rather than replacing it ([[What is the difference between Spring Boot and the core Spring Framework]]).

## One word, many artifacts

Framework overview — *What We Mean by “Spring”*: the term can mean the **Framework project** (where it started) or the **portfolio**. This documentation set covers the **core**. You pick **modules** (`spring-context`, `spring-webmvc`, `spring-webflux`, …); you do **not** have to take the entire family.

```d2
direction: down
fw: "Spring Framework\nIoC, AOP, MVC, WebFlux, JDBC" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
boot: "Spring Boot\nstarters, auto-config, embedded server" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
data: "Spring Data / Security /\nCloud / Batch / …" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}

fw -> boot: "Boot uses"
fw -> data: "projects extend"
boot -> data: "starters pull"
```

**Fig. 1.** Portfolio around the container. Cloud and Data are **not** inside `spring-beans`.

Typical layers (interview map, not an official org chart):

| Slice | Role |
| --- | --- |
| **Framework** | DI, lifecycle, web, transactions, test |
| **Boot** | Opinionated runtime: `SpringApplication`, auto-config, Actuator |
| **Data** | Repository model over JPA, JDBC, Mongo, … ([[What is Spring Data JPA]]) |
| **Security** | AuthN/AuthZ for HTTP (and more) |
| **Cloud** | Distributed systems (config, discovery, gateway, …) — separate BOM |
| **Batch / Integration / AMQP / Kafka** | Batch jobs, EIP, messaging |

Web is **two** stacks **in the Framework**: MVC (Servlet) and **WebFlux** ([[What is Spring WebFlux]]). Batch/integration apps may need **no** HTTP server. Spring **integrates selected Jakarta EE specs**; it is **not** a full application server ([[What core ideas underpin the Spring Framework]]).

Versions **do not lock together**: Framework **7.x**, Boot **4.x**, Cloud **2025.x**-style trains are **different** products. Check a Boot release’s Framework baseline.

```java
@SpringBootApplication
public class BillingApplication {
	public static void main(String[] args) {
		SpringApplication.run(BillingApplication.class, args);
	}
}
```

**Listing 1.** Conceptual. One Boot main class still **is** a Framework `ApplicationContext` plus auto-config. Adding `spring-boot-starter-data-jpa` pulls **Data** onto that same context.

> [!warning] “Spring” on a résumé is ambiguous
> Clarify **Framework vs Boot vs Cloud**. A library that only uses `ApplicationContext` is Framework. `SpringApplication.run` is Boot. `@EnableDiscoveryClient` is Cloud.

> [!warning] Do not treat Boot as a second IoC
> Ecosystem projects **register beans** in the **same** container. Auto-config and Cloud starters are extra `@Configuration`, not a competing factory.

> [!tip] Interview answer
> The Spring ecosystem is a family: the Framework is the IoC and web core, Boot packages and auto-configures it, and Data, Security, Cloud, Batch are separate projects on that core with their own releases. When I say Spring I usually mean that family; when I debug DI I mean the Framework container.
