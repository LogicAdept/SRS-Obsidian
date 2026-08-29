<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# What is the difference between close and refresh on ApplicationContext?

> [!abstract] Short answer
> Both live on `ConfigurableApplicationContext`. **`refresh()`** is **startup** (or a **hot reload** of configuration): load bean definitions, run post-processors, pre-instantiate singletons, then `LifecycleProcessor.onRefresh()` and a `ContextRefreshedEvent`. **`close()`** is **terminal shutdown**: `ContextClosedEvent`, then destroy **singleton** beans (`DisposableBean` / `destroy-method` / `@PreDestroy`). After `close()`, the context **cannot** be refreshed or restarted. `registerShutdownHook()` only arranges **`close()` on JVM exit**; it is not a refresh. `stop()` is a different API (`Lifecycle` beans) and **can** be followed by `start()`.

## Startup vs end of life

`refresh()` “loads or refreshes the persistent representation of the configuration” (Java config, XML, and so on). It is a **startup** method: if it fails, already-created singletons are destroyed so nothing is left dangling — either **all** singletons exist or **none**. A second `refresh()` is allowed **only if** that context supports **hot refresh** and it is **not yet closed**. `XmlWebApplicationContext` does; `GenericApplicationContext` throws `IllegalStateException` (“already initialized and multiple refresh attempts are not supported”). First construction of `AnnotationConfigApplicationContext(AppConfig.class)` typically **is** a `refresh()`.

When refresh finishes, the context is ready: beans loaded, post-processors active, singletons pre-instantiated ([[How does ApplicationContext publish events]]). Listeners of `ContextRefreshedEvent` / `@EventListener(ContextRefreshedEvent.class)` run **after** that full singleton initialization.

`close()` destroys **all beans in the factory** (singletons cached there). `doClose()` publishes `ContextClosedEvent` and destroys singletons; it is also what the JVM hook named `SpringContextShutdownHook` calls. `close()` **removes** that hook if you registered it. A closed context is **end of life**.

```java
ConfigurableApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
ctx.registerShutdownHook();
ctx.close();
```

**Listing 1.** Conceptual. The constructor already refreshed; `close()` (or the hook) runs destroy callbacks ([[What destroy callbacks does Spring invoke when a bean is destroyed]], [[How do you shut down a Spring ApplicationContext]]).

```d2
direction: down
r: "refresh()\nload config → singletons → ContextRefreshedEvent" {
  width: 340
  height: 60
  style.fill: "#e8f5e9"
}
live: "active context\n(optional extra refresh if supported)" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
c: "close() / JVM hook\nContextClosedEvent → destroy singletons" {
  width: 340
  height: 60
  style.fill: "#fce4ec"
}
dead: "cannot refresh or start" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}

r -> live
live -> c
c -> dead
```

**Fig. 1.** Refresh brings the context up; close ends it. `stop()`/`start()` are not this pair.

Web `XmlWebApplicationContext` is the classic “refresh again” type; a Boot servlet context ([[What ApplicationContext type does Spring Boot create for a web app]]) is still **closed** on shutdown, not left half-open. Forgetting `close()` in a **non-Boot** `main` skips destroy callbacks unless you registered the hook (Boot typically registers it).

> [!warning] Closed means closed
> Do not call `refresh()` after `close()`. Do not treat `refresh()` as cleanup. `GenericApplicationContext` also refuses a **second** refresh even while still open.

> [!warning] `stop()` is not `close()`
> `stop()` signals `Lifecycle` beans and can be reversed with `start()`. `close()` destroys singletons and finishes the context.

> [!tip] Interview answer
> refresh() builds or rebuilds the container — definitions, singletons, ContextRefreshedEvent — and only some implementations allow doing it more than once. close() publishes ContextClosedEvent and destroys singletons; after that the context is dead. registerShutdownHook() just closes on JVM exit. That is not a refresh.
