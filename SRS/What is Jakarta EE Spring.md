<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #Java/JavaEE #SRS

# What is Jakarta EE Spring?

> [!abstract] Short answer
> **Jakarta EE** (formerly **Java EE**) is a **set of specifications** for enterprise Java (Servlet, JPA, Bean Validation, JMS, Transactions, CDI, EJB, …), implemented by **compatible application servers**. **Spring** is a **framework/library**: it **does not implement the Jakarta EE platform**. It **integrates selected** specs so POJOs can use Servlet, JPA, JMS, `jakarta.inject`, `jakarta.annotation`, and so on — on a **full EE server**, on **Tomcat/Jetty** (Servlet only), or with **no** Servlet container (WebFlux). Since Framework **6.0** those APIs are **`jakarta.*`**, not **`javax.*`**. They **compose**; they are not two names for one product ([[What is the Spring Framework]], [[How does a Spring IoC container differ from a web container or EJB container]]).

## Spec platform vs Spring modules

Jakarta EE is the **Eclipse-governed** successor to Java EE. **Jakarta EE 9** moved packages from `javax.*` to `jakarta.*` (a source-incompatible rename). Compatible **products** (WildFly, GlassFish, Payara, Open Liberty, …) implement the **platform** (or a profile): EJB container, JTA, JNDI, Servlet, persistence, messaging.

Spring’s overview: **POJOs** plus **non-invasive** services on **Java SE or full/partial Java EE**. It **chooses** specs (Servlet, WebSocket, BV, JPA, JMS, DI/JSR-330, Common Annotations) rather than shipping an EJB container. Tomcat is a **web container**, not a full Jakarta EE product ([[What core ideas underpin the Spring Framework]]).

```d2
EE: "Jakarta EE specs\nServlet, JPA, JMS, EJB, …"
Server: "EE-compatible server\nor Tomcat (Servlet subset)"
Spring: "Spring Framework\nIoC + MVC/WebFlux + tx"
App: "your POJOs"
EE -> Server: implements
Spring -> EE: "uses selected APIs"
Spring -> App: manages beans
Server -> Spring: hosts (optional)
```

**Fig. 1.** Spring **calls** Jakarta APIs; it is **not** a certified platform implementation.

| | Jakarta EE | Spring |
| --- | --- | --- |
| **What it is** | Specifications + TCK + compatible servers | Modular libraries (`spring-context`, `spring-webmvc`, …) |
| **DI** | CDI (`jakarta.inject` / CDI beans) | `ApplicationContext` / `@Autowired` (also understands `@Inject`) |
| **Web** | Servlet spec (plus JAX-RS, etc. on a server) | Spring MVC or WebFlux **on** Servlet or Netty |
| **Tx** | JTA / CMT on an EE server | Spring `@Transactional` (local JDBC/JPA **or** JTA) |
| **EJB** | Session / MDB in an **EJB container** | Not required; optional JNDI lookup of existing EJBs |

```java
import jakarta.servlet.http.HttpServletRequest;
import jakarta.inject.Inject;
import jakarta.annotation.PostConstruct;
import jakarta.persistence.EntityManager;
```

**Listing 1.** Framework **6+** application code. **5.x** used `javax.*` for the same specs. **7.0** no longer recognizes leftover `javax.annotation` / `javax.inject` ([[What are the main differences between Spring Framework major versions]]).

**Baselines (official wiki):** 5.3 → Java EE **7–8** (`javax`); 6.2 → Jakarta EE **9–10**; 7.x → EE **11** (Servlet **6.1**, JPA **3.2**) with early EE **12**. Boot **embeds** a Servlet container so many apps never install WildFly — they still **depend on** the Servlet API.

> [!warning] “Jakarta EE is only legacy” is false
> Dump slides that end with “Spring won, EE is dead” skip **Jakarta EE 9–12** and Spring’s **own** EE 11 baseline. The breaking change teams hit is **`javax` → `jakarta`**, not “delete EE.” Mixing `javax.servlet` with Spring 6/7 will not compile against current APIs.

> [!tip] Interview answer
> Jakarta EE = **specs** (+ servers that implement them). Spring = **framework** that **uses** a subset of those specs and its own IoC/AOP. You can run Spring **on** an EE server or on Tomcat/Boot. Since 6.0, import **`jakarta.*`**. They nest; one does not replace the other’s contract.
