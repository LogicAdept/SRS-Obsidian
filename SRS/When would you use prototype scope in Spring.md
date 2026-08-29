<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# When would you use prototype scope in Spring?

> [!abstract] Short answer
> When the bean is **stateful** — it holds **conversational** state that **must not** be shared. Official rule: **prototype for stateful, singleton for stateless**. Each **request** to the container (`getBean`, or a **fresh** injection) gets a **new** instance. The container **assembles** it (init callbacks run) then **forgets** it — a stand-in for `new`, **no** `@PreDestroy` / `destroy-method` from Spring. A typical **DAO is not** prototype (no conversational state). Most beans stay **singleton** ([[What is the default Spring bean scope]], [[What are Spring bean scopes]]).

## Stateful instance, not “per HTTP request”

Prototype is **not** `request` / `session`. Those are **web** scopes on a web-aware context. Prototype works in **any** `ApplicationContext` and means **independent objects**, not “one per browser tab.”

Use it when:

| You need | Example |
|---|---|
| **Per-use mutable state** | Command / wizard / parser that accumulates fields while it runs |
| **No sharing** between callers | Two threads or two methods must not see the same fields |
| **A new object on each lookup** | `getBean` / `ObjectProvider.getObject()` / `@Lookup` ([[What is ObjectProvider and a scoped proxy in Spring]]) |

Do **not** reach for prototype to “make a singleton thread-safe,” to get **HTTP** isolation (`@RequestScope`), or for a **stateless** repository/service. Sharing is the **default** because most Spring beans **are** stateless.

```java
@Component
@Scope("prototype")
public class ImportCommand {
	private int rows;
	public void addRow() { rows++; }
	public int rows() { return rows; }
}
```

**Listing 1.** Conceptual. `rows` is conversational state. Two `getBean(ImportCommand.class)` calls are **two** counters. XML: `scope="prototype"`.

A **singleton** that **injects** this command still gets **one** instance for its life. If the point of prototype was “new command every run,” inject `ObjectProvider<ImportCommand>` / `@Lookup` / a prototype **scoped proxy** — not a field ([[How does a prototype Spring bean behave when injected into a singleton]]).

```d2
direction: down
need: "stateful / independent instances" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
proto: "scope = prototype" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
client: "client owns instances + cleanup" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}

need -> proto -> client
```

**Fig. 1.** After init, Spring does **not** track the object. Release JDBC handles, files, and similar **yourself** (or a custom `BeanPostProcessor` that keeps a list).

> [!warning] Dump answered the singleton-injection trap
> “Prototype is created once when injected” is **true for a singleton field**, and the fix is `Provider` / `ObjectFactory` / `@Lookup`. That is **not** when to **choose** the scope. Choose prototype for **state**; then **lookup** if a singleton must **create many**.

> [!warning] Prototype is not a destroy-managed scope
> Init (`@PostConstruct`, `InitializingBean`, `init-method`) **does** run. Configured **destruction does not**. Do not put scarce resources on a prototype and wait for context `close()`.

> [!tip] Interview answer
> I use prototype when the bean holds conversational state and each caller needs its own instance — the docs’ rule is prototype for stateful, singleton for stateless. A DAO is usually singleton. Prototype is not per-HTTP-request; that is request scope. Injecting a prototype into a singleton still captures one object unless I use ObjectProvider, @Lookup, or a scoped proxy. The client cleans up; Spring will not call destroy.
