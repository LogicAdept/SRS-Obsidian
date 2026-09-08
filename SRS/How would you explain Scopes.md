<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# How would you explain Scopes?

> [!abstract] Short answer
> A Spring **scope** is how many instances a **bean definition** produces and how long each lives. Built-in: **`singleton`** (default, one per **container**), **`prototype`** (new instance per request to the factory), plus web-only **`request`**, **`session`**, **`application`**, **`websocket`**. Injecting a **prototype** (or a short web scope) into a **singleton** by constructor/field/setter **captures one instance** at the singleton’s creation — use `ObjectFactory` / `ObjectProvider` / JSR-330 `Provider`, a **scoped proxy**, or `@Lookup` if you need a fresh target later.

## Recipe, then lifetime

You pick scope in metadata (`scope="…"`, `@Scope`, `@RequestScope`, …), not in the Java class. Singleton is **per-container, per-id**, not GoF Singleton. Prototype: new instance on `getBean` or a **fresh** injection; the container runs **init**, then **forgets** the object — **no** `@PreDestroy` from Spring ([[What are Spring bean scopes]], [[Which scopes]], [[What is the default Spring bean scope]]).

```d2
direction: down
s: "singleton\none cached instance" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
p: "prototype\nnew instance per get" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
w: "request / session / application / websocket\nweb ApplicationContext only" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Four of six scopes exist only on a web-aware context; otherwise `IllegalStateException`.

## Prototype (or request) into a singleton

Dependencies of a singleton are resolved **when that singleton is created**. A prototype collaborator injected there is **the only** prototype that singleton will ever see. The same trap applies to `request` / `session` beans injected into a longer-lived bean without a proxy.

```java
@Component
class CommandManager {

	private final ObjectProvider<Command> commands;

	CommandManager(ObjectProvider<Command> commands) {
		this.commands = commands;
	}

	void run() {
		commands.getObject().execute(); // new prototype (or current request bean)
	}
}
```

**Listing 1.** Conceptual. `ObjectProvider.getObject()` (or `ObjectFactory.getObject()`, `Provider.get()`) **re-asks** the factory. A scoped proxy (`<aop:scoped-proxy/>`, `@Scope(..., proxyMode = TARGET_CLASS)`) is the other official path: each **method call** hits the current target ([[What is ObjectProvider and a scoped proxy in Spring]], [[How does a prototype Spring bean behave when injected into a singleton]]).

> [!warning] Direct injection is not “a new prototype each use”
> `private final PrototypeWorker worker` on a singleton is **one** worker for the singleton’s life. `Provider` / lookup / proxy are required if you meant otherwise. Prototype **destroy** callbacks are the client’s problem, not the container’s.

> [!tip] Interview answer
> Scope is per bean definition: singleton by default (one per container), prototype for a new instance each time you ask. Request, session, application, and websocket need a web context. If a singleton depends on a prototype, injection runs once — use ObjectProvider, a scoped proxy, or @Lookup for a new instance at runtime.
