<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is ArC in Quarkus?

> [!abstract] Short answer
> ArC is Quarkus' dependency injection container: an implementation of the **CDI Lite** specification (Jakarta CDI 4.1 family) that passes the CDI Lite TCK, plus Quarkus-specific extras. Its defining trait is that the container is **resolved at build time** — bean discovery, qualifiers and proxy generation happen during augmentation, and at runtime ArC mostly executes a prepared layout. It is deliberately **not full CDI**: dynamic features are trimmed in exchange for startup speed and native compatibility.

## Discovery and scopes

ArC sees one synthetic bean archive with **annotated** discovery mode and no visibility boundaries, built from the Jandex index during augmentation ([[What happens at build time in Quarkus]]). Scope semantics match CDI, and the lazy-versus-eager split is also a startup story ([[Why does Quarkus start faster than a typical Spring Boot application]]): a normal scope (`@ApplicationScoped`, `@RequestScoped`) injects a **client proxy** and creates the contextual instance lazily on the first method call; a pseudo-scope (`@Singleton`, `@Dependent`) creates the instance **at injection time**. Choosing `@Singleton` over `@ApplicationScoped` avoids a proxy indirection but eagerly pays construction cost during injection.

```java
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class GreetingService {

    public String greet(String name) {
        return "Hello " + name;
    }
}
```

**Listing 1.** A normal-scoped bean (compiled on Quarkus 3.39.2, JDK 21). Injected callers receive a build-time-generated proxy; the instance appears on first invocation.

```d2
direction: down
disco: "Augmentation: Jandex index\nbean archive (annotated)" {
  width: 290
  height: 75
  style.fill: "#e3f2fd"
}
lay: "Container layout resolved\nproxies generated" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
norm: "Normal scope\nproxy injected,\ninstance on first call" {
  width: 270
  height: 80
  style.fill: "#e8f5e9"
}
pseudo: "Pseudo-scope\ninstance created at injection" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
disco -> lay
lay -> norm
lay -> pseudo
```

**Fig. 1.** The runtime is a replay of build-time decisions; the only per-scope choice left is proxy-lazy versus injection-eager instantiation.

## Beyond CDI Lite, and what is missing

Extras: `@Startup` eager instantiation with `StartupEvent`, simplified constructor injection, build-time removal of unused beans (`quarkus.arc.remove-unused-beans`, guarded by `@Unremovable`), beans conditioned on build properties. Missing from full CDI: `@SessionScoped` (only with the Undertow extension), decoration of built-in beans, runtime registration of new beans, and the heavyweight CDI Full features ArC never promised.

```java
import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;

@ApplicationScoped
public class StartupSeed {

    void onStart(@Observes StartupEvent ev) {
        // container is ready; build-time-wired beans can be touched here
    }
}
```

**Listing 2.** The Quarkus-flavored eager lifecycle hook (compiled on JDK 21): observe `StartupEvent` after the container boots — a deliberate replacement for "do work in the constructor" and for CDI Full patterns ArC does not support.

> [!warning] Bean surgery happens before boot
> If the unused-bean analysis removes a bean you only look up dynamically, you get a failure at startup — not a build error. Diagnose with `quarkus.log.category."io.quarkus.arc.processor".level=DEBUG` and mark the bean `@Unremovable` when it is genuinely used outside the build-time dependency graph. Also, private members plus native executables need care: instances injected reflectively bypass build-time wiring and break the closed-world assumption ([[How does Quarkus support GraalVM native images]]).

> [!tip] Interview answer
> ArC is Quarkus' CDI Lite container. The layout — which beans exist, their qualifiers and proxies — is computed at build time, so normal-scoped beans inject as lazy proxies and pseudo-scopes like @Singleton instantiate at injection. It adds conveniences like @Startup, constructor injection and unused-bean removal, and it deliberately drops full-CDI dynamics such as runtime bean registration. For application code it feels like CDI; for container internals it is a build artifact, not a runtime discovery engine.
