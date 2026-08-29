<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS

# What problems does the Spring Framework address?

> [!abstract] Short answer
> It exists so you can write **enterprise Java without owning the infrastructure**. Overview: Spring started in **2003** against **early J2EE complexity**; it still covers **long-lived** apps stuck on a JDK/server you cannot upgrade **and** **single-jar / cloud / batch** apps with **no** application server. The Framework supplies a **modular** platform — **IoC/DI** so types do not `new` or look up helpers, **AOP** so transactions and similar concerns are not copied into every class, **foundational** messaging / persistence / web (**MVC** and **WebFlux**) — while **integrating selected Jakarta EE specs** instead of implementing the whole platform ([[What is the Spring Framework]], [[What core ideas underpin the Spring Framework]]).

## Coupling, invasiveness, and “one server for everything”

Problems the design philosophy and history call out (or imply):

| Pain | What Spring does |
| --- | --- |
| Helpers constructed inside the class; hard to test | **DI**: declare constructor/setters; container injects ([[How would you explain dependency injection]]) |
| Domain methods full of tx / JMS / JMX APIs | **Non-invasive** services via AOP / interceptors — POJOs stay POJOs |
| All-or-nothing EE server | **Modules**: take `spring-context` without MVC; switch persistence **in config** |
| Must deploy a WAR to a heavy app server | Run **in** a server **or** **embed** one (typical **Boot**) **or** skip Servlet (**WebFlux** / Netty, batch) |
| “Spring vs Jakarta EE” | **Complementary**: Servlet, JPA, JMS, Bean Validation, JSR-330, … — not the EE **platform spec** |
| One architecture forever | **Choice at every level**; not opinionated about “the one true way” |

```d2
direction: down
pain: "new helpers / invasive APIs /\nall-or-nothing server" {
  width: 300
  height: 50
  style.fill: "#ffebee"
}
ioc: "IoC container" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
aop: "AOP / modules / selected specs" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
app: "application POJOs" {
  width: 200
  height: 40
  style.fill: "#fff3e0"
}

pain -> ioc
pain -> aop
ioc -> app
aop -> app
```

**Fig. 1.** Infrastructure around ordinary objects — the IoC container is the runtime ([[What is the Spring inversion of control container]]).

```java
@Service
public class InvoiceService {
	private final InvoiceRepository invoices;
	public InvoiceService(InvoiceRepository invoices) {
		this.invoices = invoices;
	}
}
```

**Listing 1.** Conceptual. The service does not construct JDBC or start a transaction API in the method body; the container and (if used) `@Transactional` do.

Boot addresses the **getting-started / packaging** problem (opinionated auto-config, `java -jar`) on **this same** Foundation ([[What is the difference between Spring Boot and the core Spring Framework]]). The **portfolio** (Data, Security, Cloud, Batch) extends the same idea to persistence, auth, distributed systems ([[What is the Spring ecosystem at a high level]]).

> [!warning] Spring does not “replace Tomcat” or “replace JPA”
> Those are **specs / servers** it **plugs into**. The problem it owns is **how application objects are composed and decorated**, plus portable helpers (JDBC templates, MVC).

> [!warning] It is not a silver bullet for domain modeling
> Fine-grained entities are **usually not** beans. DI does not replace a domain model; it **stops the service layer from being a service locator**.

> [!tip] Interview answer
> Spring was a response to invasive, all-or-nothing J2EE: wire POJOs with an IoC container, apply cross-cutting behavior with AOP, pick modules, and integrate Servlet/JPA/JMS instead of requiring a full EE server. Today it also covers embedded and reactive deployments. Boot is how most people start that stack, not a different problem statement.
