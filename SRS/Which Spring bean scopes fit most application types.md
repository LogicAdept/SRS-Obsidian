<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# Which Spring bean scopes fit most application types?

> [!abstract] Short answer
> **`singleton` and `prototype`.** They are the **standard** scopes: any `ApplicationContext` (CLI, batch, tests, web). **Most beans are still singleton** — the scopes chapter: “In most application scenarios, most beans in the container are singletons.” **`request`**, **`session`**, **`application`**, and **`websocket`** exist **only** on a **web-aware** context (`XmlWebApplicationContext` / Boot servlet context). The same names on `ClassPathXmlApplicationContext` throw **`IllegalStateException` (unknown scope)**. Web apps still default controllers and services to **singleton** ([[What are Spring bean scopes]], [[What is the default Spring bean scope]]).

## Portable pair vs web-only four

Six built-in scopes; **four** need HTTP (or WebSocket) binding. **`globalSession` is gone** (Framework **5.0+**). Custom scopes (`SimpleThreadScope`, …) are **opt-in**, not “most apps.”

| Scope | Fits |
|---|---|
| **`singleton`** (default) | **Every** app type; **stateless** services, DAOs, MVC controllers ([[What is the default scope of a Spring MVC controller]]) |
| **`prototype`** | **Every** app type; **stateful** objects that must not be shared ([[When would you use prototype scope in Spring]]) |
| **`request` / `session` / `application` / `websocket`** | **Web-aware** contexts only |

```java
@Component                          // singleton — CLI, batch, or web
class InvoiceService { }

@Component
@Scope("prototype")                 // also valid without a servlet
class ImportCommand { }

@Component
@RequestScope                       // web-aware ApplicationContext only
class LoginAction { }
```

**Listing 1.** Conceptual. Do not put `@RequestScope` on a batch job’s context. XML: omit `scope` or `scope="singleton"`; `scope="prototype"`; `scope="request"` only with web setup (`DispatcherServlet` already binds the request).

Injecting a shorter-lived bean into a singleton still **captures one** instance unless you use `ObjectProvider`, `@Lookup`, or a scoped proxy ([[How does a prototype Spring bean behave when injected into a singleton]]).

```d2
direction: down
any: "any ApplicationContext\nsingleton + prototype" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
web: "web-aware context only\nrequest session application websocket" {
  width: 320
  height: 50
  style.fill: "#fff3e0"
}

any -> web: "add if you have HTTP / WebSocket"
```

**Fig. 1.** “Most application types” = the **green** pair. Web scopes are **extra**, not a replacement for singleton services.

> [!warning] Web scopes are not the default in a web app
> A Boot servlet app still creates **singleton** `@Service` / `@RestController` beans. Per-request state belongs on **method arguments** or a **`request`-scoped** collaborator, not on controller fields.

> [!warning] Prototype is not “the web scope for non-web apps”
> It means **a new instance per factory request**, not per HTTP request. Using it for thread-safety of a shared singleton is the wrong tool.

> [!tip] Interview answer
> Singleton and prototype fit every Spring application type; they need no web context. Most beans stay singleton, including MVC controllers. Request, session, application, and websocket only work on a web-aware ApplicationContext. I do not put request scope on a CLI or batch factory.
