<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What are the bootstrapping phases of a Quarkus application?

> [!abstract] Short answer
> Quarkus splits boot into **three phases**: **augmentation** (build time — extensions resolve the bean container, config model and record bootstrap bytecode), **static init** (at application start — the generated main class replays the `@Record(STATIC_INIT)` bytecode and initializes components needed before the runtime comes up), and **runtime init** (final wiring of components that need live config, then the app starts serving). The point of the split is that discovery work happens once at build, so startup just executes recorded steps.

## The three phases

Augmentation runs inside the build tool: `@BuildStep` processors in extension deployment artifacts consume and produce build items over the Jandex index, and their recorders emit bytecode ([[What is a Quarkus extension]]). Recorded methods carry a `@Record(ExecutionTime)` annotation — `STATIC_INIT` code is written into a static initializer of the generated main class, `RUNTIME_INIT` code runs after static init while the application boots. At startup the generated class initializer executes the recorded steps, then runtime init components (for example services that must read runtime config or talk to a database) initialize, and finally the HTTP layer accepts traffic ([[What happens at build time in Quarkus]]).

A component that needs values collected during augmentation receives them through a *context* bean injected at runtime — the augmentation phase itself is **forbidden from obtaining bean instances**, because the container does not exist yet. That is why extension code records decisions instead of instantiating services.

```java
// Two phases of the same application, observed from user code (JDK 21, Quarkus 3.39.2).
//
// Build time:  mvn package  -> augmentation runs, recorded bytecode lands in
//              target/quarkus-app/quarkus/generated-bytecode.jar
// Startup:     java -jar target/quarkus-app/quarkus-run.jar
//   -> static init replays recorded steps (no user code visible)
//   -> runtime init: observers of StartupEvent fire, config-backed beans wire up
//
// User code that runs in the runtime-init phase:
import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;

@ApplicationScoped
public class AppLifecycle {
    void onStart(@Observes StartupEvent ev) {
        System.out.println("STARTUP-EVENT observed, app name from event: "
                + ev.getClass().getSimpleName());
    }
}
// Console during boot (verbatim):
// STARTUP-EVENT observed, app name from event: StartupEvent
```

**Listing 1.** The only user-visible moment of boot is the runtime-init phase: a `StartupEvent` observer fires after recorded static init has produced the container. The same run also showed `Profile prod activated.` and the app listening on port 8080.

```d2
direction: down
build: "Augmentation (build tool)\n@BuildStep processors, Jandex,\nrecorded bytecode emitted" {
  width: 340
  height: 80
  style.fill: "#fff3e0"
}
static: "Static init (start)\ngenerated main class initializer\nreplays @Record(STATIC_INIT) steps" {
  width: 340
  height: 80
  style.fill: "#e3f2fd"
}
runtime: "Runtime init\nStartupEvent observers,\nruntime-config components" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
serve: "Serving requests" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
build -> static: "recorded bytecode"
static -> runtime
runtime -> serve
```

**Fig. 1.** Cost and discovery move to the left; the right side is pure replay and wiring. A native build runs the same phases, but its output is a compiled executable instead of the fast-jar.

## Why the split exists

Every piece of work classified as build-time is paid once per build instead of once per boot — that is the root cause of both the fast start and the fact that some configuration is baked in ([[What is the difference between build-time and runtime configuration in Quarkus]]). Extensions declare for each property whether it is readable in static init or only at runtime, and the container layout itself is fully resolved during augmentation ([[What is ArC in Quarkus]]).

> [!warning] No beans, no dynamic tricks during augmentation
> Build steps cannot look up bean instances — the CDI container is only *described* at that point. The popular claim that "Quarkus initializes everything at build time" is wrong in the other direction too: user `@Observes StartupEvent` methods and runtime-config consumers genuinely execute at startup, just without any discovery work. Interviewers probe both misconceptions.

> [!tip] Interview answer
> Quarkus boot has three phases: augmentation at build time where extensions do all metadata processing and record bytecode; static init at startup where the generated main class replays that recorded code; and runtime init where the remaining components wire up and `StartupEvent` observers fire. Discovery happens once at build, so boot is mostly replay — that is the mechanism behind sub-second startup and the reason some config is fixed at build time.
