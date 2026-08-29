<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS

# What is the Spring Framework?

> [!abstract] Short answer
> The **Spring Framework** is the **foundation** of the Spring portfolio: a **modular** Java (also Groovy/Kotlin) platform that supplies **infrastructure** — especially a **core container** with a configuration model and **dependency injection** — so you write POJOs and apply transactions, data access, messaging, and web (Servlet **MVC** and reactive **WebFlux**) without owning those APIs yourself. As of Framework **6.0** it needs **Java 17+** and Jakarta EE **`jakarta.*`** APIs. **“Spring”** in conversation often means the **whole family** (Boot, Data, Security, Cloud, …); this project is only the core libraries.

## Infrastructure, not a full application server

Spring started in **2003** against early J2EE complexity. It does **not** implement the Jakarta EE platform spec; it **integrates selected** specs (Servlet, WebSocket, Bean Validation, JPA, JMS, DI/JSR-330, Common Annotations, …) and lets you run on an app server **or** an embedded container (typical with **Spring Boot**), or with **no** Servlet container at all (**WebFlux** / Netty).

At the heart: **Inversion of Control**. The container (`BeanFactory` / `ApplicationContext`) **creates** objects, **wires** collaborators, and runs lifecycle callbacks so you do not new-up a graph by hand ([[How would you explain dependency injection]], [[What is the difference between BeanFactory and FactoryBean]]). **AOP** (and `spring-aspects` / AspectJ) is how cross-cutting concerns such as declarative transactions attach to those POJOs. Spring MVC and [[What is Spring WebFlux]] sit in **web** modules, not in `spring-beans`.

You **choose modules** (`spring-core`, `spring-beans`, `spring-context`, `spring-webmvc`, `spring-webflux`, `spring-jdbc`, `spring-tx`, `spring-test`, …). Jars also declare `Automatic-Module-Name` (`spring.core`, `spring.context`, …) for the module path. You can use the IoC container under **another** web stack; it is not all-or-nothing.

```java
@Service
public class InvoiceService {

    private final TaxCalculator tax;

    public InvoiceService(TaxCalculator tax) {
        this.tax = tax;
    }
}

@Configuration
public class BillingConfig {

    @Bean
    TaxCalculator taxCalculator() {
        return new DefaultTaxCalculator();
    }
}
```

**Listing 1.** Conceptual. The container instantiates `InvoiceService` and injects `TaxCalculator` — the Framework’s original job.

Guiding ideas from the overview: **choice** (swap a persistence provider in configuration), **not** one true architecture, **backward compatibility**, careful APIs. **Boot** is a **separate**, opinionated project **on top** of this Framework (convention over configuration, production-ready defaults). Data, Security, Cloud, Batch each have their own repo and cadence.

```d2
direction: down
fw: "Spring Framework\n(core container, web, tx, …)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
boot: "Spring Boot" {
  width: 140
  height: 40
  style.fill: "#fff3e0"
}
others: "Data / Security / Cloud / …" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

fw -> boot
fw -> others
```

**Fig. 1.** Framework is the base; other Spring **projects** build on it. They are not “modules of one JAR.”

> [!warning] “Spring” is ambiguous
> Interviewers may mean **Framework IoC**, **Boot auto-config**, or the **portfolio**. Answer with the **project** you mean. Boot is not a rename of the Framework.

> [!warning] `javax.*` vs `jakarta.*`
> Framework **6+** is Jakarta EE 9+ (`jakarta.servlet`, `jakarta.persistence`, …). Copy-pasting `javax.*` EE APIs onto a 6/7 classpath is a classic migration break, not a DI bug.

> [!tip] Interview answer
> Spring Framework is the modular IoC-and-infrastructure core of the Spring family: it wires POJOs and offers transactions, data, messaging, MVC, and WebFlux so you do not call those APIs yourself. Since 6.0 it is Java 17 and jakarta packages. Boot and Data are separate projects on top, not extra jars of the same thing.
