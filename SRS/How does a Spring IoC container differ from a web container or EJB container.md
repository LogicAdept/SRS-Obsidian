<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Spring/Boot/Embedded #SRS

# How does a Spring IoC container differ from a web container or EJB container?

> [!abstract] Short answer
> They implement **different contracts**. The Spring **IoC container** (`ApplicationContext` / `BeanFactory`) **instantiates, configures, and wires beans** from metadata. A **servlet (web) container** is the HTTP runtime: network I/O plus servlet **`init` / `service` / `destroy`**. An **EJB container** hosts **enterprise beans** and supplies the EJB component contract (pooling, transactions, security, JNDI). Spring **can run inside** a web or EJB server, **or with neither**. A Boot app does **not** need a web container unless it is a web app.

## Three runtimes, often in one JVM

**IoC** is inversion of control for **your objects**. DI is the usual form: the container injects constructor/factory/property dependencies instead of the bean calling `new` or a service locator. `ApplicationContext` **is** that container (a `BeanFactory` plus events, i18n, AOP integration, and web-specific types such as `WebApplicationContext`). Stand-alone: `AnnotationConfigApplicationContext`. Boot **always** bootstraps one; the type depends on web vs not ([[What ApplicationContext type does Spring Boot create for a web app]], [[How would you explain IoC DI]]).

A **servlet container** (Tomcat, Jetty, …) is specified by **Jakarta Servlet**: part of a web/application server that speaks HTTP, decodes requests, and **manages servlets through their lifecycle**. It does **not** assemble your service layer. Spring’s web integration **starts an `ApplicationContext` inside** that container (`ContextLoaderListener` / Boot’s embedded server).

An **EJB container** is specified by **Jakarta Enterprise Beans**: it is the system that **contains enterprise beans**, exposes business/home views via **injection or JNDI**, and implements container services (transactions, security, pooling, passivation for stateful session beans). That is **not** `ApplicationContext.getBean`.

| | **Spring IoC** | **Web / servlet container** | **EJB container** |
|---|---|---|---|
| **Contract** | Spring beans + DI metadata | Jakarta Servlet | Jakarta Enterprise Beans |
| **Manages** | Any POJO “bean” | Servlets, filters, listeners | Session / MDB enterprise beans |
| **Typical job** | Wire the application graph | HTTP request/response | Tx, security, pooling, remote views |
| **Required for Boot?** | **Yes** (always) | Only if the app is **servlet/reactive web** | **No** |

```properties
spring.main.web-application-type=none
```

**Listing 1.** Boot **without** a web container: `AnnotationConfigApplicationContext`, no embedded Tomcat ([[How do you create a non-web Spring Boot application]]). Servlet/reactive apps still have **both**: IoC **and** a web container (embedded, or an external one for a WAR) ([[How do you deploy a Spring Boot application as a WAR]]).

```d2
direction: down
ioc: "ApplicationContext\ncreate / wire beans" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
web: "Servlet container\nHTTP + servlet lifecycle" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
ejb: "EJB container\nenterprise bean contract" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

web -> ioc: "may host"
ejb -> ioc: "may host"
```

**Fig. 1.** Nesting is optional. A CLI Boot process has **only** the left box. A classic `.war` on Tomcat has **web + IoC**. A full Jakarta EE server may add an **EJB** container; Spring still does not **become** that container.

Jakarta EE platform wording: web components **execute in a web container**; a product also has an **enterprise bean container**. Containers sit **between** components and platform services. Spring IoC is a **library container** you bootstrap in a `main` method or a listener — not a replacement for HTTP sockets or the EJB API.

> [!warning] `ApplicationContext` is not a fourth thing next to “the IoC container”
> Dumps that list “Application Context vs IoC vs web vs EJB” as four peers mix **API name** with **product**. `ApplicationContext` **is** the IoC container you use. `BeanFactory` is the smaller SPI underneath.

> [!warning] Embedded Tomcat does not retire IoC, and a JAR does not need EJB
> `SpringApplication` still builds a context when it starts Tomcat. `WebApplicationType.NONE` still builds a context **without** Tomcat. You do **not** need WebSphere/WebLogic **or** an EJB container to run Boot. Deploying on those servers is an **ops choice**, not how Spring wires beans ([[Why use Java EE application servers when servlet containers exist]]).

> [!tip] Interview answer
> Spring’s IoC container — ApplicationContext — creates and injects beans. A web container is the servlet HTTP runtime. An EJB container hosts enterprise beans with transactions and pooling. They are orthogonal: Spring can live inside Tomcat or an app server, or in a main() with no web container at all. Boot always has IoC; it only has a web container if the app is web.
