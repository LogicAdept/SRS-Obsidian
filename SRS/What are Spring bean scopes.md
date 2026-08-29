<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# What are Spring bean scopes?

> [!abstract] Short answer
> A **scope** is how many instances a **bean definition** (a recipe) produces, and **how long** each lives. The Framework documents **six** built-in scopes: **`singleton`** (default — one instance **per IoC container**), **`prototype`** (a new instance **per request** to the factory), and four **web-only** scopes on a web-aware `ApplicationContext`: **`request`**, **`session`**, **`application`** (`ServletContext`), **`websocket`**. `ClassPathXmlApplicationContext` plus `request` → `IllegalStateException`. **`globalSession` is gone** (Framework **5.0+**). **`SimpleThreadScope` exists but is not registered** until you add it. Scope is configuration (`scope="…"`, `@Scope`, `@RequestScope`, …), not something baked into the Java class.

## Six built-in scopes

The definition is a **recipe**: many objects can come from one recipe. You pick the scope in metadata.

| Scope | Instance | Where |
| --- | --- | --- |
| **`singleton`** | One per **container**, cached | Default everywhere |
| **`prototype`** | New on each `getBean` / **fresh** injection | Any context |
| **`request`** | One per HTTP **request**, then discarded | Web `ApplicationContext` |
| **`session`** | One per HTTP **`Session`** | Web |
| **`application`** | One per **`ServletContext`** (also a servlet attribute) | Web |
| **`websocket`** | One per WebSocket **session** (STOMP over WebSocket) | Web |

Spring’s singleton is **per-container, per-definition**, not the GoF ClassLoader singleton. Two definitions of the same class are two singletons. It is **not** automatically thread-safe ([[Is a singleton Spring bean thread-safe]]). `ApplicationContext` **eagerly** creates non-lazy singletons ([[How do you create a singleton Spring bean at application startup]]).

**Prototype:** recommended for **stateful** beans (stateless → singleton; a typical DAO is not prototype). The container runs **init** callbacks, then **forgets** the instance — **no** `destroy-method` / `@PreDestroy` from Spring. Injecting a prototype into a singleton **captures one** instance ([[How does a prototype Spring bean behave when injected into a singleton]]).

**`application` vs `singleton`:** one per **`ServletContext`**, not per `ApplicationContext` (a WAR can have **several** contexts). Visible as a **`ServletContext` attribute**.

Web scopes need request binding (`DispatcherServlet` already does it; otherwise `RequestContextListener` / `RequestContextFilter`). Injecting `request`/`session` into a singleton needs a **scoped proxy**, `ObjectFactory`/`ObjectProvider`, or `@Lookup` — otherwise the long-lived bean keeps **one** short-lived instance.

```java
@RequestScope
@Component
public class LoginAction {
	// one instance per HTTP request
}
```

**Listing 1.** `@RequestScope` is `@Scope("request")` for components. Same idea: `@SessionScope`, `@ApplicationScope`. XML: `scope="request"`.

```d2
direction: right
s: "singleton\nper container"
p: "prototype\nper getBean"
w: "request / session /\napplication / websocket"
```

**Fig. 1.** Two always-on scopes; four only in a **web-aware** context.

**Not in the table:** `globalSession` (Portlet) — dropped in **5.0** ([[What is global-session bean scope in Spring]]). **Thread** scope: `SimpleThreadScope`, register yourself (`ConfigurableBeanFactory.registerScope`).

> [!warning] Web scopes are not “six scopes everywhere”
> Dump tables list `request` next to `singleton` as if every app had HTTP. A console `AnnotationConfigApplicationContext` has **singleton** and **prototype** only. Using `scope="session"` there fails at startup with an **unknown bean scope**.

> [!tip] Interview answer
> Six scopes: singleton (default, per container), prototype (new each request), plus request/session/application/websocket on a web context. Prototype is not fully lifecycle-managed. `globalSession` is history. Thread scope is optional/custom.
