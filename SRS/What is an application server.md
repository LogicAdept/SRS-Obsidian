<!--
reps: 0
priority: 0
-->
#Networking/Web #SRS
# What is an application server

> [!abstract] Short answer
> An application server is the runtime that hosts and executes your application's business logic, exposing it over HTTP and managing the platform concerns the code should not hand-roll: connection pools, transactions, lifecycle, threading, dependency injection, sessions. In the Java world: Tomcat, Jetty, WildFly, WebSphere; in the wider ecosystem: Node.js process behind a proxy, uWSGI for Python, Kestrel for .NET.

## What it provides beyond "a web server that runs code"

1. **Runtime for the component model:** servlets/JSP (Jakarta EE), Spring beans, or the framework's own components — the container calls *your* code with managed lifecycles.
2. **Platform services:** JDBC connection pools, JTA transactions, JMS integration, JNDI lookups in classic Jakarta EE; embedded equivalents in Spring Boot.
3. **HTTP plumbing into the app:** mapping requests to handlers (servlet mappings, controllers), session management ([[What is an HTTP session]]), request parsing, error pages.
4. **Operational control:** thread pools, graceful shutdown, deployment/undeploy, monitoring hooks.

```d2
direction: down
ws: "Web server / reverse proxy\nstatic, TLS, cache" { width: 280; height: 90; style.fill: "#e3f2fd" }
as: "Application server\nservlet container / runtime\npools, transactions, DI" { width: 320; height: 110; style.fill: "#fff3e0" }
code: "Your application code\ncontrollers, services" { width: 280; height: 90; style.fill: "#e8f5e9" }
db: "Database / messaging" { width: 230; height: 70; style.fill: "#f3e5f5" }
ws -> as -> code -> db
```

**Fig. 1.** The application server sits between the serving edge and the code, translating HTTP into managed component calls.

## Java specifics worth naming

- **Servlet containers** (Tomcat, Jetty, Undertow): HTTP → servlet lifecycle (`init/service/destroy`), filters, async I/O — the minimum "app server" of Spring Boot's embedded model.
- **Full Jakarta EE servers** (WildFly, WebSphere, Payara): add the umbrella of platform APIs — EJB, JTA, JMS, CDI — historically with heavyweight "full profile" deployments.
- **Spring Boot** flipped the default: embed Tomcat/Jetty/Undertow *inside* the jar — same container services, no shared server installation ([[What is a web server]] pairs with this at the edge).

> [!warning] The term's meaning shifted — answer by context
> "Application server" meant heavyweight J2EE monoliths (WebLogic, WebSphere) for a generation of interviews; today's default answer — a servlet container or embedded runtime — is what a backend job actually uses. Failing to mention this evolution sounds bookish; conversely, saying "app servers are dead" ignores Jakarta EE shops and the fact that Spring Boot *is* an embedded application server. The precise split of duties lives in [[What is the difference between a web server and an application server]]; historical web-tier context in [[What is a web application]].

> [!tip] Interview answer
> An application server hosts the application runtime and the platform services around it: request-to-component mapping, sessions, pools, transactions, lifecycle. Java examples: Tomcat/Jetty as servlet containers, WildFly as full Jakarta EE; Spring Boot embeds the container in the jar. The line I draw: the web server serves HTTP and proxies; the application server executes business logic with managed infrastructure around it.
