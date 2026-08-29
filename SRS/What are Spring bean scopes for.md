<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# What are Spring bean scopes for?

> [!abstract] Short answer
> Scopes exist so **one bean definition** (a **recipe**) can produce instances with a **chosen lifetime**, in **configuration**, instead of hard-coding “how many / how long” in the Java class. You already decide **what** collaborators to inject; scope decides **how many objects** that recipe yields and **when they die**. Default **`singleton`**: share one instance per container (typical **stateless** services). **`prototype`**: a new object **per request** to the factory (**stateful**). Web scopes tie a bean to an **HTTP request**, **session**, **`ServletContext`**, or **WebSocket** — the same idea, aligned with the Servlet/WebSocket lifecycle. Catalog: [[What are Spring bean scopes]].

## Decouple lifetime from the class

Without Spring you bake lifetime into code: a GoF singleton (one per ClassLoader), or `new` on every call. The scopes chapter’s point: a `BeanDefinition` is a **recipe**. The same class can be singleton in one app and prototype in another **without editing the class**. Dependencies and configuration values are one axis; **scope is another**.

```d2
Recipe: "BeanDefinition\nLoginAction"
R1: "request 1 instance"
R2: "request 2 instance"
Recipe -> R1
Recipe -> R2
```

**Fig. 1.** Scope answers “how many live objects from this recipe, and for which unit of work?” — here, **one per HTTP request**.

Built-in answers ([[What are Spring bean scopes]]):

| You need… | Scope is for… |
| --- | --- |
| One shared service / DAO per container | **`singleton`** (default) — cache, eager `refresh()` |
| Conversational / mutable object per use | **`prototype`** — factory `new`; you own destroy |
| Per-click HTTP state | **`request`** |
| User session state | **`session`** |
| One object for the whole web app (`ServletContext`) | **`application`** (not the same as “one per `ApplicationContext`”) |
| STOMP/WebSocket session state | **`websocket`** |
| Some other lifetime (thread, …) | **Custom `Scope`** (`SimpleThreadScope` is shipped, not registered) |

As a rule the docs give: **prototype for stateful**, **singleton for stateless**. A typical DAO is **not** prototype.

```java
@Component
@Scope("prototype")
public class CartLineEditor {
	private int quantity;
	// mutated per use — do not share as a singleton
}
```

**Listing 1.** Scope on the definition. The class does not implement a singleton/thread-local pattern itself.

## Why the extra machinery exists

**Shorter into longer:** a singleton must not **capture** one `request`/`session`/`prototype` instance at injection time. Scoped **proxies**, `ObjectProvider.getObject()`, or `@Lookup` exist **so scope still means something** after the singleton is built ([[How does a prototype Spring bean behave when injected into a singleton]]).

**Web binding:** `request`/`session` need the HTTP request on the thread (`DispatcherServlet`, or `RequestContextListener` / `RequestContextFilter`). Scope is not magic without that context.

**Not thread-safety:** singleton means **shared**, not synchronized ([[Is a singleton Spring bean thread-safe]]). Do not pick prototype “to avoid locks” unless you truly want a **new object** per call.

> [!warning] Scope is not a substitute for a new class
> If two lifetimes need **different collaborators or APIs**, that is two definitions (or two types), not `@Scope` on a God object. A long constructor is still a design smell; shrinking scope will not split responsibilities.

> [!tip] Interview answer
> Scopes are for **controlling instance lifetime in config**: share (singleton), new-each-time (prototype), or bind to HTTP/WebSocket. They keep that decision **out of the class**. Use web scopes only in a web-aware context; use a proxy/`ObjectProvider` when injecting a short-lived bean into a long-lived one.
