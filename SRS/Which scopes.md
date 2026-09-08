<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# Which scopes?

> [!abstract] Short answer
> Spring documents **six** built-in bean scopes: **`singleton`** (default — one instance **per IoC container** per definition), **`prototype`** (a new instance every time that definition is requested), and four **web-only** scopes on a web-aware `ApplicationContext`: **`request`**, **`session`**, **`application`** (`ServletContext`), **`websocket`**. You can add a **custom** scope. `SimpleThreadScope` exists but is **not registered** until you do.

## The six names

A bean definition is a **recipe**. Scope is how many instances that recipe produces and how long each lives — configuration, not a field on the Java class ([[What are Spring bean scopes]]).

| Scope | Instance |
| --- | --- |
| **`singleton`** | One cached object **per container**, **per bean id**. Default. |
| **`prototype`** | New object on each `getBean` / each **fresh** injection. |
| **`request`** | One per HTTP request, then discarded. |
| **`session`** | One per HTTP `Session`. |
| **`application`** | One per `ServletContext` (also stored as a servlet attribute). |
| **`websocket`** | One per WebSocket session (STOMP over WebSocket). |

`request` / `session` / `application` / `websocket` need a web-aware context (`XmlWebApplicationContext`, Boot web, and so on). On `ClassPathXmlApplicationContext` they throw **`IllegalStateException`** (unknown scope).

```d2
direction: down
core: "Any ApplicationContext\nsingleton · prototype" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
web: "Web-aware only\nrequest · session · application · websocket" {
  width: 300
  height: 55
  style.fill: "#fff3e0"
}
```

**Fig. 1.** Four of the six scopes are web-only.

```java
@Component
class AccountService { } // singleton

@Bean
@Scope("prototype")
PrototypeWorker worker() {
	return new PrototypeWorker();
}
```

**Listing 1.** Conceptual. No `@Scope` → singleton. `@RequestScope` / `@SessionScope` / `@ApplicationScope` are the web shortcuts ([[What is the default Spring bean scope]]).

> [!warning] Spring singleton is not GoF Singleton
> One instance **per container**, not one per `ClassLoader`. Two `<bean>` ids of the same class are **two** singletons. It is **not** automatically thread-safe.

> [!tip] Interview answer
> Six built-in scopes: singleton (default, one per container), prototype (new each request), plus request, session, application, and websocket on a web ApplicationContext. Thread scope is optional and not on by default. globalSession is gone since Framework 5.
