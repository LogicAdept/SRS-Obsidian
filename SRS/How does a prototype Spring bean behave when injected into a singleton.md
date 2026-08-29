<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# How does a prototype Spring bean behave when injected into a singleton?

> [!abstract] Short answer
> **Injection runs once**, when the **singleton** is created ([[How do you create a singleton Spring bean at application startup]]). The singleton keeps **that one** prototype instance for its whole life — not a new object per method call. The scopes chapter is explicit: you **cannot** dependency-inject a prototype into a singleton if you need a **new** instance at runtime more than once. Then use **method injection** (`@Lookup` / `<lookup-method>`), an **`ObjectFactory`/`ObjectProvider`/`Provider` injection point** (`getObject()` / `get()` each time), or a **scoped proxy** on the prototype (every method call on the proxy creates a **new** target).

## Resolved at singleton instantiation

Prototype means a new instance **per request** to the container (`getBean` or a **fresh** injection). A singleton’s constructor/setter/`@Autowired` field is **one** request, at `refresh()` / first creation. After that the field is a normal Java reference.

```java
@Component
@Scope("prototype")
class Command { /* stateful */ }

@Component
class CommandManager {
    private final Command command; // captured once
    public CommandManager(Command command) { this.command = command; }
}
```

**Listing 1.** Conceptual. Every `CommandManager` method sees the **same** `Command`. Prototype **destroy** callbacks are **not** run by the container; the client owns cleanup.

```java
@Component
class CommandManager {
    private final ObjectProvider<Command> commands;
    public CommandManager(ObjectProvider<Command> commands) { this.commands = commands; }
    public void run() { commands.getObject().execute(); }
}
```

**Listing 2.** Conceptual. `getObject()` is a new lookup. `@Lookup` on a stub/`abstract` method is the same idea without holding a provider ([[What is the Lookup annotation in Spring]]). JSR-330 `Provider<Command>.get()` matches. `ServiceLocatorFactoryBean` is another factory-style option.

A **scoped proxy** (`<aop:scoped-proxy/>` or `@Scope(proxyMode = TARGET_CLASS)`) on a **prototype** forwards **each method call** to a **new** instance. That is a different tool than request/session proxies (those re-bind to the current HTTP scope). CGLIB scoped proxies do **not** intercept `private` methods.

```d2
direction: down
single: "singleton CommandManager" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
once: "inject Command once" {
  width: 200
  height: 36
  style.fill: "#ffebee"
}
each: "ObjectProvider.getObject / @Lookup" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}

single -> once
single -> each
```

**Fig. 1.** Field injection captures one prototype. A lookup API does not.

> [!warning] “Prototype” on the XML does not mean “new every call” from a singleton field
> The scope only applies when the **container** creates the bean. A field assigned at singleton construction is thereafter a plain object.

> [!warning] `@Lookup` vs `@Bean` factory methods
> Lookup needs a container-constructed class the runtime can CGLIB-subclass. A `@Bean` method’s return value cannot be subclassed that way — use `ObjectProvider` there.

> [!tip] Interview answer
> Injecting a prototype into a singleton gives you one prototype for the life of the singleton, because wiring happens once. For a new instance per use I inject ObjectProvider and call getObject, or use @Lookup, or a prototype scoped proxy. I do not expect the field to magically refresh.
