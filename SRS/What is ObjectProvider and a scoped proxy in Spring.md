<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# What is ObjectProvider and a scoped proxy in Spring?

> [!abstract] Short answer
> Both let a **long-lived** bean (usually a **singleton**) use a **shorter-lived** collaborator without capturing one instance at injection time ([[How does a prototype Spring bean behave when injected into a singleton]]). An **`ObjectProvider<T>`** (since **4.3**) is an injection-point **factory**: each `getObject()` (or `getIfAvailable` / `getIfUnique`) **freshly resolves** against the `BeanFactory`. A **scoped proxy** is an **AOP stand-in** injected *as* the collaborator: each **method call** fetches the current target from that bean’s **scope** and delegates. XML is `<aop:scoped-proxy/>`; Java is `@Scope(..., proxyMode = TARGET_CLASS)` (or `INTERFACES`). `@Lookup` is the third official option ([[What is the Lookup annotation in Spring]]).

## Two answers to “injection runs once”

A singleton’s constructor, setter, or field is wired **once**. A `request` / `session` / `prototype` (or custom) bean injected that way is **one object for the singleton’s life** — not the current HTTP session, and not a new prototype per call ([[What are Spring bean scopes]]).

**`ObjectProvider<T>`** is a variant of `ObjectFactory<T>` built for those injection points. The provider is bound to the factory **and a type**. Every method **re-asks** the factory; you do not store the target. `getObject()` never returns `null` (`NoSuchBeanDefinitionException`). `getIfAvailable()` returns `null` when missing. `getIfUnique()` returns `null` when missing **or** when several candidates have no unique winner (`@Primary` / fallback). Both `getObject` and `getIfAvailable` still throw `NoUniqueBeanDefinitionException` on an ambiguous set. Since **5.1** it is `Iterable` and has `stream()` / `orderedStream()`. JSR-330 `Provider<T>.get()` is the same idea. Since **6.2** the interface has default methods (tests can implement `stream()` or just `getObject()`).

```java
@Component
class CommandManager {
    private final ObjectProvider<Command> commands;
    CommandManager(ObjectProvider<Command> commands) { this.commands = commands; }

    void run() {
        Command command = commands.getObject(); // new prototype, or current request bean
        command.execute();
        command.finish(); // same instance — you asked once
    }
}
```

**Listing 1.** Conceptual. Hold the **provider**, not the command. `getIfAvailable()` is for optional beans; `@Lazy` injection-point proxies are weaker for optionality ([[What is the Lazy annotation in Spring]]).

A **scoped proxy** is a different shape: the singleton’s field **looks like** `UserPreferences`. The container injects a proxy that exposes the same public API. On **each method invocation** the proxy loads the real object from the active scope (HTTP request, session, …) and forwards the call. For **`prototype`**, that means **a new target per method call**. Default XML proxy is **CGLIB** (`<aop:scoped-proxy/>`); `proxy-target-class="false"` is a JDK **interface** proxy. Annotation equivalent: `proxyMode` on `@Scope`. Bare `@Scope("session")` uses `ScopedProxyMode.DEFAULT`, which is typically **`NO`** unless `@ComponentScan(scopedProxy = …)` set a default — so **no proxy**. Composed `@RequestScope` / `@SessionScope` / `@ApplicationScope` default **`TARGET_CLASS`**.

```java
@Component
@Scope(scopeName = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
class UserPreferences { /* per HTTP session */ }

@Component
class UserManager {
    private final UserPreferences prefs; // proxy, not one session forever
    UserManager(UserPreferences prefs) { this.prefs = prefs; }
}
```

**Listing 2.** Conceptual. `UserManager` stays a singleton; `prefs.foo()` uses **this request’s session** instance. XML: nest `<aop:scoped-proxy/>` in the session-scoped `<bean>`.

```d2
direction: down
long: "singleton UserManager" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
prov: "ObjectProvider.getObject()" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
proxy: "scoped proxy method call" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
now: "current scoped target" {
  width: 220
  height: 40
  style.fill: "#f3e5f5"
}

long -> prov -> now
long -> proxy -> now
```

**Fig. 1.** Provider: you choose when to resolve and you keep that instance. Proxy: every call re-binds (prototype → new object each call).

> [!warning] Prototype proxy ≠ one instance per “use”
> `<aop:scoped-proxy/>` on a **prototype** forwards **each method** to a **new** target. Two calls (`setState` then `execute`) are two objects. `ObjectProvider.getObject()` once, then several methods, is the “one command for this operation” pattern.

> [!warning] `@Scope("request")` alone does not proxy
> `proxyMode` defaults to **`DEFAULT` ≈ `NO`**. A singleton then still captures **one** request bean at its own creation. Set `TARGET_CLASS` / `INTERFACES`, use `@RequestScope`, or inject `ObjectProvider` / `@Lookup`. CGLIB scoped proxies do **not** intercept **`private`** methods.

> [!tip] Interview answer
> ObjectProvider is a typed factory on the injection point: getObject each time you need the current or a new instance, plus getIfAvailable for optional beans. A scoped proxy is an AOP object that looks like the collaborator and re-resolves on every method call from the request, session, or prototype scope. I pick the provider when I want one instance for a unit of work; I pick the proxy when the field should keep looking like the scoped type. Lookup is the third option when the container can subclass the singleton.
