<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Core/IoC/Scopes #SRS

# What is the default scope of a Spring MVC controller?

> [!abstract] Short answer
> **`singleton`** — the same as any other Spring bean. `@Controller` / `@RestController` are `@Component` stereotypes; they do **not** change scope. One instance per IoC container serves **all** requests, so **do not store request state in fields**. Per-request data belongs on method arguments, `Model`, or a **`request`/`session`-scoped** collaborator.

## Same default as every other bean

Spring *Bean Scopes*: **singleton** is the default — one instance per container, cached, returned for every lookup. That is **per-container**, not the GoF ClassLoader singleton.

Web-only scopes (`request`, `session`, `application`, `websocket`) exist only on a web-aware `ApplicationContext`. Inside `DispatcherServlet` they work without extra listeners. `@Scope("request")` on a controller is **legal**, not the default, and is rarely worth it (proxy overhead; people still expect one controller type).

```java
@Controller
public class PetController {
    // shared by every request — keep this immutable / thread-safe
    private final PetRepository pets;

    public PetController(PetRepository pets) {
        this.pets = pets;
    }
}
```

**Listing 1.** Conceptual: singleton controller, thread-safe dependency. Stereotypes: [[What is the difference between Spring RestController and Controller]]. Conversational model: [[What is the difference between SessionAttributes and SessionAttribute]]. Bean recipe: [[What is a WebApplicationContext in Spring MVC]].

```java
@Controller
@Scope("request")
public class RequestScopedFormController { /* not the default */ }
```

**Listing 2.** Conceptual: explicit web scope. Prototype is for **stateful** beans in general; a controller with mutable per-request fields is the wrong design.

```d2
direction: down
c: "@Controller bean\nsingleton (default)" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
r1: "Request A" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}
r2: "Request B" {
  width: 140
  height: 40
  style.fill: "#fff3e0"
}

c -> r1
c -> r2
```

**Fig. 1.** One instance, concurrent calls. Fields are shared.

> [!warning] Mutable fields
> A `currentUser` or `cart` instance field on a singleton controller **races** across threads. Use parameters, `SecurityContext`, session, or a scoped bean.

> [!warning] Singleton injecting prototype
> Injecting a prototype collaborator into the controller still happens **once** at controller creation. You do **not** get a new prototype per request unless you use lookup/method injection.

> [!warning] Prototype destruction
> If you did make the controller `prototype`, Spring **does not** call destruction callbacks on prototypes. That is a poor fit for a web entry point.

> [!tip] Interview answer
> **Controllers are singleton beans by default, like everything else in the container.** One object, many threads — keep them stateless. `request`/`session` scope exists for web beans, but it is not how `@Controller` is registered unless you add `@Scope`.
