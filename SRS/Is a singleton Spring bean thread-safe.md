<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# Is a singleton Spring bean thread-safe?

> [!abstract] Short answer
> **No — not because it is a singleton.** Default scope is **one shared instance per container**. The container **creates and publishes** that instance under a singleton lock (init-only fields are visible to other threads without `volatile`). **Your** fields mutated after that publication are ordinary shared Java state: concurrent writes need a lock, `volatile`, or a concurrent structure. Stateless singletons (read-only config after init) are the safe case. Scope does not add synchronization.

## Publication is safe; your mutable fields are not

A Spring singleton is **per-container, per-bean definition** — not a GoF ClassLoader singleton ([[How does a Spring singleton differ from the Gang of Four Singleton pattern]]). Every `getBean` / injection of that id returns the **same** cached object ([[What happens when you request the same singleton bean twice from ApplicationContext]]).

The core container publishes that instance in a **thread-safe** way: singleton lock, then visibility to other threads. Configuration fields written **only during initialization** (constructor / setters / `@PostConstruct`) need not be `volatile`; they behave like `final` for visibility. Controllers and repositories that only **read** that configuration after publication are concurrent-safe **for that state**. The same applies to a singleton `FactoryBean` processed under that lock.

After publication, any field you keep changing is **runtime state**. Official rule: declare it `volatile` or guard it with a lock, or keep it in a thread-safe structure. Destruction still sees the published configuration as safe; accumulated runtime state is your problem.

Spring’s own guidance on scopes: **singleton for stateless beans, prototype for stateful beans**. Prototype means a **new** instance on each injection or `getBean` — it is not a mutex. Injecting a prototype into a singleton still captures **one** prototype for the life of that singleton ([[How does a prototype Spring bean behave when injected into a singleton]]).

Web scopes isolate **instances**, not “add thread-safety to the singleton”:

- **request** — one instance per HTTP request; other requests do not see that instance’s fields. Discarded when the request ends. `DispatcherServlet` / `RequestContextListener` bind the request to the **thread** handling it.
- **session** — one instance per HTTP `Session`. Other sessions do not see that state. That is not a lock among concurrent requests that share the session.
- Injecting request/session beans into a singleton needs a **scoped proxy** (or `ObjectFactory` / `ObjectProvider`); otherwise the singleton keeps the instance resolved at its own creation.

A **thread** scope exists (`SimpleThreadScope`) but is **not** registered by default ([[How do you register a custom Spring bean scope]]).

```java
@Component
public class HitCounter {
    private int hits; // shared by every request thread

    public int bump() {
        return ++hits; // data race
    }
}

@Component
public class CatalogService {
    private final String catalogName; // set once at construction

    public CatalogService(@Value("${catalog.name}") String catalogName) {
        this.catalogName = catalogName;
    }

    public String name() {
        return catalogName; // safe to read concurrently after publication
    }
}
```

**Listing 1.** Conceptual. The singleton `HitCounter` is one instance; `hits` is racy. `catalogName` is init-only configuration — the container’s publication already gives visibility.

```d2
direction: down
t1: "HTTP thread A" {
  width: 150
  height: 50
  style.fill: "#e3f2fd"
}
t2: "HTTP thread B" {
  width: 150
  height: 50
  style.fill: "#e3f2fd"
}
bean: "One singleton instance\n(default scope)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
cfg: "Init-only fields\nvisible after publish" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
run: "Mutable runtime fields\nneed lock / volatile" {
  width: 240
  height: 70
  style.fill: "#fce4ec"
}

t1 -> bean
t2 -> bean
bean -> cfg
bean -> run
```

**Fig. 1.** Many threads share one singleton. The container made **creation** safe. **Mutation after init** is still shared-memory Java.

> [!warning] “Singleton ⇒ thread-safe” is false
> Spring does not synchronize your business methods. A singleton service with a mutable `List` or counter is a data race. The true statement is: **publication** of the singleton is thread-safe; **stateless** (or immutable-after-init) beans are then safe to call from many threads.

> [!warning] Narrower scope is not a lock — and prototype-into-singleton still shares
> `request` isolates **per HTTP request**, not a general concurrency strategy for a service. `session` is per session, still shared across that session’s requests. A `prototype` collaborator injected into a singleton is created **once**. Use a scoped proxy / `ObjectProvider` if you needed a new instance per call or per request.

> [!tip] Interview answer
> No. A Spring singleton is one shared object per container, so mutable instance fields are shared by every thread that uses the bean. The container only guarantees thread-safe creation and visibility of initialization state. Keep singletons stateless, or protect runtime fields yourself. Prototype or request scope means more instances, not a synchronized singleton, and injecting a prototype into a singleton still captures one instance.
